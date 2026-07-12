# Workato SDK Documentation

> **Source**: https://docs.workato.com/en/developing-connectors/sdk/sdk-reference/schema.html
> **Fetched**: 2026-07-12T03:07:34.718777

---

[Connector SDK](</en/developing-connectors/sdk>)

[SDK reference](</en/developing-connectors/sdk/sdk-reference>)

Are you an LLM? You can read better optimized documentation at /en/developing-connectors/sdk/sdk-reference/schema.md for this page in Markdown format

# SDK Reference - Workato Schema [​](<#sdk-reference-workato-schema>)

Copy page

The following section defines how to define input and output fields in Workato - collectively called "Schema". You can apply this information anywhere in your connector code where input fields or output fields (datapills) are defined. This could be in places such as `connection`, `actions`, `triggers`, and `object_definitions`

Quick Overview

Getting the hang of Workato schema is essential for building user-friendly and intuitive connectors. You can give various attributes to your connector to make it easier to use. This schema is a simple array of hashes where each index in the array represents a single input field or output field.

These definitions are completely interchangeable for both input and output fields, making it easier to write the schema once and reuse it.

## Structure [​](<#structure>)

ruby
```ruby

      [
        {
          name: String,
          label: String,
          optional: Boolean,
          type: String,
          hint: String,
          of: String,
          properties: Array,
          control_type: String,
          toggle_hint: String,
          toggle_field: Hash,
          default: String,
          pick_list: String,
          delimiter: String,
          sticky: Boolean,
          convert_input: String,
          convert_output: String,
          change_on_blur: Boolean,
          support_pills: Boolean,
          custom: Boolean,
          extends_schema: Boolean,
          list_mode: String,
          list_mode_toggle: Boolean,
          item_label: String,
          add_field_label: String,
          empty_schema_message: String,
          sample_data_type: String,
          ngIf: String
        },
        {
          # Another field definition
        }
      ]

```

* * *

## Attribute description [​](<#attribute-description>)

