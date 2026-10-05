# FXMacroData operation coverage

72 native MCP tools; the two deployment Skills combine discovery, history and calendars into research workflows.

The adapter preserves the full public response alongside its record projection. Dates, units, source metadata and unavailable values remain as supplied. REST access is limited by the user's dataset entitlement; public USD catalogue, recent history and calendars can be used anonymously. Streaming returns finite captures.

This table describes the included public discovery snapshot: 23 REST operations and 49 hosted MCP tools. New service operations require a refreshed package.

| Operation | Public interface | Native surface |
|---|---|---|
| `health` | GET /v1/health | `fxmacrodata_health` |
| `ping` | GET /v1/ping | `fxmacrodata_ping` |
| `forex` | GET /v1/forex/{base}/{quote} | `fxmacrodata_forex` |
| `intraday_reference_rates` | GET /v1/fx/intraday-reference-rates/{base}/{quote} | `fxmacrodata_intraday_reference_rates` |
| `fx_sources` | GET /v1/fx/sources | `fxmacrodata_fx_sources` |
| `fx_source_universe` | GET /v1/fx/source-universe | `fxmacrodata_fx_source_universe` |
| `data_catalogue` | GET /v1/data_catalogue/{currency} | `fxmacrodata_data_catalogue` |
| `release_calendar` | GET /v1/calendar/{currency} | `fxmacrodata_release_calendar` |
| `market_sessions` | GET /v1/market_sessions | `fxmacrodata_market_sessions` |
| `rate_differentials` | GET /v1/rate_differentials/{base}/{quote} | `fxmacrodata_rate_differentials` |
| `curves` | GET /v1/curves/{currency} | `fxmacrodata_curves` |
| `financial_prices` | GET /v1/financial_prices/{currency} | `fxmacrodata_financial_prices` |
| `press_releases` | GET /v1/press-releases/{currency} | `fxmacrodata_press_releases` |
| `risk_sentiment` | GET /v1/risk_sentiment | `fxmacrodata_risk_sentiment` |
| `factors` | GET /v1/factors/{currency}/{factor} | `fxmacrodata_factors` |
| `event_predictions` | GET /v1/predictions/{currency}/{indicator} | `fxmacrodata_event_predictions` |
| `latest_announcements` | GET /v1/announcements/{currency}/latest | `fxmacrodata_latest_announcements` |
| `indicator_history` | GET /v1/announcements/{currency}/{indicator} | `fxmacrodata_indicator_history` |
| `cot` | GET /v1/cot/{currency} | `fxmacrodata_cot` |
| `latest_commodities` | GET /v1/commodities/latest | `fxmacrodata_latest_commodities` |
| `commodities` | GET /v1/commodities/{indicator} | `fxmacrodata_commodities` |
| `announcement_changes` | GET /v1/announcements/changes | `fxmacrodata_announcement_changes` |
| `stream_events` | GET /v1/stream/events | `fxmacrodata_stream_events` |
| `mcp_ping` | MCP tools/call | `fxmacrodata_mcp_ping` |
| `mcp_mcp_capabilities` | MCP tools/call | `fxmacrodata_mcp_mcp_capabilities` |
| `mcp_mcp_auth_guide` | MCP tools/call | `fxmacrodata_mcp_mcp_auth_guide` |
| `mcp_subscribe_for_mcp_access` | MCP tools/call | `fxmacrodata_mcp_subscribe_for_mcp_access` |
| `mcp_data_catalogue` | MCP tools/call | `fxmacrodata_mcp_data_catalogue` |
| `mcp_risk_sentiment` | MCP tools/call | `fxmacrodata_mcp_risk_sentiment` |
| `mcp_macro_news` | MCP tools/call | `fxmacrodata_mcp_macro_news` |
| `mcp_release_calendar` | MCP tools/call | `fxmacrodata_mcp_release_calendar` |
| `mcp_release_calendar_visual_artifact` | MCP tools/call | `fxmacrodata_mcp_release_calendar_visual_artifact` |
| `mcp_event_predictions` | MCP tools/call | `fxmacrodata_mcp_event_predictions` |
| `mcp_latest_announcements` | MCP tools/call | `fxmacrodata_mcp_latest_announcements` |
| `mcp_announcement_changes` | MCP tools/call | `fxmacrodata_mcp_announcement_changes` |
| `mcp_press_releases` | MCP tools/call | `fxmacrodata_mcp_press_releases` |
| `mcp_macro_factor` | MCP tools/call | `fxmacrodata_mcp_macro_factor` |
| `mcp_fx_reference_sources` | MCP tools/call | `fxmacrodata_mcp_fx_reference_sources` |
| `mcp_fx_reference_universe` | MCP tools/call | `fxmacrodata_mcp_fx_reference_universe` |
| `mcp_fx_intraday_reference_rates` | MCP tools/call | `fxmacrodata_mcp_fx_intraday_reference_rates` |
| `mcp_rate_curve` | MCP tools/call | `fxmacrodata_mcp_rate_curve` |
| `mcp_rate_differentials` | MCP tools/call | `fxmacrodata_mcp_rate_differentials` |
| `mcp_latest_commodities` | MCP tools/call | `fxmacrodata_mcp_latest_commodities` |
| `mcp_forex` | MCP tools/call | `fxmacrodata_mcp_forex` |
| `mcp_seasonality` | MCP tools/call | `fxmacrodata_mcp_seasonality` |
| `mcp_indicator_query` | MCP tools/call | `fxmacrodata_mcp_indicator_query` |
| `mcp_plot_visual_artifact` | MCP tools/call | `fxmacrodata_mcp_plot_visual_artifact` |
| `mcp_indicator_visual_artifact` | MCP tools/call | `fxmacrodata_mcp_indicator_visual_artifact` |
| `mcp_forex_visual_artifact` | MCP tools/call | `fxmacrodata_mcp_forex_visual_artifact` |
| `mcp_commodities_visual_artifact` | MCP tools/call | `fxmacrodata_mcp_commodities_visual_artifact` |
| `mcp_cot_visual_artifact` | MCP tools/call | `fxmacrodata_mcp_cot_visual_artifact` |
| `mcp_policy_rate_differential_visual_artifact` | MCP tools/call | `fxmacrodata_mcp_policy_rate_differential_visual_artifact` |
| `mcp_macro_briefing_task` | MCP tools/call | `fxmacrodata_mcp_macro_briefing_task` |
| `mcp_indicator_intel_task` | MCP tools/call | `fxmacrodata_mcp_indicator_intel_task` |
| `mcp_pair_intel_task` | MCP tools/call | `fxmacrodata_mcp_pair_intel_task` |
| `mcp_macro_heatmap_task` | MCP tools/call | `fxmacrodata_mcp_macro_heatmap_task` |
| `mcp_policy_scenario_modeler_task` | MCP tools/call | `fxmacrodata_mcp_policy_scenario_modeler_task` |
| `mcp_macro_war_room_task` | MCP tools/call | `fxmacrodata_mcp_macro_war_room_task` |
| `mcp_event_impact_replay_task` | MCP tools/call | `fxmacrodata_mcp_event_impact_replay_task` |
| `mcp_quant_scenario_lab_task` | MCP tools/call | `fxmacrodata_mcp_quant_scenario_lab_task` |
| `mcp_known_at_time_task` | MCP tools/call | `fxmacrodata_mcp_known_at_time_task` |
| `mcp_macro_regime_classifier_task` | MCP tools/call | `fxmacrodata_mcp_macro_regime_classifier_task` |
| `mcp_release_risk_score_task` | MCP tools/call | `fxmacrodata_mcp_release_risk_score_task` |
| `mcp_portfolio_risk_engine_task` | MCP tools/call | `fxmacrodata_mcp_portfolio_risk_engine_task` |
| `mcp_fx_trade_setup_task` | MCP tools/call | `fxmacrodata_mcp_fx_trade_setup_task` |
| `mcp_fx_backtest_task` | MCP tools/call | `fxmacrodata_mcp_fx_backtest_task` |
| `mcp_macro_research_pack_task` | MCP tools/call | `fxmacrodata_mcp_macro_research_pack_task` |
| `mcp_market_sessions` | MCP tools/call | `fxmacrodata_mcp_market_sessions` |
| `mcp_cot_data` | MCP tools/call | `fxmacrodata_mcp_cot_data` |
| `mcp_commodities` | MCP tools/call | `fxmacrodata_mcp_commodities` |
| `mcp_financial_prices` | MCP tools/call | `fxmacrodata_mcp_financial_prices` |
| `mcp_official_dataset_family` | MCP tools/call | `fxmacrodata_mcp_official_dataset_family` |

[FXMacroData API reference](https://fxmacrodata.com/documentation/reference?utm_source=github&utm_medium=referral&utm_campaign=librechat-fxmacrodata&utm_content=docs)
