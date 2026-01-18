# Workato SDK Documentation

> **Source**: https://docs.workato.com/en/developing-connectors/sdk/guides/error-handling.html
> **Fetched**: 2026-01-18T02:50:12.025944

---

# [#](<#error-handling>) Error Handling

Exposing detailed and helpful error message can improve the recipe building experience for you and the end users of your custom connector. However, default custom connector actions and triggers do not expose response messages. Additionally, you may want to expose error messages in other instances (such as when action/trigger input data does not meet certain business requirements). This can be achieved using the following helper methods.

## [#](<#validating-inputs>) Validating inputs

You can raise custom errors for inputs that violate business logic. Let's use an example of a search action that tries to search for a **Contact** using a search action. You want to make sure that the user is searching for records with at least one search criteria. In this case, you will want to raise an error if there are no input values, instead of sending a request with no query parameters.

### [#](<#error>) `error`

This is a Workato SDK specific method to raise a job error with a custom message. The error method accepts arguments which will then be surfaced to end users in the Workato platform when they trigger an error using your custom connector. This can be used in a number of ways to improve usability for your custom connector.

#### [#](<#sample-code-snippet>) Sample code snippet
```ruby
 
    execute: lambda do |connection, input|
      error("Provide at least one search criteria") if input.blank?
      get("", input)
    end


```

![Input validation error message](data:image/png;base64,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) _Input validation error message_

## [#](<#handling-response-errors>) Handling response errors

Some APIs do not use response codes to indicate an error with a request. These APIs may respond with `200` HTTP code and error messages in the response body.

By default, the SDK framework will only raise errors when the HTTP response code indicates an error. Since Sage Intacct returns a response of 200 with the error nested inside its response message, it is important to validate all responses and raise an error if one is present in the response body.

### [#](<#detect-on>) `detect_on`

There are 2 ways you can catch these errors. The first method is to use [detect_on](</developing-connectors/sdk/sdk-reference/connection/authorization.html#detect-on>). This is a connector-wide method to catch errors; It applies to all actions and triggers. This method will raise errors with a standard message format that cannot be customized.

### [#](<#after-response>) `after_response`

The alternative is to handle these errors in the [after_response](</developing-connectors/sdk/sdk-reference/http.html#response-handling>) method. This method can be used together with `error()` to validate the contents of a HTTP response and raise custom errors. This method applies to individual actions/triggers. Hence the conditions used to detect an error can be customized to each request. Additionally, the error message can be changed to suit each actions/triggers.

For example, we can use the `after_response` method to check the contents of the response body before deciding to return the body as a successful request output or to raise an error with a custom message.

#### [#](<#sample-code-snippet-2>) Sample code snippet
```ruby
 
    post("https://api.intacct.com/ia/xml/xmlgw.phtml", payload).
      format_xml("request").
      after_response do |code, body, headers|
        result = body.dig("response", 0, "operation", 0, "result", 0)
        if result.dig("status", 0, "content!") == "failure"
          error(result.dig("errormessage", 0))
        else
          result["data"]
        end
      end


```

### [#](<#after-error-response>) `after_error_response`

`after_error_response` is a helper method that can be chained to a HTTP verb method to handle HTTP responses; In particular, when the API responses with an error response code.

This method accepts 2 arguments. First, a number which represents the exact error code that you wish to handle.

Next, it also accepts a conditional path that will be executed when a HTTP response code matching the first argument is received.

#### [#](<#sample-code-snippet-3>) Sample code snippet

Let's take a look at an `after_error_response` example, using **Airtable** API.
```ruby
 
    execute: lambda do |connection, input|
      patch("https://api.airtable.com/v0/#{connection['base_id']}/users/#{id}", payload).
        after_error_response(404) do |code, body, header, message|
          error("#{message}: #{body}")
        end
    end


```

When you try to update a row with an invalid ID, a HTTP error will be returned. The Error code used is `404` with a JSON body `{"error":"NOT_FOUND"}`.

![Formatted error message in recipe job detail page](data:image/png;base64,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) _Formatted error message in recipe job detail page_

## [#](<#handling-http-redirection>) Handling HTTP redirection

Some APIs return HTTP `302` redirects, which the SDK doesn't follow by default. This can cause unexpected failures, such as a `400 Bad Request`, even when the request itself is valid.

For example, an API may redirect `/v1/data` to `/v2/data`, but the SDK stops at the `302` and raises an error.

### [#](<#solution>) Solution

Complete the following steps to handle redirect responses:

1

Use the `ignore_redirection` method to capture the intermediate redirect response.

2

Use `after_response` to detect the `302` status and extract the `location` header.

3

Reissue the request manually using the redirected URL from the `location` header.

For example:
```ruby
 
    file: get("/api/packages/#{input['package_id']}/download").
      response_format_raw.
      ignore_redirection.
      after_response do |code, body, header|
        if code == 302 && header['location'].present?
          get(header['location']).
            response_format_raw.
            after_error_response(/.*/) do |_code, body, _header, message|
              error("#{message}: #{body}")
            end
        else
          body
        end
      end


```

### [#](<#conditionally-skip-authentication-for-redirected-domains>) Conditionally skip authentication for redirected domains

Some redirected domains, such as Amazon S3, may reject authentication headers. Use `current_url` in the `apply:` block to conditionally exclude headers:
```ruby
 
    apply: lambda do |connection|
      unless current_url.include?('.amazonaws.com/')
        headers(Authorization: "Bearer #{connection['api_token']}")
      end
    end


```

## [#](<#handling-picklist-errors>) Handling Picklist errors

The `after_error_response` helper method can also be chained to HTTP verb methods in other parts of your custom connector. For example, you may want to handling and provide custom error messages from dynamic [pick_lists](</developing-connectors/sdk/sdk-reference/picklists.html>). In this example, we are looking at handling errors from [Docparser (opens new window)](<https://dev.docparser.com/>).

#### [#](<#sample-code-snippet-4>) Sample code snippet
```ruby
 
    pick_lists: {
      parsers: lambda do
        get('https://slack.com/api/users.list').
          after_error_response(400) do |code, body, headers, message|
            error("Error loading parser pick list: #{body[/(?<=error\"\:\").*(?=\"\})/]}")
          end.
          pluck("label", "id")
      end
    }


```

HTTP error will be displayed in the recipe editor when the custom adapter tries to load the pick list. In the example, the API key was reset, resulting in an invalid API keys used in the request.

![HTTP request error message in recipe editor](/assets/img/pick-list-error.cd6f5bd3.png) _HTTP request error message in recipe editor_

## [#](<#handling-object-definition-errors>) Handling object definition errors

This can also be used in [dynamic fields](</developing-connectors/sdk/sdk-reference/object_definitions.html>) code block in object_definitions.

#### [#](<#sample-code-snippet-5>) Sample code snippet
```ruby
 
    object_definitions: {
      parsed_data: {
        fields: lambda do |connection, config_fields, object_definitions|
          get("https://api.docparser.com/v1/results/#{config_fields['parser_id']}1/schema").
          after_error_response(400) do |code, body, headers, message|
            error("Error loading parser schema: body[/(?<=error\"\:\").*(?=\"\})/]")
          end
        end
      }
    }


```

HTTP error will be displayed in the recipe editor when the custom adapter tries to fetch schema for an unknown parser.

![Schema error message in recipe editor](/assets/img/extended-schema-error.63655738.png) _Schema error message in recipe editor_
