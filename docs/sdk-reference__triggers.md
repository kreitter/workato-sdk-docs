# Workato SDK Documentation

> **Source**: https://docs.workato.com/en/developing-connectors/sdk/sdk-reference/triggers.html
> **Fetched**: 2026-01-18T02:50:38.783997

---

# [#](<#sdk-reference-triggers>) SDK Reference - `triggers`

This section enumerates all the possible keys to define a trigger. There are 3 types of triggers available for you to use in Workato:

  * Polling triggers (Check for new events every 5 minutes)
  * Dynamic webhook triggers (Triggers in real time from webhooks. Programmatic subscription and teardown of webhook URLs must be possible in the App)
  * Static webhook triggers (Triggers in real time from webhooks. Webhook URLs are passed from Workato to App by the end user.)

Quick Overview

The `triggers` key can only be used in both recipes and the SDK **Test code** tab after you have created a successful connection. Triggers are configured by end users of your connector and kick start recipes.

## [#](<#structure>) Structure
```ruby
 
        triggers: {

          [Unique_trigger_name]: {
            title: String,

            subtitle: String,

            description: lambda do |input, picklist_label|
              String
            end,

            help: lambda do |input, picklist_label|
              Hash
            end,

            display_priority: Integer,

            batch: Boolean,

            bulk: Boolean,

            deprecated: Boolean,

            config_fields: Array

            input_fields: lambda do |object_definitions, connection, config_fields|
              Array
            end,

            webhook_key: lambda do |connection, input|
              String
            end,

            webhook_response_type: String,

            webhook_response_body: String,

            webhook_response_headers: String,

            webhook_response_status: Integer,

            webhook_payload_type: String,

            webhook_subscribe: lambda do |webhook_url, connection, input, recipe_id|
              Hash or Array
            end,

            webhook_refresh: lambda do |webhook_subscribe_output|
              Array
            end,

            webhook_unsubscribe: lambda do |webhook_subscribe_output, connection|
              Hash
            end,

            webhook_notification: lambda do |input, payload, extended_input_schema, extended_output_schema, headers, params, connection, webhook_subscribe_output|
              Hash or Array
            end,

            poll: lambda do |connection, input, closure|
              Hash
            end,

            dedup: lambda do |record|
              String
            end,

            output_fields: lambda do |object_definitions, connection, config_fields|
              Array
            end,

            sample_output: lambda do |connection, input|
              Hash
            end,

            summarize_input: Array,

            summarize_output: Array
          },

          [Another_unique_trigger_name]: {
            ...
          }
        },


```

* * *

## [#](<#title>) `title`

Attribute | Description  
---|---  
Key | `title`  
Type | String  
Required | Optional. Defaults to title built from labeled key.  
Description | This allows you to define the title of your trigger, which might differ from the name of the key assigned to it - Key = `new_updated_object`, title = `"New/updated object"`  
Expected Output | `String`   
i.e. `"New/updated object"`  
UI reference | ![](/assets/img/title.48365f4d.png)  

TIP

In Workato, we generally advise the following structure for triggers "[Adjective] [Object]" - "New lead" or "New/updated contact" rather than "Lead created".

* * *

## [#](<#subtitle>) `subtitle`

Attribute | Description  
---|---  
Key | `subtitle`  
Type | String  
Required | Optional. Defaults to subtitle inferred from connector name and trigger title.  
Description | This allows you to define the subtitle of your trigger.  
Expected Output | `String`   
i.e. `"Use complex queries to search objects in Percolate"`  
UI reference | ![](/assets/img/subtitle.9fbdfa1b.png)  

TIP

To make your subtitles meaningful, try to provide more information in here whilst keeping your titles concise. For example, your title could be "New/updated object" whereas your subtitle could be "Trigger off new/updated leads, contacts etc." When users search for a specific triggers, Workato also searches for matches in the subtitle.

* * *

## [#](<#description>) `description`

Attribute | Description  
---|---  
Key | `description`  
Type | lambda function  
Required | Optional. Defaults to description inferred from connector name and trigger title.  
Description | This allows you to define the description of your trigger when viewed in the recipe editor. This can be a static description or a dynamic one based on your needs.  
Possible Arguments | `input` \- Hash representing user given inputs defined in `input_fields`   
`picklist_label` \- Only applicable for picklists where a user's answer consist of both a picklist label and value. This Hash represents the label for a user's given inputs for picklist fields. See below for use cases.  
Expected Output | `String`   
i.e. `"New or updated <span class='provider'>campaign</span> in <span class='provider'>Percolate</span>"` Add the `<span>` HTML tags to add weight to your description text.  
UI reference | ![](data:image/png;base64,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)  
Example - description:

