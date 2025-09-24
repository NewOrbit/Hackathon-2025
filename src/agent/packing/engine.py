"""Core packing engine scaffolding for DeepseekTravels.

This module currently provides structural placeholders only. Implementations
will be filled in during Phase 1 without adding any live HTTP calls.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List

from ..models.packing_models import PackingContext, PackingItem
from .rules import build_baseline_items


@dataclass
class PackingResult:
    """Structured response returned by the packing engine."""

    items: List[PackingItem]
    notes: List[str]


class DeepseekTravelsEngine:
    """Encapsulates rule/heuristics-based packing list generation.

    Phase 1 implementation remains offline and deterministic. The engine will
    rely on mocked MCP data provided via higher-level services.
    """

    def generate(self, context: PackingContext, weather: dict | None = None) -> PackingResult:
        """Produce an initial packing list for the provided context.

        The implementation is intentionally minimal at this stage and returns
        an empty skeleton to keep unit tests focused on structural contracts.
        """

        _ensure_valid_context(context)
        items = build_baseline_items(context, weather)
        notes = ["Baseline items generated."]
        return PackingResult(items=items, notes=notes)

    def adjust_for_constraints(
        self,
        *,
        items: Iterable[PackingItem],
        context: PackingContext,
        weather: dict | None = None,
    ) -> PackingResult:
        """Apply capacity/weight/priority rules to an existing list.

        Future iterations will house heuristics and optimization logic. For now
        it simply echoes the input and records a placeholder note.
        """

        _ensure_valid_context(context)
        return PackingResult(items=list(items), notes=["Constraints adjustment pending."])


def _ensure_valid_context(context: PackingContext) -> None:
    """Basic validation guard for early development.

    Raises:
        ValueError: if critical fields are missing. This keeps early unit tests
        simple, while preventing silent failures later in development.
    """

    if not context.destination:
        raise ValueError("destination is required")
    if context.trip_length_days <= 0:
        raise ValueError("trip_length_days must be positive")

