# Workato SDK Documentation

> **Source**: https://docs.workato.com/en/developing-connectors/sdk/guides/building-triggers/dynamic-webhook.html
> **Fetched**: 2026-01-18T02:49:58.265480

---

# [#](<#how-to-guides-dynamic-webhook-trigger>) How-to guides - Dynamic Webhook Trigger

A dynamic webhook trigger is one that can programmatically be set up and torn down. This is something should be explicitly stated in the API of application that you are building a connector to. In the example below, you can define the process of setting up and tearing down webhooks in various blocks in the trigger object.

WARNING

When you define a static webhook trigger for your connector, take note that you will not be able to define a dynamic webhook trigger. Only one type of webhook trigger is allowed in a single connector. You may have both a polling trigger and one type of webhook trigger in your connector.

## [#](<#sample-connector-cisco-webex>) Sample connector - Cisco Webex
```ruby
 
    {
      title: 'My Cisco Webex connector',

      # More connector code here
      triggers: {
        new_message: {
          title: 'New message',

          subtitle: "Triggers when a message event is " \
          "received from Cisco Webex",

          description: lambda do |input, picklist_label|
            "New <span class='provider'>message event</span> in " \
            "<span class='provider'>Cisco Webex</span>"
          end,

          help: "Triggers when webhook is sent from Cisco.",

          input_fields: lambda do |object_definitions|
            [
              {
                name: "id",
                label: "Room ID"
              }
            ]
          end,

          webhook_subscribe: lambda do |webhook_url, connection, input, recipe_id|
            post("https://api.ciscospark.com/v1/webhooks",
                 name: "Workato recipe #{recipe_id}",
                 targetUrl: webhook_url,
                 resource: "messages",
                 event: "created",
                 filter: "roomId=#{input['id']}")
          end,

          webhook_notification: lambda do |input, payload, extended_input_schema, extended_output_schema, headers, params|
            payload["data"]
          end,

          webhook_unsubscribe: lambda do |webhook_subscribe_output, connection|
            delete("https://api.ciscospark.com/v1/webhooks/#{webhook_subscribe_output['id']}")
          end,

          dedup: lambda do |message|
            message["id"]
          end,

          output_fields: lambda do |object_definitions|
            [
              {
                name: "id"
              },
              {
                name: "roomId"
              },
              {
                name: "personId"
              },
              {
                name: "personEmail"
              },
              {
                name: "created"
              }
            ]
          end
        }
      },
      # More connector code here
    }


```

## [#](<#step-1-trigger-title-subtitle-description-and-help>) Step 1 - Trigger title, subtitle, description, and help

The first step to making a good trigger is to properly communicate what the trigger does and to provide additional help to users. To do so, Workato allows you to define the title, description, and provide hints for an action. Quite simply, the title is the title of an action and the subtitle provides further details of the action. The description of the action then contains specifications and explanation on what the action accomplishes and in the context of the application it connects to. Finally, the help segment provides users any additional information required to make the action work.

