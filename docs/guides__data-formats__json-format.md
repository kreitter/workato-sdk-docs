# Workato SDK Documentation

> **Source**: https://docs.workato.com/en/developing-connectors/sdk/guides/data-formats/json-format.html
> **Fetched**: 2026-01-18T02:50:07.337127

---

# [#](<#how-to-guides-json-data-format>) How-to guides - JSON data format  

The Workato SDK's default expected data format is JSON. Action and trigger inputs will be passed as JSON payloads if no data format is specified. A JSON parser error will be shown if the SDK expected JSON and got another data format.

When you declare any HTTP request, Workato assumes the outgoing request and incoming response is in JSON. We help you append the appropriate headers `Accept: application/json` and `Content-Type: application/json` to the outgoing request.

Below we have an example of an action titled `post_message`. This simple action collects input from the user based on fields defined in the `input_fields` key in the `post_message` action and when the action is executed in a recipe, the execute key is run that creates a `POST` HTTP call to `https://api.ciscospark.com/v1/messages` with `input` as its body.

## [#](<#sample-code-snippet>) Sample code snippet
```ruby
 
    {
      title: 'My cisco connector',

      connection: {
        # Some code here
      },
      test: {
        # Some code here
      },

      actions: {
        post_message: {
          input_fields: lambda do
            [
              {
                name: "roomId"
              },
              {
                name: "text"
              }
            ]
          end,

          execute: lambda do |connection,input|
            post("https://api.ciscospark.com/v1/messages", input)
          end,

          output_fields: lambda do
            [
              {
                name: "id"
              },
              {
                name: "roomId"
              },
              {
                name: "roomType"
              },
              {
                name: "text"
              },
              {
                name: "personId"
              },
              {
                name: "personEmail"
              },
              {
                name: "created"
              }
            ]
          end
        }
      },

      triggers: {
        # Some code here
      },
      object_definitions: {
        # Some code here
      },
      pick_lists: {
        # Some code here
      },
      methods: {
        # Some code here
      },
    }


```

Here we have the resultant request that is sent when the `execute` key above is executed. We default your `Content-Type` header to `application/json` and also format your input as key-value pairs in a JSON formatted string. This minimizes the amount of pre and post request processing that you need to do.

## [#](<#request>) Request

Now lets go through what happens when we run the `post_message` action that we just defined. Below we go through the POST HTTP request we send out to <https://api.ciscospark.com/v1/messages>[ (opens new window)](<https://api.ciscospark.com/v1/messages>)

HEADERS AND BODY SECTIONS

`POST` HTTP requests are usually divided into two sections: `Headers` and `Body`. The request headers define the HTTP method and include metadata related to the request. The request body contains the actual content or payload.

### [#](<#request-headers>) Request headers

Since no data format was declared in our action, Workato defaults to JSON and assigns `Content-Type` to `application/json`. This tells the API we sent the request to that our request body is in a JSON data format.
```ruby
 
    POST https://api.ciscospark.com/v1/messages
    Accept  application/json
    Content-Type  application/json
    Authorization Bearer ---


```

### [#](<#request-body>) Request body:

This request body is generated based on the user's input and transformed into a JSON format by Workato. This request body corresponds to a user's input for the `roomId` field being `1234` and `text` field being `testing`.
```ruby
 
    {
      "roomId":"1234",
      "text":"testing"
    }


```

## [#](<#response>) Response

Whenever you send a HTTP request, you expect a response back which contains a few components

### [#](<#response-status-code>) Response status code

The response status code is an important way to know whether your request to the API was good. `HTTP/1.1 200 OK`

### [#](<#response-headers>) Response headers

This is similar to request headers and contains metadata about the response body.

### [#](<#response-body>) Response body:

The response body is where the API sends the most of information in response to your request.
```ruby
 
    {
      "id":"1",
      "roomId":"1234",
      "roomType":"group",
      "text":"testing",
      "personId":"101",
      "personEmail":"[[email protected]](</cdn-cgi/l/email-protection>)",
      "created":"2017-03-26T13:28:22.131Z"
    }


```
