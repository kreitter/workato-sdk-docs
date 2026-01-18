# Workato SDK Documentation

> **Source**: https://docs.workato.com/en/developing-connectors/sdk/cli/guides/cli/methods.html
> **Fetched**: 2026-01-18T02:49:00.534576

---

# [#](<#how-to-guides-running-methods-on-cli>) How-to guides - Running methods on CLI

In this segment, we will be going through how you can run methods using the Workato Gem.

## [#](<#prerequisites>) Prerequisites

  * You have installed and can run the Workato SDK Gem. Read our [getting-started guide](</developing-connectors/sdk/cli/guides/getting-started.html>) to know more.
  * You have a working connector with at least 1 method. You use the sample connector provided below.
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

      methods: {
        get_customers: lambda do
          get('/api/v2/customers')
        end,

        sample_method: lambda do |string1, string2|
          string1 + ' ' + string2
        end,
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

With the SDK Gem, you'll be able to invoke a method individually and gain greater control over how each method works.

## [#](<#example-1-running-the-get-customers-method>) Example 1. Running the `get_customers` method

The first method we will cover in the example above is the `get_customers` method, which does not have any declared input arguments. When this method is invoked with the SDK Gem, we expect the method to fetch customers and return the response from the API call
```bash
 
    $ workato exec methods.get_customers
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

TIP

You can also use other options like `--verbose` to see the detailed logs of any HTTP requests sent when your method is ran and `--output` to save the output of the function to a JSON file.

If no `settings.yaml` file is defined, the SDK Gem will assume the default `settings.yaml.enc` file to utilize for any HTTP requests.

## [#](<#example-2-running-the-sample-method-method>) Example 2. Running the `sample_method` method

The second method we will cover in the example above is the `sample_method` method, which has 2 arguments. You can see that we have referenced an `args` in the command which points to a JSON file stored in our `fixtures` folder. This file should contain an array **where each index in the array corresponds to a single argument.**

In this case, the contents of the file `fixtures/triggers/new_updated_object/customer_input_poll.json` contains
```ruby
 
    [
        "Hello",
        "world"
    ]


```

Here is an example the method being run:
```bash
 
    $ workato exec methods.sample_method --args='fixtures/actions/search_customers/customer_config.json' 
    "Hello world"


```

TIP

You can also use other options like `--verbose` to see the detailed logs of any HTTP requests sent when your method is ran and `--output` to save the output of the function to a JSON file.

If no `settings.yaml` file is defined, the SDK Gem will assume the default `settings.yaml.enc` file to utilize for any HTTP requests.
