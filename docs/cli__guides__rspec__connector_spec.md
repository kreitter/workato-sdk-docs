# Workato SDK Documentation

> **Source**: https://docs.workato.com/en/developing-connectors/sdk/cli/guides/rspec/connector_spec.html
> **Fetched**: 2026-01-18T02:49:08.845714

---

# [#](<#how-to-guides-writing-tests-for-your-connection>) How-to guides - Writing tests for your connection

In this segment, we will be going through how you can write tests for your connector's connection.

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
    }


```

Credentials in `settings.yaml.enc`.
```ruby
 
    api_key: valid_api_key
    domain: valid_domain


```

## [#](<#generating-your-tests>) Generating your tests

Your project should have already come with a sample `connector_spec.rb` file if you generated the connector project using `workato new [PATH]`. If not, you should create this file to house your `test` lambda tests.

### [#](<#sample-rspec-contents>) Sample RSpec contents

The code in `connector_spec.rb`.
```ruby
 
    RSpec.describe 'connector', :vcr do

      let(:connector) { Workato::Connector::Sdk::Connector.from_file('connector.rb', settings) }
      let(:settings) { Workato::Connector::Sdk::Settings.from_default_file }

      it { expect(connector).to be_present }

      describe 'test' do
        subject(:output) { connector.test(settings) }

        context 'given valid credentials' do
          it 'establishes valid connection' do
            expect(output).to be_truthy
          end

          it 'returns response that is formatted properly' do
            # large Test responses might also cause connections to be evaluated wrongly
            expect(output.to_s.length).to be < 5000
            expect(output['list']).to be_kind_of(::Array)
          end
        end
      end
    end


```

Here, we have defined 2 tests for the `test` lambda but lets go over it step by step.

## [#](<#step-1-define-your-connector-instance>) Step 1 - Define your connector instance

To begin testing, you need to use the Workato SDK Gem to create an instance of your connector.
```ruby
 
      let(:connector) { Workato::Connector::Sdk::Connector.from_file('connector.rb', settings) }


```

## [#](<#step-2-define-your-settings-instance>) Step 2 - Define your settings instance

To begin testing, you need to use the Workato SDK Gem to create an instance of your settings. This is synonymous with your connection on Workato. Take note that, your connector instance previously defined also uses this settings instance.
```ruby
 
      let(:settings) { Workato::Connector::Sdk::Settings.from_default_file }


```

To instantiate your settings from an alternative setting file, you can use `from_encrypted_file` or `from_file`.
```ruby
 
      let(:settings) { Workato::Connector::Sdk::Settings.from_encrypted_file('invalid_settings.yaml.enc') }


```

## [#](<#step-3-describe-your-tests-and-define-your-subject>) Step 3 - Describe your tests and define your subject

Here, we describe the "family" of tests we are hoping to run. In this case, we use the keyword `test`. After that, we also define a `subject` of our tests. This is where we assign the value of `output` to our connector instance running the `test` lambda. This is done with the `connector.test(settings)` defined.
```ruby
 
      describe 'test' do
        subject(:output) { connector.test(settings) }


```

## [#](<#step-4-declare-your-assertions-for-individual-tests>) Step 4 - Declare your assertions for individual tests

For a test to pass or fail, there needs to be a declared comparison.

Over here, we are declaring that we "expect" the output of the `test` lambda to be `truthy` to satisfy the test - "establishes valid connection".

We also "expect" that the output of the `test` lambda to be less than 5000 characters long and that its `list` attribute is an array. This satisfies the test - "returns response that is formatted properly"
```ruby
 
        context 'given valid credentials' do
          it 'establishes valid connection' do
            expect(output).to be_truthy
          end

          it 'returns response that is formatted properly' do
            # large Test responses might also cause connections to be evaluated wrongly
            expect(output.to_s.length).to be < 5000
            expect(output['list']).to be_kind_of(::Array)
          end
        end


```

## [#](<#step-5-run-your-rspec-tests>) Step 5 - Run your RSpec tests

Now the last step is to run your RSpec tests. This is done with the `bundle exec rspec spec/connector_spec.rb` command.
```bash
 
    $ bundle exec rspec spec/connector_spec.rb

    connector
      is expected to be present
      test
        given valid credentials
          establishes valid connection
          returns response that is formatted properly

    Finished in 0.04959 seconds (files took 1.04 seconds to load)
    3 examples, 0 failures


```
