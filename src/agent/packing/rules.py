"""Rule helpers for the DeepseekTravels packing engine."""

from __future__ import annotations

from typing import Iterable, List

from ..models.packing_models import ItemCategory, PackingContext, PackingItem, Priority, SafetyStatus


BASE_CLOTHING = {
    "day": [
        PackingItem(name="Breathable T-Shirt", category=ItemCategory.CLOTHING, quantity=1),
        PackingItem(name="Lightweight Pants", category=ItemCategory.CLOTHING, quantity=1),
    ],
    "night": [
        PackingItem(name="Comfortable Sleepwear", category=ItemCategory.CLOTHING, quantity=1),
    ],
}

aux_items = [
    PackingItem(name="Reusable Water Bottle", category=ItemCategory.ACCESSORIES, quantity=1),
    PackingItem(name="Travel Toiletry Kit", category=ItemCategory.TOILETRIES, quantity=1),
]

weather_rules = [
    (
        lambda w: w and "rain" in w.get("condition", "").lower(),
        PackingItem(
            name="Rain Jacket",
            category=ItemCategory.CLOTHING,
            quantity=1,
            priority=Priority.MUST_HAVE,
            safety_status=SafetyStatus.SAFE,
        ),
    ),
    (
        lambda w: w and w.get("temperature_c") is not None and w["temperature_c"] <= 5,
        PackingItem(
            name="Insulated Jacket",
            category=ItemCategory.CLOTHING,
            quantity=1,
        ),
    ),
]


def build_baseline_items(context: PackingContext, weather: dict | None = None) -> List[PackingItem]:
    items: List[PackingItem] = []

    include_base_layers = context.trip_length_days > 1 or "night" in context.time_of_day_usage

    if include_base_layers:
        items.append(
            PackingItem(
                name="Socks",
                category=ItemCategory.CLOTHING,
                quantity=max(1, context.trip_length_days),
            )
        )
        items.append(
            PackingItem(
                name="Underwear",
                category=ItemCategory.CLOTHING,
                quantity=max(1, context.trip_length_days),
            )
        )

    for period in context.time_of_day_usage:
        items.extend(BASE_CLOTHING.get(period, []))

    items.extend(aux_items)

    items.append(
        PackingItem(
            name="Passport / ID",
            category=ItemCategory.DOCUMENTS,
            quantity=1,
            priority=Priority.MUST_HAVE,
        )
    )

    for predicate, item in weather_rules:
        if predicate(weather):
            items.append(item)

    return _dedupe(items)


def _dedupe(items: Iterable[PackingItem]) -> List[PackingItem]:
    seen = {}
    for item in items:
        key = (item.name, item.category, item.priority)
        if key not in seen:
            seen[key] = item
        else:
            seen[key].quantity += item.quantity
    return list(seen.values())


__all__ = ["build_baseline_items"]

