# Workato SDK Documentation

> **Source**: https://docs.workato.com/en/developing-connectors/sdk/cli/guides/cli/test.html
> **Fetched**: 2026-01-18T02:49:04.223574

---

# [#](<#how-to-guides-running-your-test-lambda-on-cli>) How-to guides - Running your test lambda on CLI

In this segment, we will run through how to run CLI commands for the test lambda function.

## [#](<#prerequisites>) Prerequisites

  * You have installed and can run the Workato SDK Gem. Read our [getting-started guide](</developing-connectors/sdk/cli/guides/getting-started.html>) to know more.
  * You have a connector with at least the authentication (connection key) and test lambda defined. You use the samples provided below.
  * You have a working set of credentials. If you are using a sample connector code, ensure that you have the appropriate credentials for the connector.

## [#](<#this-guide-will-walk-you-through-how-to>) This guide will walk you through how to:

  * Invoke the test lambda for simple auth scenarios

  * Simple auth scenarios include basic authentication, API key, or any similar forms. The threshold for this authentication is that the credentials the user supplies are all that is needed to authenticate. No additional follow-up steps are needed, such as retrieving an access token.

  * Invoke the test lambda for advanced auth scenarios

  * Advanced auth scenarios are when you use the input that the user has supplied to get another set of credentials later on. For example, if you're authenticating with OAuth 2.0 client credentials flow, when the user passes over a client ID and secret, you'd use these to get an access token in the `acquire:` lambda.

  * Invoke the test lambda for OAuth2 (Auth code grant) scenarios

  * If your type in the connection is set to `oauth2`.

## [#](<#why-you-should-run-the-test-lambda>) Why you should run the test lambda

This connection test lambda is run when the user first attempts to connect after they have supplied all the inputs for the connection, except for OAuth2 (Auth code grant) connections.

Additionally, all authentication types including OAuth 2 (Auth code grant) will invoke the test lambda to verify the connection is still valid when a recipe is first started.

Why OAuth2 does not require the test lambda on first connection

The OAuth2 (Auth code grant) connection is confirmed by Workato when a token is retrieved from the OAuth2 token endpoint. Once a valid token has been received from your authorization server, the connection is deemed valid. Thus, there is no need to run additional connection test.

## [#](<#invoking-the-test-lambda-for-simple-auth>) Invoking the test lambda for Simple Auth

### [#](<#sample-connector>) Sample connector

The code in `connector.rb`.
```ruby
 
    {
      title: 'Chargebee-demo',

      connection: {
        fields: [
          {
            name: 'api_key',
            control_type: 'password',
            hint: 'You can find your API key final change3' \
              "under 'Settings'=>'Configure Chargebee'=>'API Keys and Webhooks'" \
              " in Chargebee's web console.",
            label: 'Your API Key'
          },
          {
            name: 'domain',
            control_type: 'subdomain',
            url: 'chargebee.com'
          }
        ],

        authorization: {
          type: 'basic_auth',  

          apply: lambda do |connection|
            user(connection['api_key'])
          end
        },

        base_uri: lambda do |connection|
          "https://#{connection['domain']}.chargebee.com"
        end
      },

      test: lambda do |_connection|
        get('/api/v2/plans', limit: 1)
      end,
    }


```

Credentials in `settings.yaml.enc`.
```ruby
 
    api_key: valid_api_key
    domain: valid_domain


```

### [#](<#running-the-test-lambda>) Running the test lambda

When you run the command
```bash
 
    $ workato exec test


```

You get the output
```ruby
 
    {
      "list": [
        {
          "plan": {
            "id": "cool-product",
            "name": "cool product",
            "price": 10000,
            "period": 2,
            "period_unit": "week",
            "pricing_model": "flat_fee",
            "free_quantity": 0,
            "status": "active",
            "enabled_in_hosted_pages": true,
            "enabled_in_portal": false,
            "addon_applicability": "all",
            "is_shippable": false,
            "updated_at": 1630235299,
            "giftable": false,
            "resource_version": 1630235299389,
            "object": "plan",
            "charge_model": "flat_fee",
            "taxable": true,
            "currency_code": "SGD",
            "show_description_in_invoices": true,
            "show_description_in_quotes": false,
          }
        }
      ],
      "next_offset": "[\"10000\",\"487940\"]"
    }


```

This is the literal output of the `test` lambda we have defined but Workato relies not so much on the actual output, but that the request was executed successfully.

TIP

You can also use other options like `--verbose` to see the detailed logs of any HTTP requests sent when building your `output_fields` and `--output` to save the output of the function to a JSON file.

