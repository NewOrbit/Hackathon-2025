import importlib

import pytest

from src.agent.services import mcp_clients


def test_build_mock_clients_returns_expected(monkeypatch):
    monkeypatch.setenv("DEEPSEEKTRAVELS_USE_MOCKS", "true")

    clients = mcp_clients.build_mock_clients()

    assert "mcp_client" in clients
    # Ensure the MCP client has entries for each expected server
    config = clients["mcp_config"]
    for server in ("attractions", "weather", "requirements", "booking"):
        assert server in config


def test_build_mock_clients_requires_mock(monkeypatch):
    monkeypatch.setenv("DEEPSEEKTRAVELS_USE_MOCKS", "false")

    with pytest.raises(RuntimeError):
        mcp_clients.build_mock_clients()

    # Reset for other tests
    monkeypatch.setenv("DEEPSEEKTRAVELS_USE_MOCKS", "true")
    importlib.reload(mcp_clients)

