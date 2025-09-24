from src.agent.packing.engine import DeepseekTravelsEngine
from src.agent.models.packing_models import PackingContext, PackingItem


def make_context():
    return PackingContext(
        destination="Lisbon",
        trip_length_days=3,
        activities=["beach"],
        time_of_day_usage=["day", "night"],
    )


def test_adjust_for_constraints_echoes_items():
    engine = DeepseekTravelsEngine()
    ctx = make_context()
    items = [PackingItem(name="T-Shirt")]

    result = engine.adjust_for_constraints(items=items, context=ctx)

    assert result.items == items
    assert "pending" in result.notes[0].lower()

