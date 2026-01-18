# Workato SDK Documentation

> **Source**: https://docs.workato.com/en/developing-connectors/sdk/guides/building-triggers.html
> **Fetched**: 2026-01-18T02:49:57.107381

---

# [#](<#building-triggers>) Building triggers

Triggers are a crucial part of any connector. They allow users of your connector to trigger recipes in Workato based on events in your target application. There are multiple types of related triggers available in Workato:

  * Polling triggers
  * Static webhook triggers
  * Dynamic webhook triggers
  * Hybrid triggers (Webhooks + polling)

TIP

Before we start, it is also important to get familiar with the different types of [HTTP request methods](</developing-connectors/sdk/sdk-reference/http.html>) which power all triggers.

### [#](<#general-structure-of-triggers>) General structure of triggers

You can find a full reference of the `triggers` key in our [SDK reference.](</developing-connectors/sdk/sdk-reference/triggers.html>)
