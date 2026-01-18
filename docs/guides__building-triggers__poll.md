# Workato SDK Documentation

> **Source**: https://docs.workato.com/en/developing-connectors/sdk/guides/building-triggers/poll.html
> **Fetched**: 2026-01-18T02:50:00.507148

---

# [#](<#how-to-guides-polling-trigger>) How-to guides - Polling Trigger

A poll trigger constantly executes a poll key for new events at fixed time intervals. This time interval defaults to every 5 minutes but can be changed by users when configuring the trigger in a recipe. Polling triggers function by executing a HTTP request every interval to query an API for new records or events since the last time it polled. This is possible via cursors embedded in the trigger logic.

## [#](<#sample-connector-freshdesk>) Sample connector - Freshdesk
```ruby
 
    {
      title: 'My Freshdesk connector',

      # More connector code here
      triggers: {
        updated_ticket: {
          title: 'New/updated ticket',

          subtitle: "Triggers when a ticket is created or " \
          "updated in Freshdesk",

          description: lambda do |input, picklist_label|
            "New/updated <span class='provider'>ticket</span> " \
            "in <span class='provider'>Freshdesk</span>"
          end,

          help: "Creates a job when tickets are created or " \
          "updated in Freshdesk. Each ticket creates a separate job.",

          input_fields: lambda do |object_definitions|
            [
              {
                name: 'since',
                label: 'When first started, this recipe should pick up events from',
                type: 'timestamp',
                optional: true,
                sticky: true,
                hint: 'When you start recipe for the first time, it picks up ' \
                'trigger events from this specified date and time. Defaults to ' \
                'the current time.'
              }
            ]
          end,

          poll: lambda do |connection, input, closure, _eis, _eos|

            closure = {} unless closure.present?

            page_size = 100

            updated_since = (closure['cursor'] || input['since'] || Time.now ).to_time.utc.iso8601

            tickets = get("https://#{connection['helpdesk']}.freshdesk.com/api/v2/tickets.json").
                      params(order_by: 'updated_at',
                             order_type: 'asc',
                             per_page: page_size,
                             updated_since: updated_since)

            closure['cursor'] = tickets.last['updated_at'] unless tickets.blank?

            {
              events: tickets,
              next_poll: closure,
              can_poll_more: tickets.length >= page_size
            }
          end,

          dedup: lambda do |record|
            "#{record['id']}@#{record['updated_at']}"
          end,

          output_fields: lambda do |object_definitions|
            [
              {
                name: 'id',
                type: 'integer'
              },
              {
                name: 'email'
              },
              {
                name: 'subject'
              },
              {
                name: 'description'
              },
              {
                name: 'created_at'
              },
              {
                name: 'updated_at'
              }
            ]
          end,

          sample_output: lambda do |connection, input|
            {
              "id": 1234,
              "email": "[[email protected]](</cdn-cgi/l/email-protection>)",
              "subject": "Account provisioning",
              "description": "I need access to my account"
            }
          end
        }
      }
      # More connector code here
    }


```

## [#](<#step-1-trigger-title-subtitle-description-and-help>) Step 1 - Trigger title, subtitle, description, and help

The first step to making a good trigger is to properly communicate what the trigger does and to provide additional help to users. To do so, Workato allows you to define the title, description, and provide hints for an action. Quite simply, the title is the title of an action and the subtitle provides further details of the action. The description of the action then contains specifications and explanation on what the action accomplishes and in the context of the application it connects to. Finally, the help segment provides users any additional information required to make the action work.

