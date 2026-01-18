# Workato SDK Documentation

> **Source**: https://docs.workato.com/en/developing-connectors/sdk/guides/authentication/multi_auth.html
> **Fetched**: 2026-01-18T02:49:35.418925

---

# [#](<#how-to-guide-building-multiple-authentication-flows>) How-to Guide - Building multiple authentication flows

You may have to build multiple authentication (multi-auth) methods depending on the various use cases that you plan for your connector to support. For example, you can choose to support the OAuth2 Authorization Code Grant method that requires impersonation of a particular user during API authentication. You can also use API keys or client credentials for stable machine-to-machine authentication if you plan for your connector to support data orchestration use cases. However, it's important to note that Workato doesn't currently support runtime user connections for multi-auth connections.

To achieve multiple authentication flows, Workato's Connector SDK enables you to define segregated and isolated authentication flows within your connector.

AUTHENTICATION METHODS

This guide assumes you have basic knowledge of the other forms of authentication supported in Workato. Ensure you understand other basic forms of authentication in Workato such as [OAuth2](</developing-connectors/sdk/guides/authentication/oauth/auth-code.html>) and [API keys](</developing-connectors/sdk/guides/authentication/api-key.html>) as we reference them in this guide.

## [#](<#sample-connector-stripe>) Sample Connector - Stripe

