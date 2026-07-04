# Workato SDK Documentation

> **Source**: https://docs.workato.com/en/developing-connectors/sdk/guides/building-triggers/poll.html
> **Fetched**: 2026-07-04T03:07:28.248998

---

[Connector SDK](</en/developing-connectors/sdk>)

[How-to guides](</en/developing-connectors/sdk/guides>)

[Building triggers](</en/developing-connectors/sdk/guides/building-triggers>)

Are you an LLM? You can read better optimized documentation at /en/developing-connectors/sdk/guides/building-triggers/poll.md for this page in Markdown format

# How-to guides - Polling Trigger [​](<#how-to-guides-polling-trigger>)

Copy page

A poll trigger constantly executes a poll key for new events at fixed time intervals. This time interval defaults to every 5 minutes but can be changed by users when configuring the trigger in a recipe. Polling triggers function by executing a HTTP request every interval to query an API for new records or events since the last time it polled. This is possible via cursors embedded in the trigger logic.

## Sample connector - Freshdesk [​](<#sample-connector-freshdesk>)

ruby
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

## Step 1 - Trigger title, subtitle, description, and help [​](<#step-1-trigger-title-subtitle-description-and-help>)

The first step to making a good trigger is to properly communicate what the trigger does and to provide additional help to users. To do so, Workato allows you to define the title, description, and provide hints for an action. Quite simply, the title is the title of an action and the subtitle provides further details of the action. The description of the action then contains specifications and explanation on what the action accomplishes and in the context of the application it connects to. Finally, the help segment provides users any additional information required to make the action work.

To know more about this step, take a look at our [SDK reference](</en/developing-connectors/sdk/sdk-reference/triggers#title>)

## Step 2 - Define input fields [​](<#step-2-define-input-fields>)

This component tells Workato what fields to show to a user configuring this trigger. In this case, we want a simple input field that allows a user to pick a timestamp value. This will be used in our trigger code later on to pull tickets created/updated before the recipe was started. This is a great tool to provide to users of your connector for retrospective syncs of data.

ruby
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

![New/updated ticket input fields](/assets/new_ticket_input.Cj3w4dQ5.png) _New/updated ticket input fields_

Various other key value pairs exist for input/output fields other than the ones defined above. Refer to [Input fields](</en/developing-connectors/sdk/sdk-reference/triggers#input-fields>) for more information.

Object definitions

Note that `object_definitions` is passed in as an argument. Workato allows connector builders to supply the definitions of an object separately in the "object_definitions" key. This key is used when the definitions of an object are large and/or can be dynamically obtained.

To know more about this, take a look at our [SDK reference](</en/developing-connectors/sdk/sdk-reference/object_definitions>)

## Step 3 - Defining the poll key [​](<#step-3-defining-the-poll-key>)

The poll key tells Workato what to do every time interval. At every time interval, this `poll` lambda function will be invoked and expect to receive any applicable new/updated tickets.

ruby
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

To know more about the poll key, take a look at our [SDK reference](</en/developing-connectors/sdk/sdk-reference/triggers#poll>)

## Step 4 - Defining output fields and dedup [​](<#step-4-defining-output-fields-and-dedup>)

This section tells us what datapills to show as the output of the trigger as well as how to prevent duplicate records to create duplicate jobs. To prevent a job from being repeated (this might happen due to a bug on the API end), use the `dedup` key which tells your connector how to create a unique signature for each record. This signature is stored for each recipe and if a record with the same signature is found, no job will be created.

For datapills, use the `output_fields` key. The `name` attributes of each datapill should match the keys of a single ticket record.

ruby
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

![New/updated ticket output fields](/assets/ticket_output.B1ihfv14.png) _New/updated ticket output fields_

ruby
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

To know more about the output fields key, take a look at our [SDK reference](</en/developing-connectors/sdk/sdk-reference/triggers#output-fields>)

Object definitions

Note that `object_definitions` is passed in as an argument. Workato allows connector builders to supply the definitions of an object separately in the "object_definitions" key. This key is used when the definitions of an object are large and/or can be dynamically obtained.

To know more about this, take a look at our [SDK reference](</en/developing-connectors/sdk/sdk-reference/object_definitions>)

## Step 5 - Defining sample output [​](<#step-5-defining-sample-output>)

A optional supplementary component to a connector, the sample output key nonetheless greatly improves a user's experience by giving him/her some context to what the datapill's value could be. This allows users to build recipes more quickly.

ruby
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

To know more about the sample output key, take a look at our [SDK reference](</en/developing-connectors/sdk/sdk-reference/triggers#sample-output>)

**Last updated:**
