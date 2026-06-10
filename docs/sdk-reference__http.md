# Workato SDK Documentation

> **Source**: https://docs.workato.com/en/developing-connectors/sdk/sdk-reference/http.html
> **Fetched**: 2026-06-10T03:12:38.866304

---

[Connector SDK](</en/developing-connectors/sdk>)

[SDK reference](</en/developing-connectors/sdk/sdk-reference>)

Are you an LLM? You can read better optimized documentation at /en/developing-connectors/sdk/sdk-reference/http.md for this page in Markdown format

# HTTP Methods [​](<#http-methods>)

Copy page

In this section we cover the various HTTP methods that Workato supports. You should already be familiar with most of them. We also cover how you can do post-response processing of your HTTP calls to manipulate data into formats that are easier to use later on in your connector code.

## HTTP verb methods [​](<#http-verb-methods>)

HTTP verb| Method| Example  
---|---|---  
GET| `get()`| `get("url", parameters)`  
POST| `post()`| `post("url", payload)`  
PUT| `put()`| `put("url", payload)`  
PATCH| `patch()`| `patch("url", payload)`  
DELETE| `delete()`| `delete("url", parameters)`  
OPTIONS| `options()`| `options("url", parameters)`  

## Forming a request [​](<#forming-a-request>)

Each HTTP verb method must be provided a `url` string as the first argument. The second argument (optional) can be in 2 forms.

Firstly, `input` can be passed as a single hash. This hash can simply be the `input` argument of the `execute` or `poll` argument, such as the following:

ruby
```ruby

    execute: lambda do |connection, input|
      get("https://www.some_api_endpoint.com/api", input)
    end

```

The hash can also be formed before like this:

ruby
```ruby

    execute: lambda do |connection, input|
      params = {
        "id" => input["id"]
      }

      get("https://www.some_api_endpoint.com/api", params)
    end

```

The Workato SDK framework processes this hash value and transforms it into the respective data format. For GET, DELETE OPTIONS requests, the hash data is converted to URL query parameters.

For POST, PUT, and PATCH, the payload is formed into the request body into a format that you specify. Refer to [Data formats](</en/developing-connectors/sdk/guides/data-formats>) for more information on working with the various data formats.

The other method of passing request data is as a series of key/value pairs.

ruby
```ruby

    execute: lambda do |connection, input|
      post("https://www.some_api_endpoint.com/api", name: input["name"], email: input["email"])
    end

```

All arguments after the first will be transformed into request data. In this case, since the default data format is JSON, the following request body is formed:

json
```ruby

    {
      "name": "Ee Shan",
      "email": "[[email protected]](</cdn-cgi/l/email-protection>)"
    }

```

For a GET request, the following URL parameters are formed.

ruby
```ruby

    execute: lambda do |connection, input|
      get("https://www.some_api_endpoint.com/api", name: input["name"], email: input["email"])
    end

```

The full request URL string will be:
```ruby

    https://www.some_api_endpoint.com/api?name%3DEe%20Shan%26email%3Deeshan%40workato.com

```

AUTHENTICATION APPENDS TO THE REQUEST URL

Any authentication you define is appended to the request URL. The preceding example assumes no authentication is required. Authentication is applied through the `apply` block defined in the `connection` object.

## Additional helper methods to form requests [​](<#additional-helper-methods-to-form-requests>)

You may use a variety of other helper methods on Workato by chaining them after the initial HTTP verb method. Here are some methods that might be useful:

### payload [​](<#payload>)

This method allows you to add a payload to a request and follows the same syntax that we covered above.

ruby
```ruby

    execute: lambda do |connection, input|
      post("https://www.some_api_endpoint.com/api")
        .payload(name: input["name"], email: input["email"])
    end

```

Resulting the payload of the post request:

json
```ruby

    {
      "name": "Ee Shan",
      "email": "[[email protected]](</cdn-cgi/l/email-protection>)"
    }

```

## params [​](<#params>)

This method allows you to add a query parameters to a request and follows the same syntax that we covered above. These values will be URL-encoded.

ruby
```ruby

    execute: lambda do |connection, input|
      get("https://www.some_api_endpoint.com/api")
        .params(name: input["name"], email: input["email"])
    end

```
```ruby

    https://www.some_api_endpoint.com/api?name%3DEe%20Shan%26email%3Deeshan%40workato.com

```

## headers [​](<#headers>)

This method allows you to add a headers to a request and follows the same syntax that we covered above. Headers defined here **are not case sensitive.**