To learn more about this connector, see [Stripe API Authentication (opens new window)](<https://stripe.com/docs/api/authentication>) documentation.
```ruby
 
    {
      title: 'Stripe',

      connection: {
        fields: [
          {
            name: "auth_type",
            control_type: "select",
            pick_list: [["OAuth2", "stripe_oauth2"], ["API Key", "stripe_api_key"]],
            extends_schema: true
          }
        ],
        authorization: {

          type: "multi",

          selected: lambda do |connection|
            connection["auth_type"]
          end,

          options: {
            stripe_oauth2: {
              type: "oauth2",

              fields: [
                { name: 'client_id' },
                { name: 'client_secret' },
              ],

              authorization_url: lambda do |connection|
                "https://connect.stripe.com/oauth/authorize?scope=read_write"
              end,

              token_url: lambda do
                "https://connect.stripe.com/oauth/token"
              end,

              apply: lambda do |_, access_token|
                headers("Authorization": "Bearer #{access_token}")
              end,
            },

            stripe_api_key: {
              type: "custom_auth",

              fields: [
                {
                  name: "api_key",
                }
              ],

              apply: lambda do |connection|
                headers("Authorization": "Bearer #{connection['api_key']}")
              end
            }
          },
        },

        base_uri: lambda do
           "https://api.stripe.com/"
        end
      },

      test: lambda do |connection|
        get('/v1/customers', limit: 1)
      end,

      #More connector code here
    }


```

## [#](<#build-a-connector-with-multiple-authentication-flows>) Build a connector with multiple authentication flows

Complete the following steps to build a connector with multiple authentication flows:

1

Define common connection fields

When planning for multiple authentication flows for the connector, start by deciding which fields are common across all authentication flows. This could be the API base url, or the target connector environment. Minimally, you must dedicate a field to selecting the authentication type that supports each connection scenario.

The example we use in this discussion, Stripe, has only the authentication type as a common connection field.

Authentication Type
    The authentication type from a defined picklist.  
Has the following important attributes 

Schema attribute
    `extends_schema: true` tells Workato to evaluate the connection schema again when the use changes the value of this field
Picklist values
    `stripe_oauth2` and `stripe_api_key`are important in the subsequent connector definition.

This is done in the `fields` key, which accepts an array of hashes. Each hash in this array corresponds to a separate input field.
```ruby
 
        fields: [
          {
            name: "auth_type",
            label: "Authentication Type",
            control_type: "select",
            pick_list: [["OAuth2", "stripe_oauth2"], ["API Key", "stripe_api_key"]],
            extends_schema: true
          }
        ]


```

2

Define the pathway to the selected authentication flow

This component informs Workato what to do with the values it receives from the input fields, and what authentication flow to use. It is implemented through the `authorization` key. Start by defining the `type` of authorization as `"multi"`.
```ruby
 
        authorization: {
          type: "multi",

          selected: lambda do |connection|
            connection["auth_type"]
          end,
        },


```

3

Define the various authentication flows

Define the multiple authentication flows within the `options` hash that contains all flows for your connector. Implement this through the `selected` lambda that receives the `connection` argument. This enables you to reference all connection inputs defined in `fields`, and expects a string value as the output.
```ruby
 
        authorization: {
          type: "multi",

          selected: lambda do |connection|
            connection["auth_type"]
          end,

          options: {
            stripe_oauth2: {
              type: "oauth2",

              fields: [
                { name: 'client_id' },
                { name: 'client_secret' },
              ],

              authorization_url: lambda do |connection|
                "https://connect.stripe.com/oauth/authorize?scope=read_write"
              end,

              token_url: lambda do
                "https://connect.stripe.com/oauth/token"
              end,

              apply: lambda do |_, access_token|
                headers("Authorization": "Bearer #{access_token}")
              end,
            },

            stripe_api_key: {
              type: "custom_auth",

              fields: [
                {
                  name: "api_key",
                }
              ],

              apply: lambda do |connection|
                headers("Authorization": "Bearer #{connection['api_key']}")
              end
            }
          },
        },


```

Each key in the `option` hash must correspond exactly to one possible output value of the `selected` lambda. In our case, you can see that the result value of `selected` can be either `stripe_oauth2` or `stripe_api_key`, because they are the only two possible options that we defined in the `auth_type` input field. This matches exactly to the keys you defined in the `options` hash.

Within each key, you can define further attributes for the authentication flows, such as `type`, `apply`, `acquire`, and others. This enables you to build specific authentication flows based on existing use cases. You can also define an additional key within each option as a nested `fields` array, to support the authentication flow for specific fields.

In our example, we define fields `client_id` and `client_secret` for OAuth2, and the field `api_key` for API key authentication. We also define all keys required for an OAuth2 flow within the `stripe_oauth2` hash, and all keys required for API key authentication in the `stripe_api_key` hash.

AUTHENTICATION TYPES

Multi-authentication supports multiple authentication flows and types. Refer to the [SDK authentication](</developing-connectors/sdk/guides/authentication.html>) guide for a complete list of authentication types.

CONVERT AN EXISTING CONNECTOR TO MULTI-AUTH

Use the `||` operator to specify the existing authentication method as the default when you add new authentication methods to an existing connector.

In the following example, the value left of the `||` operator, `auth_type`, is evaluated first. If the value is `nil` or `false`, the right value, `api_key`, is evaluated.
```ruby
 
    selected: lambda do |connection|
      connection["auth_type"] || 'api_key'
    end,


```

4

Set the API's base URI

The API's base URI instructs Workato on the base URL of the API. This key is optional; however, it enables you to provide relative-only paths in the rest of your connector definition through HTTP requests. Learn how to configure your [base URI](</developing-connectors/sdk/sdk-reference/connection.html#base-uri>).
```ruby
 
        base_uri: lambda do
           "https://api.stripe.com/"
        end


```

URI CONNECTION ARGUMENT

This lambda function has access to the `connection` argument. This is very useful when the base URI of the API changes depending on the user's instance. You can access the `connection` argument in the following format:
```ruby
 
        base_uri: lambda do |connection|
          #some code here
        end


```

Additionally, if the base URI changes with the authentication type, you can implement `IF-ELSE` structures to change it dynamically, as demonstrated in the following example:
```ruby
 
        base_uri: lambda do |connection|
          if connection['auth_type'] == "stripe_oauth2"
           "https://api.stripe.com/"
          else 
           "https://www.stripe.com/api" 
          end
        end


```

5

Test the connection

After defining the fields and the flows for each authentication option, you must test the new connection. Use the `test` key:
```ruby
 
      test: lambda do |connection|
        get('/customers', limit: 1)
      end,


```

The `test` key provides an endpoint for sending sample requests using the new credentials from the user. Successful connections get a `200 OK HTTP` response. In the preceding example above, a `GET` request to the `/api/channels` endpoint returns a `200` response when we have a valid API key.

## [#](<#connections-sdk-reference>) Connections SDK reference

For further information about the available keys within the `connection` key and their parameters, see the [SDK reference](</developing-connectors/sdk/sdk-reference/connection.html>).
