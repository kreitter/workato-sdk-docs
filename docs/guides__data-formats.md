# Workato SDK Documentation

> **Source**: https://docs.workato.com/en/developing-connectors/sdk/guides/data-formats.html
> **Fetched**: 2026-09-25T02:15:55.924489

---

[](<https://www.workato.com/>)/[docs](</en>)

  * [Product Updates](<https://www.workato.com/product-hub/changelog/?utm_source=docs.workato.com>)
  * [Status Page](<https://status.workato.com?utm_source=docs.workato.com>)
  * [Workato Academy](<https://academy.workato.com/?utm_source=docs.workato.com>)

  * [ English](</en/developing-connectors/sdk/guides/data-formats>)
  * [ 日本語](</ja/developing-connectors/sdk/guides/data-formats>)

[Get a trial](<https://www.workato.com/request_demo?utm_content=docs_nav_cta>)

[Connector SDK](</en/developing-connectors/sdk>)

[How-to guides](</en/developing-connectors/sdk/guides>)

Are you an LLM? You can read better optimized documentation at /en/developing-connectors/sdk/guides/data-formats.md for this page in Markdown format

# Handling different data formats [​](<#handling-different-data-formats>)

Copy page

When looking to connect to an API, one of the first questions to ask is what data format the API supports. The Workato SDK supports the following data formats which should cover all but a small minority of APIs out there. The Workato Connector SDK allows you to send and receive data using various `Content-Types`:

  * JSON
  * XML
  * Multipart Form
  * URL Encoded Form

Before we start, it is also important to get familiar with the different types of [HTTP request methods](</en/developing-connectors/sdk/sdk-reference/http>). These HTTP request methods are what give life to the actions that you are building.

**Last updated:**

Ask AI
