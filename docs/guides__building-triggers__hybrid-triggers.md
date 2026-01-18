# Workato SDK Documentation

> **Source**: https://docs.workato.com/en/developing-connectors/sdk/guides/building-triggers/hybrid-triggers.html
> **Fetched**: 2026-01-18T02:49:59.349998

---

# [#](<#how-to-guides-hybrid-polling-webhook-triggers>) How-to guides - Hybrid polling + webhook triggers

Webhooks open up a wide range of use cases that are time sensitive in nature, such as receiving the event when a customer makes a purchase. There are, however, scenarios where webhook events can be lost. This could be due to transient network errors that any HTTP requests can be susceptible to, or simply when the recipe is stopped for a short period of time and webhooks were sent during that period.

Hybrid polling + webhook triggers give you the best of both worlds, where your triggers can function in real-time to produce jobs but also provide you with the additional guarantee of picking up events even if the webhook was lost.

Before continuing

The guide below builds on top of knowledge for both webhook and polling triggers. It is recommended that you read through the guides for those respective triggers first.

## [#](<#why-implement-hybrid-triggers>) Why implement Hybrid triggers

Hybrid triggers present numerous benefits over traditional webhook triggers through three key improvements:

  1. Webhook events trigger a signal to Workato to pull new records from the target system. This lowers potential for spoofed webhooks from creating bad data and also ensures that potentially lost webhooks will still be retrieve when a new webhook is eventually received.
  2. Allow your trigger output for each job to have all data needed, instead of a skinny payload that is often sent in the webhook.
  3. Prevent job loss when a recipe is stopped for a period of time. When the recipe is started again, Workato executes a poll immediately to retrieve all records.

## [#](<#mechanics-of-hybrid-triggers>) Mechanics of Hybrid triggers

Hybrid trigger combine important lambdas from webhook triggers and polling triggers respectively. For static webhook hybrid triggers, you will need the `webhook_keys` and `webhook_key` lambdas, alongside the `poll` lambda. For dynamic webhook hybrid triggers, you will need the `webhook_subscribe` and `webhook_unsubscribe` lambdas, alongside the `poll` lambda.

When using hybrid triggers, the mechanics for pulling events change in 2 significant ways:

  1. When a webhook event is received, the `poll` lambda is invoked to get new events based on the closure from the previous poll.
  2. When a recipe is started/restarted, the `poll` lambda is invoked to get new events based on the closure from the previous poll.

TIP

In the case of a burst of webhook events to a trigger, Workato's engine throttles polls intelligently to pull all records without having poll the API for each webhook event. This prevents rate limits from being hit from busy webhooks.

For example, when a burst of 100 webhook events are received over 1 minute, you can expect to receive 4-5 polls with the last poll being later than the time when the last webhook event was received.

Workato also executes the `poll` lambda every 12 hours to ensure that in case of webhook outages, records are still picked up with some delay.