## [#](<#invoking-the-test-lambda-for-advanced-auth>) Invoking the test lambda for advanced Auth

### [#](<#sample-connector-advanced-auth>) Sample connector - advanced auth

The code in `connector.rb`.
```ruby
 
    {
        name: "Percolate",
        connection: {
          fields: [
            { name: "client_id",
              optional: false,
              hint: "To create client ID, the system admin or manager can click " \
              "<a href='https://percolate.com/app/settings/developer/apps/new' " \
              "target='_blank'>here</a> to register a new client application." },
            { name: "client_secret",
              control_type: "password",
              optional: false,
              hint: "To create client secret, the system admin or manager can click" \
              " <a href='https://percolate.com/app/settings/developer/apps/new' " \
              "target='_blank'>here</a> to register a new client application." },
            { name: "environment",
              optional: false,
              control_type: "select",
              pick_list: [%w[Production production], %w[Sandbox sandbox],
                          %w[Internal internal]] }
          ],

          authorization: {
            type: "custom_auth",

            acquire: lambda do |connection|
              hash = Base64.encode64("client:#{connection['client_id']}:#{connection['client_secret']}").gsub("\n", "")
              post("https://percolate.com/auth/v5/token/")
                .payload(grant_type: "client_credentials")
                .headers(Authorization: "Basic " + hash)
                .request_format_www_form_urlencoded
                .after_response do |_code, body, headers|
                  body["headers"] = headers
                  body
                end
            end,

            detect_on: [401, 403],

            refresh_on: [401, 403],

            apply: lambda do |connection|
              if current_url.include?("https://percolate.com")
                headers(Authorization: "Bearer #{connection['access_token']}")
              end
            end
          },

          base_uri: lambda do |_connection|
            "https://percolate.com"
          end
        },

        test: lambda do |_connection|
          get("/api/v5/me")
        end,
    }


```

Credentials in `settings.yaml.enc`.
```ruby
 
    client_id: valid_client_id
    client_secret: valid_client_secret
    environment: production


```

### [#](<#running-the-test-lambda-2>) Running the test lambda

When you run the command
```ruby
 
    workato exec test --verbose


```

You may get the output
```ruby
 
    SETTINGS
    {
      "client_id": "valid_client_id",
      "client_secret": "valid_client_secret",
      "environment": "production",
    }
    INPUT
    {
    }

    RestClient.get "https://percolate.com/api/v5/me", "Accept"=>"application/json", "Accept-Encoding"=>"gzip, deflate", "Authorization"=>"Bearer ", "User-Agent"=>"rest-client/2.0.2 (darwin19.6.0 x86_64) ruby/2.4.10p364"
    # => 401 Unauthorized | application/json 65 bytes         
    Progress: |=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=|
    RestClient.post "https://percolate.com/auth/v5/token/", "grant_type=client_credentials", "Accept"=>"application/json", "Accept-Encoding"=>"gzip, deflate", "Authorization"=>"Basic ", "Content-Length"=>"29", "Content-Type"=>"application/x-www-form-urlencoded", "User-Agent"=>"rest-client/2.0.2 (darwin19.6.0 x86_64) ruby/2.4.10p364"
    # => 200 OK | application/json 25 bytes                                       
    Progress: |=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=|

    Refresh token triggered on response "401 Unauthorized"
    Update settings file with new connection attributes? (Yes or No) 


```

First, the output indicates that there is no `access_token` in the settings file as the connection test lambda (`api/v5/me` endpoint) returned a `401` response.

This triggers the `acquire` lambda (`auth/v5/token` endpoint). The `acquire` lambda is `POST` api call to the authorization endpoint. When this happens the output of `acquire` block is then merged to the `connection` hash. This is the same behavior on the Workato platform where the `acquire` lambda is only invoked if the `refresh_on` signals.

The `refresh_on` attribute in the `acquire` lambda triggers if the current access token expires and will retrieve a new access token. This will trigger whenever you invoke the connection test lambda or any other lambdas.

Lastly, the Gem asks for permissions to override your settings file, which is synonymous with your `connection` hash on the Workato platform. If you type "Yes", the Gem will now update your settings file with the output of the `acquire` lambda.
```ruby
 
    Update settings file with new connection attributes? (Yes or No) Yes
    RestClient.get "https://percolate.com/api/v5/me", "Accept"=>"application/json", "Accept-Encoding"=>"gzip, deflate", "Authorization"=>"Bearer example_token", "User-Agent"=>"rest-client/2.0.2 (darwin19.6.0 x86_64) ruby/2.4.10p364"
    # => 200 OK | application/json 65 bytes         
    Progress: |=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=|

    OUTPUT
    # Output of the test lambda


```

