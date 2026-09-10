# FXMacroData for LibreChat

Install native economic research tools and Skills in LibreChat. The package exposes all 23 REST operations and 49 MCP tools in its public discovery snapshot, with source-linked tables and complete structured responses.

[FXMacroData](https://fxmacrodata.com/?utm_source=github&utm_medium=referral&utm_campaign=open_source_integrations&utm_content=librechat_readme) · [API reference](https://fxmacrodata.com/documentation/reference?utm_source=github&utm_medium=referral&utm_campaign=open_source_integrations&utm_content=librechat_docs)

## Install

LibreChat must support the Agent Plugins 1.0.0 format. Install this package in the Python environment available to the LibreChat API process (Python 3.10 or later):

```sh
python -m pip install .
fxmacrodata-librechat --install-plugin /path/to/LibreChat/plugin
```

Use your configured `DEPLOYMENT_PLUGINS_DIR` when it differs from `plugin`. The installer creates a new `fxmacrodata` child directory and refuses to overwrite an existing plugin. Restart LibreChat after installation. Its API process must have the installed `fxmacrodata-librechat` executable on PATH; container deployments must install the wheel inside that container, not only on the host.

Enable the FXMacroData tools and the `fxmacrodata-macro-brief` or `fxmacrodata-series-research` deployment Skill in the normal Agent/Skills interface. Ask for a USD macro briefing or a source-linked release calendar. The tools are also available through LibreChat's MCP tool picker. Normal LibreChat model configuration is independent of data access.

The default plugin uses public access without reading credentials. USD catalogue, recent history (currently a rolling 90-day window) and release calendars require no FXMacroData account or key. Other data may require authorized access.

## Optional authenticated access

Merge the server entry from `authenticated.librechat.yaml` into your existing operator configuration, then restart LibreChat. Enter your key through its sensitive MCP variable setting. This overrides only the default anonymous server connection; the installed tools and Skills remain available. Do not put a key in the YAML, plugin files, prompts, command arguments or source control. Each authenticated connection receives its user's credential through the host's runtime environment.

Use the optional YAML configuration for per-user credentials; LibreChat's plugin `mcp.json` supports path expansion only.

## Research output

Each tool returns a readable table preview and `structuredContent` containing the original response, its tabular projection, source URL and provider link. All rows and response metadata remain in structuredContent. No units, timestamps, forecast classes or source labels are inferred. Event streams are finite captures bounded by duration and count.

Website links contain static attribution tags. API requests, MCP requests and canonical provenance URLs are untagged. The plugin sends no click beacons.

## Development

```sh
python -m pip install -e . pytest pytest-asyncio build
python -m pytest tests -q
python -m build
```

The adapter vendors the MIT-licensed FXMacroData public client. It connects only to documented FXMacroData services. See `CAPABILITIES.md` for the operation matrix and `PUBLIC_FILES.json` for the source allowlist.