## [#](<#sample-connector-chargebee>) Sample connector - Chargebee
```ruby
 
    {
      title: 'My Chargebee connector',

      webhook_keys: lambda do |params, headers, payload|
        # Chargebee events come in the form "subscription_changed", "subscription_renewed", "customer_changed" etc
        # Use .split to get the main object
        "#{payload['event_type']}".split("_").first
      end,

      # More connector code here
      triggers: {
        new_updated_subscription: {
          title: 'New/updated subscription',

          subtitle: "Triggers when a subscription is " \
          "created/updated in Chargebee",

          description: lambda do |input, picklist_label|
            "New/updated <span class='provider'>subscription</span> in " \
            "<span class='provider'>Chargebee</span>"
          end,

          help: lambda do |input, picklist_label, connection, webhook_base_url|
            next unless webhook_base_url.present?
            <<~HTML
            Creates a job immediately when a subscription is created/updated from Chargebee. To set this webhook up,
            you will need to register the webhook below in Chargebee under "settings" => "webhooks" => "new" and provide the events for subscription_changed and subscription_created. <br>
            <b>Webhook endpoint URL</b>
            <b class="tips__highlight">#{webhook_base_url}</b>
            HTML
          end,

          input_fields: lambda do
             [
               {
                 name: 'since',
                 type: :timestamp,
                 optional: true
               }
             ]
          end,

          webhook_key: lambda do |connection, input|
            "subscription"
          end,

          poll: lambda do |connection, input, closure|
            page_size = 100
             closure = {} unless closure.present?
             closure['updated_since'] = (closure['updated_since'] || input['since'] || 1.hours.ago).to_time.utc.to_i 

             params = {
                "sort_by[asc]": 'updated_at',
                limit: page_size,
                "updated_at[after]": closure['updated_since']
             }

             params['offset'] = closure['offset'] 

             response = get("/api/v2/subscriptions", params)

             if response['next_offset'].present?
               closure['offset'] = response['next_offset']
             else
               closure['offset'] = nil
               closure['updated_since'] = response['list'].last[input['object']]['updated_at'] unless response['list'].size == 0 
             end

             {
               events: response['list'],
               next_poll: closure,
               can_poll_more: response['next_offset'].present?
             } 
          end,

          dedup: lambda do |record|
            "#{record['subscription']['id']}@#{record['subscription']['updated_at']}"
          end,

          output_fields: lambda do |object_definitions|
            object_definitions['subscription']
          end
        }
      },
      # More connector code here
    }


```

## [#](<#step-1-implement-your-chosen-webhook-trigger>) Step 1 - Implement your chosen webhook trigger

Depending on what the app you are building the connector for, build the appropriate webhook trigger type. Dynamic webhooks are always preferred as they minimize the amount of setup needed by the end user. In our example, Chargebee requires you to manually setup webhook subscriptions so we have used a static webhook trigger. Refer more to our guides on each of the types of webhooks to learn more.

For dynamic webhook triggers, you are expected to define the `webhook_subscribe` and `webhook_unsubscribe` lambda. For static webhook triggers, you are expected to define the `webhook_keys` and `webhook_key` lambda.

## [#](<#step-2-define-the-poll-block>) Step 2 - Define the poll block

Instead of defining the `webhook_notification` lambda, building a hybrid trigger requires that you define the `poll` lambda instead. The `poll` lambda should function similar to any other polling trigger, whereby it needs an API endpoint to pull new records. [Refer to our polling trigger guides to understand more.](</developing-connectors/sdk/guides/building-triggers/poll.html>)
```ruby
 
          poll: lambda do 
            page_size = 100
             closure = {} unless closure.present?
             closure['updated_since'] = (closure['updated_since'] || input['since'] || 1.hours.ago).to_time.utc.to_i 

             params = {
                "sort_by[asc]": 'updated_at',
                limit: page_size,
                "updated_at[after]": closure['updated_since']
             }

             params['offset'] = closure['offset'] 

             response = get("/api/v2/subscriptions", params)

             if response['next_offset'].present?
               closure['offset'] = response['next_offset']
             else
               closure['offset'] = nil
               closure['updated_since'] = response['list'].last[input['object']]['updated_at'] unless response['list'].size == 0 
             end

             {
               events: response['list'],
               next_poll: closure,
               can_poll_more: response['next_offset'].present?
             } 
          end,


```

In our example, we simply query Chargebee's subscription API to give us the subscriptions created/updated after the last time we polled.

## [#](<#step-4-defining-output-fields-and-dedup>) Step 4 - Defining output fields and dedup

When defining the output fields and dedup, take note that this should be based on the `poll` lambda's output and not the actual webhook payload. Essentially, the webhook payload is discarded in favor of the records received in the `poll` lambda.
```ruby
 
          dedup: lambda do |record|
            "#{record['subscription']['id']}@#{record['subscription']['updated_at']}"
          end,

          output_fields: lambda do |object_definitions|
            object_definitions['subscription']
          end


```

## [#](<#rate-limits>) Rate limits

This trigger is subject to our [webhook gateway's limits.](</troubleshooting/webhook-gateway-limits.html>)