For the `description` block, you have access to two arguments to make your descriptions dynamic. This is useful when you want to change your description based on how a given user has configured the action. These changes can be incredibly useful for your users to ensure they know what this action is doing without having to click and view the action's configuration to understand what it does.
```ruby
 
        new_updated_object: {
          description: lambda do |input, picklist_label|
            "New or updated <span class='provider'>#{picklist_label['object'] || 'object'}</span> in " \
            "<span class='provider'>Percolate</span>"
          end,

          config_fields: [
            {
              name: 'object',
              control_type: 'select',
              pick_list: 'object_types',
              optional: false
            }
          ]

          # More keys to define the action
        }


```

In the preceding example, the action is a generic object action that allows the user to choose between multiple object types when configuring the recipe. You can change the description of the object the user selects by referencing the `picklist_label` argument.

![](/assets/img/trigger-description-example.2c423386.gif)

* * *

## [#](<#help>) `help`

Attribute | Description  
---|---  
Key | `help`  
Type | lambda function  
Required | Optional. No help is displayed otherwise.  
Description | The help text that is meant to guide your users as to how to configure this trigger. You can also point them to documentation.  
Possible Arguments | `input` \- Hash representing user given inputs defined in `input_fields`   
`picklist_label` \- Only applicable for picklists where a user's answer consist of both a picklist label and value. This Hash represents the label for a user's given inputs for picklist fields. See below for use cases.  
`connection` \- Hash representing user given inputs defined in `connection`.   
`webhook_base_url` \- Used when you are using [static webhook triggers](</developing-connectors/sdk/guides/building-triggers/static-webhook.html>). String representing the static webhook url of your connector.  
Expected Output | `Hash` or `String` See below for examples.  
UI reference | ![](data:image/png;base64,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)  
Example - help:

The output of the `help` lambda function can either be a simple String or a Hash. Below we go through the two examples:

  * String

```ruby
 
        help: lambda do |input, picklist_label, connection, webhook_base_url|
          'Create an object in Percolate. First, select from a list of ' \
          'objects that we currently support. After selecting your object,' \
          ' dynamic input fields specific to your scope and object selected ' \
          'will be populated.' \
          ' Creating an approval denotes submitting a specified piece of content' \
          ' or campaign for a specific approval workflow.'
        end,


```

  * Hash

```ruby
 
        help: lambda do |input, picklist_label, connection, webhook_base_url|
          {
            body: "First, filter by the object you want then fill up the input fields " \
            "which appear based on the object you have selected. Amongst other things, " \
            "you’ll be able to search for contacts in your company and cloud recordings from the past. ",
            learn_more_url: "https://docs.workato.com/connectors/zoom/event-actions.html#search-event-details",
            learn_more_text: "Learn more"
          }
        end,


```

![](/assets/img/help-example.bdfb4b3c.png)

Example - Static webhook triggers - Using connection and inputs to create a Unique webhook URL

When you may have a single connector and static webhook url that needs to power multiple recipes across multiple connections, you might need your users to register webhook URLs that contain attributes specific to their connections. You can now do this through the `help` lambda where you can provide a webhook URL for your users to register that include any connection attributes within the webhook's URL parameters.
```ruby
 
        {
          title: "Sample connector",

          webhook_keys: lambda do |params, headers, payload|
            "#{params['org_id']}@#{payload['formId']}"
          end,

          triggers: {
            sample_static_webhook_trigger: {

              help: lambda do |input, picklist_label, connection, webhook_base_url|
                next unless webhook_base_url.present?
                <<~HTML
                Creates a job when an form submission is received. To set this webhook up,
                'you will need to register the webhook below under "settings" => "webhooks" => "new". <br>
                <b>Webhook endpoint URL</b>
                <b class="tips__highlight">#{webhook_base_url}?org_id=#{connection['org_id']}</b>
                HTML
              end,

              webhook_key: lambda do |connection, input|
                "#{connection['org_id']}@#{input['formId']}"
              end,

              input_fields: lambda do |object_definitions, connection, config_fields|
                [
                  {
                    name: 'formId',
                    label: "Form",
                    control_type: "select",
                    pick_list: "forms",
                    hint: "Select the form you want to trigger this recipe off."
                  }
                ]
              end,
            }
          }
        }


```

* * *

## [#](<#display-priority>) `display_priority`

Attribute | Description  
---|---  
Key | `display_priority`  
Type | Integer  
Required | Optional. Defaults to zero, otherwise to the alphabetical ordering of actions titles.  
Description | This allows you to influence the ordering of the trigger in the recipe editor so that you can highlight top triggers. The higher the integer, the higher the priority. If two triggers have the same priority, they are ordered by their titles.  

