# Workato SDK Documentation

> **Source**: https://docs.workato.com/en/developing-connectors/sdk/cli/guides/cli/pick_lists.html
> **Fetched**: 2026-01-18T02:49:02.911204

---

# [#](<#how-to-guides-running-picklists-on-cli>) How-to guides - Running Picklists on CLI

In this segment, we will be going through how you can run methods Picklists the Workato Gem.

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

      pick_lists: {

        static: lambda do
          [
            %w[Subscription subscription],
            %w[Customer customer],
            %w[Plans plan]
          ]
        end,

        dynamic: lambda do 
          get('/api/v2/customers')['list'].map do |index|
              [
                index['customer']['first_name'],
                index['customer']['id']
              ]
          end
        end,

        dependent: lambda do |connection, params|
          get('/api/v2/customers', params)['list'].map do |index|
              [
                index['customer']['first_name'],
                index['customer']['id']
              ]
          end
        end,

        dependent_with_names: lambda do |connection, limit:|
          get('/api/v2/customers', limit: limit)['list'].map do |index|
              [
                index['customer']['first_name'],
                index['customer']['id']
              ]
          end
        end

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

With the SDK Gem, you'll be able to invoke a picklist individually.

## [#](<#example-1-running-the-static-pick-list>) Example 1. Running the `static` pick_list

The first pick_list we will cover in the example above is the `static` pick_list. Like it's name suggests, it stores a static list of values and when invoked, will just return this value.

Here is an example the pick_list being run:
```bash
 
    $ workato exec pick_lists.static
    [
      [
        "Subscription",
        "subscription"
      ],
      [
        "Customer",
        "customer"
      ],
      [
        "Plans",
        "plan"
      ]
    ]


```

## [#](<#example-2-running-the-dynamic-pick-list>) Example 2. Running the `dynamic` pick_list

The next pick_list is one that sends a request out and massages the response into a pick_list format. Here, the connection settings required to authorize the request is assumed to be the default `settings.yaml.enc` file. If this is not what you want, you can use `--settings` to override this.

Here is an example the pick_list being run:
```bash
 
    $ workato exec pick_lists.dynamic
    [
      [
        "dd",
        "AzyuHzSiORQAo1JUb"
      ],
      [
        "fdsfdf",
        "16Bji8SfZHHDm7v"
      ]
    ]


```

## [#](<#example-3-running-the-dependent-pick-list>) Example 3. Running the `dependent` pick_list

The next pick_list is one that sends a request out and massages the response into a pick_list format. Here, the connection settings required to authorize the request is assumed to be the default `settings.yaml.enc` file. If this is not what you want, you can use `--settings` to override this.

In this case, the contents of the file `fixtures/pick_lists/dependent/input.json` contains
```ruby
 
    {
        "limit": "1"
    }


```

Here is an example the pick_list being run:
```bash
 
    $ workato exec pick_lists.dependent --args='fixtures/pick_lists/dependent/input.json' 
    [
      [
        "dd",
        "AzyuHzSiORQAo1JUb"
      ]
    ]


```

## [#](<#example-4-running-the-dependent-with-names-pick-lists>) Example 4. Running the `dependent_with_names` pick_lists

In other cases, you might have a picklist that accepts named arguments. In this case, this picklist has the named argument `limit:`.

When you pass the arguments via CLI, the contents of the file `fixtures/pick_lists/dependent_with_names/input.json` should look like this:
```ruby
 
    {
        "limit": "1"
    }


```

Here is an example the pick_list being run:
```bash
 
    $ workato exec pick_lists.dependent_with_names --args='fixtures/pick_lists/dependent_with_names/input.json' 
    [
      [
        "dd",
        "AzyuHzSiORQAo1JUb"
      ]
    ]


```
