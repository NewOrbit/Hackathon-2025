import pytest

from src.agent.packing.engine import DeepseekTravelsEngine
from src.agent.models.packing_models import PackingContext


def make_context(**overrides):
    data = {
        "destination": "Paris",
        "trip_length_days": 5,
        "activities": ["museum"],
        "time_of_day_usage": ["day"],
    }
    data.update(overrides)
    return PackingContext(**data)


def test_engine_requires_destination():
    engine = DeepseekTravelsEngine()
    ctx = make_context(destination="")
    with pytest.raises(ValueError):
        engine.generate(ctx)


def test_engine_placeholder_output():
    engine = DeepseekTravelsEngine()
    ctx = make_context()
    result = engine.generate(ctx)
    names = {item.name for item in result.items}
    assert "Socks" in names
    assert "Underwear" in names
    assert "Baseline items" in result.notes[0]


def test_engine_requires_positive_trip_length():
    engine = DeepseekTravelsEngine()
    ctx = make_context(trip_length_days=0)
    with pytest.raises(ValueError):
        engine.generate(ctx)

def test_engine_short_daytrip_skips_base_layers():
    engine = DeepseekTravelsEngine()
    ctx = make_context(trip_length_days=1, time_of_day_usage=["day"])
    result = engine.generate(ctx)
    names = {item.name for item in result.items}
    assert "Socks" not in names
    assert "Underwear" not in names

