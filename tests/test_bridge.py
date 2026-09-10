from __future__ import annotations

import asyncio
import json
import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import pytest

from librechat_fxmacrodata._client import FXMacroDataError, Result, list_operations
from librechat_fxmacrodata.server import (
    APP_LINK,
    FXMacroDataBridge,
    install_plugin,
    render_result,
)


class SyntheticClient:
    calls = []

    def __init__(self, *, api_key):
        self.api_key = api_key

    def __enter__(self):
        return self

    def __exit__(self, *_):
        pass

    def execute(self, operation, arguments):
        self.calls.append((operation, arguments, self.api_key))
        return Result(
            operation,
            {
                "data": [{"period": "2026-01", "value": 1.25, "unit": "synthetic unit", "publication_time_status": "unknown"}],
                "synthetic_fixture": True,
            },
            "https://fxmacrodata.com/documentation/reference",
        )


@pytest.mark.parametrize("operation", list_operations(), ids=lambda op: op.name)
def test_every_operation_is_registered_and_consumable(operation):
    bridge = FXMacroDataBridge(client_factory=SyntheticClient)
    tool = next(tool for tool in bridge.tools() if tool.name == "fxmacrodata_" + operation.name)
    assert tool.inputSchema == operation.input_schema
    assert "api_key" not in tool.inputSchema.get("properties", {})
    result = asyncio.run(bridge.call(tool.name, {"fixture_argument": "routing only"}))
    assert not result.isError
    assert SyntheticClient.calls[-1] == (operation.name, {"fixture_argument": "routing only"}, "")
    assert result.structuredContent["records"][0]["unit"] == "synthetic unit"
    assert result.structuredContent["data"]["synthetic_fixture"] is True
    assert result.structuredContent["provider_url"] == APP_LINK
    assert "https://fxmacrodata.com" in result.content[0].text


def test_native_output_and_schemas_are_not_shared_mutable_state():
    bridge = FXMacroDataBridge(client_factory=SyntheticClient)
    bridge.tools()[0].inputSchema["properties"]["leaked"] = {}
    assert "leaked" not in bridge.tools()[0].inputSchema["properties"]
    assert len(bridge.tools()) == len(list_operations())


def test_anonymous_mode_ignores_host_credentials(monkeypatch):
    monkeypatch.setenv("FXMACRODATA_API_KEY", "synthetic-test-credential")
    bridge = FXMacroDataBridge(client_factory=SyntheticClient)
    asyncio.run(bridge.call("fxmacrodata_ping", {}))
    assert SyntheticClient.calls[-1][2] == ""


def test_authenticated_mode_uses_runtime_credential(monkeypatch):
    monkeypatch.setenv("FXMACRODATA_API_KEY", "synthetic-test-credential")
    bridge = FXMacroDataBridge(anonymous=False, client_factory=SyntheticClient)
    asyncio.run(bridge.call("fxmacrodata_ping", {}))
    assert SyntheticClient.calls[-1][2] == "synthetic-test-credential"
    assert "synthetic-test-credential" not in json.dumps([x.model_dump() for x in bridge.tools()])


def test_unresolved_native_variable_never_becomes_a_key(monkeypatch):
    monkeypatch.setenv("FXMACRODATA_API_KEY", "{{FXMACRODATA_API_KEY}}")
    response = asyncio.run(FXMacroDataBridge(anonymous=False).call("fxmacrodata_ping", {}))
    assert response.isError
    assert "{{" not in response.content[0].text


@pytest.mark.parametrize(
    "failure", [FXMacroDataError("Credentials synthetic-test-credential"), RuntimeError("private-debug synthetic-test-credential")]
)
def test_errors_never_echo_credentials_or_internal_diagnostics(monkeypatch, failure):
    monkeypatch.setenv("FXMACRODATA_API_KEY", "synthetic-test-credential")

    class FailedClient(SyntheticClient):
        def execute(self, *_):
            raise failure

    response = asyncio.run(FXMacroDataBridge(anonymous=False, client_factory=FailedClient).call("fxmacrodata_ping", {}))
    assert response.isError
    assert "synthetic-test-credential" not in response.content[0].text
    assert "private-debug" not in response.content[0].text


