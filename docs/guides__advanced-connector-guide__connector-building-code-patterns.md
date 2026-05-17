# Workato SDK Documentation

> **Source**: https://docs.workato.com/en/developing-connectors/sdk/guides/advanced-connector-guide/connector-building-code-patterns.html
> **Fetched**: 2026-05-17T03:10:50.032266

---

[Connector SDK](</en/developing-connectors/sdk>)

[How-to guides](</en/developing-connectors/sdk/guides>)

Tips

# Connector building - Useful coding patterns [​](<#connector-building-useful-coding-patterns>)

There are some known limitations to Workato's platform that have fixes in the works. In the meantime, here are some ways that you can easily solve for any limitations that you might find when building a custom connector.

## Handling special characters [​](<#handling-special-characters>)

One known limitation of relates closely to datapills in Workato. When input or output fields are defined with names that have these special characters, input fields don’t show up and output datapills render incorrectly.
```ruby

    -<>!@#$%^&*()+={}:;'"`~,.?

```

For example, schema defined where

ruby
```ruby

    {
      name: “due-date”
    }

```

Would not show up as a string input field and datapills would turn render as long strings instead of datapills.

![Broken datapill](/assets/broken-datapill.BAl9H38s.png)_When names of schema have special characters, datapills are renders incorrectly_

instead of

![Proper datapill](/assets/proper-datapill.DroiaEjz.png) _There is a need to render them properly by switching out the special characters in their names_

Fortunately, there is a workaround which we highly recommend you build into your connector as well. ( You could even copy and paste the following if it fits.) We create a series of 3 methods, `format_schema`, `format_payload`, `format_schema` which can be called at the beginning and end of each `execute` block. We had done something similar in our earlier example when defining our action.

### `format_schema` [​](<#format-schema>)

Sample code snippet:

ruby
```ruby

    format_schema: lambda do |schema|
      if schema.is_a?(Array)
        schema.map do |array_value|
          call('format_schema', array_value)
        end
      elsif schema.is_a?(Hash)
        schema.map do |key,value|
          if %w[name].include?(key.to_s)
            value = call('replace_special_characters',value.to_s)
          elsif %w[properties toggle_field].include?(key.to_s)
            value = call('format_schema', value)
          end
          { key => value }
        end.inject(:merge)
      end
    end,

```

Since fields where names contain keys cause errors, we need a service method that can take invalid schema and convert any names into formats we can handle. The method above recursively searches through a given schema and replaces any special characters with a valid string. For example,

ruby
```ruby

    [
      {
        control_type: "text",
        label: "Txn date",
        type: "string",
        name: "Txn-Date"
      }
    ]

```

Would be converted to

ruby
```ruby

    [
      {
        control_type: "text",
        label: "Txn date",
        type: "string",
        name: "Txn__hyp__Date"
      }
    ]

```

This allows the field to be displayed in Workato with no observable difference to the end user as labels are preserved. This service method can be called on either static or dynamic schema.

### `format_payload` [​](<#format-payload>)

Sample code snippet:

ruby
```ruby

    format_payload: lambda do |payload|
      if payload.is_a?(Array)
        payload.map do |array_value|
          call('format_payload', array_value)
        end
      elsif payload.is_a?(Hash)
        payload.map do |key, value|
          key = call('inject_special_characters',key)
          if value.is_a?(Array) || value.is_a?(Hash)
            value = call('format_payload', value)
          end
          { key => value }
        end.inject(:merge)
      end
    end,

```

This method should be called when input from the job is passed through the `execute` block. At this stage, this method recursively searches through the input hash and finds any markers that a special character was replaced and transforms it back to its original form. The return from this method is a formatted payload with all special characters replaced back in.

### `format_response` [​](<#format-response>)

Sample code snippet:

ruby
```ruby

    format_response: lambda do |payload|
      if payload.is_a?(Array)
        payload.map do |array_value|
          call('format_response', array_value)
        end
      elsif payload.is_a?(Hash)
        payload.map do |key, value|
          key = call('replace_special_characters',key)
          if value.is_a?(Array) || value.is_a?(Hash)
            value = call('format_response',value)
          end
          { key => value }
        end.inject(:merge)
      end
    end,

