# Workato SDK Documentation

> **Source**: https://docs.workato.com/en/developing-connectors/sdk/sdk-reference.html
> **Fetched**: 2026-01-18T02:50:23.360277

---

# [#](<#sdk-reference>) SDK Reference

This is the full list of all possible attributes that you can include in your Workato connector. This section is organized by the root keys of a connector:

  * `connection` \- Handles all aspects pertaining to how your connector should establish a connection with a target API.
  * `test` \- Works hand in hand with the `connection` key to verify that a connection has been successfully established.
  * `actions` \- Contains the definition of all actions in your connector.
  * `triggers` \- Contains the definition of all triggers in your connector.
  * `object_definitions` \- Define commonly used input or output fields and reference them later on in your actions and triggers.
  * `pick_lists` \- Used to generate drop-downs in input fields.
  * `methods` \- Create reusable methods which can be called from anywhere in your connector.
  * `secure_tunnel` \- Used to created OPA compatible connectors to communicate with on-premise systems.
  * `webhook_keys` \- Used in conjunction with Static webhook triggers.
  * `streams` \- Used in conjunction with actions and triggers to implement file streaming.

In addition to this, the SDK reference also contains the following information regarding

  * Defining input and output fields
  * Using HTTP Methods to send requests
  * Available ruby methods that can be used in your connector code

## [#](<#sample-connector-skeleton>) Sample Connector Skeleton

Each connector in Workato is a big hash that contains the root keys detailed above. Below, we have an example of a summarized connector. Not all keys are required.
```ruby
 
    {
      title: 'My sample connector',

      connection: Hash,

      test: lambda do
        Boolean
      end,

      custom_action: Boolean,

      custom_action_help: Hash,

      actions: Hash,

      triggers: Hash,

      object_definitions: Hash,

      pick_lists: Hash,

      methods: Hash,

      secure_tunnel: Boolean,

      webhook_keys: lambda do
        String
      end,

      streams: Hash
    }


```
