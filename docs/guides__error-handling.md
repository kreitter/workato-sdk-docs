# Workato SDK Documentation

> **Source**: https://docs.workato.com/en/developing-connectors/sdk/guides/error-handling.html
> **Fetched**: 2026-06-10T03:12:22.225414

---

[Connector SDK](</en/developing-connectors/sdk>)

[How-to guides](</en/developing-connectors/sdk/guides>)

Are you an LLM? You can read better optimized documentation at /en/developing-connectors/sdk/guides/error-handling.md for this page in Markdown format

# Error Handling [​](<#error-handling>)

Copy page

Exposing detailed and helpful error message can improve the recipe building experience for you and the end users of your custom connector. However, default custom connector actions and triggers do not expose response messages. Additionally, you may want to expose error messages in other instances (such as when action/trigger input data does not meet certain business requirements). This can be achieved using the following helper methods.

## Validating inputs [​](<#validating-inputs>)

You can raise custom errors for inputs that violate business logic. Let's use an example of a search action that tries to search for a **Contact** using a search action. You want to make sure that the user is searching for records with at least one search criteria. In this case, you will want to raise an error if there are no input values, instead of sending a request with no query parameters.

### `error` [​](<#error>)

This is a Workato SDK specific method to raise a job error with a custom message. The error method accepts arguments which will then be surfaced to end users in the Workato platform when they trigger an error using your custom connector. This can be used in a number of ways to improve usability for your custom connector.

#### Sample code snippet [​](<#sample-code-snippet>)

ruby
```ruby

    execute: lambda do |connection, input|
      error("Provide at least one search criteria") if input.blank?
      get("", input)
    end

```

