# Workato SDK Documentation

> **Source**: https://docs.workato.com/en/developing-connectors/sdk/guides/building-triggers.html
> **Fetched**: 2026-09-19T02:15:50.853979

---

[](<https://www.workato.com/>)/[docs](</en>)

  * [Product Updates](<https://www.workato.com/product-hub/changelog/?utm_source=docs.workato.com>)
  * [Status Page](<https://status.workato.com?utm_source=docs.workato.com>)
  * [Workato Academy](<https://academy.workato.com/?utm_source=docs.workato.com>)

  * [ English](</en/developing-connectors/sdk/guides/building-triggers>)
  * [ 日本語](</ja/developing-connectors/sdk/guides/building-triggers>)

[Get a trial](<https://www.workato.com/request_demo?utm_content=docs_nav_cta>)

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

Ask AI