* * *

## [#](<#batch>) `batch`

Attribute | Description  
---|---  
Key | `batch`  
Type | Boolean  
Required | Optional.  
Description | This presents a "Batch" tag next to your action to indicate that this action works with multiple records. Normally used in batch triggers or batch create/update/upsert actions where users can pass a list of records.  
UI reference | ![](data:image/png;base64,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)  

* * *

## [#](<#bulk>) `bulk`

Attribute | Description  
---|---  
Key | `bulk`  
Type | Boolean  
Required | Optional.  
Description | This presents a "Bulk" tag next to your action to indicate that this action works with a large flat file of records. Normally used bulk create/update/upsert actions where users pass a CSV of records.  
UI reference | ![](/assets/img/bulk.1d2a80e6.png)  

* * *

## [#](<#deprecated>) `deprecated`

Attribute | Description  
---|---  
Key | `deprecated`  
Type | Boolean  
Required | Optional.  
Description | This presents a "deprecated" tag next to your action to indicate that this action has been deprecated. Recipes which used to use this action will continue to work but future recipes will not be able to search and select this action.  
UI reference | ![](/assets/img/deprecated.3e09de36.png)  

TIP

Deprecation is a great way to move users to new actions when changes are not backwards compatible. This gives you more freedom to make your actions more usable or cater for upcoming API changes.

* * *

## [#](<#config-fields>) `config_fields`

Attribute | Description  
---|---  
Key | `config_fields`  
Type | Array  
Required | Optional.  
Description | This key accepts an array of hashes which show up as input fields shown to a user. Config fields are shown to a user before input fields are rendered and can be used to alter what set of input fields are shown to an end user. This is often used in generic object actions where config fields prompt a user to select the object and input fields are rendered based on that selection. Inputs given to `config_fields` can be referenced by the connector in the `input_fields` lambda function via an argument. It is also present as an argument in all `object_defintions`. To know more about how to define config fields in Workato, click [here.](</developing-connectors/sdk/sdk-reference/schema.html>)  
Expected Output | Array of hashes. Each hash in this array corresponds to a separate config field.  
UI reference | ![](/assets/img/config_fields.02e2eb97.gif)  

TIP

Config fields are powerful tools to introduce dynamic behavior to your actions. Use them to make your connector easier to use and discover new features. In the example gif above, you can see that the input "Event" actually causes more input fields to render. These input fields are rendered based on the selection of the value "Meeting".

* * *

## [#](<#input-fields>) `input_fields`

Attribute | Description  
---|---  
Key | `input_fields`  
Type | lambda function  
Required | True  
Description | This lambda function allows you to define what input fields should be shown to a user configuring this trigger in the recipe editor. Output of this lambda function should be an array of hashes, where each hash in this array corresponds to a separate input field. To know more about how to define input fields in Workato, click [here.](</developing-connectors/sdk/sdk-reference/schema.html>)  
Possible Arguments | `object_definitions` \- Allows you to reference an object definitions. Object definitions are stores of these arrays hashes which may be used to represent both input fields or output fields (datapills). These can be referenced by any action or trigger.   
`connection` \- Hash representing user given inputs defined in `connection`.   
`config_fields` \- Hash representing user given inputs defined in `config_fields`, if applicable.  
Expected Output | Array of hashes. Each hash in this array corresponds to a separate input field.  
UI reference | ![](/assets/img/input_fields.a652188c.png)  

* * *

## [#](<#webhook-key>) `webhook_key`

Attribute | Description  
---|---  
Key | `webhook_key`  
Type | lambda function  
Required | True if trigger is a static webhook trigger. False otherwise. Should not be used when `webhook_subscribe`, `webhook_unsubscribe` is defined.  
Description | **Used in conjunction with`webhook_keys` which should be present as a root level key in the connector - same level as `actions` and `triggers`**   

Allows you to use any user input from the connection or trigger to build a unique signature for this trigger. This can also be a static string value. When the signature in this lambda function match the signature in the `webhook_keys` lambda function, webhooks are sent to this trigger. See our [Static webhook guide for more details.](</developing-connectors/sdk/guides/building-triggers/static-webhook.html>)  
Possible Arguments | `connection` \- Hash representing user given inputs defined in `connection`.   
`input` \- Hash representing user given inputs defined in `input_fields`  
Expected Output | Array of hashes. Each hash in this array corresponds to a separate input field.  
Example - webhook_key:

