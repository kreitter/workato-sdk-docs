# Workato SDK Documentation

> **Source**: https://docs.workato.com/en/developing-connectors/sdk/guides/advanced-connector-guide/connector-building-building-actions.html
> **Fetched**: 2026-07-17T03:05:18.140957

---

[Connector SDK](</en/developing-connectors/sdk>)

[How-to guides](</en/developing-connectors/sdk/guides>)

[Advanced connector guide](</en/developing-connectors/sdk/guides/advanced-connector-guide/introduction>)

Are you an LLM? You can read better optimized documentation at /en/developing-connectors/sdk/guides/advanced-connector-guide/connector-building-building-actions.md for this page in Markdown format

# Connector building - Building actions [​](<#connector-building-building-actions>)

Copy page

Now that we’ve defined objects schema in methods, we can now start building out our CRUDS actions which will reference the schema methods we have just defined.

## Defining config fields [​](<#defining-config-fields>)

When dealing with object-based actions, we first need to define something called configuration fields. [Configuration fields](</en/developing-connectors/sdk/sdk-reference/actions#config-fields>) are special input fields that you can define whose answers can dynamically generate other input fields.

ruby
```ruby

    config_fields: [
      {
        name: 'object',
        optional: false,
        label: 'Object type',
        control_type: 'select',
        pick_list: 'object_list_create',
        hint: 'Select the object type from picklist.'
      }
    ],

```

![Config fields](/assets/config_fields.BiCb-coL.gif)_Selecting invoice causes invoice related input fields to appear_

Here we also introduce a [picklist](</en/developing-connectors/sdk/sdk-reference/picklists>) which we can easily add additional objects as we introduce support for them.

DYNAMIC INPUT FIELDS

You can also use configuration fields to dynamically generate input fields based on the user's selections. Refer to the [Defining input fields](<#defining-input-fields>) section for scenarios where the selected object requires additional information before accurate input fields can be displayed.

## Defining your title, subtitle, description, and help text [​](<#defining-your-title-subtitle-description-and-help-text>)

It is also highly recommended and really important to define helpful titles and descriptions for your actions. When dealing with object-based actions, this helps with the readability of recipes using your connector as well as improves user experience for those building recipes with your connector.

ruby
```ruby

    actions: {
      create_object: {
        title: 'Create object',

        subtitle: 'Supports the creation of invoices, payments, and customers',

        description: lambda do |input, picklist_label|
          "Create a <span class='provider'>" \
          "#{picklist_label['object'] || 'object'}</span> in " \
          "<span class='provider'>XYZ Accounting</span>"
        end,

        help: lambda do |input, picklist_label|
          "Creates an #{picklist_label['object'] || 'object'} in XYZ. First, select from a list of " \
          'objects that we currently support. After selecting your object,' \
          ' dynamic input fields specific to the object selected ' \
          'will be populated.'
        end,

        config_fields: [
          {
            name: 'object',
            optional: false,
            label: 'Object type',
            control_type: 'select',
            pick_list: 'object_list_create',
            hint: 'Select the object type from picklist.'
          }
        ],
        # More code truncated here
      }
    }

```

Over here we define title and subtitles to give users an idea of the action out of all the different actions in your connector. Remember to keep your title concise whilst using subtitles to provide a bit more information.

For descriptions, we allow you to use a lambda function (as shown in the example above) to dynamically change the description of the action when a user makes a selection in the config_field. The same can be done for help text as shown in the example above.

![Bad example of dynamic descriptions](/assets/dynamic-description-1.CfR1Me_n.png)_Bad example with no dynamic description_

![Good example of dynamic descriptions](/assets/dynamic-description-2.DhvLWrIN.png) _Good example with dynamic description_

## Defining input fields [​](<#defining-input-fields>)

Another feature of creating clean and scalable input fields are that a single action can support multiple objects with a single `object_definitions` call. Since the value of configuration fields can only be accessed through an object_definitions method, we suggest calling a generic object_definitions that can later pull the appropriate schema based on the object the user has selected.

### Input [​](<#input>)

ruby
```ruby

    input_fields: lambda do |object_definitions, connection, config_fields|

      object = config_fields['object']

      input_schema = object_definitions[object] # If user select invoice, evaluates to object_definitions['invoice']

      case object
      when 'invoice'
        input_schema.where('name !=': 'Id')
      else
        input_schema
      end
    end,

```

### Object definition [​](<#object-definition>)

ruby
```ruby

      object_definitions: {
        invoice: lambda do |connection, config_fields, object_definitions|
          [
            { name: "Id" },
            { name: "TxnDate" },
            { name: "TotalAmt", type: "number" },
            {
              name: "Line",
              type: "array",
              of: "object",
              properties: [
                { name: "Description" },
                {
                  name: "SalesItemLineDetail",
                  type: "object",
                  properties: [
                    { name: "Qty", type: "number" },
                    { name: "UnitPrice", type: "number" }
                  ]
                },
                { name: "Line-Num", type: "number" },
                { name: "Amount", type: "number" },
                { name: "Id" }
              ]
            },
            # More schema
          ]
        end
      }

```

When the object definition `invoice` is called, the schema relevant to the invoice is returned. In the `input_fields`, we then conditionally filter out the `id` field as it is not applicable to the creation of an invoice and should not be shown.

## Defining the execute block [​](<#defining-the-execute-block>)

When defining the execute block, we first store any generic methods for pre processing or post processing of data in the execute block. In the example below, use to generic methods that format payloads before being sent out the target API. After the formatting of the payload, a call is then made to a method which houses any specific data processing that needs to be done on a `action`-`object` level as well as the final HTTP call to the appropriate endpoint.

Error handling surfaces relevant error messages, saving users significant time during recipe design and debugging.

ACTION TIMEOUT

SDK actions have a 180 second [timeout](</en/recipes/recipe-job-errors#timeouts>) limit.

You can use the `checkpoint!` method with file streaming actions to transfer files that exceed the timeout limit. Refer to the [Using our multistep framework to extend upload times](</en/developing-connectors/sdk/guides/building-actions/streaming/upload-stream-chunk-id#using-our-multistep-framework-to-extend-upload-times>) section for additional information.

### Execute block [​](<#execute-block>)

ruby
```ruby

    execute: lambda do |connection,input|
      object_name = input.delete('object')

      response = call('create_#{object_name}_execute', payload).
                  after_error_response(/.*/) do |_code, body, _header, message|
                    error("#{message}: #{body}")
                  end

      formatted_response
    end,

```

### `action`-`object` method [​](<#action-object-method>)

ruby
```ruby

    create_invoice_execute: lambda do |payload|
      post('api/invoice/create', payload)
    end,

```

## Defining the output fields [​](<#defining-the-output-fields>)

Output fields can be defined in the same way as input fields using the same schema method used earlier. When calling the schema method, remember to pass the parameter `output` so your method knows to return fields expected in the response. Often this includes metadata about the object that cannot be changed by users such as `created_at` or `updated_at` timestamps.

### Output [​](<#output>)

ruby
```ruby

    output_fields: lambda do |object_definitions, connection, config_fields|
      object = config_fields['object']

      input_schema = object_definitions[object] # If user select invoice, evaluates to object_definitions['invoice']
    end,

```

No further manipulation is needed as the invoice schema contained in `object_definition['invoice']` matches the fields returned from the API exactly.

## Example 1: Update invoice action in XYZ Accounting [​](<#example-1-update-invoice-action-in-xyz-accounting>)

Below, we go through one full example for an update object action in XYZ accounting.

### Sample code [​](<#sample-code>)

ruby
```ruby

    methods: {
      update_invoice_execute: lambda do |payload|
        patch('api/invoice/update', payload)
      end,

    },

    object_definitions: {

      invoice: {
        fields: lambda do |connection, config_fields, object_definitions|
          # same schema as above
        end
      },

    },
    actions: {

      update_object: {
        title: 'Update object',

        subtitle: 'Updates an object in XYZ accounting.',

        description: lambda do |input, picklist_label|
          "Update a <span class='provider'>" \
          "#{picklist_label['object'] || 'object'}</span> in " \
          "<span class='provider'>XYZ Accounting</span>"
        end,

        help: lambda do |input, picklist_label|
          {
            body:
            "Updates an #{picklist_label['object'] || 'object'} in XYZ. First, select from a list of " \
            'objects that we currently support. After selecting your object,' \
            ' dynamic input fields specific to the object selected ' \
            'will be populated.'
          }
        end,

        config_fields: [
          {
            name: 'object',
            optional: false,
            label: 'Object type',
            control_type: 'select',
            pick_list: 'object_list_update',
            hint: 'Select the object type from picklist.'
          }
        ],

        input_fields: lambda do |object_definitions, connection, config_fields|
          object = config_fields['object']

          input_schema = object_definitions[object]
        end,

        execute: lambda do |connection,input|
          object_name = input.delete('object')

          response = call('update_#{object_name}_execute', payload).
                      after_error_response(/.*/) do |_code, body, _header, message|
                        error("#{message}: #{body}")
                      end

          response
        end,

        output_fields: lambda do |object_definitions, connection, config_fields|
          object = config_fields['object']

          input_schema = object_definitions[object]
        end,

        sample_output: lambda do |connection, input|
          payload = {
            "limit" => 1,
            "status" => "closed"
          }
          call("search_#{input['object']}_execute", payload)
        end

      }
      # More actions below
    },

    pick_lists: {
      object_list_update: lambda do
        [
          ["Invoice","invoice"]
        ]
      end,
      # More picklists below
    }

```

The example below showcases all the different steps needed to create an update object action. Currently this code only shows support for a single object - `Invoices`. The structure for the update object action is largely identical to that of the create object action where configuration fields, titles, subtitles, descriptions, help text, input fields, output fields, execute, and sample output blocks are defined generically. Most of the magic happens in object definitions and methods where object-specific code is introduced to retrieve specific schema and make HTTP calls to endpoints related to that object.

### Building triggers [​](<#building-triggers>)

Lets move on to learning about building object based triggers.

**Last updated:**
