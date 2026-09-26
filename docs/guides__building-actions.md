# Workato SDK Documentation

> **Source**: https://docs.workato.com/en/developing-connectors/sdk/guides/building-actions.html
> **Fetched**: 2026-09-26T02:15:16.655083

---

[](<https://www.workato.com/>)/[docs](</en>)

  * [Product Updates](<https://www.workato.com/product-hub/changelog/?utm_source=docs.workato.com>)
  * [Status Page](<https://status.workato.com?utm_source=docs.workato.com>)
  * [Workato Academy](<https://academy.workato.com/?utm_source=docs.workato.com>)

  * [ English](</en/developing-connectors/sdk/guides/building-actions>)
  * [ 日本語](</ja/developing-connectors/sdk/guides/building-actions>)

[Get a trial](<https://www.workato.com/request_demo?utm_content=docs_nav_cta>)

[Connector SDK](</en/developing-connectors/sdk>)

[How-to guides](</en/developing-connectors/sdk/guides>)

Are you an LLM? You can read better optimized documentation at /en/developing-connectors/sdk/guides/building-actions.md for this page in Markdown format

# Building actions [​](<#building-actions>)

Copy page

Once you have figured out how to connect to your applications, you can build actions for your connectors. Actions give your connectors functionality and purpose, without them, your connectors can't really do much. In this segment, we go through the building of various types of actions:

  * Creating objects
  * Updating objects
  * Get (Retrieving) objects
  * Download files/documents
  * Upload files/documents
  * Adding custom actions
  * Multi-step actions that work with Asynchronous APIs
  * Multi-threaded actions which support sending multiple requests

TIP

Before we start, it is also important to get familiar with the different types of [HTTP request methods](</en/developing-connectors/sdk/sdk-reference/http>) which power all actions.

ACTION TIMEOUT

SDK actions have a 180-second [timeout](</en/recipes/recipe-job-errors#timeouts>) quota.

You can use the [checkpoint!](</en/developing-connectors/sdk/sdk-reference/ruby_methods#checkpoint>) method with file streaming actions to transfer files that exceed the timeout limit. The `checkpoint!` method checks the duration of an action's execution. If it exceeds 120 seconds, Workato refreshes the timeout with a slight delay to ensure fair processing.

### General structure of actions [​](<#general-structure-of-actions>)

Refer to the `actions` key section in the [SDK reference](</en/developing-connectors/sdk/sdk-reference/actions>) for full details.

**Last updated:**

Ask AI
