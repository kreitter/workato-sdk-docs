# Workato SDK Documentation

> **Source**: https://docs.workato.com/en/developing-connectors/sdk/guides/building-actions/get-objects.html
> **Fetched**: 2026-01-18T02:49:46.635909

---

# [#](<#how-to-guides-get-retrieve-objects>) How-to guides - Get (Retrieve) objects

In this segment, we will be going through the creation of actions that help retrieve information of an object in our target application. Typically, The `GET` HTTP request method is used to send requests to retrieve objects.

ACTION TIMEOUT

SDK actions have a 180 second [timeout](</recipes/recipe-job-errors.html#timeouts>) limit.

## [#](<#sample-connector-zuora>) Sample connector - Zuora
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

![Selecting the get account action](/assets/img/get_overall.35232818.png) _Selecting the get account action_

## [#](<#step-1-action-title-subtitle-description-and-help>) Step 1 - Action title, subtitle, description, and help

The first step to making a good action is to properly communicate what the actions does, how it does it and to provide additional help to users. To do so, Workato allows you to define the title, description, and provide hints for an action. Quite simply, the title is the title of an action and the subtitle provides further details of the action. The description of the action then contains specifications and explanation on what the action accomplishes and in the context of the application it connects to. Finally, the help segment provides users any additional information required to make the action work.

To know more about this step, take a look at our [SDK reference](</developing-connectors/sdk/sdk-reference/actions.html#title>)

## [#](<#step-2-define-input-fields>) Step 2 - Define input fields
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

![Get account input fields](/assets/img/get_input.b0f6e957.png) _Get account input fields_

This component tells Workato what fields to show to a user trying to retrieve an object. In the case of retrieving an account in Zuora for example, the user has to input the ID of the account to be retrieved.

Various other key value pairs exist for input/output fields other than the ones defined above. Click [here](</developing-connectors/sdk/sdk-reference/actions.html#input-fields>) to find out more.

Object definitions

Note that `object_definitions` is passed in as an argument. Workato allows connector builders to supply the definitions of an object separately in the "object_definitions" key. This key is used when the definitions of an object are large and/or can be dynamically obtained.

To know more about this, take a look at our [SDK reference](</developing-connectors/sdk/sdk-reference/object_definitions.html>)

## [#](<#step-3-defining-the-execute-key>) Step 3 - Defining the execute key

The execute key tells Workato the endpoint to send the request to and using which HTTP request method. In this example, we send our request to `https://rest.zuora.com/v1/object/account/#{input["Id"]}` using the `Get` method. We also append the `after_error_response` method to the request to catch any errors and to display them to users to aid in the debugging during recipe building.

For this get action, we append the `id` \- Account ID input by the user to the API endpoint to tell Workato and subsequently Zuora, which specific account to retrieve.
```ruby
 
      execute: lambda do |connection, input|
        get("https://rest.zuora.com/v1/object/account/#{input["id"]}", input).
          after_error_response(/.*/) do |_, body, _, message|
            error("#{message}: #{body}")
          end
      end


```

![Get account error](/assets/img/create_error.d2fefe6d.png) _Error example_

To know more about the execute key, take a look at our [SDK reference](</developing-connectors/sdk/sdk-reference/actions.html#execute>)

## [#](<#step-4-defining-output-fields>) Step 4 - Defining output fields

This section tells us what datapills to show as the output of the trigger. The `name` attributes of each datapill should match the keys in the output of the `execute` key.
```ruby
 
      output_fields: lambda do |object_definitions|
        [
          # Various output fields
        ]
      end


```

![Get account output fields](/assets/img/get_output.74815f89.png) _Get account output fields_

To know more about the output fields key, take a look at our [SDK reference](</developing-connectors/sdk/sdk-reference/actions.html#output-fields>)

Object definitions

Note that `object_definitions` is passed in as an argument. Workato allows connector builders to supply the definitions of an object separately in the "object_definitions" key. This key is used when the definitions of an object are large and/or can be dynamically obtained.

To know more about this, take a look at our [SDK reference](</developing-connectors/sdk/sdk-reference/object_definitions.html>)
