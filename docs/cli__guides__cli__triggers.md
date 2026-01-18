# Workato SDK Documentation

> **Source**: https://docs.workato.com/en/developing-connectors/sdk/cli/guides/cli/triggers.html
> **Fetched**: 2026-01-18T02:49:05.458577

---

# [#](<#how-to-guides-running-triggers-on-cli>) How-to guides - Running Triggers on CLI

In this segment, we will be going through how you can run triggers using the Workato Gem.

## [#](<#prerequisites>) Prerequisites

  * You have installed and can run the Workato SDK Gem. Read our [getting-started guide](</developing-connectors/sdk/cli/guides/getting-started.html>) to know more.
  * You have a working connector with at least 1 trigger. You use the sample provided below.
  * You have a working set of credentials. If you are using a sample connector code, ensure that you have the appropriate credentials for the connector.

## [#](<#sample-connector-chargebee>) Sample connector - Chargebee

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

      triggers: {
        new_updated_object: {

          description: lambda do |_input, picklist_label|
            "New/updated <span class='provider'>#{picklist_label['object'] || 'object'}</span> in <span class='provider'>Chargebee</span>"
          end,

          config_fields: [
            {
              name: 'object',
              control_type: 'select',
              pick_list: 'objects',
              optional: false
            }
          ],

          input_fields: lambda do
            [
              {
                name: 'since',
                type: :date_time,
                optional: true, 
                sticky: true
              }
            ]
          end,

          poll: lambda do |_connection, input, closure|
            page_size = 100
            closure = {} if closure.blank?
            closure['updated_since'] = (closure['updated_since'] || input['since'] || 1.hour.ago).to_time.utc.to_i

            params = {
              "sort_by[asc]": 'updated_at',
              limit: page_size,
              "updated_at[after]": closure['updated_since']
            }

            params['offset'] = closure['offset']

            response = get("/api/v2/#{input['object'].pluralize}", params)

            if response['next_offset'].present?
              closure['offset'] = response['next_offset']
            else
              closure['offset'] = nil
              unless response['list'].size == 0
                closure['updated_since'] =
                  response['list'].last[input['object']]['updated_at']
              end
            end

            {
              events: response['list'],
              next_poll: closure,
              can_poll_more: response['next_offset'].present?
            }
          end,

          dedup: lambda do |event|
            if event['subscription'].present?
              "#{event['subscription']['id']}@#{event['subscription']['updated_at']}"
            else
              "#{event['customer']['id']}@#{event['customer']['updated_at']}"
            end
          end,

          output_fields: lambda do |object_definitions|
            object_definitions['new_updated_object_output']
          end
        },

      },
    }


```

Credentials in `settings.yaml.enc` .
```ruby
 
    api_key: valid_api_key
    domain: valid_domain


```

TIP

If you're using an encrypted settings.yaml file, you will need to use `workato edit <PATH>` to edit or create the file. Find out more [here](</developing-connectors/sdk/cli/reference/cli-commands#workato-edit>)

With the SDK Gem, you'll be able to invoke individual lambda functions in your action and gain greater control over how each part of your action works. For example, you may run your `execute` lambda function independently from your `input_fields` lambda.

## [#](<#running-your-input-fields-and-output-fields-lambdas>) Running your input fields and output fields lambdas

In this guide, we will be covering output_fields lambdas. You can run input_fields lambdas the same way.

TIP

Sometimes, you may find yourself with a sample payload request or response. You can also use the `workato generate schema` CLI command to convert this payload easily into Workato schema. Learn more about [Workato CLI generate schema](</developing-connectors/sdk/cli/reference/cli-commands#workato-generate-schema>).

Your output_fields lambda is expected to return Workato schema which corresponds to the input fields we should show to the user. In the case we have above, when you invoke the `output_fields` lambda, the Gem will handle the evaluation of any downstream `object_definitions` or `methods` you have referenced.
```bash
 
    $ workato exec triggers.new_updated_object.output_fields --config-fields='fixtures/triggers/new_updated_object/customer_config.json'

    [
      {
        "name": "customer",
        "type": "object",
        "properties": [
          {
            "control_type": "text",
            "label": "ID",
            "type": "string",
            "name": "id"
          },
          # More Schema here
        ]
      }
    ]


```

TIP

You can also use other options like `--verbose` to see the detailed logs of any HTTP requests sent when building your `output_fields` and `--output` to save the output of the function to a JSON file.

You do not need to pass anything for the object_definitions argument as the gem can reference it when it looks at your connector.

## [#](<#running-your-poll-lambda>) Running your poll lambda

Your poll lambda is expected to return a hash which represents the output of the poll lambda. You have two ways to run your poll lambda to test functionality.

  1. [Running your poll lambda with pagination](<#running-your-poll-lambda-with-pagination>)
  2. [Running your poll lambda without pagination](<#running-your-poll-lambda-without-pagination>)

### [#](<#running-your-poll-lambda-with-pagination>) Running your poll lambda with pagination

This is done with the command `.poll` which tells the SDK Gem to paginate through all records if `can_poll_more` is true. In the example below, you can see that we have given `.poll` and given the `since` input of `6/09/2021`. The SDK Gem would then send as many requests as necessary to simulate the polling mechanism. You can see that we have referenced an `input` in the command which points to a JSON file stored in our `fixtures` folder. This file should contain the actual value passed to the `poll` lambda from the `input_fields` and `config_fields`.

In this case, the contents of the file `fixtures/triggers/new_updated_object/customer_input_poll.json` contains
```ruby
 
    {
      "object": "customer",
      "since": "6/09/2021"
    }


