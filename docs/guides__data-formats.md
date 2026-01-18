# Workato SDK Documentation

> **Source**: https://docs.workato.com/en/developing-connectors/sdk/guides/data-formats.html
> **Fetched**: 2026-01-18T02:50:05.097892

---

# [#](<#handling-different-data-formats>) Handling different data formats

When looking to connect to an API, one of the first questions to ask is what data format the API supports. The Workato SDK supports the following data formats which should cover all but a small minority of APIs out there. The Workato Connector SDK allows you to send and receive data using various `Content-Types`:

  * JSON
  * XML
  * Multipart Form
  * URL Encoded Form

Before we start, it is also important to get familiar with the different types of [HTTP request methods](</developing-connectors/sdk/sdk-reference/http.html>). These HTTP request methods are what give life to the actions that you are building.