To know more about this step, take a look at our [SDK reference](</developing-connectors/sdk/sdk-reference/triggers.html#title>)

## [#](<#step-2-define-input-fields>) Step 2 - Define input fields

This component tells Workato what fields to show to a user configuring this trigger. In this case, we want a simple input field that allows a user to pick the type of Candidate event. This will be used in our trigger code later on create the trigger's personal webhook key.
```ruby
 
        input_fields: lambda do |object_definitions|
          [
            {
              name: "id",
              label: "Room ID"
            }
          ]
        end,


```

Various other key value pairs exist for input/output fields other than the ones defined above. Click [here](</developing-connectors/sdk/sdk-reference/triggers.html#input-fields>) to find out more.

Object definitions

Note that `object_definitions` is passed in as an argument. Workato allows connector builders to supply the definitions of an object separately in the "object_definitions" key. This key is used when the definitions of an object are large and/or can be dynamically obtained.

To know more about this, take a look at our [SDK reference](</developing-connectors/sdk/sdk-reference/object_definitions.html>)

## [#](<#step-3-defining-the-trigger-webhook-subscription-logic-webhook-handling-and-teardown-logic>) Step 3 - Defining the trigger webhook subscription logic, webhook handling and teardown logic

When a recipe is started, a webhook subscription should be created. This webhook subscription should be given the "webhook url" specific to the recipe to receive and process as jobs. The `webhook_subscribe` lambda function is responsible for this and is executed whenever a recipe is started. To achieve this, the lambda function receives the following arguments:

  1. `webhook_url` \- The dynamically generated webhook URL specific to each recipe.
  2. `connection` \- Corresponds to the values given by the user when making the connection to Freshworks
  3. `input` \- Corresponds to the inputs of this trigger. In this case, its the single input - `id`.
  4. `recipe_id` \- Corresponds to the recipe id that uses this specific trigger. Useful for tracking webhook subscriptions.

Below we have the lambda function inside our `new_message` trigger that handles the subscription of our webhook_url. Inside this block, we send a POST request to the Cisco spark API endpoint with the relevant details documented [here (opens new window)](<https://developer.webex.com/docs/api/v1/webhooks/create-a-webhook>).
```ruby
 
        webhook_subscribe: lambda do |webhook_url, connection, input, recipe_id|
          post("https://api.ciscospark.com/v1/webhooks",
               name: "Workato recipe #{recipe_id}",
               targetUrl: webhook_url,
               resource: "messages",
               event: "created",
               filter: "roomId=#{input['id']}")
        end,


```

TIP

If the HTTP request in the `webhook_subscribe` results in an error, this will be raised to the end user and prevent the recipe from being started.

The next step is to define the webhook handling in the `webhook_notifications` lambda function. You have numerous arguments available which represent both the user's inputs to the trigger as well as the webhook itself. To send the payload of the webhook as a job, you can simply pass on the `payload` argument. You may also add on attributes from the `headers` if required. In the case of Cisco, we have stripped away some irrelevant details from the payload found [here (opens new window)](<https://developer.webex.com/docs/api/guides/webhooks#creating-a-webhook>)
```ruby
 
        webhook_notification: lambda do |input, payload, extended_input_schema, extended_output_schema, headers, params|
          payload["data"]
        end,


```

Webhook Validations

  * Workato performs validations on JSON based webhooks - denoted by the webhook's `Content-Type` header, to ensure that the payload is valid JSON. Otherwise, Workato responds with 400 bad request.
  * Incoming webhook payloads are expected to be UTF-8 compatible and Workato responds with 400 bad request if UTF-8 incompatible characters are found.

The last part is to tear down this webhook subscription when the recipe is stopped. This is crucial for proper sanitization of webhooks in a target application. This is handled by the `webhook_unsubscribe` lambda function which is invoked when the recipe is stopped.. You have a single argument available which represents the output of the `webhook_subscribe` lambda function. In this case, it was the response from our initial request to the Cisco `/v1/webhooks` endpoint.

We can use this argument to discern the created subscription's `id` and send a matching `DELETE` request to the `v1/webhooks` endpoint to delete this webhook.
```ruby
 
        webhook_unsubscribe: lambda do |webhook_subscribe_output, connection|
          delete("https://api.ciscospark.com/v1/webhooks/#{webhook_subscribe_output['id']}")
        end,


```

To know more about the keys above, take a look at our [SDK reference](</developing-connectors/sdk/sdk-reference/triggers.html#webhook-subscribe>)

## [#](<#step-4-defining-output-fields-and-dedup>) Step 4 - Defining output fields and dedup

This section tells us what datapills to show as the output of the trigger as well as how to prevent duplicate records to create duplicate jobs. To prevent a job from being repeated (this might happen when a webhook is sent twice), use the `dedup` block which tells your connector how to create a unique signature for each record. This signature is stored for each recipe and if a record with the same signature is found, no job will be created.

For datapills, use the `output_fields` lambda function. The `name` attributes of each datapill should match the keys of a Hash that is the output of the `webhook_notifications` lambda function.
```ruby
 
        dedup: lambda do |message|
          message["id"]
        end,

        output_fields: lambda do |object_definitions|
          [
            {
              name: "id"
            },
            {
              name: "roomId"
            },
            {
              name: "personId"
            },
            {
              name: "personEmail"
            },
            {
              name: "created"
            }
          ]
        end


```
```bash

      # Sample output of the webhook_notification: lambda function
      {
        "id": "Y2lzY29zcGFyazovL3VzL01FU1NBR0UvOTJkYjNiZTAtNDNiZC0xMWU2LThhZTktZGQ1YjNkZmM1NjVk",
        "roomId": "Y2lzY29zcGFyazovL3VzL1JPT00vYmJjZWIxYWQtNDNmMS0zYjU4LTkxNDctZjE0YmIwYzRkMTU0",
        "personId": "Y2lzY29zcGFyazovL3VzL1BFT1BMRS9mNWIzNjE4Ny1jOGRkLTQ3MjctOGIyZi1mOWM0NDdmMjkwNDY",
        "personEmail": "[[email protected]](</cdn-cgi/l/email-protection>)",
        "created": "2015-10-18T14:26:16.000Z"
      }


```

To know more about the output fields block, take a look at our [SDK reference](</developing-connectors/sdk/sdk-reference/triggers.html#output-fields>)

Object definitions

Note that `object_definitions` is passed in as an argument. Workato allows connector builders to supply the definitions of an object separately in the "object_definitions" key. This key is used when the definitions of an object are large and/or can be dynamically obtained.

To know more about this, take a look at our [SDK reference](</developing-connectors/sdk/sdk-reference/object_definitions.html>)

## [#](<#step-5-optional-configure-how-workato-responds-to-webhook-events>) Step 5 - [OPTIONAL] Configure how Workato responds to webhook events

If the webhook sender requires custom responses, you may configure additional attributes to do so. [Learn more](</developing-connectors/sdk/sdk-reference/triggers.html#webhook-response-body>)

## [#](<#step-6-secure-your-webhook-events>) Step 6 - Secure your webhook events

Now that you're receiving webhooks, you can now consider adding [additional checks to verify the authenticity of incoming webhook events.](</developing-connectors/sdk/guides/building-triggers/securing-webhooks.html>)

## [#](<#rate-limits>) Rate limits

This trigger is subject to our [webhook gateway's limits.](</troubleshooting/webhook-gateway-limits.html>)