Your credentials in `settings.yaml.enc` will be updated.
```ruby
 
    client_id: valid_client_id
    client_secret: valid_client_secret
    environment: production
    id: token:example_token
    expires_in: 2592000
    updated_at: '2021-08-30T14:54:35+00:00'
    user_id: user:130135
    grant_id: grant:1216779461986395763
    access_token: example_token
    token_type: bearer


```

## [#](<#invoking-the-test-lambda-for-oauth2-auth-code-grant-scenarios>) Invoking the test lambda for OAuth2 (Auth code grant) scenarios

For Auth code grant flows, the Workato Gem allows you to emulate the OAuth2 flow using the `workato oauth2` command. This behavior allows you to quickly debug and understand how the OAuth2 experience will look like for your end users.

### [#](<#sample-connector-oauth-2-connector>) Sample connector - OAuth 2 Connector

The code in `connector.rb`.
```ruby
 
    {
      title: 'TrackVia',
      connection: {
        fields: [
          {
            name: 'custom_domain',
            control_type: 'subdomain',
            label: 'TrackVia subdomain',
            hint: 'Enter your TrackVia subdomain. e.g. customdomain.trackvia.com. By default, <b>go.trackvia.com</b> will be used.',
            optional: 'true'
          },
          {
            name: 'account_id',
            control_type: :number,
            label: 'Account ID',
            hint: 'Specify the account to connect to',
            optional: true
          },
          {
            name: 'client_id',
            control_type: :text,
            label: 'TrackVia App Client ID',
            hint: 'Enter the Client ID of your own OAuth app registered on TrackVia',
            optional: 'false'
          },
          {
            name: 'client_secret',
            control_type: :text,
            label: 'TrackVia App Client secret',
            hint: 'Enter the Client secret of your own OAuth app registered on TrackVia',
            optional: 'false'
          }
        ],

        authorization: {
          type: 'oauth2',

          authorization_url: lambda { |connection|
            "https://#{connection['custom_domain'].presence || 'go.trackvia.com'}/oauth/authorize?response_type=code"
          },

          acquire: lambda do |connection, auth_code, redirect_uri|
            url = "https://#{connection['custom_domain'].presence || 'go.trackvia.com'}"
            response = post("#{url}/oauth/token").payload(
              redirect_uri: redirect_uri,
              grant_type: 'authorization_code',
              code: auth_code,
              client_id: connection['client_id'],
              client_secret: connection['client_secret']
            ).request_format_www_form_urlencoded
            user_key = get("#{url}/3scale/openapiapps").params(access_token: response['access_token']).dig(0, 'userKey')
            [
              response,
              nil,
              {
                user_key: user_key
              }
            ]
          end,

          refresh: lambda do |connection, refresh_token|
            url = "https://#{connection['custom_domain'].presence || 'go.trackvia.com'}"
            post("#{url}/oauth/token").payload(
              client_id: connection['client_id'],
              client_secret: connection['client_secret'],
              grant_type: 'refresh_token',
              refresh_token: refresh_token
            ).request_format_www_form_urlencoded
          end,

          refresh_on: [401, 403],

          apply: lambda { |connection, access_token|
            params(user_key: connection['user_key'])
            headers(Authorization: "Bearer #{access_token}")
            headers('account-id': connection['account_id']) if connection['account_id'].present?
          }
        },

        base_uri: lambda do |connection|
          if connection['custom_domain'].presence
            "https://#{connection['custom_domain']}/openapi/"
          else
            "https://go.trackvia.com/openapi/"
          end
        end
      },

      test: lambda do |connection|
        get('views') 
      end,
    }


```

Credentials in `settings.yaml.enc`.
```ruby
 
    client_id: valid_client_id
    client_secret: valid_client_secret


```

You can now run the following commands to go through the OAuth2 Authorization code flow which includes a browser popup. Include `--verbose` to enable detailed logging of the OAuth2 flow.
```ruby
 
    workato oauth2 --verbose


```

This will simulate the entire flow from the browser popup to the output url of the `authorization_url`, receiving the Auth Code to your callback url as well as subsequent calls contained in either your `token_url` lambda or your `acquire` lambda. Lastly, the flow will update your `settings.yaml` file with the latest set of credentials received from the OAuth2 flow.

![SDK Gem OAuth2 flow](/assets/img/SDK_gem_oauth2_flow.0ee6ffff.gif) _The SDK Gem emulates the OAuth2 flow on Workato_