The `webhook_key` lambda function is specific to a single trigger and the output signature if built from user inputs. On the other hand, the `webhook_keys` lambda function is tied to the entire connector and the output signature is built from the incoming webhook's attributes like its body, headers, and query parameters. When expecting a match in these two signature, it becomes easy to see how routing is done from incoming webhooks to the proper trigger to create jobs.
```ruby
 
        {
          title: "Sample connector",

          webhook_keys: lambda do |params, headers, payload|
            payload['formId']
          end,

          triggers: {
            sample_static_webhook_trigger: {

              help: lambda do |_input, _picklist_label|
                {
                  body: “Triggers in real-time whenever an event is created. Set up this trigger by registering the Webhook URL ” \
                        “below in <b>Settings</b> => <b>Webhooks</b>.“,
                  learn_more_url: “https://docs.workato.com”,
                  learn_more_text: “Learn more”
                }
              end,

              webhook_url_help: lambda do |_connection, _input, webhook_base_url|
                webhook_base_url
              end,

              input_fields: lambda do |object_definitions, connection, config_fields|
                [
                  {
                    name: 'formId',
                    label: "Form",
                    control_type: "select",
                    pick_list: "forms",
                    hint: "Select the form you want to trigger this recipe off."
                  }
                ]
              end,

              webhook_key: lambda do |connection, input|
                input['formId']
              end,
            }
          }
        }


```

* * *

## [#](<#webhook-response-type>) `webhook_response_type`

Attribute | Description  
---|---  
Key | `webhook_response_type`  
Type | String  
Required | Optional. Only applies to Dynamic webhook triggers ( triggers with `webhook_subscribe` and `webhook_unsubscribe`)  
Description | By default, Workato responds with no content-type headers to webhook events. `webhook_response_type` allows for 'plain' and 'json' which corresponds to content-type headers `text/plain` and `application/json` respectively.  

* * *

## [#](<#webhook-response-body>) `webhook_response_body`

Attribute | Description  
---|---  
Key | `webhook_response_body`  
Type | String  
Required | Optional. Only applies to Dynamic webhook triggers ( triggers with `webhook_subscribe` and `webhook_unsubscribe`)  
Description | By default, Workato responds with an empty body to webhook events. `webhook_response_body` allows for a mustache template that allows you to define how Workato should respond to webhooks.  

Mustache templates have access to the following variables:

name | description | example usage  
---|---|---  
headers | Contains request headers. Headers are normalized (x–custom-header -> X-Custom-Header) | ` { “challenge”:“{{{headers.X-Challenge}}}” } `  
body | Request body is parsed according to the `webhook_response_type`. You can use dot notation to access nested values. | ` { “challenge”: “{{body.x-challenge}}” } `  
query | Contains query params | ` { “X-Challenge”: “{{query.challenge}}” } `  
Example - webhook_response_body: - Defining a custom webhook response

Use `webhook_response_body` in two scenarios:

  1. You need to respond with a static string or JSON response to the webhook sender.

```ruby
 
      webhook_response_type: 'json',
      webhook_response_body: '{ "success": true }',


```

will result in Workato responding with a content-type `application/json` and the body
```ruby
 
    {
      "success": true
    }


```

  2. You need to respond with a dynamic response based on the webhook event. For example, when webhook senders send a webhook event to confirm that the webhook URL is ready.

```ruby
 
      webhook_response_type: 'json',
      webhook_response_body: '{ “challenge”: “{{body.verification.Challenge}}” }',


```

If the sender sends a webhook with the body
```ruby
 
    {
      "verification": {
        "Challenge": "abc123"
      }
    }


```

Then Workato would respond with
```ruby
 
    {
      "challenge": "abc123"
    }


```

In some cases, webhook senders may also send an array of events. You may also use regular iterators in Mustache to work with arrays.

For example, if the sender (based on Microsoft Event Grid)sends a webhook validation event with the body
```ruby
 
    [
      {
        "id": "2d1781af-3a4c-4d7c-bd0c-e34b19da4e66",
        "topic": "/subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
        "subject": "",
        "data": {
          "validationCode": "512d38b6-c7b8-40c8-89fe-f46f9e9622b6",
          "validationUrl": "https://rp-eastus2.eventgrid.azure.net:553/eventsubscriptions/myeventsub/validate?id=0000000000-0000-0000-0000-00000000000000&t=2022-10-28T04:23:35.1981776Z&apiVersion=2018-05-01-preview&token=1A1A1A1A"
        },
        "eventType": "Microsoft.EventGrid.SubscriptionValidationEvent",
        "eventTime": "2022-10-28T04:23:35.1981776Z",
        "metadataVersion": "1",
        "dataVersion": "1"
      }
    ]


```

