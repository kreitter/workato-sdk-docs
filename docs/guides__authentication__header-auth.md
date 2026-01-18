# Workato SDK Documentation

> **Source**: https://docs.workato.com/en/developing-connectors/sdk/guides/authentication/header-auth.html
> **Fetched**: 2026-01-18T02:49:33.113493

---

# [#](<#how-to-guides-header-authentication>) How-to Guides - Header Authentication

For APIs requiring header authentication, this can be easily accomplished if the token is supplied by the user directly through user input fields.

## [#](<#sample-connector-generic-connector>) Sample connector - Generic connector
```ruby
 
    {
      title: 'My connector',

      connection: {

        fields: [
          {
            name: "token",
            control_type: "string",
            label: "Bearer token",
            optional: false,
            hint: "Available in 'My Profile' page"
          }
        ],

        authorization: {
          type: 'custom_auth',

          apply: lambda do |connection|
            headers("Authorization": "Bearer #{connection["token"]}")
          end
        },

        base_uri: lambda do |connection|
          "https://api.acmestudios.com"
        end
      },

      test: lambda do |connection|
        get('/me')
      end,
    }


```

## [#](<#step-1-defining-connection-fields>) Step 1 - Defining Connection fields

In the `connection` key, we define the input fields in the `fields` key in an array of hashes. Each hash in the array represents a single input field. Inside, we will be able to declare the name of the input field, hints that are displayed to the end user among other parameters. In our example, we define the 'token' input fields.

TIP

When defining fields, you need to at least provide the `name` key. Additional attributes like `optional`, `hint` and `control_type` allow you to customize other aspects of these fields. For sensitive information like Client Secrets, remember to use the `control_type` as `password`.

To know more about how to define input fields in Workato, click [here.](</developing-connectors/sdk/sdk-reference/connection.html#fields>)

## [#](<#step-2-applying-the-token-to-subsequent-http-requests>) Step 2 - Applying the token to subsequent HTTP requests

In the `apply` key, we pass in the token provided by the user in `header()` in the from of a key-value pair. By doing so, Workato will append the token to every HTTP request made by the connector to help authenticate each request.

## [#](<#step-3-setting-the-api-s-base-uri>) Step 3 - Setting the API's base URI

This component tells Workato what the base URL of the API is. This key is optional but allows you to provide only relative paths in the rest of your connector when defining HTTP requests. Learn how to configure your `base_uri` [here](</developing-connectors/sdk/sdk-reference/connection.html#base-uri>).
```ruby
 
        base_uri: lambda do |connection|
          "https://api.acmestudios.com"
        end


```

TIP

This lambda function also has access to the `connection` argument. This is especially useful if the base URI of the API might change based on the user's instance. The `connection` argument can be accessed in the following format:
```ruby
 
        base_uri: lambda do |connection|
          "https://#{connection['domain'].com/api}"
        end


```

## [#](<#step-4-testing-the-connection>) Step 4 - Testing the connection

Now that we have defined the fields we need to collect from an end user and what to do with the inputs from those fields, we now need a way to test this connection. This is handled in the `test` key.
```ruby
 
        test: lambda do |connection|
          get("/me")
        end


```

In this block, you need to provide an endpoint that allows us to send a sample request using the new credentials we just received. If we receive a 200 OK HTTP response, we show the connection as Successful. In the example above, we are sending a `GET` request to an example endpoint `/me` and expecting a 200 response if the token is valid.

## [#](<#connections-sdk-reference>) Connections SDK reference

To be more familiar with the available keys within the `connection` key and their parameters, check out our [SDK reference](</developing-connectors/sdk/sdk-reference/connection.html>).
