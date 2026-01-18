# Workato SDK Documentation

> **Source**: https://docs.workato.com/en/developing-connectors/sdk/sdk-reference/object_definitions.html
> **Fetched**: 2026-01-18T02:50:31.493402

---

# [#](<#sdk-reference-object-definitions>) SDK Reference - `object_definitions`

Object definitions represent specific resources from a target application. For example, they represent the schema for Salesforce leads or Snowflake rows.

These definitions are stored as arrays of hashes, and are used in both input and output fields.

Avoid repeating code with object definitions

Store object definition in one place and reuse throughout the custom connector.

## [#](<#structure>) Structure
```ruby
 
        object_definitions: {

          [Unique_object_definition_name]: {
            fields: lambda do |connection, config_fields, object_definitions|
              Array
            end
          },

          [Another_unique_object_definition_name]: {
            ...
          }
        },


```

* * *

Attribute | Description  
---|---  
Key | `fields`  
Type | lambda function  
Required | True  
Description | This lambda function is invoked whenever its parent object_definition's key is called in an action or trigger. It is able to make HTTP requests to dynamically build schema from metadata endpoints. The output of this lambda function should be an array of hashes that represents the input or output fields. This is called Workato Schema. Find out more [here](</developing-connectors/sdk/sdk-reference/schema.html>)  
Possible Arguments | `connection` \- Hash representing user given inputs defined in the connection.   
`config_fields` \- Hash representing the user given inputs from config fields in the action or trigger that referenced this object definition.   
`object_definitions` \- Allows you to reference other object_definitions.  
Expected Output | Array  

DEFINE ARGUMENTS FOR OBJECT DEFINITIONS

You must define arguments for your object definitions, even if they are not used. Workato determines whether your schema is static or dynamic based on whether your object definitions have arguments defined. Changing your schema from static to dynamic is considered backward incompatible; you must stop running recipes and refresh the schema for the changes to take effect.

**Static object definition**
```ruby
 
    lead: {
      fields: lambda do 
        [
          { name: "name", type: :boolean },
          { name: "email" },
          { name: "number"}
        ]
      end
    }


```

**Dynamic object definition**
```ruby
 
    lead: {
      fields: lambda do |connection, config_fields, object_definitions|
        [
          { name: "name", type: :boolean },
          { name: "email" },
          { name: "number"}
        ]
      end
    }


```

_Workato recommends that you define all object_definitions dynamically (with arguments) to ensure no issues arise from any future changes._

Example - fields

Object_definitions can be static and simply store an array. When this object definition is referenced, the `fields` lambda function returns this array.
```ruby
 
        object_definitions: {
          lead: {
            fields: lambda do |connection, config_fields, object_definitions|
              [
                { name: "name", type: :boolean },
                { name: "email" },
                { name: "number"}
              ]
            end
          }
        }


```

Object_definitions can also be dynamic and make HTTP requests to metadata endpoints. When this object definition is referenced, the `fields` lambda function makes this request, receives the response and should massage the response into the same array that can be returned to the `input_fields` or `output_fields` lambda function that referenced it. Find out more about defining these `input_fields` and `output_fields` (called Workato schema) [here](</developing-connectors/sdk/sdk-reference/schema.html>)
```ruby
 
        object_definitions: {
          form: {
            fields: lambda do |connection|
              get("https://api.unbounce.com/pages/#{connection['page_id']}/form_fields")["formFields"].
                map { |field| { name: field["id"] } }
            end
          }
        }


```

Example - Building schema from multiple object_definitions

To keep your code DRY, our recommendation is to logically break up your schema definitions into separate object_definitions. These object_definitions may be dynamically generated separately and pieced together.
```ruby
 
        object_definitions: {
          create_object_output: {
            fields: lambda do |connection, config_fields, object_definitions|
              if config_fields['object'] == 'customer'
                [
                  {
                    name: 'customer',
                    type: 'object',
                    properties: object_definitions['customer_schema']
                  },
                  {
                    name: 'card',
                    type: 'object',
                    properties: object_definitions['card_schema']
                  }
                ]
              elsif config_fields['object'] == 'subscription'
                [
                  {
                    name: 'customer',
                    type: 'object',
                    properties: object_definitions['customer_schema']
                  },
                  {
                    name: 'subscription',
                    type: 'object',
                    properties: object_definitions['subscription_schema']
                  },
                  {
                    name: 'card',
                    type: 'object',
                    properties: object_definitions['card_schema']
                  }
                ]
              end
            end
          }
        }


```
