from src.agent.models.packing_models import PackingContext
from src.agent.services.assistant_service import PackingAssistantService


def make_context():
    return PackingContext(
        destination="Paris",
        destination_country="FR",
        nationality="PL",
        trip_length_days=4,
        activities=["city"],
        time_of_day_usage=["day"],
    )


def test_requirements_notes_include_security_and_visa():
    service = PackingAssistantService.create()
    response = service.generate_packing_list(make_context())

    notes = " ".join(response["notes"])
    assert "visa" in notes.lower()
    assert "liquids" in notes.lower()