ruby
```ruby

    execute: lambda do |connection, input|
      get("https://www.some_api_endpoint.com/api")
        .headers(Authorization: "Bearer HTB674HJK1")
    end

```

TIP

Whilst case sensitive headers are a departure from [RFC](<http://www.w3.org/Protocols/rfc2616/rfc2616-sec4.html#sec4.2>), you may use them in your HTTP methods through the method `case_sensitive_headers` in place of `headers`.

## tls_client_cert [​](<#tls-client-cert>)

This method allows you to add SSL certs, keys, passphrases, and intermediates certs.

ruby
```ruby

    execute: lambda do |connection, input|
      get("https://www.some_api_endpoint.com/api")
        .tls_client_cert(
          certificate: connection['ssl_client_cert'],
          key: connection['ssl_client_key'],
          passphrase: connection['ssl_key_passphrase'],
          intermediates: connection['ssl_client_intermediate_cert']
        )
    end

```

## Post-response processing [​](<#post-response-processing>)

### Default response data [​](<#default-response-data>)

By default, all HTTP verb methods will return the response body of the request. For example, the following request creates a user in **Okta**.

ruby
```ruby

    execute: lambda do |connection, input|
      response = post("/api/v1/users", profile: { login: input["email"], displayName: input["name"] })
    end

```

`response` variable will a hash that looks like this:

ruby
```ruby

    {
      "id": "00ub0oNGTSWTBKOLGLNR",
      "status": "STAGED",
      "created": "2018-03-13T21:36:25.344Z",
      "activated": null,
      "statusChanged": null,
      "lastLogin": null,
      "lastUpdated": "22018-03-13T21:36:25.344Z",
      "passwordChanged": null,
      "profile": {
        "firstName": "Ee Shan",
        "lastName": "Sim",
        "email": "[[email protected]](</cdn-cgi/l/email-protection>)",
        "login": "[[email protected]](</cdn-cgi/l/email-protection>)",
        "mobilePhone": null
      },
      "credentials": {
        "provider": {
          "type": "OKTA",
          "name": "OKTA"
        }
      }
    }

```

### Response handling [​](<#response-handling>)

`after_response` is an optional block that can be chained to the HTTP verb methods to handle the various parts of a HTTP response. Let's take a look at an example, again using the **Okta** API.

When a request is sent to the [List all users](<https://developer.okta.com/docs/api/resources/users#list-all-users>) endpoint, the truncated response looks like this.

http
```ruby

    HTTP/1.1 200 OK
    Content-Type: application/json
    Link: <https://workatotest.okta.com/api/v1/users?limit=200>; rel="self"

    [
      {
        "id": "00utti9t3j1xO9jOm2p6",
        "status": "ACTIVE",
        "created": "2018-03-15T08:23:05.000Z",
        "activated": null,
        "statusChanged": "2018-03-15T08:39:39.000Z",
        "lastLogin": "2018-03-15T08:39:40.000Z",
        "lastUpdated": "2018-03-15T08:39:40.000Z",
        "passwordChanged": "2018-03-15T08:39:39.000Z",
        "profile": {},
        "credentials": {},
        "_links": {}
      }
    ]

```

This response can be broken down into 3 parts. The HTTP response **code** , **header** , and **body**.

`after_response` can be used to handle all these parts of the HTTP response. Suppose I have an action that lists all users and outputs the entire response, including the link to the existing page from the header.

ruby
```ruby

    execute: lambda do |connection, input|
      get("/api/v1/users").after_response do |code, body, headers|
        {
          code: code,
          next_link: headers["link"],
          users: body
        }
      end
    end

```

The resultant output of this action will contain all 3 parts of the response.

json
```ruby

    {
      "code": 200,
      "next_link": "<https://workatotest.okta.com/api/v1/users?limit=200>; rel=\"self\"",
      "users": [
        {
          "id": "00utti9t3j1xO9jOm2p6",
          "status": "ACTIVE",
          "created": "2018-03-15T08:23:05.000Z",
          "activated": null,
          "statusChanged": "2018-03-15T08:39:39.000Z",
          "lastLogin": "2018-03-15T08:39:40.000Z",
          "lastUpdated": "2018-03-15T08:39:40.000Z",
          "passwordChanged": "2018-03-15T08:39:39.000Z",
          "profile": {},
          "credentials": {},
          "_links": {}
        }
      ]
    }

```

### Testing [​](<#testing>)

You can easily verify this while developing your custom connector. When you include post-request handling, the output tab should reflect the expected JSON object.

![Output with response code and header values](/assets/response_with_headers.Ce_SG2OX.png)_Output with response code and header values_

**Last updated:**
