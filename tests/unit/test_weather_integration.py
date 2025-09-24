from src.agent.models.packing_models import PackingContext
from src.agent.services.assistant_service import PackingAssistantService


def make_context(destination: str) -> PackingContext:
    return PackingContext(
        destination=destination,
        trip_length_days=3,
        activities=["sightseeing"],
        time_of_day_usage=["day"],
    )


def test_rainy_destination_adds_rain_jacket():
    service = PackingAssistantService.create()
    response = service.generate_packing_list(make_context("Paris"))
    item_names = {item["name"] for item in response["items"]}
    assert "Rain Jacket" in item_names


def test_cold_destination_adds_insulated_layer():
    service = PackingAssistantService.create()
    response = service.generate_packing_list(make_context("Oslo"))
    item_names = {item["name"] for item in response["items"]}
    assert "Insulated Jacket" in item_names

