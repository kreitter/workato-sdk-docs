# Workato SDK Documentation

> **Source**: https://docs.workato.com/en/developing-connectors/sdk/cli/guides/rspec/writing_tests.html
> **Fetched**: 2026-01-18T02:49:13.483086

---

# [#](<#how-to-guides-writing-tests-for-triggers-actions>) How-to guides - Writing tests for triggers/actions

In this segment, we will be going through how you can write tests for any lambda in your connector. For this, we will be writing tests for a single action's execute lambda. The same logic can be applied to the rest of the lambdas as well.

## [#](<#sample-connector>) Sample connector

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

        base_uri: lambda do |connect|
          "https://#{connect['domain']}.chargebee.com"
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

## [#](<#generating-your-tests>) Generating your tests

You can create a separate spec file for each action or generate your tests based on your connector by using the `workato generate test` command. This will generate a spec file which will include most of the necessary stubs for your to start writing tests.

### [#](<#sample-rspec-contents>) Sample RSpec contents
```ruby
 
    RSpec.describe 'actions/search_customers', :vcr do

      subject(:output) { connector.actions.search_customers(input) }

      let(:connector) { Workato::Connector::Sdk::Connector.from_file('connector.rb', settings) }
      let(:settings) { Workato::Connector::Sdk::Settings.from_default_file }
      let(:input) { JSON.parse(File.read('fixtures/actions/search_customers/input.json')) }

      let(:expected_output) { JSON.parse(File.read('fixtures/actions/search_customers/output.json')) }

      describe 'given valid input' do
        it 'gives expected output' do
          expect(output).to eq(expected_output)
        end
      end

      let(:action) { connector.actions.search_customers }

      describe 'execute' do
        subject(:output) { action.execute(settings, input) }
        let(:input) { JSON.parse(File.read('fixtures/actions/search_customers/input_parsed.json')) }
        let(:expected_output) { JSON.parse(File.read('fixtures/actions/search_customers/output.json')) }

        context 'given valid input' do
          it 'gives expected output' do
            expect(output).to eq(expected_output)
          end
        end
      end

      describe 'sample_output' do
        subject(:sample_output) { action.sample_output(settings, input) }

        pending 'add some examples'
      end

      describe 'input_fields' do
        subject(:input_fields) { action.input_fields(settings, config_fields) }

        pending 'add some examples'
      end

      describe 'output_fields' do
        subject(:output_fields) { action.output_fields(settings, config_fields) }

        pending 'add some examples'
      end
    end


```

Here, you can see that we have stubs for various tests for this action. This is given when you generate tests using the Gem. We will be going through how to write tests for just the `execute` lambda.

## [#](<#step-1-define-your-connector-instance>) Step 1 - Define your connector instance

To begin testing, you need to use the Workato SDK Gem to create an instance of your connector.
```ruby
 
      let(:connector) { Workato::Connector::Sdk::Connector.from_file('connector.rb', settings) }


```

## [#](<#step-2-define-your-settings-instance>) Step 2 - Define your settings instance

Next, you need to use the Workato SDK Gem to create an instance of your settings. This is synonymous with your connection on Workato. Take note that, your connector instance previously defined also uses this settings instance.
```ruby
 
      let(:settings) { Workato::Connector::Sdk::Settings.from_default_file }


```

## [#](<#step-3-define-your-action>) Step 3 - Define your action

After creating the related instances, we instantiate the `action` so we can reference it more easily in the rest of the tests.
```ruby
 
      let(:action) { connector.actions.search_customers }


```

## [#](<#step-3-describe-your-tests-and-define-your-subject>) Step 3 - Describe your tests and define your subject

Here, we describe the "family" of tests we are hoping to run. In this case, we use the keyword `execute`. After that, we also define a `subject` of our tests. This is where we assign the value of `output` to our connector instance running the `execute` lambda of the `search_customers` action. This is done with the `action.execute(settings,input)` defined.
```ruby
 
      describe 'execute' do
        subject(:output) { action.execute(settings, input) }


```

TIP

When you generate tests, you might be curious why you have 2 additional arguments for `execute` which are `extended_input_schema` and `extended_output_schema`. Similar to the `execute:` lambda when you define it in your connector, the `execute` here can accept the same 4 arguments. We've removed them for this action as they weren't needed.

## [#](<#step-4-declare-your-assertions-for-individual-tests>) Step 4 - Declare your assertions for individual tests

For a test to pass or fail, there needs to be a declared comparison.

Over here, we are declaring that we "expect" the output of the `execute` lambda to be equals to a previously known response where we gave it a valid input. This was done by creating 2 new variables, `input` and `expected_output`. Generating `expected_output` doesn't need to be done manually but can be done when you run the CLI commands to invoke the `execute` lambda. For example, `workato exec actions.search_customers.execute --input='fixtures/actions/search_customers/input.json' --output='fixtures/actions/search_customers/output.json'`.
```ruby
 
      describe 'execute' do
        subject(:output) { action.execute(settings, input) }
        let(:input) { JSON.parse(File.read('fixtures/actions/search_customers/input.json')) }
        let(:expected_output) { JSON.parse(File.read('fixtures/actions/search_customers/output.json')) }

        context 'given valid input' do
          it 'gives expected output' do
            expect(output).to eq(expected_output)
          end
        end
      end


```

## [#](<#step-5-run-your-rspec-tests>) Step 5 - Run your RSpec tests

Now the last step is to run your RSpec tests. This is done with the `bundle exec rspec spec/actions/search_customers_spec.rb` command.
```bash
 
    $ bundle exec rspec spec/actions/search_customers_spec.rb 

    actions/search_customers
      execute
        given valid input
          gives expected output
      sample_output
        add some examples (PENDING: Not yet implemented)
      input_fields
        add some examples (PENDING: Not yet implemented)
      output_fields
        add some examples (PENDING: Not yet implemented)

    Pending: (Failures listed here are expected and do not affect your suites status)

      1) actions/search_customers sample_output add some examples
         # Not yet implemented
         # ./spec/actions/search_customers_spec.rb:28

      2) actions/search_customers input_fields add some examples
         # Not yet implemented
         # ./spec/actions/search_customers_spec.rb:34

      3) actions/search_customers output_fields add some examples
         # Not yet implemented
         # ./spec/actions/search_customers_spec.rb:40

    Finished in 0.03218 seconds (files took 0.90373 seconds to load)
    4 examples, 0 failures, 3 pending


```
