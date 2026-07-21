# Workato SDK Documentation

> **Source**: https://docs.workato.com/en/developing-connectors/sdk/sdk-reference/methods.html
> **Fetched**: 2026-07-21T03:06:46.157867

---

[Connector SDK](</en/developing-connectors/sdk>)

[SDK reference](</en/developing-connectors/sdk/sdk-reference>)

Connector key reference

Are you an LLM? You can read better optimized documentation at /en/developing-connectors/sdk/sdk-reference/methods.md for this page in Markdown format

# SDK Reference - `methods` [​](<#sdk-reference-methods>)

Copy page

Reusable methods are supported in Workato. Reusable methods help keep your custom adapter code DRY and may be used in any lambda function in your connector.

Quick Overview

Reusable methods are the same as custom functions that can be called in any portion of the code. Use them to keep your code concise and maintainable.

## Structure [​](<#structure>)

ruby
```ruby

        methods: {

          [Unique_method_name]: lambda do |[unique_argument_name]|
            Array, Hash, String, Int, Boolean
          end,

          [Another_unique_method_name]: lambda do |[unique_argument_name], [another_unique_argument_name]|
            Array, Hash, String, Int, Boolean
          end
        },

```

* * *

Attribute| Description  
---|---  
Key| `[Unique_method_name]`  
Type| lambda function  
Required| True  
Description| This lambda function can be invoked anywhere in the connector code such as actions, triggers, object_definitions, or even other methods. This is done by the using the special syntax `call('unique_method_name', input)`  
Possible Arguments| Arguments can be defined by you. There can be any number of arguments. Splat operators are not allowed.  
Expected Output| Variable  
Example - methods: - Using a reusable method

Use the `call()` method to reference a method. This method takes in two parameters:

  1. The method name - You can use either "method_name" (string) or :method_name (symbol) representations.
  2. Input fields - This is mapped to the arguments defined in the method definition.

Here we have the definition of a recursive method which returns the factorial of a number.

ruby
```ruby

        methods: {
          factorial: lambda do |input|
            number = input['number']
            if number > 1
              number * call('factorial', { number: number - 1 })
            else
              number
            end
          end
        }

```

ruby
```ruby

        actions: {
          factorial: {
            input_fields: lambda do
              [
                { name: "number", type: :integer }
              ]
            end,

            execute: lambda do |connection, input|
              { factorial: call(:factorial, { number: input['number'] }) }
            end
        },

```

**Last updated:**
