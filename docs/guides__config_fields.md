# Workato SDK Documentation

> **Source**: https://docs.workato.com/en/developing-connectors/sdk/guides/config_fields.html
> **Fetched**: 2026-01-18T02:50:03.982200

---

# [#](<#how-to-guides-using-config-fields>) How-to guides - Using Config fields

Occasionally, input/output fields depend on user input. For example, when input fields for an action depend on a user's input in the same action. Here, we introduce `config_fields`. It is an optional key available in both actions and triggers. It is a special type of input field that can be used to generate other dependent input/output fields.

TIP

Config fields keys can be used in both actions and triggers to introduce dynamicity to your connector.

## [#](<#sample-connector-chargebee>) Sample connector - Chargebee
```ruby
 
    {
      title: "Chargebee",

      # More connector code here

      actions: {
        create_object: {
          title: "Create object",
          subtitle: "Create object in Chargebee",

          description: lambda do |input, picklist_label|
            "Create <span class='provider'>#{picklist_label['object'] || 'object'}</span> in <span class='provider'>Chargebee</span>"
          end,

          config_fields: [
            {
              name: "object",
              label: "Object",
              control_type: 'select',
              pick_list: "objects",
              optional: false
            }
          ],

          input_fields: lambda do |object_definitions, connection, config_fields|
            object = config_fields['object']

            object_definitions[object]
          end,

          execute: lambda do |connection, input|
            object = input.delete('object')

            # Route to the appropriate endpoint based on selected object
            endpoint = case object
            when 'customer'
              '/api/v2/customers'
            when 'subscription'
              '/api/v2/subscriptions'
            when 'plan'
              '/api/v2/plans'
            else
              raise "Unsupported object type: #{object}"
            end

            post(endpoint, input).
              request_format_www_form_urlencoded
          end,

          output_fields: lambda do |object_definitions, connection, config_fields|
            object = config_fields['object']

            object_definitions[object]
          end
        }
      },

      object_definitions: {
        customer: {
          fields: lambda do |connection, config_fields, object_definitions|
            get("/api/v2/customers", limit: 1).
              dig('list',0,'customer').
              map do |key, value|
                if value.is_a?(Integer)
                  type = 'integer'
                  control_type = 'number'
                else 
                  type = 'string'
                  control_type = 'text'
                end

                {
                  name: key,
                  label: key.labelize,
                  type: type,
                  control_type: control_type,
                  sticky: true
                }
              end
          end
        },

        subscription: {
          fields: lambda do |connection, config_fields, object_definitions|
            get("/api/v2/subscriptions", limit: 1).
              dig('list',0,'subscription').
              map do |key, value|
                if value.is_a?(Integer)
                  type = 'integer'
                  control_type = 'number'
                else 
                  type = 'string'
                  control_type = 'text'
                end

                {
                  name: key,
                  label: key.labelize,
                  type: type,
                  control_type: control_type,
                  sticky: true
                }
              end
          end
        },

        plan: {
          fields: lambda do |connection, config_fields, object_definitions|
            get("/api/v2/plans", limit: 1).
              dig('list',0,'plan').
              map do |key, value|
                if value.is_a?(Integer)
                  type = 'integer'
                  control_type = 'number'
                else 
                  type = 'string'
                  control_type = 'text'
                end

                {
                  name: key,
                  label: key.labelize,
                  type: type,
                  control_type: control_type,
                  sticky: true
                }
              end
          end
        }
      },

      pick_lists: {
        objects: lambda do
          [
            ["Subscription", "subscription"],
            ["Customer", "customer"],
            ["Plans", "plan"]
          ]
        end,
      }
    }


```

  * [Chargebee API (opens new window)](<https://apidocs.chargebee.com/docs/api/customers?prod_cat_ver=1#create-usecases>)

## [#](<#step-1-action-title-subtitle-description-and-help>) Step 1 - Action title, subtitle, description, and help

The first step to making a good action is to properly communicate what the actions does, how it does it and to provide additional help to users. To do so, Workato allows you to define the title, description, and provide hints for an action. Quite simply, the title is the title of an action and the subtitle provides further details of the action. The description of the action then contains specifications and explanation on what the action accomplishes and in the context of the application it connects to. Finally, the help segment provides users any additional information required to make the action work.

To know more about this step, take a look at our [SDK reference](</developing-connectors/sdk/sdk-reference/actions.html#title>)

## [#](<#step-2-define-config-fields>) Step 2 - Define config_fields

The `config_fields` key allows us to first collect some input from the end user to generate more input fields. In this action, we want the user to first select the object that they want to create, then use that input to generate fields relevant to the object they have just selected.
```ruby
 
      config_fields: [
        {
          name: "object",
          label: "Object",
          control_type: 'select',
          pick_list: "objects",
          optional: false
        }
      ],


```

Here, we are using the `select` control_type which indicates a select drop-down input field. The valid options in this drop-down are from the `objects` picklist - `Subscription`, `Customer` and `Plans`.

![config-select](data:image/png;base64,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) _Config fields look like input fields to the user_

## [#](<#step-3-define-input-fields>) Step 3 - Define input_fields

With config_fields defined, we can now utilize the `config_fields` argument passed to the `input_fields` lambda function. We can reference the input given for the Object input drop-down from this argument and route it to the proper object_definition.
```ruby
 
      input_fields: lambda do |object_definitions, connection, config_fields|
        object = config_fields['object']

        object_definitions[object]
      end,


```

For example, if the user selects the `Customer` input in the drop-down, the `input_fields` key would call the `object_definition['customer']`.
```ruby
 
      object_definitions: {
        customer: {
          fields: lambda do |connection, config_fields, object_definitions|
            get("/api/v2/customers", limit: 1).
              dig('list',0,'customer').
              map do |key, value|
                if value.is_a?(Integer)
                  type = 'integer'
                  control_type = 'number'
                else 
                  type = 'string'
                  control_type = 'text'
                end

                {
                  name: key,
                  label: key.labelize,
                  type: type,
                  control_type: control_type,
                  sticky: true
                }
              end
          end
        }
      },


```

The `object_definition['customer']` key sends a secondary request to Chargebee and transforms the response into [Workato Schema](</developing-connectors/sdk/sdk-reference/schema.html>).

![config-select](/assets/img/input-fields-dynamics.e6afb281.gif) _Selecting customers creates additional fields_

## [#](<#step-4-defining-the-execute-key>) Step 4 - Defining the execute key

The execute key tells Workato the endpoint to send the request to and which HTTP request method to use. Different objects usually require posting to different endpoints. Extract the config field value from the `input` hash before you send the request to the API.
```ruby
 
      execute: lambda do |connection, input|
        object = input.delete('object')

        # Route to the appropriate endpoint based on selected object
        endpoint = case object
        when 'customer'
          '/api/v2/customers'
        when 'subscription'
          '/api/v2/subscriptions'
        when 'plan'
          '/api/v2/plans'
        else
          raise "Unsupported object type: #{object}"
        end

        post(endpoint, input).
          request_format_www_form_urlencoded
      end,


```

In this example:

  * We extract the selected object using `input.delete('object')`, which returns the value and removes it from the input hash
  * We use a `case` statement to map each object type to its corresponding API endpoint
  * We construct the appropriate POST request to the endpoint for the selected object
  * Chargebee requires the input to be form urlencoded so we use `.request_format_www_form_urlencoded`

USE STRING INTERPOLATION TO SIMPLIFY ROUTING

You can simplify routing with string interpolation when your API endpoints follow a consistent pattern (such as `/api/v2/{object}s`):
```ruby
 
    execute: lambda do |connection, input|
      object = input.delete('object')

      post("/api/v2/#{object}s", input).
        request_format_www_form_urlencoded
    end,


```

Use the explicit `case` statement approach shown in the preceding example when endpoint paths vary or require additional logic.

## [#](<#step-5-defining-output-fields>) Step 5 - Defining output fields

For the output fields, we use the same logic as step 3 to generate the output fields.
```ruby
 
      output_fields: lambda do |object_definitions, connection, config_fields|
        object = config_fields['object']

        object_definitions[object]
      end


```

![config-select](/assets/img/output-fields-dynamics.7b85888e.gif) _Selecting customers creates additional fields_

Object definitions

Note that `object_definitions` is passed in as an argument. Workato allows connector builders to supply the definitions of an object separately in the "object_definitions" key. This key is used when the definitions of an object are large and/or can be dynamically obtained.

To know more about this, take a look at our [SDK reference](</developing-connectors/sdk/sdk-reference/object_definitions.html>)
