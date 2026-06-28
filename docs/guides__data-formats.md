# Workato SDK Documentation

> **Source**: https://docs.workato.com/en/developing-connectors/sdk/guides/data-formats.html
> **Fetched**: 2026-06-28T03:12:31.315390

---

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
