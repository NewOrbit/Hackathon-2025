from src.agent.cli.deepseek_travels_cli import main
from src.agent.models.packing_models import PackingContext
from src.agent.services.assistant_service import PackingAssistantService


def make_context():
    return PackingContext(
        destination="Paris",
        destination_country="FR",
        nationality="PL",
        trip_length_days=3,
        activities=["city"],
        time_of_day_usage=["day"],
    )


def test_booking_suggestions_provide_mock_flights_and_hotels():
    service = PackingAssistantService.create()
    result = service.suggest_bookings(make_context())

    assert result["flights"], "Expected mock flights in suggestions"
    assert result["hotels"], "Expected mock hotels in suggestions"
    assert result["hold_id"].startswith("HOLD-")


def test_booking_confirmation_requires_explicit_yes():
    service = PackingAssistantService.create()
    result = service.suggest_bookings(make_context())

    message = service.confirm_booking(result["hold_id"], confirm=False)
    assert "not confirmed" in message.lower()

    message_yes = service.confirm_booking(result["hold_id"], confirm=True)
    assert "confirmed" in message_yes.lower()


def test_cli_book_flow(monkeypatch, capsys):
    inputs = iter(["yes"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    exit_code = main(["book", "Paris", "3"])

    assert exit_code == 0
    captured = capsys.readouterr()
    assert "Booking confirmed" in captured.out