![Input validation error message](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAigAAACqCAMAAACwNERNAAADAFBMVEX86uzNJFn///fz3K9SUlLPJBnz///////n5+fNJBni+P/5////+dv86uXx6uzipmDhmlb/+dPNJGDXUxn95cXxzKNyUlLNTa/h5O1SUmxsUlL///DVThnR4O3xyJrUNxn3+f/848v05Ovv///NJFTNNqTSJBnNJERSUmDTfJPOn9vNOK/b0+3U1ffOlMvUxeXUx/LjplnNJED16+z749bp6uvjp3DNJH7c4//36uz49/fNS6T//t/s6u3z5Mfj3NrSteLir37WSRnOToHf8P9hU1LNVKzq+P/gyctvUlL97d3f+P9hlMfWyurObKXNdLve5O7YpaJWV1ffkFVSaKHi09ZXUlJSWZjanH1UU3v6+P/UqcuaxePo///e3e3QlbjUbljdz9zOdq/Sp8W0xdbcnojVvNbOmNPNJHDTv+fgvqrYtdrZpHL/+OvRcYfWX0P02aPgrJbNT5bYfXTftKfbur7QSxnqz8jcilzZinTz0qzemmXNJI7NJJvp18DZxd7e4/fZf1zV3P/VzN3RmcN/mbvquIjXw8nYm2zruZfj0sjQn8SZt8fNLXjNN3uabVfC0+X34uGzjG7ZZBnftprUz/fY3PfOkGDr3dvg0uTowaLQn83s3NL86tbW+f/w0rfo4+jYuM7OUHDJQDfZcBnY1crNXZ1WZHvUs9P/8c3r8fv57+H+/+nNN5Pek0Tu8enNN2jRhK/r49xZhrrUlJ3TU0SAVVLVobpxo9hzr93gpY9tndP42Lt7pcqd0/Tz//fVXBnT9P/ef0HNNpyMYFLQp9vkx7fNdsXbtbno8fHRY23Rd6P86s3Ug4mHgYRXdqmv3vTNY7fNfce+eVK/l3jOi8q6sZjKzMFUUmLDv7vQNhn84MXKooXk3enNltHt49PRUVfONxnVcUTNN4bOfLrg6vfYdWDMro7OTlrQdZLVrLDF2O1xi6ScqrCSwd7e//+5xsTNJKiEm6jck3iSmozvwpOxorKj2fTI7v/BmYLR5ezVbkDMj1bp/+nNn9vNNlRv3YxoAAALeklEQVR42u2dd1RUZxqH7wx3uL7ODKAUGRhBig6LRA1FlGYFORoVRIkuq4hiwR4rYk/s8djXlhh7ibHr2lZXY6Kx5KwxTY3xpJhE088m2V7f786dYcRx4IQQ4vp7/pjLfG3ume+Z932/+4dKKUl1AKgUKXeLBEDlbCF8B6AKEEQBEAVAFABRAEQBEAVAFAAgCoAoAKIAiAIgCoAoAKIAAFEARAEQBUAU8BCKsizS8+zs4J/kJpb5YCMeZlFOHpHlHcUeJgfkf+NZgKLWVbmHk/lXXMdNiY9Tr+YzyZV5OGkjdrD2RVl/JObrd0N6etjrgJDfeFy83bT0qtzDzaBDrm+n0HY1wiwgXY7niZ2blGAHa1+UMJk1MHtKPgGZnkXxa5zwI25pClFb4el7VL+SiPI6dcUO/hJEOWVPAe/nyzuWSuY7+XKfpVJgn3cz5S9Fm6U4IOS7V0WXGDSIaP/wDdGcNVpu90nsT3R54/cfxV8qTEicRdRhrRQRf5ho4DqibknqYG4KXDyeRJpZ/+op+7JXVDH8Fk+cmsTLxA/SBUvD3qP4wZK0YSJFHz4cl/gZzw+WWnbrTTQ7YcOHtHlznDpkNqqc2hOl8xI55rtnJGl1TPHzy2MalsmLFi7pExwmy1//JWm1PGfb3+cEBHHbq0+KTcqjo70GzV5HzXmjX/E5qyuadDn4/D8XT9j0Unj0pkln4uMiSDfvKaJN46mZlBc9fM2s6H6BRF8cZSVuhjzBVvYpHpb5hCpKgw30nBRAbwZGB79uKOw1i+IiDAduraQDB8NvF02a+Er6FOrWaxCVJOZS4YRbC2hAr6eoe2vsZa0Vs+ZhS2T5VEBIz3nz7shqkvlzTMMwuVgUJ4ecNUq7mIaSFEHdRUOgKkpjn63xmyK11BMo8kgENYvgrvVNmkmSNTWDxmZnr6SSQC1zBAhRxCpvqc7xrLPRwWd1wSyKWsJQ8wCezHkmkAqzs/Pic1hFab2hmZp6zO33cCGUF52DvazF43Hr9Uss20J2/JFZan4/U5YtDcMs/xBbe8pZo4TZRXnOVZQITj3d0sVf3BQnqk5VFHP7ZpJZiLJ51KhRn8cF6oLvFWW+JopPhCGezklClPETiai5eQWNoqEcgnjeqMsbxbpiLfuaV7kQmqsLxl7WliiJa/lltWVbkJoQpH9ZiluLiCJ21BFRXETRIgrHiLzGYrs5YpRHlAC6RxTDO+qKWsQoF2WKQxRpLnGc4P4FVBApZq7YPqFIW0sbYReFI4pVFDR5OkSUWhPlLfmrG8vlQ9J8rkfu5C99q88z54MsdlEkUaMsv5LhFIVrlMKFs7IyuHjoTak+446uOcGRJG/ohYFqjWIVNYpTlHQ/TiEn4uM8iGLOjVNFmkszJp3hme3pv3dHDTZb4wdmT56aVC5KYW7cAv7ME6hRajOiLJdl+at0yfw2X+ekl4XIMT+I1CO86Mx94tQjRLE38NlGN1w6wceZ/qk+fKqhAkniM87YpMTRfB6aITlEkVZkJZi/5/7CdGfq4ZilrqKlnlTtCMP9iVaiw4bmZVR4IXdidI44TUUXtBYjxFqdR4uTNJfIdCAdW1mLNYp5mfY7jXR5dfTd94DlnkHL7E9Q1NdIN89iIqsaASLFEnnqeVkUrBXWsi8TmYCNrN1i9pfCSaK7RLORXiBKJSReyD26FrsFUQBEARAFQBQAIAqAKACiAIgCIAqAKACiAABRAEQBEAVAFABRAEQBj5YoCgCVAlEARAEQBUAUAFEARAEQBQCIAiAKgCgAogCIAiAKgCgAeBYlJalOtUjB1/toiJJkrNbSKUn4eh8NUepUc+06+HohCkSBKBAFQBQAUQBEARAFQBSI8oiKYjrSg5GPQRSI4nGj64XILEo+RIEolYgSZHkBqQeiVFkU05FFb8vHvK4XL5H/qqzMlC2LFKXdjmtBlpchCkRRRbm+6Nq1hnyVZfn4GH6R3xghyzv4jcJXuWK8gSiPrCjCjSfE9Zt9jcbIlqXppiD5DcUr3/LCCLlnzkWkHoiiibLoxo0v+drTW1HGyL8X9e2TUUraEcvLI+Q/oEaBKM4a5Vv71UUU/nP3EogCUdwUs/eIcv1vyouZEAWi3Jt6emT2yD/mIoqyWrb8EMJ1C0SBKBWKWfl4vaArqijHuU2v/p/I3izKGxAFongkpZrzwSMiigJRIApEARAFQBQAUQBEARAFQBSIAlGqKQr4/wH/PgqodkQBAKIAiAIgCoAoAKIAiAIgCgAQBUAUAFEARAEQBUAUAFEAgCgAogCIAiAKgCgAogCIAgBEARAFQBQAUQBEARAFQJTKSfC2X9d0evCYkbeMNXTf+rXebpt3uWtN6YSNrklR9P5EpHs2ym3ni9RdlcBEv3XTq9nja+vifuk11d26MnK78l5qpYzsV8HO0PDkvtjpGhVl6LwJ/emq29+uyfCOJspj93eGNrHb41u/rtuVHf0/Hi+d25Vb6joqc6dVUFu/4hWIUrOiNGAXSnVdPMw3prkTJY2e9iiKo786onyrPCCtPd7UiH39uUWJEpvdpd2AdjSt78jJRGNn3qQS7irtvtvaVtH3JrrEouifIuowU12Ox3TrlPEhbe7QShMl8XdEz3krH4xWL4n+ZCtw9ouJ+7sq+tHPfka6ropjrL1j7Exl5DiiAXW1VRXtNrht+0wv2xfcpSYwreH2MLJ1DEuuO+gj26VmRm2mfUppd6N+JdHimdjvmosoL1nr121JyROGh4brZnxwxvapP0f2AGproliuCHZuLGVR/HRd95Vy0FeUdouLptNrCeNpYHZHuygv0ie7ptMQZUW3fiupJLRJ1sXzs/c5+v1oZ9J8KuFiaODBWbqOjrGKEkbNDx5eFRq+J+egtXGUfVWj8zaeH9fCi5L7nVeHOhvoQkEUWz3p49vZMxwz1Sl6a4Ook7bBH/hPRQaqqWL27kdEXRXfoZxBvKiFqEhiy7h69Uuuy3+ZxEZx6jFRVpte65xF7d7GUS6px5cG92oT/qcodUv/s7vJHlFqav0meoc/xZp62soLBdBj5WPnUsEu8ZHPtmnjZy+IedXy2xCph1u3pkaVN9AqLYT5cupxzFSnsPBqmRXoMYmCahWz84o4vD8uvmgvPlBwFRobGn41jc4pqiglajFrog6/YkQueYmTBGV5OypcVRTRV2B8vj/3xCoZE4nOGbV+E7Xl17MNTltj1YUcY/mjB3Hq6ehFn/P7A520VbXbWOUsZn2bujSo5ZAQ5XFudcxUpwhRRC6jB1RM4CcpZtXy0Fv75dbjvZ5L/TnNOCJKPRbFMMR5EE39VPFryqI4I0pLNSXxaXr2Ln14rCgp5tu6mBwR5U0RUZyiaGPtTDcM0YKFY9Xy29BEua9BE8XoaLSPEKLsrd/PWKaDKDVYzDq+brUW8Ld1VNIMYn9FjbLCtnOhgYODLwf68TaOKLubdL84TI0oA8drxWw9Si5a+PFrGbRz33yK3X1pxr7S5L6Ofj8q2DiZWug1UbSxbOe6AcHTqa3e3za4Te+p/9ZWdd5GG/+25aK4Nqii+CVn7zxtn9nXKcrW5JzpBkSUmhFF2Zplf4Tiq+b4ND637I8TDyuEEybDOaWzlShXnHr49EPqg7kFfPzp3cA7lIeKn3RL3hqRbDr005cSXd4aG/oZJ4BViqNfTLQNVxyiaGO5YwMv+EmUksb5SjfYqK1qv43OfDIa20rNNPc1qB9YxmkqSpvpa089Wd4Z/DYXotSQKBX5daOKLY2M9/1R4b2YZnSdbO+5f6LrWCalketHNvJ4GxUbjO4aG+Hpys8mCoAoAEAUAFEARAEQBUAUAFEARAEAogCIAiAKgCgAogCIAiAKABAFQBQAUQBEARAFQBQAUQCAKACiAIgCIAp4KEXZAlFAVUTJ3YIvAVRBlJSkOgBUioTfCqgK/wP3lIez1r7UWwAAAABJRU5ErkJggg==) _Input validation error message_

## Handling response errors [​](<#handling-response-errors>)

Some APIs do not use response codes to indicate an error with a request. These APIs may respond with `200` HTTP code and error messages in the response body.

By default, the SDK framework will only raise errors when the HTTP response code indicates an error. Since Sage Intacct returns a response of 200 with the error nested inside its response message, it is important to validate all responses and raise an error if one is present in the response body.

### `detect_on` [​](<#detect-on>)

There are 2 ways you can catch these errors. The first method is to use [detect_on](</en/developing-connectors/sdk/sdk-reference/connection/authorization#detect-on>). This is a connector-wide method to catch errors; It applies to all actions and triggers. This method will raise errors with a standard message format that cannot be customized.

### `after_response` [​](<#after-response>)

The alternative is to handle these errors in the [after_response](</en/developing-connectors/sdk/sdk-reference/http#response-handling>) method. This method can be used together with `error()` to validate the contents of a HTTP response and raise custom errors. This method applies to individual actions/triggers. Hence the conditions used to detect an error can be customized to each request. Additionally, the error message can be changed to suit each actions/triggers.

For example, we can use the `after_response` method to check the contents of the response body before deciding to return the body as a successful request output or to raise an error with a custom message.

#### Sample code snippet [​](<#after-response-sample-code-snippet>)

ruby
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

### `after_error_response` [​](<#after-error-response>)

`after_error_response` is a helper method that can be chained to a HTTP verb method to handle HTTP responses; In particular, when the API responses with an error response code.

This method accepts 2 arguments. First, a number which represents the exact error code that you wish to handle.

Next, it also accepts a conditional path that will be executed when a HTTP response code matching the first argument is received.

#### Sample code snippet [​](<#after-error-response-sample-code-snippet>)

Let's take a look at an `after_error_response` example, using **Airtable** API.

ruby
```ruby

    execute: lambda do |connection, input|
      patch("https://api.airtable.com/v0/#{connection['base_id']}/users/#{id}", payload).
        after_error_response(404) do |code, body, header, message|
          error("#{message}: #{body}")
        end
    end

```

When you try to update a row with an invalid ID, a HTTP error will be returned. The Error code used is `404` with a JSON body `{"error":"NOT_FOUND"}`.

![Formatted error message in recipe job detail page](/assets/formatted-error-message.D4d-YRLJ.png)_Formatted error message in recipe job detail page_

## Handling HTTP redirection [​](<#handling-http-redirection>)

Some APIs return HTTP `302` redirects, which the SDK doesn't follow by default. This can cause unexpected failures, such as a `400 Bad Request`, even when the request itself is valid.

For example, an API may redirect `/v1/data` to `/v2/data`, but the SDK stops at the `302` and raises an error.

### Solution [​](<#solution>)

Complete the following steps to handle redirect responses:

1

Use the `ignore_redirection` method to capture the intermediate redirect response.

2

Use `after_response` to detect the `302` status and extract the `location` header.

3

Reissue the request manually using the redirected URL from the `location` header.

For example:

ruby
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

### Conditionally skip authentication for redirected domains [​](<#conditionally-skip-authentication-for-redirected-domains>)

Some redirected domains, such as Amazon S3, may reject authentication headers. Use `current_url` in the `apply:` block to conditionally exclude headers:

ruby
```ruby

    apply: lambda do |connection|
      unless current_url.include?('.amazonaws.com/')
        headers(Authorization: "Bearer #{connection['api_token']}")
      end
    end

```

## Handling Picklist errors [​](<#handling-picklist-errors>)

The `after_error_response` helper method can also be chained to HTTP verb methods in other parts of your custom connector. For example, you may want to handling and provide custom error messages from dynamic [pick_lists](</en/developing-connectors/sdk/sdk-reference/picklists>). In this example, we are looking at handling errors from [Docparser](<https://dev.docparser.com/>).

#### Sample code snippet [​](<#handling-picklist-errors-sample-code-snippet>)

ruby
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

![HTTP request error message in recipe editor](/assets/pick-list-error.CLjhhkou.png)_HTTP request error message in recipe editor_

## Handling object definition errors [​](<#handling-object-definition-errors>)

This can also be used in [dynamic fields](</en/developing-connectors/sdk/sdk-reference/object_definitions>) code block in object_definitions.

#### Sample code snippet [​](<#handling-object-definition-errors-sample-code-snippet>)

ruby
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

![Schema error message in recipe editor](/assets/extended-schema-error.B9TFZtc7.png)_Schema error message in recipe editor_

**Last updated:**