```
```bash

    $ workato exec triggers.new_updated_object.poll --input='fixtures/triggers/new_updated_object/customer_input_poll.json' --verbose

    SETTINGS
    {
      "api_key": "valid_api_key",
      "domain": "valid_domain"
    }
    INPUT
    {
      "object": "customer",
      "since": "6/09/2021"
    }

    RestClient.get "https://live_Zbaoo7hGqvi3cqrza8WiXxQa8kBPAPQF@empressporridge.chargebee.com/api/v2/customers?limit=10&offset=&sort_by%5Basc%5D=updated_at&updated_at%5Bafter%5D=1630857600", "Accept"=>"application/json", "Accept-Encoding"=>"gzip, deflate", "User-Agent"=>"rest-client/2.0.2 (darwin19.6.0 x86_64) ruby/2.4.10p364"
    # => 200 OK | application/json 2608 bytes                                                                                           
    RestClient.get "https://live_Zbaoo7hGqvi3cqrza8WiXxQa8kBPAPQF@empressporridge.chargebee.com/api/v2/customers?limit=10&offset=%5B%221630857607410%22%2C%2240736845%22%5D&sort_by%5Basc%5D=updated_at&updated_at%5Bafter%5D=1630857600", "Accept"=>"application/json", "Accept-Encoding"=>"gzip, deflate", "User-Agent"=>"rest-client/2.0.2 (darwin19.6.0 x86_64) ruby/2.4.10p364"
    # => 200 OK | application/json 1800 bytes                                                                                           
    Progress: |=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---|

    OUTPUT
    {
      "events": [
        {
          "customer": {
            "id": "abc",
            "first_name": "John",
            "last_name": "Doe",
            "email": "[[email protected]](</cdn-cgi/l/email-protection>)",
            "phone": "+100",
            "auto_collection": "on",
            "net_term_days": 0,
            "allow_direct_debit": false,
            "created_at": 1629814951,
            "taxability": "taxable",
            "updated_at": 1630857613,
            "locale": "en-SG",
            "pii_cleared": "active",
            "resource_version": 1630857613348,
            "deleted": false,
            "object": "customer",
            "card_status": "valid",
            "promotional_credits": 0,
            "refundable_credits": 0,
            "excess_payments": 0,
            "unbilled_charges": 0,
            "preferred_currency_code": "SGD",
          },
        },
        # More customers here
      ],
      "can_poll_more": false,
      "next_poll": {
        "updated_since": 1630857613,
        "offset": null
      }
    }


```

Note that we have used `--verbose` so the SDK gem has printed out more information including the API requests and responses.

TIP

You can also use other options like `--output` to save the output of the function to a JSON file.

You can see that the `config_field` \- `object` is passed in the input json. In Workato, config_fields are merged with normal `input_fields` when received in the `execute`, `poll` or `webhook` lambdas.

### [#](<#running-your-poll-lambda-without-pagination>) Running your poll lambda without pagination

This is done with the command `.poll_page` which tells the SDK Gem to only invoke the `poll` lambda once regardless of the `can_poll_more` value. In the example below, you can see that we have given `.poll` and given the `since` input of `6/09/2021`. The SDK Gem sends a single request and stops execution after the first request is done.
```ruby
 
    workato exec triggers.new_updated_object.poll_page --input='fixtures/triggers/new_updated_object/customer_input_poll.json' --verbose

    SETTINGS
    {
      "api_key": "valid_api_key",
      "domain": "valid_domain"
    }
    INPUT
    {
      "object": "customer",
      "since": "6/09/2021"
    }

    RestClient.get "https://live_Zbaoo7hGqvi3cqrza8WiXxQa8kBPAPQF@empressporridge.chargebee.com/api/v2/customers?limit=10&offset=&sort_by%5Basc%5D=updated_at&updated_at%5Bafter%5D=1630857600", "Accept"=>"application/json", "Accept-Encoding"=>"gzip, deflate", "User-Agent"=>"rest-client/2.0.2 (darwin19.6.0 x86_64) ruby/2.4.10p364"
    # => 200 OK | application/json 2608 bytes 

    Progress: |=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---|

    OUTPUT
    {
      "events": [
        {
          "customer": {
            "id": "abc",
            "first_name": "John",
            "last_name": "Doe",
            "email": "[[email protected]](</cdn-cgi/l/email-protection>)",
            "phone": "+100",
            "auto_collection": "on",
            "net_term_days": 0,
            "allow_direct_debit": false,
            "created_at": 1629814951,
            "taxability": "taxable",
            "updated_at": 1630857613,
            "locale": "en-SG",
            "pii_cleared": "active",
            "resource_version": 1630857613348,
            "deleted": false,
            "object": "customer",
            "card_status": "valid",
            "promotional_credits": 0,
            "refundable_credits": 0,
            "excess_payments": 0,
            "unbilled_charges": 0,
            "preferred_currency_code": "SGD",
          },
        },
        # More customers here
      ],
      "next_poll": {
        "updated_since": 1630857600,
        "offset": "[\"1630857607410\",\"40736845\"]"
      },
      "can_poll_more": true
    }


```

Note that we have used `--verbose` so the SDK gem has printed out more information including the API requests and responses.

TIP

You can also use other options like `--output` to save the output of the function to a JSON file.

You can see that the `config_field` \- `object` is passed in the input json. In Workato, config_fields are merged with normal `input_fields` when received in the `execute`, `poll` or `webhook` lambdas.