Key| Definition  
---|---  
name| Required. The name of this field. For example, id or created_at  
optional| Optional. Default is false. Applies to input fields and ensures users provide input for this field before running the recipe.  
label| Optional. All fields have default labels based on the field name. Use this to change the default value of the field label.  
hint| Optional. This allows you to add some hints below the input field to guide the user. Links to documentation can be given using HTML syntax.  
type| Optional. The data type of this field. Default value is "string". Possible values are:   
\- "string"   
\- "integer"   
\- "number"   
\- "date_time"   
\- "date"   
\- "timestamp"   
\- "boolean"   
\- "object" - Must be accompanied by `properties`   
\- "array" - Must be accompanied by `of`  
of| Optional except when `type: "array"`. Used in conjunction with Arrays to define the data type of the Array. Possible values are:   
\- "string"   
\- "integer"   
\- "number"   
\- "date_time"   
\- "date"   
\- "timestamp"   
\- "boolean"   
\- "object" - Denotes an array of objects. Must be accompanied by the `properties` attribute.  
properties| Optional except when `type: "object"` or when `type: "array"` and `of: "object"`. Accepts an array of schema to denote the properties of the object.  
control_type| Optional. This field relates only to input fields, and it dictates the input field type to expose in a recipe. Default is "string". When this schema is used as an output field, this attribute is ignored.   
Refer to the list of [supported control types](</en/developing-connectors/sdk/sdk-reference/schema#control-types>).  
toggle_hint| Optional. This represents the label of the primary toggle. See [toggle fields](<#using-toggle-fields>) for more information.  
toggle_field| Optional. Hash representing the secondary toggle for this input field. See [toggle fields](<#using-toggle-fields>) for more information.  
default| Optional. Allows you to set a default value for that input field.  
pick_list| Optional. If control_type is :select or :multiselect, this property is required. Allows you to reference a picklist defined in the `pick_lists` key or define one directly. If defining a picklist directly, provide the same 2D array described in [Picklists](</en/developing-connectors/sdk/sdk-reference/picklists>)  
options| Synonymous with pick_list and used only for `connection` input fields.  
delimiter:| Optional unless `control_type: "multiselect"`. This delimiter is used between each input the user provides.  
sticky| Optional. Use this property to make this field always visible as an input field. By default, inputs that are optional are hidden inside the optional fields drop-down. Use `sticky: true` so they show up beside required fields.  
convert_input| Optional. When defining input fields, values passed into these fields are assumed to be strings regardless of their `type` defined. `convert_input` allows you to convert and transform these inputs even before they are passed to your `execute` block's `input` argument. [Learn more](<#using-convert-input-and-convert-output-for-easy-transformations>)  
convert_output| Optional. When defining output fields, the `name` of each field is matched against the keys in the actual output of the `execute` lambda function. This does not, however, ensure that the `value` of the output matches the `type` declared for its matched field. `convert_output` allows you to convert and transform these inputs as well as correctly "cast" incoming values assigned to a specific output field. [Learn more](<#using-convert-input-and-convert-output-for-easy-transformations>)  
change_on_blur| Optional. When true, config fields and dependent fields only evaluate the value when the user blurs out of the field instead of after every keystroke. This parameter often doesn't need to be configured.  
support_pills| Optional. The default value is true. When false, this field doesn't allow datapills to be mapped to it. This parameter often doesn't need to be configured.  
custom| Optional. When true, a special marker is introduced to indicate to the user that this field is custom. Normally used when dynamically generating object definitions which may contain custom fields.  
extends_schema| Optional. Allows a field to behave like a `config_field`  
list_mode| Optional. Used when `type: "array"` and `of: "object"`. Workato defaults to dynamic lists but this parameter allows you to set this input field to a static array input field. Possible values are:   
\- "static" - Users must define each index in this array.   
\- "dynamic" - Users can dynamically define each index in this array using list datapills.  
list_mode_toggle| Optional. Used when `type: "array"` and `of: "object"`. Allows users to toggle between static and dynamic lists when working with arrays. Defaults to true. Set list_mode_toggle: false to disallow users to toggle list modes.  
item_label| Optional. Only used with `control_type: "schema-designer"` or `control_type: "key_value"`. This allows you to configure the item name stated in the modal popup. Setting item_label: "Item Label" results in the following: ![](/assets/item_label.wY46U7Dj.png)  
add_field_label| Optional. Only used with `control_type: "schema-designer"` or `control_type: "key_value"`. This allows you to configure the label of the add button. Setting add_field_label: "Custom Add Label" results in the following: ![](/assets/add_field_label.CFbAOyZw.png)  
empty_schema_message| Optional. Only used with `control_type: "schema-designer"` or `control_type: "key_value"`. This allows you to configure the message when the input field is empty. Setting empty_schema_message: `Custom empty schema message that allows you to add field and generate schema` results in the following: ![](/assets/empty_schema_message.BMdmektL.png)  
sample_data_type| Optional. Only used with `control_type: "schema-designer"`. This allows you to configure the type of data the schema-designer input field accepts. Setting `sample_data_type: csv` results in the following: ![](/assets/sample_data_type.doQiRpct.png) Other possible inputs are json_input and xml. The schema-designer defaults to json_input.  
ngIf| Optional. Allows you to define a boolean statement. If true, this field displays. The boolean statement can reference other inputs in the same schema. For example, `ngIf: 'input.object_name != "approval"'` where the root node is `input` and you can traverse to a specific field via dot notation. Refer to [Using ngIf to conditionally hide or display fields](<#using-ngif-to-conditionally-hide-or-display-fields>) for more details.  
tree_options| Optional. Only used when `control_type: 'tree'`. This allows you to control the behavior of the `tree` picklist. This key expects a Hash which has three possible keys - `selectable_folder`,`multi_select` and `force_selection_hierarchy`. Refer to [Picklists](</en/developing-connectors/sdk/sdk-reference/picklists>) for more information.  

## Control types [​](<#control-types>)

The `control_type` key affects how users configure the input fields you define. For each input field (index in the schema array), you can control its look by assigning one of the values to the `control_type` attribute:

Control type| Description  
---|---  
text|  Simple text input field with a formula mode option.  
![text control type](/assets/text.Xh8vKjkT.png)  
text-area|  Long text input field with a formula mode option.  
![text-area control type](/assets/text-area.CEbcnTzt.png)  
plain-text|  Simple text input field without a formula mode option.  
![plain-text control type](data:image/png;base64,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A5dkf14RHzxr0JDD43KPJLl8afy7/1n9slFa/osfY7Lty/FFzv3z4elBa7HzYU6tQe1krQfLRkzu7VMWjWip6gcyGpfNHtZ9xzEdP6A2ZOWy2ZXf9M7Opq2cXXk3Fy2b3enJQxbN7vmdXtSyqtMPg8+b3x5OoCaz9j83ao/S2o6SgWEdrcoYE17FbxoBsvbfZGfTngZTM9ZV1m7oOZuArK0vdfce1NPdC9bVIGvITef5HoCsvRasmux/H/C6yhqArAGyBiBrALIGIGsAsgbIGoCsAcgagKwByBogawCyBiBrALIGIGuArAHIGoCsAcgawKvLWktbaz1AH9Da1lJN1lp8UkDf0VJF1trql4/dAKAPGLu8vq2KrLXWqxrQV7pW31pF1urrfVJAX1FfL2uArAHIGoCsAcgagKwBsgYgawCyBiBrALIGyBqArAHIGoCsAcgaIGsAsgYgawCyBiBrgKwByBqArAHIGoCsAbIma4CsAcgagKwByBoga7IGyBqArAHIGoCsAbIma4CsAcgagKwByBoga7IGyBqArAHIGoCsAbIma4CsAcgagKwByBoga7IGyBqArAHIGoCsAbIma4CsAcgagKwByBoga7IGyBqArAHIGoCsAbIma4CsAcgagKwByBoga7IGyBqArAHIGoCsAbIma4CsAcgagKwByBoga7IGyBpAX85aa/1YnxTQN4ytb60ia231y3UN6BtVW17fVkXWWuoB+oyWKrKWtLS1+qSAvqC1rUvVXiFrAH2WrAGyBiBrALIGIGsAsgbIGoCsAcgagKwByBogawCyBiBrALIGIGuArAHIGoCsAcgagKwBsgYgawCyBiBrALIGyBqArAHIGsA68R/lCqbFVacfIQAAAABJRU5ErkJggg==)  
plain-text-area|  Long text input field with formula mode option. This input field can be expanded using the adjust icon.  
![plain-text-area control type](data:image/png;base64,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)  
password|  Text input field specifically designed for sensitive information, such as passwords. Text input in this control type is masked.  
![password control type](data:image/png;base64,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)  
integer|  Simple number field with icon to indicate an integer value. This control type has a formula mode option.  
![integer control type](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAuUAAABqCAMAAAAsnd/oAAABR1BMVEUeO0UpRE4wS1Q6VF0+Vl9BWWJEXGVHX2hMY2xXbXVXb3tacHdec3pfdHxgdoJkeIBleYBne4JofYhofolqfYRrfoVwhY9xhZB3iZB4ipB5ipF5jJaAkJaAkZeBk52CkpmClJ2JmJ6Kmp+Km6SNnKGPnaOPnqSSoKaToaeToqqToquWlpaYpquZp6ybqbGcqrKdqq+grLGhrbKksLWksbilsbamsbaotLiptLmrtrqst7ysuL+vub6wur+xu7+xvMW1vsO1v8a3wcm6w8e7xMy9xsq9xs6+x83AyMzByc3Dy87Ey8/GztPHztLI0NPKysrL0tXM09bP1dnP1drR19rT2dzW297X3N/X3eHZ3uPb4OLf4+bg4ODg5Ojg5efi5unj5+nl6Ovl6evn6u3o6+3p7O7s7/Ht7/Lv8fPw8vTx8/Tx8/X///8GPv3oAAACrUlEQVR42u3d208UBxTA4cPWBZ0qVamITqFQrBUv9CKoddVl1wvW2tLaYgVBpVKrjv//szPgg4nZpI/18H0JOft88svmzPCwUUF2YQWoHFQOKgeVg8pB5aByUDkqB5WDykHloHJQOagcPqj8+dKSlZC88sWI3+yE3JUfasXMzodX1fsD8lS+FRPtffU804r28LHq7v4YuWtF5Kr8StyYjAfVUhy5FK0f/4z26fbQMzsiVeWfxd+341T1ddyrDrSqL+L6X9+Fx1FSVb4dMdKO4epeHLwQh6uD0Vi0IzJVfi0OTU6OxOqz1vDIyafViVja2tr6147IVPnn8bCqLsU3V+P8z788qb/S2z9cnbEiMlX+Ipr3K49j//rOqfJ9dXko4tN/7IhUT5/vfDn06+83o11Vr9a3bYiclR+Oiz99FROWQ+LKVw9EfDLzwnJIXHl9qry0GbJXDioHlYPKQeWgclA5qByVQ97K1/pdyKG/NqDyO883/7PuG/g/6w+o/NamysmiO6DyrspRucpROagcVA4qB5WDylG5ylG5ylE5qBxUDioHlYPKUfkHld8vO83oTU/3mtkpp5dVTq7Kl0eL+WYUU+PF/TryYnZ89JHKSVX50dndyufr0Osv897CZq+pXeWkust3Kq/NF380Y2Fs1sVC0so7RWd3lmMuFnJW/i7yXq++XJZVTq6nz2+L5iVLpzhelvVdPlecPb57uaicNJV3yrKcq+uuR1P7o/lyyptE0l0s/iuEykHloHJQOagcVI7KVY7KVc5Ha2NF5WSP/NyGytkDkauc/JGrnOSRu8vJH7m7nD0RucpJa2Vj90/l7AVdv1BOeoN+oXyt34Uc+msDKoecVI7KQeWgclA5qBxUDiqHuvLXkJ3KUTmoHFQOKgeVg8pB5aByVA4ZvAWCidxA64uwygAAAABJRU5ErkJggg==)  
number|  Decimal number field with icon to indicate a float value. This control type has a formula mode option.  
![number control type](/assets/number.Iv8HloeG.png)  
url|  Text field with icon to indicate a URL value. This control type has a formula mode option.  
![url control type](/assets/url.B3Z4HO60.png)  
select|  Control type to provide a predefined list of values to choose from. Make sure to include the `pick_list` property.  
![select control type](/assets/select.BzAoqzv8.png)  
checkbox|  Simple Yes/No select interface. It is advisable to add a [toggle field](<#using-toggle-fields>) for dynamic mapping and formula mode option.  
![checkbox control type](/assets/checkbox.mZEfir9Z.png)  
multiselect|  Control type similar to `select` with additional ability to select multiple values. This control type must be accompanied with `pick_list` and `delimiter` properties.  
![multiselect control type](/assets/multiselect.Cs_x0JQC.png)  
date|  Control type indicating date value. This control type has a formula mode option. ![date control type](/assets/date.hdXxA2D2.png)  
date_time|  Control type indicating date with time value. This control type has a formula mode option. ![date_time control type](/assets/date_time.DhnrWT5N.png)  
phone|  Control type indicating phone value. This control type has a formula mode option.  
![phone control type](/assets/phone.ZJjd17Ly.png)  
email|  Control type indicating email value. This control type has a formula mode option.  
![email control type](/assets/email.BHFt5sNP.png)  
subdomain|  Control type to indicate a subdomain of a particular site. Typically used in connection fields. Make sure to include the `url` property.  
![subdomain control type](/assets/subdomain.bgfrKsaU.png)  
schema-designer|  Control type that allows you to collect schema information from users. This is useful when you need users to give your input during recipe design time to create input or output fields. This requires `extends_schema: true` to take effect. 
```ruby

    {
      name: "schema",
      extends_schema: true,
      schema_neutral: false,
      control_type: 'schema-designer',
      label: 'Schema designer label',
      hint: 'Hint for schema designer field',
      item_label: 'button',
      add_field_label: 'Custom Add Label',
      empty_schema_message: 'Custom empty schema message that allows to <button type="button" data-action="addField">add field</button> and <button type="button" data-action="generateSchema">generate schema</button>',
      sample_data_type: 'csv' # json_input / xml
    },

```

![schema-designer](/assets/schema_designer.CvG4-6tv.png)  
key_value|  Control type that allows you to collect key and value pairs from users. This is useful when you need users to give your input during recipe design time for URL query parameters. Must be accompanied with `properties` defined and two inputs given. 
```ruby

    {
      name: "key_value",
      control_type: "key_value",
      label: "key_value",
      empty_list_title: "Add query parameters",
      empty_list_text: "Description for empty list",
      item_label: "Query parameter",
      type: "array",
      of: "object",
      properties: [
        { name: "key"},
        { name: "value"}
      ]
    },


```

![key_value](/assets/key_value.B5-eh5vw.png)  

## Nested objects [​](<#nested-objects>)

Often, data returned from API request is not a simple one-level JSON. More often than not, the returned JSON object is much more complex, with multiple levels of nesting. This section aims to illustrate how to define nested fields.

#### Sample code snippet [​](<#sample-code-snippet>)

json
```ruby

    {
      "id": "00ub0oNGTSWTBKOLGLNR",
      "status": "STAGED",
      "created": "2013-07-02T21:36:25.344Z",
      "activated": null,
      "lastLogin": "2013-07-02T21:36:25.344Z",
      "profile": {
        "firstName": "Isaac",
        "lastName": "Brock",
        "email": "[[email protected]](</cdn-cgi/l/email-protection>)",
        "login": "[[email protected]](</cdn-cgi/l/email-protection>)",
        "mobilePhone": "555-415-1337"
      },
      "credentials": {
        "provider": {
          "type": "OKTA",
          "name": "OKTA"
        }
      },
      "_links": {
        "activate": {
          "href": "https://your-domain.okta.com/api/v1/users/00ub0oNGTSWTBKOLGLNR/lifecycle/activate"
        }
      }
    }

```

Nested object field `profile` can be defined `type: :object` with fields nested inside using `properties`. Properties should be an array of fields objects (just like `fields` within the `user` object).

ruby
```ruby

    object_definitions: {
      user: {
        fields: lambda do
          [
            {
              name: "id"
            },
            {
              name: "status"
            },
            {
              name: "created",
              type: :timestamp
            },
            {
              name: "activated",
              type: :timestamp
            },
            {
              name: "lastLogin",
              type: :timestamp
            },
            {
              name: "profile",
              type: :object,
              properties: [
                {
                  name: "firstName"
                },
                {
                  name: "lastName"
                },
                {
                  name: "email",
                  control_type: :email
                },
                {
                  name: "login",
                  control_type: :email
                },
                {
                  name: "mobilePhone",
                  control_type: :phone
                }
              ]
            }
          ]
        end
      }
    }

```

## Nested Arrays [​](<#nested-arrays>)

The other common type of nested field is an array of objects. This type of field contains a list of repeated objects of the same fields. The defining such fields is similar to defining objects. Take the following sample `user` object from Asana as an example.

#### Sample code snippet [​](<#nested-arrays-sample-code-snippet>)

json
```ruby

    {
      "data": {
        "id": 12149914544379,
        "email": "[[email protected]](</cdn-cgi/l/email-protection>)",
        "name": "Ee Shan",
        "workspaces": [
          {
            "id": 1041269201604,
            "name": "Workato"
          },
          {
            "id": 498346130780,
            "name": "Product Documentation"
          }
        ]
      }
    }

```

The `workspaces` array should be given `type: :array` as well as `of: :object`. This tells the `object_definitions` framework that the field contains an array of objects. Similar to nested objects, you must define `properties`, which is an array of fields corresponding to the fields of each object in the `workspaces` array.

ruby
```ruby

    object_definitions: {
      user: {
        fields: lambda do
          [
            {
              name: 'id',
              type: :integer
            },
            { name: 'name' },
            {
              name: 'email',
              control_type: :phone
            },
            {
              name: 'workspaces',
              type: :array,
              of: :object,
              properties: [
                {
                  name: 'id',
                  label: 'Workspace ID',
                  type: :integer
                },
                { name: 'name' }
              ]
            }
          ]
        end
      }
    }

```

## Using toggle fields [​](<#using-toggle-fields>)

Toggle fields are a special type of input fields that allow 2 input types. They are a great way to introduce greater flexibility and increase usability in your input fields. When used, toggle fields allow users to switch between two control types.

TIP

Toggle fields are often used in conjunction with pick lists. Since pick lists produce drop-downs, users are unable to map datapills which they normally would in recipes. Toggle fields fix that by allowing them to toggle to plain text fields which can accept datapills.

#### Sample code snippet [​](<#using-toggle-fields-sample-code-snippet>)

ruby
```ruby

        input_fields: lambda do |object_definition, connection, config_fields|
          {
            name: "parser_id",
            label: "Document Parser",
            hint: "The Document Parser the file gets imported to",
            control_type: :select,
            pick_list: "parsers",
            optional: false,
            toggle_hint: "Select from list",
            toggle_field: {
              name: "parser_id",
              label: "Parser ID",
              type: :string,
              control_type: "text",
              optional: false,
              toggle_hint: "Use Parser ID",
              hint: "Go to home page and select the required parser. If the URL is 'https://app.docparser.com/stack/ynrqkdxvaghs/overview', then 'ynrqkdxvaghs' is the ID"
            }
          },
        end

```

![toggle primary](/assets/toggle-primary.D-S6XfQA.png) _Primary toggle field_

![toggle secondary](/assets/toggle-secondary.C5lcqgrz.png) _Secondary toggle field_

You can use a picklist input type to create a customized user experience. However, this makes the action value mapping static. All recipe jobs executing this action use the single parser ID value you selected, because only one value can be selected from the picklist. You can avoid this limitation by using a text field. A text field allows you to dynamically map the input field value.

If both field types are preferred for your planned use case, you can use the `toggle_field` to provide both input options to users. The picklist type is set as the primary toggle and the text field is set as the secondary (nested `toggle_field`) because the most common scenario is for users to select one parser per action.

## Using fields with extends_schema [​](<#using-fields-with-extends-schema>)

In some cases, the input fields you plan to show in an action depend on the answer to an input field in the same action. The `extends_schema` feature enables you to add dynamic behavior to your actions without using configuration fields.

#### Sample code snippet [​](<#using-fields-with-extends-schema-sample-code-snippet>)

ruby
```ruby

    object_definitions:
      schema_input: {
        fields: lambda do |connection, config_fields, object_definitions|
          input_schema = parse_json(config_fields.dig('schema') || '[]')
          [
            {
              name: "schema",
              extends_schema: true,
              schema_neutral: false,
              control_type: 'schema-designer',
              label: 'Schema designer label',
              hint: 'Hint for schema designer field',
              item_label: 'button',
              add_field_label: 'Custom Add Label',
              empty_schema_message: 'Custom empty schema message that allows you to <button type="button" data-action="addField">add field</button> and <button type="button" data-action="generateSchema">generate schema</button>',
              sample_data_type: 'csv' # json_input / xml
            },
            if input_schema.present?
              { name: 'data', type: 'object', properties: input_schema }
            end
          ].compact
        end
      }

```

The preceding code sample demonstrates how to use an input field with `control_type` set to `schema-designer`. By setting `extends_schema` to `true`, user inputs trigger a re-evaluation of the `object_definitions` block. The inputs become `config_fields` for further processing. This setup allows inputs for the `schema` field to directly influence the creation of the `data` input field.

The `schema_neutral` parameter enables you to update titles or descriptions without modifying the schema's logic. This provides increased flexibility and control when changes impact the title or description but not the schema itself. `schema_neutral` allows you to return results of an extended schema even when the input is empty.

## Arrays of primitive scalar data types [​](<#arrays-of-primitive-scalar-data-types>)

Arrays in Workato input and output schema currently only work with objects. In cases where you need to collect an array of primitive data types such as strings or integers, consider the code below. In this example, we plan to send an array of strings to a target API in the format `["column1","column2","column3"]`. This can be done by declaring an array of objects with the declaration for the `column names` input field wrapped inside the object layer.

#### Sample code snippet [​](<#arrays-of-primitive-scalar-data-types-sample-code-snippet>)

ruby
```ruby

    object_definitions: {
      columns: {
        fields: lambda do
          [
            {
              label: 'String Array',
              name: 'array_of_strings',
              type: "array",
              of: "string"
            }
          ]
        end
      }
    }

```

## Using ngIf to conditionally hide or display fields [​](<#using-ngif-to-conditionally-hide-or-display-fields>)

Sometimes, you need to hide or display fields based on a user's input. This could be in the `input_fields` key or the `config_fields` key. For example, if you want to showcase an additional `config_field` based on a user's input to another `config_field`. Another use case would be to showcase a new input field based on a user's input for another input field. For example, if we have an action that creates a user - if one input field is `assign_new_password`, we would use `ngIf` to conditionally show `new_password` if the user gave `true` to that input.

#### Sample code snippet [​](<#using-ngif-to-conditionally-hide-or-display-fields-sample-code-snippet>)

ruby
```ruby

    object_definitions: {
      create_user: {
        fields: lambda do |_connection, config_fields|
          [
            {
              name: 'assign_new_password',
              label: 'Assign new password during creation',
              hint: "Select <b>yes</b> to provide a password for this newly created user. If set to <b>no</b>, an email is sent to user to define their own password.",
              control_type: 'checkbox',
              type: 'boolean',
              sticky: true,
            },
            {
              name: 'password_input',
              label: 'Custom password',
              control_type: 'password',
              ngIf: 'input.assign_new_password == "false"',
              sticky: true,
              hint: 'Required if <b>Assign new password during creation</b> is set to <b>yes</b>. ' \
                      'Provide a password of length 8 to 100 characters.'
            },
          ]
        end
      }
    }

```

## Using `convert_input` and `convert_output` for easy transformations [​](<#using-convert-input-and-convert-output-for-easy-transformations>)

In most cases, when users map fields to your action's input fields, these values are assumed to be of the data type `string` regardless of the actual `type` or `control_type` you have configured for the input field.

For example, the schema below:
```ruby

    [
      {
        name: "account_id",
        control_type: "integer"
        type: "int"
      }
    ]

```

When the `input` is passed to the `execute` lambda, it would still arrive in the JSON object as
```ruby

    {
      "account_id": "123"
    }

```

In these cases, you can use `convert_input` to transform the input into its expected data type even before it's passed to the `execute` lambda.

For example:
```ruby

    [
      {
        name: "account_id",
        control_type: "integer"
        type: "int",
        convert_input: "integer_conversion"
      }
    ]

```

With `convert_input` defined, the `input` argument passed to your `execute` lambda is:
```ruby

    {
      "account_id": 123
    }

```

This allows you to configure the expected data formats when defining the schema and allows you to skip any unnecessary code in your `execute` for ensuring data is in the correct format. The same behavior is also seen in reverse when you use `convert_output`, where a value from the output of your `execute` lambda is transformed when its mapped to a output field which contains a `convert_output` attribute.

### Predefined `convert_input` values [​](<#predefined-convert-input-values>)

  * `integer_conversion`

  * Converts input into data type integer

  * `float_conversion`

  * Converts input into data type float

  * `date_conversion`

  * Converts input into data type date

  * `render_iso8601_timestamp`

  * Converts input into date string that conforms to ISO8601 standards

  * `boolean_conversion`

  * Converts input into data type boolean

### Predefined `convert_output` values [​](<#predefined-convert-output-values>)

  * `integer_conversion`

  * Converts output into data type integer/number

  * `float_conversion`

  * Converts output into data type float

  * `date_conversion`

  * Converts output into data type date

  * `date_time_conversion`

  * Converts output into a format that matches JavaScript's Date object's `toJSON` method

  * `boolean_conversion`

  * Converts output into data type boolean

TIP

Sometimes the above transformations may not suite your needs. For example, when you need transformations to a specific time format or if you want to manipulate the structure of your data. In these cases, you can create your own custom `convert_input` and `convert_output` functions. Continue reading to learn how to do this.

## Advanced transformations using methods in `convert_input` and `convert_output` [​](<#advanced-transformations-using-methods-in-convert-input-and-convert-output>)

In some situations, APIs require you to send data in a specific format. For example, an API can require date times in `epoch` time. In many cases, we cannot assume that users in the recipe editor are comfortable with `epoch` time or that the upstream systems they are mapping data from provide date times in `epoch` format. In cases like these, we would use methods in conjunction with `convert_input` to cast their inputs to the proper format.

For example:

ruby
```ruby

    [
      {
        name: 'invoice_date',
        control_type: "date_time",
        convert_input: "epoch_time_conversion"
      }
    ]

```

and a matching method named `epoch_time_conversion`:

ruby
```ruby

    methods: {
      epoch_time_conversion: lambda do |val|
        val.to_time.to_i
      end
    }

```

which would render inputs such as `"2021-10-27T00:00:00-07:00"` to `1635318000`.

You can also use custom lambdas to perform custom transformations on nested structures. For example, when an API requires you to send a payload in the format:

json
```ruby

    {
      "data": {
        "name": {
          "value": "abc123"
        },
        "address": {
          "value": "def456"
        }
      }
    }

```

The corresponding input_field representation might be overly nested, making it cumbersome for users.

![Nested fields](/assets/before_custom_lambda.DjigiwPo.png)_Input fields represented by the earlier example_

Custom lambdas help you improve the UX of your connector by allowing you to present a relatively flat input field structure and performing the transformations afterwards.

For example:

ruby
```ruby

    [
      {
        name: 'data',
        type: 'object',
        properties: [
          {
            name: "name"
          },
          {
            name: "address"
          }
        ],
        convert_input: "key_value_conversion"
      }
    ]

```

and a matching method named `key_value_conversion`:

ruby
```ruby

    methods: {
      key_value_conversion: lambda do |val|
        # val in this case is the entire "data" object
        val.map do |key, value|
          {
            key => {
              "value" => value
            }
          }
        end.inject(:merge)
      end
    }

```

Resultant JSON:

json
```ruby

    {
      "data": {
        "name": {
          "value": "abc123"
        },
        "address": {
          "value": "def456"
        }
      }
    }

```

![Flattened fields](/assets/after_custom_lambda.N7Q4DLVe.png)_Input fields that produce the same output due to custom lambdas_

Furthermore, you can call `convert_input` and `convert_output` on schema of type `arrays`. This allows you to perform transformations on the entire array of inputs.

For example:

ruby
```ruby

    [
      {
        name: 'products',
        type: 'array',
        of: 'object',
        convert_input: "product_conversion",
        properties: [
          {
            name: "name"
          },
          {
            name: "qty"
          }
        ]
      }
    ]

```

and a matching method named `string_concat_conversion`:

ruby
```ruby

    methods: {
      product_conversion: lambda do |val|
        # Render_input is called on each index of the array THEN the whole array
        if val.is_a?(Array)
          val
        else
          {
            val['name'] => val['qty']
          }
        end
      end,
    }

```

The user's input would look something like this:

json
```ruby

    {
      "products": [
        {
          "name": "car",
          "qty": "100"
        },
        {
          "name": "wrench",
          "qty": "10"
        }
      ]
    }

```

Resultant JSON:

json
```ruby

    {
      "products": [
        "car": "100"
        "wrench": "10"
      ]
    }

```

**Last updated:**