@pytest.mark.parametrize("depth", [1, 70])
def test_encoded_errors_are_redacted_or_fail_closed_at_protocol_boundary(monkeypatch, depth):
    key = "synthetic-error-key-never-valid"
    monkeypatch.setenv("FXMACRODATA_API_KEY", key)
    encoded = "".join(f"\\u{ord(character):04x}" for character in key)
    message = "[" * depth + '{"note":"' + encoded + '"}' + "]" * depth

    class FailedClient(SyntheticClient):
        def execute(self, *_):
            raise FXMacroDataError(message)

    response = asyncio.run(FXMacroDataBridge(anonymous=False, client_factory=FailedClient).call("fxmacrodata_ping", {}))
    assert response.isError
    assert key not in response.model_dump_json()
    assert encoded not in response.model_dump_json().replace("\\\\", "\\")


def test_echo_redaction_applies_to_text_structured_payload_and_links(monkeypatch):
    key = "synthetic-test-credential"
    monkeypatch.setenv("FXMACRODATA_API_KEY", key)

    class EchoClient(SyntheticClient):
        def execute(self, operation, _):
            return Result(operation, {"rows": [{"value": key}]}, "https://fxmacrodata.com/?api_key=" + key)

    response = asyncio.run(FXMacroDataBridge(anonymous=False, client_factory=EchoClient).call("fxmacrodata_ping", {}))
    assert key not in response.model_dump_json()


def test_unknown_and_invalid_arguments_return_actionable_errors_without_network():
    bridge = FXMacroDataBridge()
    assert asyncio.run(bridge.call("unknown", {})).isError
    assert asyncio.run(bridge.call("fxmacrodata_release_calendar", {})).isError
    assert asyncio.run(bridge.call("fxmacrodata_ping", {"api_key": "must-not-be-an-argument"})).isError


def test_catalogue_access_flags_remain_typed_while_sensitive_fields_are_redacted():
    payload = {
        "requires_api_key": False,
        "optional_token": None,
        "data": [{"value": 1.25}],
        "credentials": {"api_key": "synthetic-only", "password": "synthetic-only"},
    }

    class CatalogueClient(SyntheticClient):
        def execute(self, operation, _):
            return Result(operation, payload)

    result = asyncio.run(FXMacroDataBridge(client_factory=CatalogueClient).call("fxmacrodata_data_catalogue", {"currency": "usd"}))
    assert not result.isError
    assert result.structuredContent["data"]["requires_api_key"] is False
    assert result.structuredContent["data"]["optional_token"] is None
    assert result.structuredContent["data"]["credentials"] == {"api_key": "[redacted]", "password": "[redacted]"}
    assert result.structuredContent["records"][0]["value"] == 1.25
    assert "synthetic-only" not in result.model_dump_json()


def test_table_preview_is_bounded_and_escapes_cell_separators():
    payload = {"data": [{"value": "a|b\nc", "count": n} for n in range(45)]}
    result = Result("fixture", payload)
    rendered = render_result(result)
    assert "a\\|b c" in rendered
    assert "limited to 40 rows" in rendered
    assert len(result.records()) == 45


def test_sparse_table_columns_disclose_omissions_without_losing_data():
    payload = {"data": [{f"field_{index}": index} for index in range(13)]}
    result = Result("fixture", payload)
    rendered = render_result(result)
    assert "field_11" in rendered
    assert "field_12" not in rendered
    assert "limited to 40 rows and 12 columns" in rendered
    assert result.records()[-1] == {"field_12": 12}


def test_installation_refuses_overwrite_and_contains_only_public_assets(tmp_path):
    installed = install_plugin(tmp_path)
    assert json.loads((installed / "plugin.json").read_text())["name"] == "fxmacrodata"
    assert json.loads((installed / "mcp.json").read_text())["mcpServers"]["fxmacrodata"]["args"] == ["--anonymous"]
    assert len(list(installed.rglob("SKILL.md"))) == 2
    with pytest.raises(FileExistsError):
        install_plugin(tmp_path)


@pytest.mark.asyncio
async def test_real_stdio_protocol_lists_all_tools_and_rejects_bad_input():
    parameters = StdioServerParameters(command=sys.executable, args=["-m", "librechat_fxmacrodata.server", "--anonymous"])
    async with stdio_client(parameters) as (reader, writer):
        async with ClientSession(reader, writer) as session:
            initialized = await session.initialize()
            assert initialized.serverInfo.name == "fxmacrodata"
            tools = await session.list_tools()
            assert {tool.name for tool in tools.tools} == {"fxmacrodata_" + op.name for op in list_operations()}
            invalid = await session.call_tool("fxmacrodata_release_calendar", {})
            assert invalid.isError
            assert "api_key" not in invalid.content[0].text
