# Workato SDK Documentation

> **Source**: https://docs.workato.com/en/developing-connectors/sdk/guides/authentication/basic-authentication.html
> **Fetched**: 2026-05-24T03:11:24.369691

---

[Connector SDK](</en/developing-connectors/sdk>)

[How-to guides](</en/developing-connectors/sdk/guides>)

[API authorization](</en/developing-connectors/sdk/guides/authentication>)

# How-to Guide - Basic Authentication [​](<#how-to-guide-basic-authentication>)

Typically, a basic authentication requires a username and password combination when making requests. Make sure to include those two fields in the connection fields definition.

## Sample Connector - ClickTime [​](<#sample-connector-clicktime>)

ruby
```ruby

    {
      title: 'ClickTime',

      connection: {
        fields: [
          {
            name: 'username',
            optional: true,
            hint: 'Your email used for login'
          },
          {
            name: 'password',
            control_type: 'password',
          }
        ],

        authorization: {
          type: 'basic_auth',

          apply: lambda do |connection|
            user(connection['username'])
            password(connection['password'])
          end
        },

        base_uri: lambda do |connection|
          "https://app.clicktime.com"
        end
      },

      test: lambda do |connection|
        get("/api/1.3/session")
      end

      #More connector code here
    }

```

  * Refer to the [full ClickTime connector code](<https://github.com/workato/custom_connector_docs/blob/master/custom_connectors/basic_auth/click_time_connector.rb>) for a complete example.
  * Check out the [ClickTime API](<https://support.clicktime.com/hc/en-us/articles/360002884071-REST-API-v2-General-Information#basic>)

## Step 1 - Defining Connection fields [​](<#step-1-defining-connection-fields>)

This component tells Workato what fields to show to a user trying to establish a connection. In the case of Basic Authentication, you would need the `username` and `password` of the end user to establish a connection.

Information from User| Description  
---|---  
username| The username of the individual who will authenticate the connection.  
password| The password of the individual who will authenticate the connection.  

This is done in the `fields` key, which accepts an array of hashes. Each hash in this array corresponds to a separate input field.

ruby
```ruby

        fields: [
          {
            name: 'username',
            optional: true,
            hint: 'Your email used for login'
          },
          {
            name: 'password',
            control_type: 'password',
          }
        ],

```

![Configured ClickTime connection fields](/assets/clicktime_conn.BG1KzMy5.png)

TIP

When defining fields, you need to at least provide the `name` key. Additional attributes like `optional`, `hint` and `control_type` allow you to customize other aspects of these fields. For sensitive information like Client Secrets, remember to use the `control_type` as `password`.

Refer to [Connection fields](</developing-connectors/sdk/sdk-reference/connection#fields>) for more information on defining input fields in Workato.

## Step 2 - Defining authorization [​](<#step-2-defining-authorization>)

This component tells Workato what to do with the values received from the input fields to establish a connection. This is handled through your `authorization` key. In this key, you begin by first defining the `type` of authorization. For Basic authentication, you should use `basic_auth`.

ruby
```ruby

        authorization: {
          type: 'basic_auth',

          apply: lambda do |connection|
            user(connection['username'])
            password(connection['password'])
          end
        }

```

## Step 3 - Applying the credentials to subsequent HTTP requests [​](<#step-3-applying-the-credentials-to-subsequent-http-requests>)

Next, you need to tell Workato how to make use of the username and password you expect to receive from a user of this connector. This is done in the `apply` key where you can reference the username and password collected through the `connection` argument. Any instructions you introduce in the `apply` key are subsequently applied to all HTTP requests this connector sends after connection is established.

In this example, we have defined the username we received (`connection['username']`) to be added to the `user` field of any request. The same has been done for the password (`connection['password']`) to be added to the `password` field of any request.

## Step 4 - Setting the API's base URI [​](<#step-4-setting-the-api-s-base-uri>)

This component tells Workato what the base URL of the API is. This key is optional but allows you to provide only relative paths in the rest of your connector when defining HTTP requests. Refer to [base URI configuration](</developing-connectors/sdk/sdk-reference/connection#base-uri>) for more information on configuring your `base_uri`.

ruby
```ruby

        base_uri: lambda do |connection|
          "https://app.clicktime.com"
        end

```

TIP

This lambda function also has access to the `connection` argument. This is especially useful if the base URI of the API might change based on the user's instance. The `connection` argument can be accessed in the following format:

ruby
```ruby

        base_uri: lambda do |connection|
          "https://#{connection['domain']}.com/api"
        end

```

## Step 5 - Testing the connection [​](<#step-5-testing-the-connection>)

Now that we have defined the fields we need to collect from an end user and what to do with the inputs from those fields, we now need a way to test this connection. This is handled in the `test` key. Take note that this is a root level key - outside of the `connection` definition.

ruby
```ruby

        test: lambda do |connection|
          get("/api/1.3/session")
        end

```

In this key, you need to provide an endpoint that allows us to send a sample request using the new credentials we just received. If we receive a 200 OK HTTP response, we show the connection as Successful. In the example above, we are sending a `GET` request to the `/api/1.3/session` endpoint and expecting a 200 response if the username and password provided are valid.

## Connections SDK reference [​](<#connections-sdk-reference>)

To be more familiar with the available keys within the `connection` key and their parameters, check out our [SDK reference](</developing-connectors/sdk/sdk-reference/connection>).

**Last updated:**
