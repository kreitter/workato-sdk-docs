# Workato SDK Documentation

> **Source**: https://docs.workato.com/en/developing-connectors/sdk/cli/guides/cli/actions.html
> **Fetched**: 2026-01-18T02:48:58.268618

---

# [#](<#how-to-guides-running-actions-on-cli>) How-to guides - Running actions on CLI

In this segment, we will be going through how you can run actions using the Workato Gem.

## [#](<#prerequisites>) Prerequisites

  * You have installed and can run the Workato SDK Gem. Read our [getting-started guide](</developing-connectors/sdk/cli/guides/getting-started.html>) to know more.
  * You have a working connector with at least 1 action. You use the sample connector provided below.
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

      actions: {

        search_customers: {
          title: 'Search customers',
          subtitle: 'Search for customers using name',
          description: 'Search customer in Chargebee',

          input_fields: lambda do |_object_definitions|
            [
              {
                name: 'name',
                label: 'Name to query by',
                hint: 'Provide the name of the customer to query'
              },
              {
                name: 'id',
                label: 'Name to query by',
                hint: 'Provide the name of the customer to query'
              }
            ]
          end,

          execute: lambda do |_connection, input, _input_schema, _output_schema|
            get('/api/v2/customers', input)
          end,

          output_fields: lambda do |_object_definitions|
            [
              {
                name: 'first_name'
              },
              {
                name: 'last_name'
              },
              {
                name: 'id'
              }
            ]
          end
        }

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

In this guide, we will be covering input_fields lambdas. You can run output_fields lambdas the same way.

TIP

Sometimes, you may find yourself with a sample payload request or response. You can also use the `workato generate schema` CLI command to convert this payload easily into Workato schema. Learn more about [Workato CLI generate schema](</developing-connectors/sdk/cli/reference/cli-commands.html#workato-generate-schema>).

Your input_fields lambda is expected to return Workato schema which corresponds to the input fields we should show to the user. In the case we have above, it simply returns the Workato schema stored within.
```bash
 
    $ workato exec actions.search_customers.input_fields 

    [  
      {
        "name": "name",
        "label": "Name to query by",
        "hint": "Provide the name of the customer to query"
      },
      {
        "name": 'limit',
        "hint": 'Total number of records to return'
      }
    ]


```

But you may also provide additional arguments when required. For example, if your input_fields is dependent on your `config_fields`, you would be required to pass `config_fields` for it to work. This can be done using something similar to below - where `customer_config.json` represents the `config_fields` argument of the lambda.
```bash
 
    $ workato exec actons.search_customers.input_fields --config-fields='fixtures/actions/search_customers/customer_config.json'


```

TIP

You can also use other options like `--verbose` to see the detailed logs of any HTTP requests sent when building your `input_fields` and `--output` to save the output of the function to a JSON file.

You do not need to pass anything for the object_definitions argument as the gem can reference it when it looks at your connector.

## [#](<#running-your-execute-lambda>) Running your execute lambda

Your execute lambda is expected to return a hash which represents the output of the action. In the case we have above, it returns response that Chargebee sends to us. You can see that we have referenced an `input` in the command which points to a JSON file stored in our `fixtures` folder. This file should contain the actual value passed to the `execute` lambda from the `input_fields`.

In this case, the contents of the file `fixtures/actions/search_customers/input.json` contains
```ruby
 
    {
      "name": "bennett",
      "limit": 1
    }


```

When we run the CLI command to run the `execute` lambda:
```bash
 
    $ workato exec actions.search_customers.execute --input='fixtures/actions/search_customers/input.json' --verbose

    SETTINGS
    {
      "api_key": "valid_api_key",
      "domain": "valid_domain"
    }
    INPUT
    {
      "name": "bennett",
      "limit": 1
    }

    RestClient.get "https://test.chargebee.com/api/v2/customers?limit=1&name=bennett", "Accept"=>"application/json", "Accept-Encoding"=>"gzip, deflate", "User-Agent"=>"rest-client/2.0.2 (darwin19.6.0 x86_64) ruby/2.4.10p364"
    # => 200 OK | application/json 753 bytes                                                                                
    Progress: |--=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=-|

    OUTPUT
    {
      "list": [
        {
          "customer": {
            "id": "abc",
            "first_name": "John",
            "last_name": "doe",
            "email": "[[email protected]](</cdn-cgi/l/email-protection>)",
            "phone": "+100",
            "auto_collection": "on",
            "net_term_days": 0,
            "allow_direct_debit": false,
            "created_at": 1630848839,
            "taxability": "taxable",
            "updated_at": 1630848840,
            "locale": "en-US",
            "pii_cleared": "active",
            "resource_version": 1630848840782,
            "deleted": false,
            "object": "customer",
            "card_status": "valid",
            "promotional_credits": 0,
            "refundable_credits": 0,
            "excess_payments": 0,
            "unbilled_charges": 0,
            "preferred_currency_code": "SGD",
          }
        }
      ],
      "next_offset": "[\"1630848839000\",\"42903379\"]"
    }


```

Note that we have used `--verbose` so the SDK gem has printed out more information including the API requests and responses.

The input for `connection` is assumed to be the `settings.yaml.enc` file and does not need to be declared unless you want to use a different settings.yaml file.

TIP

You can also use other options like `--output` to save the output of the function to a JSON file.

## [#](<#running-the-entire-action>) Running the entire action

Whilst running your execute lambda allows you to stub the `input` argument, often time, you also want to see how input passed to the input fields is then run through the action. For example, in cases where you may use schema attributes like `convert_input` and `convert_output` which do casting of data types.

For example, when a user gives you input for the above example where `limit` is provided as a string, you would need to convert this value to an integer.
```bash
 
    #fixtures/actions/search_customers/input.json
    {
      "name": "bennett",
      "limit": "1"
    }


```

This can be done with schema attributes like `convert_input` which takes this value and done the conversion.
```ruby
 
    [  
      {
        "name": "name",
        "label": "Name to query by",
        "hint": "Provide the name of the customer to query"
      },
      {
        "name": 'limit',
        "convert_input": "integer_conversion",
        "hint": "Total number of records to return"
      }
    ]


```

After transformation, your `input` argument to the `execute` lambda will look like this:
```ruby
 
    {
      "name": "bennett",
      "limit": 1
    }


```

TIP

When users provide static values or text values in input fields, you should assume they will be passed to your execute as strings. Using attributes like `convert_input` and `convert_output` allow you to do transformation of data even before it is presented as the `input` argument to your `execute` lambda.

Learn more about [converting input and converting output](</developing-connectors/sdk/sdk-reference/schema.html#using-convert-input-and-convert-output-for-easy-transformations>).

To test this transformation out that occurs from schema, when we have to run the CLI command to run the entire action:
```bash
 
    $ workato exec actions.search_customers --input='fixtures/actions/search_customers/input.json' --verbose

    SETTINGS
    {
      "api_key": "valid_api_key",
      "domain": "valid_domain"
    }
    INPUT
    {
      "name": "bennett",
      "limit": "1"
    }

    RestClient.get "https://test.chargebee.com/api/v2/customers?limit=1&name=bennett", "Accept"=>"application/json", "Accept-Encoding"=>"gzip, deflate", "User-Agent"=>"rest-client/2.0.2 (darwin19.6.0 x86_64) ruby/2.4.10p364"
    # => 200 OK | application/json 753 bytes                                                                                
    Progress: |--=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=---=-|

    OUTPUT
    {
      "list": [
        {
          "customer": {
            "id": "1",
            "first_name": "bennett",
            "last_name": "doe",
            "email": "[[email protected]](</cdn-cgi/l/email-protection>)",
            "phone": "+100",
            "auto_collection": "on",
            "net_term_days": 0,
            "allow_direct_debit": false,
            "created_at": 1630848839,
            "taxability": "taxable",
            "updated_at": 1630848840,
            "locale": "en-US",
            "pii_cleared": "active",
            "resource_version": 1630848840782,
            "deleted": false,
            "object": "customer",
            "card_status": "valid",
            "promotional_credits": 0,
            "refundable_credits": 0,
            "excess_payments": 0,
            "unbilled_charges": 0,
            "preferred_currency_code": "SGD",
          }
        }
      ],
      "next_offset": "[\"1630848839000\",\"42903379\"]"
    }


```
