"""High-level orchestration for DeepseekTravels."""

from __future__ import annotations

import inspect
import json
import os
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from ..models.packing_models import PackingContext
from ..packing.engine import DeepseekTravelsEngine
from .langchain_agent import build_langchain_agent, _run_async
from .mcp_clients import build_mock_clients
from .safety_service import CountrySafetyService, extract_country_from_destination


@dataclass
class PackingAssistantService:
    """Facade for coordinating packing logic and optional LangChain agent."""

    engine: DeepseekTravelsEngine
    clients: Dict[str, Any]
    safety_service: CountrySafetyService
    history: List[str] = field(default_factory=list)
    agent_executor: Optional[Any] = None
    mcp_agent_client: Optional[Any] = None
    llm_enabled: bool = False
    _tool_cache: Dict[tuple[str, str], Any] = field(default_factory=dict)

    @staticmethod
    def _format_tool_error(error: str) -> dict[str, Any]:
        return {
            "errors": [
                error,
                (
                    "Action needed: confirm origin, destination, departure date, travellers (number/ages/nationalities), trip length, planned activities, "
                    "baggage limits, health/mobility constraints, and budget. If all details look right, let me know and we can retry or adjust the request."
                ),
            ]
        }

    def _should_use_llm() -> bool:
        env_flag = os.getenv("DEEPSEEKTRAVELS_USE_LLM")
        if env_flag is not None:
            return env_flag.lower() == "true"
        required_env = [
            "AZURE_OPENAI_ENDPOINT",
            "AZURE_OPENAI_API_KEY",
            "AZURE_OPENAI_API_VERSION",
            "AZURE_OPENAI_DEPLOYMENT",
        ]
        
        return all(os.getenv(key) for key in required_env)

    @classmethod
    def create(cls) -> "PackingAssistantService":
        clients = build_mock_clients()
        engine = DeepseekTravelsEngine()
        safety_service = CountrySafetyService()
        use_llm = cls._should_use_llm()
        agent_executor: Optional[Any] = None
        mcp_client: Optional[Any] = clients.get("mcp_client")
        if use_llm:
            try:
                agent_executor, mcp_client = build_langchain_agent()
            except Exception as exc:  # pragma: no cover - integration guard
                print(f"[MCP ERROR] Failed to initialise LangChain agent: {exc}")
                raise
        return cls(
            engine=engine,
            clients=clients,
            safety_service=safety_service,
            agent_executor=agent_executor,
            mcp_agent_client=mcp_client,
            llm_enabled=use_llm,
        )

    # ------------------------------------------------------------------
    # Chat entry points
    # ------------------------------------------------------------------
    def start_conversation(self) -> str:
        return (
            "Hi! I'm DeepseekTravels. Describe your trip (where, when, who, activities, luggage limits, budgets) and I'll guide you."
        )

    def check_destination_safety(self, destination: str) -> Optional[str]:
        """Check if destination has safety warnings and return formatted message."""
        country = extract_country_from_destination(destination)
        if not country:
            return None

        warning = self.safety_service.get_safety_warning(country)
        if not warning:
            return None

        # Only show warnings for moderate risk and above
        from .safety_service import SafetyLevel
        if warning.level in {SafetyLevel.MODERATE_RISK, SafetyLevel.HIGH_RISK,
                           SafetyLevel.EXTREME_RISK, SafetyLevel.TRAVEL_BANNED}:
            return self.safety_service.format_warning_message(warning)

        return None

    def process_conversation_turn(
        self,
        user_input: str,
        *,
        callbacks: Optional[List[Any]] = None,
    ) -> str:
        if not user_input.strip():
            return "I didn't catch that—could you repeat?"

        # The LangChain agent now handles safety checks through the safety tool
        reply = self.chat_once(message=user_input, context=None, callbacks=callbacks)
        if isinstance(reply, dict) and reply.get("errors"):
            error_messages = "\n".join(f"- {err}" for err in reply["errors"])
            return (
                "I hit some issues calling required tools:\n"
                f"{error_messages}\n"
                "Can you confirm or update: origin, destination, departure date, travellers (number/ages/nationalities), trip length, planned activities, baggage limits, health constraints, and budget?"
            )
        return reply

    def chat_once(
        self,
        message: str,
        context: Optional[PackingContext] = None,
        *,
        callbacks: Optional[List[Any]] = None,
    ) -> str:
        if self.llm_enabled and self.agent_executor is not None:
            payload = {"input": message}
            try:
                result = _run_async(self.agent_executor.ainvoke(payload, callbacks=callbacks))
                return result.get("output") or result.get("final_output") or ""
            except RuntimeError as exc:
                return self._format_tool_error(str(exc))
            except Exception as exc:  # pragma: no cover - defensive catch
                return self._format_tool_error(str(exc))

        # Fallback heuristic response using rule-based engine (should rarely be used)
        self.history.append(f"user: {message}")
        minimal_context = context or PackingContext(
            destination="Unknown destination",
            trip_length_days=3,
            activities=["general"],
            time_of_day_usage=["day"],
        )
        try:
            weather = self._weather_tool(minimal_context.destination, callbacks=callbacks)
            requirements = self._gather_requirements(minimal_context, callbacks=callbacks)
        except RuntimeError as exc:
            return self._format_tool_error(str(exc))

        # Add safety check in fallback mode only after required details exist
        safety_warning = None
        if minimal_context.destination not in {"", "Unknown destination"}:
            safety_warning = self.check_destination_safety(minimal_context.destination)

        result = self.engine.generate(minimal_context, weather)
        summary = ", ".join(f"{item.name} x{item.quantity}" for item in result.items[:5])
        reply = (
            f"DeepseekTravels: Based on your trip to {minimal_context.destination or 'your destination'}, consider {summary}. "
            f"(Weather: {weather.get('condition')} at {weather.get('temperature_c')}°C; "
            f"Security: {'; '.join(requirements['security'])})"
        )

        if safety_warning:
            reply = safety_warning + "\n\n" + reply

        self.history.append(f"assistant: {reply}")
        return reply

    # ------------------------------------------------------------------
    # Deterministic utilities used by non-chat commands
    # ------------------------------------------------------------------
    def generate_packing_list(self, context: PackingContext) -> dict[str, Any]:
        weather = self._weather_tool(context.destination)
        requirements = self._gather_requirements(context)

        # Check for safety warnings
        safety_warning = self.check_destination_safety(context.destination)

        result = self.engine.generate(context, weather)
        return {
            "items": [item.__dict__ for item in result.items],
            "notes": result.notes + requirements["notes"] + ([safety_warning] if safety_warning else []),
            "weather": weather,
            "requirements": requirements,
            "safety_warning": safety_warning,
        }

    def describe(self, context: PackingContext) -> str:
        weather = self._weather_tool(context.destination, callbacks=None)
        requirements = self._gather_requirements(context, callbacks=None)
        result = self.engine.generate(context, weather)

        lines = [f"DeepseekTravels packing list for {context.destination}:"]

        # Add safety warning at the top if present
        safety_warning = self.check_destination_safety(context.destination)
        if safety_warning:
            lines.append("\n" + safety_warning)

        for item in result.items:
            lines.append(f"- {item.name} x{item.quantity} ({item.category.value})")
        lines.extend(result.notes + requirements["notes"])
        lines.append(
            f"Weather reference: {weather.get('condition')} at {weather.get('temperature_c')}°C"
        )
        lines.append(f"Security notes: {'; '.join(requirements['security'])}")
        return "\n".join(lines)

    def suggest_bookings(self, context: PackingContext) -> dict[str, Any]:
        safety_warning = self.check_destination_safety(context.destination)

        booking_data = self._booking_tools(context.destination, callbacks=None)
        hold_id = f"HOLD-{context.destination.upper()}-001"
        booking_data["hold_id"] = hold_id
        booking_data["safety_warning"] = safety_warning
        return booking_data

    def confirm_booking(self, hold_id: str, *, confirm: bool) -> str:
        if not confirm:
            return f"Booking with hold {hold_id} not confirmed."
        return f"Booking confirmed for hold {hold_id}."

    def simple_checklist(self, context: PackingContext) -> str:
        weather = self._weather_tool(context.destination, callbacks=None)
        result = self.engine.generate(context, weather)

        lines = [f"Quick checklist for {context.destination}:"]

        # Add safety warning if present
        safety_warning = self.check_destination_safety(context.destination)
        if safety_warning:
            lines.append("\n" + safety_warning)

        for item in result.items[:5]:
            lines.append(f"- {item.name} x{item.quantity}")
        lines.append("Pack essentials and double-check documents.")
        return "\n".join(lines)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _weather_tool(
        self,
        destination: str,
        *,
        callbacks: Optional[List[Any]] = None,
    ) -> Dict[str, Any]:
        tool = self._get_tool("weather", "get_current_weather")
        result = self._invoke_tool(tool, {"location": destination}, callbacks=callbacks)
        return result

    def _get_tool(self, server: str, tool_name: str) -> Any:
        cache_key = (server, tool_name)
        if cache_key in self._tool_cache:
            return self._tool_cache[cache_key]

        if self.mcp_agent_client is None:
            raise RuntimeError("MCP client not initialised; cannot load tools.")

        async def _fetch_tool() -> Any:
            tools = await self.mcp_agent_client.get_tools(server_name=server)
            for tool in tools:
                if tool.name == tool_name:
                    return tool
            raise ValueError(f"Tool {tool_name} not found on server {server}")

        try:
            tool = _run_async(_fetch_tool())
        except Exception as exc:
            message = f"Unable to load tool {server}.{tool_name}: {exc}"
            print(f"[MCP ERROR] {message}")
            raise RuntimeError(message) from exc

        self._tool_cache[cache_key] = tool
        return tool

    def _requirements_tools(
        self,
        context: PackingContext,
        *,
        callbacks: Optional[List[Any]] = None,
    ) -> dict[str, Any]:
        if self.mcp_agent_client is None:
            raise RuntimeError("MCP client not initialised; cannot retrieve requirements data.")
        requirements = {}
        security_tool = self._get_tool("requirements", "get_airport_security_rules")
        security = self._invoke_tool(
            security_tool,
            {
                "airport_code": context.origin_city,
                "country_code": context.destination_country,
                "airline": context.airline,
                "cabin_class": context.transportation_cabin_class,
            },
            callbacks=callbacks,
        )
        requirements["security"] = security
        if context.nationality and context.destination_country:
            visa_tool = self._get_tool("requirements", "get_visa_requirements")
            visa = self._invoke_tool(
                visa_tool,
                {
                    "nationality": context.nationality,
                    "destination_country": context.destination_country,
                    "stay_length_days": context.trip_length_days,
                },
                callbacks=callbacks,
            )
            requirements["visa"] = visa
        return requirements

    def _booking_tools(
        self,
        destination: str,
        *,
        callbacks: Optional[List[Any]] = None,
    ) -> dict[str, Any]:
        if self.mcp_agent_client is None:
            raise RuntimeError("MCP client not initialised; cannot retrieve booking data.")
        errors: list[str] = []

        def _safe_call(server: str, tool_name: str, payload: Dict[str, Any]) -> Dict[str, Any]:
            try:
                tool = self._get_tool(server, tool_name)
                return self._invoke_tool(tool, payload, callbacks=callbacks)
            except Exception as exc:
                message = f"{server}.{tool_name} failed: {exc}"
                print(f"[MCP ERROR] {message}")
                errors.append(message)
                return {}

        flights = _safe_call(
            "booking",
            "search_flights",
            {
                "origin": "",
                "destination": destination,
                "depart_date": "",
                "return_date": None,
                "passengers": 1,
                "cabin_class": "economy",
            },
        )
        hotels = _safe_call(
            "booking",
            "search_hotels",
            {
                "destination": destination,
                "check_in": "",
                "check_out": "",
                "guests": 1,
                "budget": None,
            },
        )
        activities = _safe_call(
            "booking",
            "search_activities",
            {
                "destination": destination,
                "start_date": "",
                "end_date": None,
                "interests": None,
                "budget": None,
            },
        )

        result = {
            "flights": flights.get("flights", []),
            "hotels": hotels.get("hotels", []),
            "activities": activities.get("activities", []),
        }

        if errors:
            result["errors"] = errors

        return result

    def _gather_requirements(
        self,
        context: PackingContext,
        *,
        callbacks: Optional[List[Any]] = None,
    ) -> dict[str, list[str]]:
        requirements_data = self._requirements_tools(context, callbacks=callbacks)
        security = requirements_data.get("security", {})
        visa = requirements_data.get("visa", {})
        notes: list[str] = []
        if visa:
            need = "Visa required" if visa.get("visa_requirement", visa.get("visa_required")) else "Visa exemption"
            notes.append(f"Visa status: {need}")
            visa_notes = visa.get("notes")
            if visa_notes:
                if isinstance(visa_notes, list):
                    notes.extend(visa_notes)
                else:
                    notes.append(str(visa_notes))
        restricted = security.get("restricted") or security.get("restricted_items") or []
        if restricted:
            notes.append("Security reminders: " + ", ".join(restricted))
        security_notes = security.get("notes") or []
        if isinstance(security_notes, str):
            security_notes = [security_notes]
        return {
            "security": security_notes,
            "notes": notes,
        }

    def _invoke_tool(
        self,
        tool: Any,
        params: Dict[str, Any],
        *,
        callbacks: Optional[List[Any]] = None,
    ) -> Dict[str, Any]:
        try:
            if hasattr(tool, "ainvoke"):
                result = _run_async(tool.ainvoke(params, callbacks=callbacks))
            else:
                result = tool.invoke(params, callbacks=callbacks)
                if inspect.isawaitable(result):
                    result = _run_async(result)
        except Exception as exc:
            tool_name = getattr(tool, "name", repr(tool))
            message = f"Tool invocation failed for {tool_name}: {exc}"
            print(f"[MCP ERROR] {message}")
            raise RuntimeError(message) from exc
        if isinstance(result, str):
            try:
                return json.loads(result)
            except json.JSONDecodeError:  # pragma: no cover - defensive fallback
                return {"raw": result}
        return result

