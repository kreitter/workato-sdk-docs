# Workato SDK Documentation

> **Source**: https://docs.workato.com/en/developing-connectors/sdk/guides/building-actions.html
> **Fetched**: 2026-01-18T02:49:43.222612

---

# [#](<#building-actions>) Building actions

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

Before we start, it is also important to get familiar with the different types of [HTTP request methods](</developing-connectors/sdk/sdk-reference/http.html>) which power all actions.

ACTION TIMEOUT

SDK actions have a 180 second [timeout](</recipes/recipe-job-errors.html#timeouts>) limit.

You can use the [checkpoint!](</developing-connectors/sdk/sdk-reference/ruby_methods.html#checkpoint>) method with file streaming actions to transfer files that exceed the timeout limit. The `checkpoint!` method checks the duration of an action's execution. If it exceeds 120 seconds, Workato refreshes the timeout with a slight delay to ensure fair processing.

### [#](<#general-structure-of-actions>) General structure of actions

Refer to the `actions` key section in the [SDK reference](</developing-connectors/sdk/sdk-reference/actions.html>) for full details.
