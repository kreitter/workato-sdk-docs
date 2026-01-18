# Workato SDK Documentation

> **Source**: https://docs.workato.com/en/developing-connectors/sdk/guides/advanced-connector-guide/connector-building-code-patterns.html
> **Fetched**: 2026-01-18T02:49:23.876659

---

# [#](<#connector-building-useful-coding-patterns>) Connector building - Useful coding patterns

There are some known limitations to Workato's platform that have fixes in the works. In the meantime, here are some ways that you can easily solve for any limitations that you might find when building a custom connector.

## [#](<#handling-special-characters>) Handling special characters

One known limitation of relates closely to datapills in Workato. When input or output fields are defined with names that have these special characters, input fields don’t show up and output datapills render incorrectly.
```ruby
 
    -<>!@#$%^&*()+={}:;'"`~,.?


```

For example, schema defined where
```ruby
 
    {
      name: “due-date”
    }


```

Would not show up as a string input field and datapills would turn render as long strings instead of datapills.

![Broken datapill](data:image/png;base64,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) _When names of schema have special characters, datapills are renders incorrectly_

instead of

![Proper datapill](data:image/png;base64,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) _There is a need to render them properly by switching out the special characters in their names_

Fortunately, there is a workaround which we highly recommend you build into your connector as well. ( You could even copy and paste the following if it fits.) We create a series of 3 methods, `format_schema`, `format_payload`, `format_schema` which can be called at the beginning and end of each `execute` block. We had done something similar in our earlier example when defining our action.

### [#](<#format-schema>) `format_schema`

Sample code snippet:
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

### [#](<#format-payload>) `format_payload`

Sample code snippet:
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

### [#](<#format-response>) `format_response`

Sample code snippet:
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

### [#](<#replace-special-characters-and-inject-special-characters>) `replace_special_characters` and `inject_special_characters`

Samples code snippet:
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

## [#](<#avoid-encoded-query-parameters>) Avoid encoded query parameters

Workato's SDK automatically encodes query parameters in GET requests, which can break requests for APIs that expect exact formatting. To avoid this, build the query string manually and append it directly to the URL.

For example:
```ruby
 
    url = "https://api.example.com/reports"
    query_string = "addressVerification=true&poi[latitude]=#{input['latitude']}&poi[longitude]=#{input['longitude']}"

    get("#{url}?#{query_string}")


```

This preserves the exact casing and structure required by the API. Use this pattern when the API expects raw query strings or rejects encoded characters.

## [#](<#header-casing-in-sdk-console>) Header casing in SDK console

Case-sensitive headers may appear with incorrect casing when you test connectors in the SDK console.

This issue affects only the console interface. The SDK console formats header names for display, but Workato sends the request with the exact casing defined in your code.

For example:
```ruby
 
    case_sensitive_headers(BPMCSRF: connection['BPMCSRF'],
                           Cookie: connection['Cookie'])


```

In the console, a header like `BPMCSRF` may display as `Bpmcsrf`, but the actual request uses the correct casing. You don't need to change your code.

## [#](<#summary>) Summary

Object based actions and triggers in Connectors are something we highly recommend. Not only do they improve user experience for your users but they also make it so much easier to extend your connector when done properly. Here are a few of the main concepts we covered:

  1. Defining the base schema of each object in a service method. Don’t forget to include an input argument that allows you to adjust the schema based on the action type.
  2. Use object_definitions to pull the proper input and output field schema based on the object selected
  3. When defining actions or triggers, make sure to declare all blocks especially `description` blocks. This will vastly increase usability for your users.
  4. Contain any general processing inside execute blocks but leverage on dedicated object execute methods (i.e. `create_invoice_execute`)for anything specific. i.e. Use `format_paylod` and `format_response` in the execute block before using the `create_#{object}_execute` method.

### [#](<#usability-rules>) Usability rules

Great connectors not only have great architecture but look and feel great to use. Read on to find out more about how you can make your connector easy to use.
