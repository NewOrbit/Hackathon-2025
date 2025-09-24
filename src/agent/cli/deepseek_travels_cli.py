"""Console interface for DeepseekTravels."""

from __future__ import annotations

import argparse
import threading
import time
from typing import Optional

from langchain.callbacks.base import BaseCallbackHandler

from ..models.packing_models import PackingContext
from ..services.assistant_service import PackingAssistantService

USER_COLOR = "\033[32m"  # Green
ASSISTANT_COLOR = "\033[36m"  # Cyan/pale blue
TOOL_COLOR = "\033[33m"  # Yellow
RESET_COLOR = "\033[0m"


class Spinner:
    """Simple terminal spinner."""

    def __init__(self, message: str = "thinking") -> None:
        self.message = message
        self._running = False
        self._thread: Optional[threading.Thread] = None

    def _animate(self) -> None:
        sequence = [".", "..", "..."]
        idx = 0
        while self._running:
            print(
                f"\r{ASSISTANT_COLOR}{self.message}{sequence[idx % len(sequence)]}{RESET_COLOR}",
                end="",
                flush=True,
            )
            idx += 1
            time.sleep(0.35)
        print("\r" + " " * (len(self.message) + 3) + "\r", end="", flush=True)

    def start(self) -> None:
        if self._running:
            return
        self._running = True
        self._thread = threading.Thread(target=self._animate, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        if not self._running:
            return
        self._running = False
        if self._thread:
            self._thread.join()


class CliCallbackHandler(BaseCallbackHandler):
    def __init__(self, spinner: Spinner) -> None:
        super().__init__()
        self.spinner = spinner

    # Synchronous callbacks -------------------------------------------------
    def on_llm_start(self, *args, **kwargs) -> None:  # type: ignore[override]
        self.spinner.start()

    def on_llm_end(self, *args, **kwargs) -> None:  # type: ignore[override]
        self.spinner.stop()

    def on_llm_error(self, *args, **kwargs) -> None:  # type: ignore[override]
        self.spinner.stop()

    def on_tool_start(self, *args, **kwargs) -> None:  # type: ignore[override]
        self._log_tool_start(**kwargs)

    def on_tool_end(self, *args, **kwargs) -> None:  # type: ignore[override]
        self.spinner.start()

    def on_tool_error(self, *args, **kwargs) -> None:  # type: ignore[override]
        self.spinner.stop()

    # Async callbacks -------------------------------------------------------
    async def aon_llm_start(self, *args, **kwargs) -> None:  # type: ignore[override]
        self.spinner.start()

    async def aon_llm_end(self, *args, **kwargs) -> None:  # type: ignore[override]
        self.spinner.stop()

    async def aon_llm_error(self, *args, **kwargs) -> None:  # type: ignore[override]
        self.spinner.stop()

    async def aon_tool_start(self, *args, **kwargs) -> None:  # type: ignore[override]
        self._log_tool_start(**kwargs)

    async def aon_tool_end(self, *args, **kwargs) -> None:  # type: ignore[override]
        self.spinner.start()

    async def aon_tool_error(self, *args, **kwargs) -> None:  # type: ignore[override]
        self.spinner.stop()

    # Internal helpers ------------------------------------------------------
    def _log_tool_start(self, **kwargs) -> None:
        self.spinner.stop()
        name = kwargs.get("name") or kwargs.get("tool") or "tool"
        tool_input = kwargs.get("input") or kwargs.get("tool_input")
        print(f"{TOOL_COLOR}[calling {name} with {tool_input}] {RESET_COLOR}")
        self.spinner.start()


def _build_context_from_args(args: argparse.Namespace) -> PackingContext:
    return PackingContext(
        destination=getattr(args, "destination", ""),
        trip_length_days=getattr(args, "trip_length_days", 1),
        activities=[],
        time_of_day_usage=["day"],
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="DeepseekTravels",
        description="DeepseekTravels packing assistant.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("assist", help="Interactive conversation mode")

    generate = sub.add_parser("generate", help="One-shot packing list")
    generate.add_argument("destination")
    generate.add_argument("trip_length_days", type=int)

    simple = sub.add_parser("simple", help="Keep-it-simple checklist")
    simple.add_argument("destination")

    book = sub.add_parser("book", help="Booking suggestion flow (mock only)")
    book.add_argument("destination")
    book.add_argument("trip_length_days", type=int)

    return parser


def main(argv: Optional[list[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    service = PackingAssistantService.create()
    ctx: Optional[PackingContext] = (
        _build_context_from_args(args) if args.command != "assist" else None
    )

    spinner = Spinner()
    handler = CliCallbackHandler(spinner)
    callbacks = [handler]

    if args.command == "generate":
        assert ctx is not None
        print(f"{ASSISTANT_COLOR}{service.describe(ctx)}{RESET_COLOR}")
    elif args.command == "simple":
        assert ctx is not None
        print(f"{ASSISTANT_COLOR}{service.simple_checklist(ctx)}{RESET_COLOR}")
    elif args.command == "assist":
        opener = service.start_conversation()
        print(f"{ASSISTANT_COLOR}Entering chat mode. Type 'exit' to quit.{RESET_COLOR}")
        print(f"{ASSISTANT_COLOR}{opener}{RESET_COLOR}")
        while True:
            try:
                question = input(f"{USER_COLOR}You:{RESET_COLOR} ").strip()
            except (EOFError, KeyboardInterrupt):
                print(f"\n{ASSISTANT_COLOR}Goodbye!{RESET_COLOR}")
                break
            if not question:
                continue
            if question.lower() in {"exit", "quit", "q"}:
                print(f"{ASSISTANT_COLOR}Goodbye!{RESET_COLOR}")
                break
            spinner.start()
            try:
                reply = service.process_conversation_turn(question, callbacks=callbacks)
            finally:
                spinner.stop()
            print(f"{ASSISTANT_COLOR}{reply}{RESET_COLOR}")
    elif args.command == "book":
        assert ctx is not None
        booking = service.suggest_bookings(ctx)

        # Display safety warning if present
        if booking.get("safety_warning"):
            print(f"{TOOL_COLOR}{booking['safety_warning']}{RESET_COLOR}")
            print()  # Add spacing after warning

        print(f"{ASSISTANT_COLOR}Suggested flights:{RESET_COLOR}")
        for flight in booking["flights"]:
            print(
                f"{ASSISTANT_COLOR}- {flight['summary']} ({flight['price']} {flight['currency']}){RESET_COLOR}"
            )
        print(f"{ASSISTANT_COLOR}Suggested hotels:{RESET_COLOR}")
        for hotel in booking["hotels"]:
            print(
                f"{ASSISTANT_COLOR}- {hotel['summary']} ({hotel['price']} {hotel['currency']}){RESET_COLOR}"
            )

        # For dangerous destinations, add extra confirmation
        if booking.get("safety_warning"):
            print(f"{TOOL_COLOR}⚠️  WARNING: This destination has safety concerns. Proceed with extreme caution.{RESET_COLOR}")

        confirmation = input(
            f"{ASSISTANT_COLOR}Hold ID {booking['hold_id']} ready. Confirm booking? (yes/no): {RESET_COLOR}"
        ).strip().lower()
        message = service.confirm_booking(booking["hold_id"], confirm=confirmation in {"y", "yes"})
        print(f"{ASSISTANT_COLOR}{message}{RESET_COLOR}")
    else:
        print(f"{ASSISTANT_COLOR}DeepseekTravels interactive modes coming soon. (mock mode){RESET_COLOR}")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())