At the end of the flow, you should have a `settings.yaml.enc` file that is updated with the latest credentials.
```ruby
 
    client_id: valid_client_id
    client_secret: valid_client_secret
    user_key: valid_user_key
    tokenType: bearer
    expires_in: 299
    expiration: '2021-10-19T15:36:39.221+0000'
    scope:
    - trust
    - read
    - write
    apiVersion: '22.18'
    access_token: valid_access_token
    refresh_token: valid_refresh_token


```

### [#](<#running-the-test-lambda-3>) Running the test lambda

Now after you've successfully gone through the flow, you may be use the same `workato exec test` command to verify you're applying your token properly in your requests!

Depending on when you received your token, you may also see a intermediary command from the Gem asking if you'd like to refresh your access tokens (if it has expired). This is done when HTTP requests are made which have a response that triggers the `refresh_on` block. Selecting yes would cause the Gem to update your settings file with the latest auth credentials.
```bash
 
    $ workato exec test --verbose


```

You may get the output
```ruby
 
    SETTINGS
    {
      "client_id": "valid_client_id",
      "client_secret": "valid_client_secret",
      "user_key": "valid_user_key",
      "tokenType": "bearer",
      "expires_in": "299",
      "expiration": "2021-10-19T15:36:39.221+0000",
      "scope": ["trust", "read", "write"],
      "apiVersion": "2.18",
      "access_token": "valid_access_token",
      "refresh_token": "valid_refresh_token"
    }
    INPUT
    {
    }

    RestClient.get "https://go.trackvia.com/openapi/views", "Accept"=>"application/json", "Accept-Encoding"=>"gzip, deflate", "Authorization"=>"Bearer valid_access_token", "User-Agent"=>"rest-client/2.0.2 (darwin19.6.0 x86_64) ruby/2.4.10p364"
    # => 401 Unauthorized | application/json 65 bytes         
    Progress: |=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=|
    RestClient.post "https://go.trackvia.com/oauth/token", "grant_type"=>"client_credentials", "Accept"=>"application/json", "Accept-Encoding"=>"gzip, deflate", "refresh_token"=>"valid_refresh_token", "Content-Length"=>"29", "Content-Type"=>"application/x-www-form-urlencoded", "User-Agent"=>"rest-client/2.0.2 (darwin19.6.0 x86_64) ruby/2.4.10p364"
    # => 200 OK | application/json 25 bytes                                       
    Progress: |=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=|

    Refresh token triggered on response "401 Unauthorized"
    Updated settings file with new connection attributes? (Yes or No) 


```

First, the output indicates that there is no valid `access_token` in the settings file as the connection test lambda (`openapi/views` endpoint) returned a `401` response. The access token may have expired.

This triggers the `acquire` lambda (`/oauth/token` endpoint). The `acquire` lambda is a `POST` api call to the authorization endpoint. When this happens the output of `acquire` block is then merged to the `connection` hash. This is the same behavior on the Workato platform where the `acquire` lambda is only invoked if the `refresh_on` signals.

The `refresh_on` attribute in the `acquire` lambda triggers if the current access token expires and will retrieve a new access token. This will trigger whenever you invoke the connection test lambda or any other lambdas.

Lastly, the Gem asks for permissions to override your settings file, which is synonymous with your `connection` hash on the Workato platform. If you type "Yes", the Gem will now update your settings file with the output of the `acquire` lambda.
```ruby
 
    Updated settings file with new connection attributes? (Yes or No) Yes
    RestClient.get "https://go.trackvia.com/openapi/views", "Accept"=>"application/json", "Accept-Encoding"=>"gzip, deflate", "Authorization"=>"Bearer new_valid_access_token", "User-Agent"=>"rest-client/2.0.2 (darwin19.6.0 x86_64) ruby/2.4.10p364"
    # => 200 OK | application/json 65 bytes                
    Progress: |=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=|

    OUTPUT
    # Output of the test lambda


```

Your credentials in `settings.yaml.enc` will be updated.
```ruby
 
    client_id: valid_client_id
    client_secret: valid_client_secret
    user_key: valid_user_key
    tokenType: bearer
    expires_in: 299
    expiration: '2021-10-19T15:41:39.221+0000'
    scope:
    - trust
    - read
    - write
    apiVersion: '22.18'
    access_token: new_valid_access_token
    refresh_token: new_valid_refresh_token


```

Note

You may also use `workato exec` to execute lambdas in your `authorization` hash like `acquire` and `refresh`. **That said, we highlight recommend you use`workato exec test` and `workato oauth2` which handle the updating of your `settings.yaml` file automatically.**