```

When working with responses, we still need to match them back to the Workato valid schema. As such, we need to transform the keys in our responses from our network traffic back to replace any special characters. This should be done immediately after we get a response back from a HTTP call.

### `replace_special_characters` and `inject_special_characters` [​](<#replace-special-characters-and-inject-special-characters>)

Samples code snippet:

ruby
```ruby

    replace_special_characters: lambda do |input|
      input.gsub(/[-<>!@#$%^&*()+={}:;'"`~,.?|]/,
      '-' => '__hyp__',
      '<' => '__lt__',
      '>' => '__gt__',
      '!' => '__excl__',
      '@' => '__at__',
      '#' => '__hashtag__',
      '$' => '__dollar__',
      '%' => '__percent__',
      '^' => '__pwr__',
      '&' => '__amper__',
      '*' => '__star__',
      '(' => '__lbracket__',
      ')' => '__rbracket__',
      '+' => '__plus__',
      '=' => '__eq__',
      '{' => '__rcrbrack__',
      '}' => '__lcrbrack__',
      ';' => '__semicol__',
      '\'' => '__apost__',
      '`' => '__bckquot__',
      '~' => '__tilde__',
      ',' => '__comma__',
      '.' => '__period__',
      '?' => '__qmark__',
      '|' => '__pipe__',
      ':' => '__colon__',
      '\"' => '__quote__'
    )
    end,

    inject_special_characters: lambda do |input|
      input.gsub(/(__hyp__|__lt__|__gt__|__excl__|__at__|__hashtag__|__dollar__|\__percent__|__pwr__|__amper__|__star__|__lbracket__|__rbracket__|__plus__|__eq__|__rcrbrack__|__lcrbrack__|__semicol__|__apost__|__bckquot__|__tilde__|__comma__|__period__|__qmark__|__pipe__|__colon__|__quote__|__slash__|__bslash__)/,
      '__hyp__' => '-',
      '__lt__' => '<',
      '__gt__' => '>',
      '__excl__' => '!',
      '__at__' => '@',
      '__hashtag__' => '#',
      '__dollar__' => '$',
      '__percent__' => '%',
      '__pwr__' => '^',
      '__amper__' => '&',
      '__star__' => '*',
      '__lbracket__' => '(',
      '__rbracket__' => ')',
      '__plus__' => '+',
      '__eq__' => '=',
      '__rcrbrack__' => '{',
      '__lcrbrack__' => '}',
      '__semicol__' => ';',
      '__apost__' => '\'',
      '__bckquot__' => '`',
      '__tilde__' => '~',
      '__comma__' => ',',
      '__period__' => '.',
      '__qmark__' => '?',
      '__pipe__' => '|',
      '__colon__' => ':',
      '__quote__' => '"'
    )
    end

```

## Avoid encoded query parameters [​](<#avoid-encoded-query-parameters>)

Workato's SDK automatically encodes query parameters in GET requests, which can break requests for APIs that expect exact formatting. To avoid this, build the query string manually and append it directly to the URL.

For example:

ruby
```ruby

    url = "https://api.example.com/reports"
    query_string = "addressVerification=true&poi[latitude]=#{input['latitude']}&poi[longitude]=#{input['longitude']}"

    get("#{url}?#{query_string}")

```

This preserves the exact casing and structure required by the API. Use this pattern when the API expects raw query strings or rejects encoded characters.

## Header casing in SDK console [​](<#header-casing-in-sdk-console>)

Case-sensitive headers may appear with incorrect casing when you test connectors in the SDK console.

This issue affects only the console interface. The SDK console formats header names for display, but Workato sends the request with the exact casing defined in your code.

For example:

ruby
```ruby

    case_sensitive_headers(BPMCSRF: connection['BPMCSRF'],
                           Cookie: connection['Cookie'])

```

In the console, a header like `BPMCSRF` may display as `Bpmcsrf`, but the actual request uses the correct casing. You don't need to change your code.

## Summary [​](<#summary>)

Object based actions and triggers in Connectors are something we highly recommend. Not only do they improve user experience for your users but they also make it so much easier to extend your connector when done properly. Here are a few of the main concepts we covered:

  1. Defining the base schema of each object in a service method. Don’t forget to include an input argument that allows you to adjust the schema based on the action type.
  2. Use object_definitions to pull the proper input and output field schema based on the object selected
  3. When defining actions or triggers, make sure to declare all blocks especially `description` blocks. This will vastly increase usability for your users.
  4. Contain any general processing inside execute blocks but leverage on dedicated object execute methods (i.e. `create_invoice_execute`)for anything specific. i.e. Use `format_paylod` and `format_response` in the execute block before using the `create_#{object}_execute` method.

### Usability rules [​](<#usability-rules>)

Great connectors not only have great architecture but look and feel great to use. Read on to find out more about how you can make your connector easy to use.

**Last updated:**
