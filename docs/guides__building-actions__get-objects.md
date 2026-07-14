# Workato SDK Documentation

> **Source**: https://docs.workato.com/en/developing-connectors/sdk/guides/building-actions/get-objects.html
> **Fetched**: 2026-07-14T03:05:18.247574

---

[Connector SDK](</en/developing-connectors/sdk>)

[How-to guides](</en/developing-connectors/sdk/guides>)

[Building actions ](</en/developing-connectors/sdk/guides/building-actions>)

Are you an LLM? You can read better optimized documentation at /en/developing-connectors/sdk/guides/building-actions/get-objects.md for this page in Markdown format

# How-to guides - Get (Retrieve) objects [​](<#how-to-guides-get-retrieve-objects>)

Copy page

In this segment, we will be going through the creation of actions that help retrieve information of an object in our target application. Typically, The `GET` HTTP request method is used to send requests to retrieve objects.

ACTION TIMEOUT

SDK actions have a 180 second [timeout](</en/recipes/recipe-job-errors#timeouts>) limit.

## Sample connector - Zuora [​](<#sample-connector-zuora>)

ruby
```ruby

    {
      title: 'My Zuora connector',

      # More connector code here
      actions: {
        get_account: {
          title: "Get account",

          subtitle: "Retrieves details of an account in Zuora",

          description: lambda do |input, picklist_label|
            "Get an <span class='provider'>account</span> in " \
            "<span class='provider'>Zuora</span>"
          end,

          help: "Retrieves the information of an existing account in Zuora",

          input_fields: lambda do |object_definitions|
            [
              {
                name: "id",
                label: "Account ID",
                hint: "The ID of the specific account that you wish to retrieve."
              }
            ]
          end,

          execute: lambda do |connection, input|
            get("https://rest.zuora.com/v1/object/account/#{input["Id"]}", input).
              after_error_response(/.*/) do |_, body, _, message|
                error("#{message}: #{body}")
              end
          end,

          output_fields: lambda do |object_definitions|
            [
              # Various output fields
            ]
          end
        }
      }
      # More connector code here
    }

```

![Selecting the get account action](/assets/get_overall.CQD8Yomy.png)_Selecting the get account action_

## Step 1 - Action title, subtitle, description, and help [​](<#step-1-action-title-subtitle-description-and-help>)

The first step to making a good action is to properly communicate what the actions does, how it does it and to provide additional help to users. To do so, Workato allows you to define the title, description, and provide hints for an action. Quite simply, the title is the title of an action and the subtitle provides further details of the action. The description of the action then contains specifications and explanation on what the action accomplishes and in the context of the application it connects to. Finally, the help segment provides users any additional information required to make the action work.

To know more about this step, take a look at our [SDK reference](</en/developing-connectors/sdk/sdk-reference/actions#title>)

## Step 2 - Define input fields [​](<#step-2-define-input-fields>)

ruby
```ruby

      input_fields: lambda do |object_definitions|
        [
          {
            name: "id",
            label: "Account ID",
            hint: "The ID of the specific account that you wish to retrieve."
          }
        ]
      end

```

![Get account input fields](/assets/get_input.Ca0v6_IF.png) _Get account input fields_

This component tells Workato what fields to show to a user trying to retrieve an object. In the case of retrieving an account in Zuora for example, the user has to input the ID of the account to be retrieved.

Various other key value pairs exist for input/output fields other than the ones defined above. Refer to [Input fields](</en/developing-connectors/sdk/sdk-reference/actions#input-fields>) for more information.

Object definitions

Note that `object_definitions` is passed in as an argument. Workato allows connector builders to supply the definitions of an object separately in the "object_definitions" key. This key is used when the definitions of an object are large and/or can be dynamically obtained.

To know more about this, take a look at our [SDK reference](</en/developing-connectors/sdk/sdk-reference/object_definitions>)

## Step 3 - Defining the execute key [​](<#step-3-defining-the-execute-key>)

The execute key tells Workato the endpoint to send the request to and using which HTTP request method. In this example, we send our request to `https://rest.zuora.com/v1/object/account/#{input["Id"]}` using the `Get` method. We also append the `after_error_response` method to the request to catch any errors and to display them to users to aid in the debugging during recipe building.

For this get action, we append the `id` \- Account ID input by the user to the API endpoint to tell Workato and subsequently Zuora, which specific account to retrieve.

ruby
```ruby

      execute: lambda do |connection, input|
        get("https://rest.zuora.com/v1/object/account/#{input["id"]}", input).
          after_error_response(/.*/) do |_, body, _, message|
            error("#{message}: #{body}")
          end
      end

```

![Get account error](/assets/create_error.B78gvRXW.png) _Error example_

To know more about the execute key, take a look at our [SDK reference](</en/developing-connectors/sdk/sdk-reference/actions#execute>)

## Step 4 - Defining output fields [​](<#step-4-defining-output-fields>)

This section tells us what datapills to show as the output of the trigger. The `name` attributes of each datapill should match the keys in the output of the `execute` key.

ruby
```ruby

      output_fields: lambda do |object_definitions|
        [
          # Various output fields
        ]
      end

```

![Get account output fields](/assets/get_output.DYNX9VYj.png) _Get account output fields_

To know more about the output fields key, take a look at our [SDK reference](</en/developing-connectors/sdk/sdk-reference/actions#output-fields>)

Object definitions

Note that `object_definitions` is passed in as an argument. Workato allows connector builders to supply the definitions of an object separately in the "object_definitions" key. This key is used when the definitions of an object are large and/or can be dynamically obtained.

To know more about this, take a look at our [SDK reference](</en/developing-connectors/sdk/sdk-reference/object_definitions>)

**Last updated:**
