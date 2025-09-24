from src.agent.models.packing_models import PackingContext
from src.agent.services.assistant_service import PackingAssistantService


def make_context():
    return PackingContext(
        destination="Lisbon",
        destination_country="PT",
        nationality="PL",
        trip_length_days=1,
        activities=["daytrip"],
        time_of_day_usage=["day"],
    )


def test_simple_checklist_minimal_output():
    service = PackingAssistantService.create()
    output = service.simple_checklist(make_context())

    assert "Quick checklist" in output
    assert "Weather" not in output
    assert "Security" not in output
    assert "Socks" not in output  # short trip skip base layers

