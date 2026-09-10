"""Exercise every native tool through the actual public REST/MCP client."""

import asyncio
import json
from threading import Event

import pytest
import requests

from librechat_fxmacrodata._client import list_operations
from librechat_fxmacrodata.server import FXMacroDataBridge
from transport_fixtures import PAYLOAD, Transport, arguments


@pytest.mark.parametrize("operation", list_operations(), ids=lambda operation: operation.name)
def test_every_protocol_operation_reaches_transport_and_keeps_records(monkeypatch, operation):
    transport = Transport()
    monkeypatch.setattr(requests.Session, "request", lambda session, *args, **kwargs: transport.request(session, *args, **kwargs))
    result = asyncio.run(FXMacroDataBridge().call("fxmacrodata_" + operation.name, arguments(operation)))
    assert not result.isError
    data = result.structuredContent
    assert data["operation"] == operation.name
    assert data["records"]
    assert all(response.closed for response in transport.responses)
    assert all("api_key" not in options["params"] for _, _, options in transport.calls)
    if operation.name == "stream_events":
        assert data["data"]["events"][0]["data"] == PAYLOAD
    elif operation.method == "MCP":
        assert data["data"]["structuredContent"] == PAYLOAD
        assert transport.calls[-1][2]["json"]["params"]["name"] == operation.name[4:]
    else:
        assert data["data"] == PAYLOAD


@pytest.mark.parametrize("sensitive_value", [True, False, None, 123])
def test_encoded_mcp_text_is_safe_in_protocol_text_and_structured_records(monkeypatch, sensitive_value):
    key = "synthetic/review-key + never-valid"
    monkeypatch.setenv("FXMACRODATA_API_KEY", key)
    encoded = "".join(f"\\u{ord(character):04x}" for character in key)
    payload_text = '{"note":"' + encoded + '","apiKey":' + json.dumps(sensitive_value) + ',"value":1.25,"requires_api_key":false}'
    transport = Transport(payload={"content": [{"type": "text", "text": payload_text}]})
    monkeypatch.setattr(requests.Session, "request", lambda session, *args, **kwargs: transport.request(session, *args, **kwargs))
    result = asyncio.run(FXMacroDataBridge(anonymous=False).call("fxmacrodata_mcp_ping", {}))
    assert not result.isError
    assert key not in result.model_dump_json()
    assert result.structuredContent["records"][0]["value"] == 1.25
    assert result.structuredContent["records"][0]["requires_api_key"] is False
    assert result.structuredContent["records"][0]["apiKey"] == "[redacted]"
    assert "[redacted]" in json.dumps(result.structuredContent)


@pytest.mark.parametrize("operation", ["ping", "mcp_ping"])
@pytest.mark.parametrize("hex_case", ["04x", "04X"])
def test_plain_text_encoded_credential_is_redacted(monkeypatch, operation, hex_case):
    key = "synthetic-review-key-never-valid"
    monkeypatch.setenv("FXMACRODATA_API_KEY", key)
    encoded = "".join("\\u" + format(ord(character), hex_case) for character in key)
    payload = {"data": [{"note": "Public note containing " + encoded + " and preserved context.", "value": None}]}
    transport = Transport(payload=payload)
    monkeypatch.setattr(requests.Session, "request", lambda session, *args, **kwargs: transport.request(session, *args, **kwargs))
    result = asyncio.run(FXMacroDataBridge(anonymous=False).call("fxmacrodata_" + operation, {}))
    assert not result.isError
    rendered = result.model_dump_json().replace("\\\\", "\\")
    assert key not in rendered and encoded not in rendered
    assert "preserved context" in rendered and "[redacted]" in rendered


def test_cancelling_one_call_keeps_concurrent_results_and_closes_responses(monkeypatch):
    started, release = Event(), Event()
    responses = []
    sessions = []

    def request(session, method, url, **kwargs):
        currency = url.rsplit("/", 1)[-1]
        sessions.append(session)
        if currency == "usd":
            started.set()
            assert release.wait(5)
        response = Transport(payload={"data": [{"currency": currency, "value": None}]}).request(session, method, url, **kwargs)
        responses.append(response)
        return response

    monkeypatch.setattr(requests.Session, "request", request)

    async def exercise():
        bridge = FXMacroDataBridge()
        first = asyncio.create_task(bridge.call("fxmacrodata_data_catalogue", {"currency": "usd"}))
        try:
            assert await asyncio.to_thread(started.wait, 5)
            second = await bridge.call("fxmacrodata_data_catalogue", {"currency": "eur"})
            first.cancel()
            with pytest.raises(asyncio.CancelledError):
                await first
            assert not second.isError and second.structuredContent["records"] == [{"currency": "eur", "value": None}]
        finally:
            release.set()

    asyncio.run(exercise())
    assert len(sessions) == 2 and sessions[0] is not sessions[1]
    assert len(responses) == 2 and all(response.closed for response in responses)
