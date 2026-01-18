# Workato SDK Documentation

> **Source**: https://docs.workato.com/en/developing-connectors/sdk/guides/authentication/oauth/ropc.html
> **Fetched**: 2026-01-18T02:49:39.939350

---

# [#](<#how-to-guide-oauth-2-0-resource-owner-password-credentials-authentication>) How-to Guide - OAuth 2.0 Resource owner password credentials authentication

The OAuth 2.0 resource owner password credentials flow is traditionally a server-to-server authentication method. This allows you to build a connector that can authenticate as the Workato server and communicate to your target API server. This flow allows the exchange of a user's username and password for an access token and, optionally, a refresh token.

## [#](<#sample-connector-microsoft-entra-id>) Sample Connector - Microsoft Entra ID
```ruby
 
    {
      title: 'My Azure connector',

      connection: {
        fields: [
          {
            name: 'tenant_id',
            optional: false,
          }
          {
            name: 'client_id',
            optional: false,
          },
          {
            name: 'client_secret',
            control_type: 'password',
            optional: false,
          },
          {
            name: 'username',
            optional: false,
          },
          {
            name: 'password',
            control_type: 'password',
            optional: false,
          }
        ],

        authorization: {
          type: 'custom_auth', #Set to custom_auth

          acquire: lambda do |connection|
            token_url = "https://login.microsoftonline.com/#{connection['tenant_id']}/oauth2/v2.0/token"
            response = post(token_url). 
                        payload(client_id: "#{connection['client_id']}",
                          client_secret: "#{connection['client_secret']}",
                          username: "#{connection['username']}",
                          password: "#{connection['password']}",
                          grant_type: "password").
                        request_format_www_form_urlencoded

            {
              access_token: response["access_token"],
            }
          end,

          refresh_on: 401,

          apply: lambda do |connection|
            headers("Authorization": "Bearer #{connection['access_token']}")
          end
        }

      },

      test: lambda do |connection|
        get( #Some accessible endpoint )
      end,

      #More connector code here
    }


```

## [#](<#step-1-defining-connection-fields>) Step 1 - Defining Connection fields

This component tells Workato what fields to show to a user trying to establish a connection. In the case of resource owner password credentials, you would need the Client ID and Client Secret that the user has generated in Azure. You will also need to provide the Username and Password of the user account that you will be using to authorize the connection.

Information needed | Description  
---|---  
Client ID | This is the public ID of the OAuth app that should be tied to Workato. This might mean signing Workato up as a verified application in the application  
Client secret | This is the matching private key that the API will verify along with the Client ID. This might mean signing Workato up as a verified application in the application. **Never share your client secret with others**  
Username | This is the username of the user account that is giving permission to authenticate the client.  
Password | This is the password of the user account that is giving permission to authenticate the client.  

This is done in the `fields` key, which accepts an array of hashes. Each hash in this array corresponds to a separate input field.
```ruby
 
        fields: [
          {
            name: 'tenant_id',
            optional: false,
          }
          {
            name: 'client_id',
            optional: false,
          },
          {
            name: 'client_secret',
            control_type: 'password',
            optional: false,
          },
          {
            name: 'username',
            optional: false,
          },
          {
            name: 'password',
            control_type: 'password',
            optional: false,
          }
        ],


```

![Configured Azure connection fields](/assets/img/azure_conn.578f7534.png)

TIP

When defining fields, you need to at least provide the `name` key. Additional attributes like `optional`, `hint` and `control_type` allow you to customize other aspects of these fields. For sensitive information like Client Secrets, remember to use the `control_type` as `password`.

To know more about how to define input fields in Workato, click [here.](</developing-connectors/sdk/sdk-reference/connection.html#fields>)

## [#](<#step-2-defining-the-authorization-type>) Step 2 - Defining the authorization type

This component tells Workato what type of authentication type this connection should use. This is handled through your `type` key in the `authorization` object. For Client Credentials authentication, you should use `custom_auth`.
```ruby
 
          type: 'custom_auth'


```

## [#](<#step-3-acquiring-the-access-token>) Step 3 - Acquiring the access token

In the `acquire` key, we pass in the `client_id`, `client_secret`, `username`, and `password` provided by users of connector as payload. Note that the payload of the request must be sent with `request_format_www_form_urlencoded`. We also identify `password` as the grant type and we pass this in as payload in the `POST` request. This request is then sent to Microsoft's Token URL.
```ruby
 
        acquire: lambda do |connection|
          response = post("https://login.microsoftonline.com/#{connection['tenant_id']}/oauth2/v2.0/token"). # Token URL
                        payload(client_id: "#{connection['client_id']}",
                          client_secret: "#{connection['client_secret']}",
                          username: "#{connection['username']}",
                          password: "#{connection['password']}",
                          grant_type: "password").
                        request_format_www_form_urlencoded

          {
            access_token: response["access_token"],
          }
        end,


```

Upon receiving a the request, the API returns a JSON response.
```ruby
 
    {
      "access_token": "my-authentication-token",
      "token_type": "bearer",
      "expires_in": "seconds-until-expiration",
      "error": "optional-error-message"
    }


```

The expected output of the `acquire` lambda function is a hash which is merged into the original connection hash. For example:
```bash
 
    # Original Connection hash
    {
      client_id: "abcd1234",
      client_secret: "secretClientSecret"
    }

    # After acquire block is executed
    {
      client_id: "abcd1234",
      client_secret: "secretClientSecret",
      access_token: "my-authentication-token"
    }


```

## [#](<#step-4-applying-the-access-token-to-subsequent-http-requests>) Step 4 - Applying the access token to subsequent HTTP requests

Next, you need to tell Workato how to make use of the access token it has retrieved from Microsoft. This is done in the `apply` key where you can reference the access token now stored in the `connection` argument. Any instructions you introduce in the `apply` block are subsequently applied to all HTTP requests this connector sends after connection is established.
```ruby
 
        apply: lambda do |connection|
          headers("Authorization": "Bearer #{connection['access_token']}")
        end


```

In this example, we have defined the access token (`connection['access_token']`) to be added to the headers of any request. For every HTTP request sent, the headers will contain `Authorization: Bearer XXX` where `XXX` is the access token stored in the `connection` hash.

## [#](<#step-5-setting-the-api-s-base-uri>) Step 5 - Setting the API's base URI

This component tells Workato what the base URL of the API is. This key is optional but allows you to provide only relative paths in the rest of your connector when defining HTTP requests. Learn how to configure your `base_uri` [here](</developing-connectors/sdk/sdk-reference/connection.html#base-uri>).

TIP

This lambda function also has access to the `connection` argument. This is especially useful if the base URI of the API might change based on the user's instance. The `connection` argument can be accessed in the following format:
```ruby
 
        base_uri: lambda do |connection|
          #some code here
        end


```

## [#](<#step-6-testing-the-connection>) Step 6 - Testing the connection

Now that we have defined the fields we need to collect from an end user and what to do with the inputs from those fields, we now need a way to test this connection. This is handled in the `test` key.
```ruby
 
        test: lambda do
          get(# Some accessible code)
        end,


```

In this key, you need to provide an endpoint that allows us to send a sample request using the new credentials we just received. If we receive a 200 OK HTTP response, we show the connection as Successful.

## [#](<#connections-sdk-reference>) Connections SDK reference

To be more familiar with the available keys within the `connection` key and their parameters, check out our [SDK reference](</developing-connectors/sdk/sdk-reference/connection.html>).