To know more about this step, take a look at our [SDK reference](</developing-connectors/sdk/sdk-reference/triggers.html#title>)

## [#](<#step-2-define-input-fields>) Step 2 - Define input fields

This component tells Workato what fields to show to a user configuring this trigger. In this case, we want a simple input field that allows a user to pick a timestamp value. This will be used in our trigger code later on to pull tickets created/updated before the recipe was started. This is a great tool to provide to users of your connector for retrospective syncs of data.
```ruby
 
      input_fields: lambda do |object_definitions|
        [
          {
            name: 'since',
            label: 'When first started, this recipe should pick up events from',
            type: 'timestamp',
            optional: true,
            sticky: true,
            hint: 'When you start recipe for the first time, it picks up ' \
            'trigger events from this specified date and time. Defaults to ' \
            'the current time.'
          }
        ]
      end


```

![New/updated ticket input fields](/assets/img/new_ticket_input.dfe073e7.png) _New/updated ticket input fields_

Various other key value pairs exist for input/output fields other than the ones defined above. Click [here](</developing-connectors/sdk/sdk-reference/triggers.html#input-fields>) to find out more.

Object definitions

Note that `object_definitions` is passed in as an argument. Workato allows connector builders to supply the definitions of an object separately in the "object_definitions" key. This key is used when the definitions of an object are large and/or can be dynamically obtained.

To know more about this, take a look at our [SDK reference](</developing-connectors/sdk/sdk-reference/object_definitions.html>)

## [#](<#step-3-defining-the-poll-key>) Step 3 - Defining the poll key

The poll key tells Workato what to do every time interval. At every time interval, this `poll` lambda function will be invoked and expect to receive any applicable new/updated tickets.
```ruby
 
        poll: lambda do |connection, input, closure, _eis, _eos|

          closure = {} unless closure.present? # initialize the closure hash when recipe is first started.

          page_size = 100

          updated_since = (closure['cursor'] || input['since'] || Time.now ).to_time.utc.iso8601

          tickets = get("/tickets.json").
                    params(order_by: 'updated_at',
                           order_type: 'asc',
                           per_page: page_size,
                           updated_since: updated_since)

          closure['cursor'] = tickets.last['updated_at'] unless tickets.blank?

          {
            events: tickets,
            next_poll: closure,
            can_poll_more: tickets.length >= page_size
          }
        end,


```

In the example above, we receive 3 arguments:

  1. `connection` \- Corresponds to the values given by the user when making the connection to Freshworks
  2. `input` \- Corresponds to the inputs of this trigger. In this case, it's a single input: `since`
  3. `closure` \- Corresponds to a hash that was passed from the previous poll. `nil` when the recipe is first started

Inside the `poll` lambda function, we go on to initialize the `closure` argument as an object before initializing a new variable `updated_since` as well. This `updated_since` variable is either assigned to `closure['cursor']` if it is present (indicating a cursor passed from a previous poll) or the `input['since']` indicating this is the first poll when a recipe was first started.

In the following lines, we send a GET request to the `/tickets.json` endpoint with query parameters to retrieve the relevant tickets. `closure['cursor']` is updated to the timestamp of the last ticket's `updated_at` attribute if there were any tickets.

The expected output of the `poll` lambda function is a object that should have 3 keys:

  * `events` \- The array of events, or data, should be passed into the events key. Each index in the array will be processed as a separate job.
  * `next_poll` \- This becomes the closure argument in the next poll of the trigger.
  * `can_poll_more` \- This tells the trigger to poll again immediately or poll during the next interval. This is used when there are 100 tickets returned from Freshdesk, indicating there might be more tickets that have been created/updated in the time since the previous poll.

To know more about the poll key, take a look at our [SDK reference](</developing-connectors/sdk/sdk-reference/triggers.html#poll>)

## [#](<#step-4-defining-output-fields-and-dedup>) Step 4 - Defining output fields and dedup

This section tells us what datapills to show as the output of the trigger as well as how to prevent duplicate records to create duplicate jobs. To prevent a job from being repeated (this might happen due to a bug on the API end), use the `dedup` key which tells your connector how to create a unique signature for each record. This signature is stored for each recipe and if a record with the same signature is found, no job will be created.

For datapills, use the `output_fields` key. The `name` attributes of each datapill should match the keys of a single ticket record.
```ruby
 
        dedup: |record|
          "#{record['id']}@#{record['updated_at']}"
        end,

        output_fields: lambda do |object_definitions|
          [
            {
              name: 'id',
              type: 'integer'
            },
            {
              name: 'email'
            },
            {
              name: 'subject'
            },
            {
              name: 'description'
            }
          ]
        end


```

![New/updated ticket output fields](data:image/png;base64,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) _New/updated ticket output fields_
```bash
 
      # Entire tickets array assigned to the events key
      [
        {
          "id": 1234,
          "email": "[[email protected]](</cdn-cgi/l/email-protection>)",
          "subject": "Account provisioning",
          "description": "I need access to my account"
        },
        {
          "id": 4321,
          "email": "[[email protected]](</cdn-cgi/l/email-protection>)",
          "subject": "Account deprovisioning",
          "description": "I want to cancel my account"
        },
        ...
      ]


```

To know more about the output fields key, take a look at our [SDK reference](</developing-connectors/sdk/sdk-reference/triggers.html#output-fields>)

Object definitions

Note that `object_definitions` is passed in as an argument. Workato allows connector builders to supply the definitions of an object separately in the "object_definitions" key. This key is used when the definitions of an object are large and/or can be dynamically obtained.

To know more about this, take a look at our [SDK reference](</developing-connectors/sdk/sdk-reference/object_definitions.html>)

## [#](<#step-5-defining-sample-output>) Step 5 - Defining sample output

A optional supplementary component to a connector, the sample output key nonetheless greatly improves a user's experience by giving him/her some context to what the datapill's value could be. This allows users to build recipes more quickly.
```ruby
 
        sample_output: lambda do |connection, input|
          {
            "id": 1234,
            "email": "[[email protected]](</cdn-cgi/l/email-protection>)",
            "subject": "Account provisioning",
            "description": "I need access to my account"
          }
        end


```

To know more about the sample output key, take a look at our [SDK reference](</developing-connectors/sdk/sdk-reference/triggers.html#sample-output>)
