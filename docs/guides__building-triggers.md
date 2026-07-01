# Workato SDK Documentation

> **Source**: https://docs.workato.com/en/developing-connectors/sdk/guides/building-triggers.html
> **Fetched**: 2026-07-01T03:12:51.349076

---

[Connector SDK](</en/developing-connectors/sdk>)

[How-to guides](</en/developing-connectors/sdk/guides>)

Are you an LLM? You can read better optimized documentation at /en/developing-connectors/sdk/guides/building-triggers.md for this page in Markdown format

# Building triggers [​](<#building-triggers>)

Copy page

Triggers are a crucial part of any connector. They allow users of your connector to trigger recipes in Workato based on events in your target application. There are multiple types of related triggers available in Workato:

  * Polling triggers
  * Static webhook triggers
  * Dynamic webhook triggers
  * Hybrid triggers (Webhooks + polling)

TIP

Before we start, it is also important to get familiar with the different types of [HTTP request methods](</en/developing-connectors/sdk/sdk-reference/http>) which power all triggers.

### General structure of triggers [​](<#general-structure-of-triggers>)

You can find a full reference of the `triggers` key in our [SDK reference.](</en/developing-connectors/sdk/sdk-reference/triggers>)

**Last updated:**