and expects us to respond with the `data.validationCode`. You may define your `webhook_response_body` as such.
```ruby
 
      webhook_response_type: 'json',
      webhook_response_body: '{{#body}}{ "validationResponse": “{{data.validationCode}}” }{{/body}}',


```

There may be a variety of situations where webhook senders may expect custom responses:

  1. Static or dynamic responses for each webhook event
  2. Responding to a challenge to confirm the webhook URL is ready to accept events

In our investigation, we have rarely found both to be the case. As such, this singular key `webhook_response_body` aims to accomplish both use cases. You may also use inbuilt logic such as [inverted sections (opens new window)](<https://mustache.github.io/mustache.5.html#Inverted-Sections>) in mustache templates for greater control over the webhook responses.

* * *

## [#](<#webhook-response-headers>) `webhook_response_headers`

Attribute | Description  
---|---  
Key | `webhook_response_headers`  
Type | String  
Required | Optional. Only applies to Dynamic webhook triggers ( triggers with `webhook_subscribe` and `webhook_unsubscribe`)  
Description | By default, Workato responds with an standard headers (rate limit, byte limit) to webhook events. `webhook_response_headers` allows for a mustache template that allows you to define what headers Workato should include in response headers. See [webhook_response_body](<#webhook-response-body>)  

WARNING

Workato only supports customization of headers starting with `x-` with the exception of `x-forwarded-host`, `x-forwarded-proto`, `x-forwarded-port`, `x-forwarded-for`, `x-request-id`, `x-frame-options` and `x-powered-by`.

* * *

## [#](<#webhook-response-status>) `webhook_response_status`

Attribute | Description  
---|---  
Key | `webhook_response_status`  
Type | Integer  
Required | Optional. Only applies to Dynamic webhook triggers ( triggers with `webhook_subscribe` and `webhook_unsubscribe`)  
Description | By default, Workato responds with 200 to webhook events. `webhook_response_status` allow you to customize this to any 2XX response codes.  

WARNING

Workato only supports customization 2XX response codes.

* * *

## [#](<#webhook-payload-type>) `webhook_payload_type`

Attribute | Description  
---|---  
Key | `webhook_payload_type`  
Type | String  
Required | Optional. Defaults to "parsed"  
Description | By default, Workato parses incoming webhook payloads using [JSON.parse() (opens new window)](<https://ruby-doc.org/stdlib-2.6.3/libdoc/json/rdoc/JSON.html#method-i-parse>). Setting `webhook_payload_type` to "raw" allows you to receive the raw webhook payload instead of a JSON parsed one.  
Example - webhook_payload_type: - Verifying webhooks or handling XML webhooks

Use `webhook_payload_type` in two scenarios:

  1. You need to compute a webhook payload signature based on the **raw** payload. You may do so in the webhook notification lambda before using `workato.parse_json` to get the parsed json payload.

```ruby
 
          webhook_payload_type: "raw",

          webhook_notification: lambda do |input, payload, extended_input_schema, extended_output_schema, headers, params, connection, webhook_subscribe_output|
            original_payload = payload
            client_secret = input['client_secret'] || account_property('hubspot_webhook_client_secret')
            if client_secret.present?
              source_string = client_secret + original_payload
              v1_signature = source_string.encode_sha256.encode_hex
            end

            if (client_secret.present? && v1_signature == headers['X-Hubspot-Signature']) || !client_secret.present?
              payload = workato.parse_json(payload).select do |event|
                event['propertyName'] == input['contact_property'] && event['subscriptionType'] == 'contact.propertyChange'
              end

              if payload.length > 0 
                { 
                  events: payload,
                  headers: headers,
                  webhook_validated: client_secret.present? ? true : false
                }
              end
            end
          end,


```

  2. You are receiving a webhook that is not in JSON format.

```ruby
 
          webhook_payload_type: "raw",

          webhook_notification: lambda do |input, payload, extended_input_schema, extended_output_schema, headers, params, connection, webhook_subscribe_output|
            payload.from_xml
          end,


```

* * *

## [#](<#webhook-subscribe>) `webhook_subscribe`

Attribute | Description  
---|---  
Key | `webhook_subscribe`  
Type | lambda function  
Required | True if trigger is a dynamic webhook trigger. False otherwise. Should not be used when `webhook_key` is defined.  
Description | This lambda function is used by dynamic webhook triggers to programmatically subscribe to webhooks. This function is invoked when a user starts the recipe using the trigger with this defined. See our [Dynamic webhook guide for more details.](</developing-connectors/sdk/guides/building-triggers/dynamic-webhook.html>)  
Possible Arguments | `webhook_url` \- String representing the **recipe-specific webhook URL**. This should be passed on to the API when creating the webhook subscription.   
`connection` \- Hash representing user given inputs defined in `connection`.   
`input` \- Hash representing user given inputs defined in `input_fields`   
`recipe_id` \- Int representing the ID of the recipe in Workato.  
Expected Output | There are two possible outputs:   
\- A hash which is passed on as `webhook_subscribe_output` to `webhook_unsubscribe`, `webhook_notification` and `webhook_refresh` lambda functions.   
\- An array where the first index is the same hash passed on as `webhook_subscribe_output` and the second index is the webhook expiration datetime which will trigger `webhook_refresh`.  
Dealing with webhook subscriptions that expire

Certain APIs like [Microsoft's Graph API (opens new window)](<https://docs.microsoft.com/en-us/graph/api/subscription-post-subscriptions?view=graph-rest-1.0&tabs=http>) allow you to create webhook subscriptions but they expire after a certain amount of time. This means your triggers need to be able to intelligently know when the webhook subscription is about to expire and refresh this subscription so you continue to receive events.

Sample code where webhook expires after 1 hour.
```ruby
 
          webhook_subscribe: lambda do |webhook_url, connection, input, recipe_id|    
            [
              post("https://www.acme.com/api/webhook_subscriptions", url: webhook_url),
              1.hour.from_now
            ]
          end,

          webhook_refresh: lambda do |webhook_subscribe_output|
            [
              patch("https://www.acme.com/api/webhook_subscriptions/#{webhook_subscribe_output['id']}", refresh: true),
              1.hour.from_now
            ]
          end,

          webhook_unsubscribe: lambda do |webhook_subscribe_output, connection|
            delete("https://www.acme.com/api/webhook_subscriptions/#{webhook_subscribe_output['id']}")
          end,


```

In the example above, the output of `webhook_subscribe` is an array that contains a datetime value that corresponds to the next time `webhook_refresh` is invoked to refresh the webhook subscription. This is similarly done for `webhook_refresh` as well. Take note that the output of `webhook_refresh` replaces the original `webhook_subscribe_output` as well.

* * *

## [#](<#webhook-refresh>) `webhook_refresh`

Attribute | Description  
---|---  
Key | `webhook_refresh`  
Type | lambda function  
Required | False. Only applicable when `webhook_subscribe` is defined.  
Description | This lambda function is invoked when your webhook subscription is set to have an expiry time, defined in the output of `webhook_subscribe`. It allows you to refresh as webhook subscriptions so your trigger can continue to receive events.  
Possible Arguments | `webhook_subscribe_output` \- Hash representing the output of the `webhook_subscribe` lambda function.  
Expected Output | \- An array where the first index is the same hash passed on as `webhook_subscribe_output` and the second index is the webhook expiration datetime which will trigger `webhook_refresh`.  

* * *

## [#](<#webhook-unsubscribe>) `webhook_unsubscribe`

Attribute | Description  
---|---  
Key | `webhook_unsubscribe`  
Type | lambda function  
Required | True if trigger is a dynamic webhook trigger. False otherwise. Should not be used when `webhook_key` is defined.  
Description | This lambda function is used by dynamic webhook triggers to programmatically teardown webhooks subscriptions. This function is invoked when a user stops the recipe using the trigger with this defined. See our [Dynamic webhook guide for more details.](</developing-connectors/sdk/guides/building-triggers/dynamic-webhook.html>)  
Possible Arguments | `webhook_subscribe_output` \- Hash representing the output of the `webhook_subscribe` lambda function.   
`connection` \- Hash representing user given inputs defined in `connection`.  
Expected Output | No output necessary.  

* * *

## [#](<#webhook-notification>) `webhook_notification`

Attribute | Description  
---|---  
Key | `webhook_notification`  
Type | lambda function  
Required | True if trigger is either a dynamic webhook trigger or a static webhook trigger.  
Description | This lambda function handles what this trigger should do with a webhook sent to it. You may use this function to do any data manipulation. This lambda function does not allow you to make additional HTTP requests or invoke additional reusable `methods`.  
Possible Arguments | `input` \- Hash representing user given inputs defined in `input_fields`   
`payload` \- Hash representing the incoming webhook's payload.   
`extended_input_schema` \- See below for examples.   
`extended_output_schema` \- See below for examples   
`headers` \- Hash representing the incoming webhook's headers.   
`params` \- Hash representing the incoming webhook's query parameters.   
`connection` \- Hash representing user given inputs defined in `connection`.   
`webhook_subscribe_output` \- Hash representing the output of the `webhook_subscribe` lambda function.  
Expected Output | Hash which represents the output of a single job or an array of hashes which represent individual jobs.  

Note

The webhook_notification lambda does not allow users to call `methods` or HTTP methods. If webhook payloads are skinny, please add actions that can take the output of the trigger to perform additional HTTP requests.

Webhook Validations

  * Workato performs validations on JSON based webhooks - denoted by the webhook's `Content-Type` header, to ensure that the payload is valid JSON. Otherwise, Workato responds with 400 bad request.
  * Incoming webhook payloads are expected to be UTF-8 compatible and Workato responds with 400 bad request if UTF-8 incompatible characters are found.

* * *

## [#](<#poll>) `poll`

Attribute | Description  
---|---  
Key | `poll`  
Type | lambda function  
Required | True if trigger is a [polling trigger](</developing-connectors/sdk/guides/building-triggers/poll.html>) or [Hybrid triggers](</developing-connectors/sdk/guides/building-triggers/hybrid-triggers.html>)  
Description | This lambda function handles the how this trigger retrieves new records from an API to create jobs. This function is invoked every poll interval (5 mins by default but configurable on a recipe level).  
Possible Arguments | `connection` \- Hash representing user given inputs defined in `connection`.   
`input` \- Hash representing user given inputs defined in `input_fields`   
`closure` \- Hash representing the cursor values passed to the `poll` lambda function from the previous execution of this same function.   
`extended_input_schema` \- See below for examples.   
`extended_output_schema` \- See below for examples  
Expected Output | Hash which contains 3 attributes   
\- Array of records to be turned into jobs   
\- Boolean flag which tells the trigger to poll again immediately instead of 5 mins later   
\- Value/Hash which is stored as the closure which will be passed to the next execution of this same function.   
See below for examples  

TIP

Closure values can be either a simple string/integer or a hash if you need to store multiple values for your cursor.

Example - poll:

The poll block's output should be a hash in the following structure:
```ruby
 
        poll: lambda do |connection, input, closure, _eis, _eos|

          # Timestamp which we need to filter records based off.
          updated_since = (closure || input['since']).to_time.utc.iso8601
          request_page_size = 100

          records = get("/records/endpoint").
                      params(
                         # filter for records only updated after this time
                        updated_since: updated_since,
                        page_size: request_page_size
                      )
          # Example JSON response
          # {
          #   data: [
          #     {
          #       "id": "abcd123",
          #       "name": "record1"
          #       ...
          #     },
          #     {
          #       "id": "dcba321",
          #       "name": "record2",
          #       ...
          #     },
          #     ...
          #   ],
          #   total_records: 1000
          # }

          # Derive last updated since timestamp to filter
          next_updated_since = records['data'].last['updated_at'] unless records.blank?

          {
            # Event accepts an array of records. Each record is a new job.
            events: records['data'],
            # Closure value which is passed as closure argument in next poll
            next_poll: next_updated_since,
            # Boolean flag to denote whether we should wait 5 mins to poll or poll immediately.
            # Poll immediately if total records is still more than page size.
            can_poll_more: records['total_records'] >= request_page_size
          }
        end,


```

Example - poll: - extended_input_schema and extended_output_schema

Extended input and output schema is any schema from `object_definitions` that is used in your action. This information is often useful when you dynamically generate schema and you want to use it to do data pre- or post-processing. These arguments do not include config_fields.

For example, you may use extended_input_schema to know which inputs are datetimes and should be transformed to Epoch time which is accepted by the target API. In the same fashion, you may use extended_output_schema to take the response and transform Epoch variables into ISO8601 datetimes again.
```ruby
 
        create_object: {
          description: lambda do |input, picklist_label|
            "Create a <span class='provider'>#{picklist_label['object'] || 'object'}</span> in " \
            "<span class='provider'>Percolate</span>"
          end,

          config_fields: [
            {
              name: 'object',
              control_type: 'select',
              pick_list: 'object_types',
              optional: false
            }
          ],

          input_fields: lambda do |object_definitions, connection, config_fields|
            object = config_fields['object']
            object_definitions[object].ignored('id')
          end,

         execute: lambda do |connection, input, extended_input_schema, extended_output_schema|
           puts extended_input_schema
           # [
           #   {
           #     "type": "string",
           #     "name": "status",
           #     "control_type": "select",
           #     "label": "Status",
           #     "hint": "Status is required for creating Content",
           #     "pick_list": "post_statuses",
           #     "optional": false
           #   },
           #   ...
           # ]

           puts extended_output_schema
           # [
           #   {
           #     "type": "string",
           #     "name": "id",
           #     "control_type": "text",
           #     "label": "Content ID",
           #     "hint": "The Content ID, Example: <b>post:45565410</b>.",
           #     "optional": true
           #   },
           #   {
           #     "type": "string",
           #     "name": "status",
           #     "control_type": "select",
           #     "label": "Status",
           #     "hint": "Status is required for creating Content",
           #     "pick_list": "post_statuses",
           #     "optional": false
           #   },
           #   ...
           # ]
         end,

         output_fields: lambda do |object_definitions, connection, config_fields|
           object = config_fields['object']
           object_definitions[object]
          end,
        }


```

* * *

## [#](<#dedup>) `dedup`

Attribute | Description  
---|---  
Key | `dedup`  
Type | lambda function  
Required | True.  
Description | This lambda function allows you to deduplicate trigger events so you don't trigger off the same events twice. This is done by forming a unique signature string based off attributes of the incoming record.  
Possible Arguments | `record` \- Hash representing a single record. This is a single index in the `events` array of a `poll` lambda function or the Hash output of the `webhook_notification` lambda function. .  
Expected Output | String - "#{record['id']}@#{record['created_at']}" or "#{record['id']}@#{record['updated_at']}"  

* * *

## [#](<#output-fields>) `output_fields`

Attribute | Description  
---|---  
Key | `output_fields`  
Type | lambda function  
Required | True  
Description | This lambda function allows you to define what output fields (datapills) should be shown to a user configuring this trigger in the recipe editor. The output of this lambda function should be an array of hashes, where each hash in this array corresponds to a separate output field (datapill). To know more about how to define input fields in Workato, click [here.](</developing-connectors/sdk/sdk-reference/schema.html>)  
Possible Arguments | `object_definitions` \- Allows you to reference an object definitions. Object definitions are stores of these arrays which can represent either input and output fields. These can be referenced by any action or trigger.   
`connection` \- Hash representing user given inputs defined in `connection`.   
`config_fields` \- Hash representing user given inputs defined in `config_fields`, if applicable.  
Expected Output | Array of hashes. Each hash in this array corresponds to a separate input field.  
UI reference | ![](/assets/img/output_fields.ea775e7c.png)  

* * *

## [#](<#sample-output>) `sample_output`

Attribute | Description  
---|---  
Key | `sample_output`  
Type | lambda function  
Required | False.  
Description | This lambda function allows you to define a sample output that is displayed next to your output fields (datapills).  
Possible Arguments | `connection` \- Hash representing user given inputs defined in `connection`.   
`input` \- Hash representing user given inputs defined in `input_fields`  
Expected Output | Hash. This hash should be a stubbed output of the `execute` lambda function.  
UI reference | ![](/assets/img/sample_output.1785f345.png)  

* * *

## [#](<#summarize-input>) `summarize_input`

Attribute | Description  
---|---  
Key | `summarize_input`  
Type | Array  
Required | False.  
Description | Use this to summarize your input which contain long lists. Summarizing your input is important to keep the jobs page lightweight so it can load quickly. In general, when your input has lists that are longer than 100 lines, they should be summarized.  
Expected Output | Array. For example, `['leads']` or `['report.records', 'report.description']`  

* * *

## [#](<#summarize-output>) `summarize_output`

Attribute | Description  
---|---  
Key | `summarize_output`  
Type | Array  
Required | False.  
Description | Use this to summarize your actions output which contain long lists. Summarizing your output is important to keep the jobs page lightweight so it can load quickly. In general, when your output has lists that are longer than 100 lines, they should be summarized.  
Expected Output | Array. For example, `['leads']` or `['report.records', 'report.description']`  
UI reference | ![](/assets/img/job_input_summarized.631f2b8f.png)  
Example - Summarizing inputs and outputs in job data

When working with large arrays or data, Workato tries to show all the data in the input and output tabs of the job for each action. Sometimes, this can get confusing when we are working with a large numbers of records or large strings. You can use the `summarize_input` and `summarize_output` keys to summarize the data in your job input and output tabs to make it more human readable for users of your connector.
```ruby
 
        input_fields: lambda do
          [
            {
              name: 'report',
              type: 'object',
              properties: [
                {
                  name: 'records',
                  type: :array,
                  of: :object,
                  properties: [
                    {
                      name: 'item_name',
                      type: 'string'
                    }
                  ]
                },
                {
                  name: 'description',
                  type: 'string'
                },
                {
                  name: 'comment',
                  type: 'string'
                }
              ],
            }
          ]
        end,

        summarize_input: ['report.records', 'report.description'],


```
