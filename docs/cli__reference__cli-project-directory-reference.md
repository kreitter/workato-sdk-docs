# Workato SDK Documentation

> **Source**: https://docs.workato.com/en/developing-connectors/sdk/cli/reference/cli-project-directory-reference.html
> **Fetched**: 2026-01-18T02:49:18.117569

---

# [#](<#sdk-project-directory-and-file-reference>) SDK - Project Directory and File Reference

A typical connector project built with the SDK gem usually looks something like this:
```ruby
 
    . # root
    ├── connector.rb
    ├── fixtures
    ├── Gemfile 
    ├── Gemfile.lock
    ├── logo.png 
    ├── master.key 
    ├── README.md
    ├── settings.yaml.enc
    ├── spec 
    |   ├── connector_spec.rb
    |   └── spec_helper.rb
    ├── tape_library
    ├── .github
    ├── .gitignore 
    └── .rspec


```

An overview of what each file or directory does:

File/directory | Created | Description  
---|---|---  
**connector.rb** | Via workato new | Stores the actual connector code. This should be a replica of your connector code in Workato.   
**fixtures** | Via workato new | Stores input and output JSON files for RSpec or CLI. See an example file and learn more [here](<#fixtures>).   
**Gemfile** | Via workato new | Declares the gems (dependencies) required by the project. These are required to run RSpec. See an example file and learn more [here](<#gemfile>).   
**Gemfile.lock** | Via workato new | Stores gem dependency data, including versions and dependencies of dependencies. This file is automatically created when your project is built.   
**logo.png** | By you | Your connector's logo. When synced with your Workato workspace via [`workato push`](</developing-connectors/sdk/cli/reference/cli-commands.html#workato-push>), this will be used as the default for your connector's logo image.   
**master.key** | Via workato new | Stores the encryption key used to encrypt your files. These files can include credentials and other sensitive data, such as environment properties.   

**Note** : Created only if `secure` was selected during project setup.   
**README.md** | By you | Used to document what your connector does and how to use it. When synced with your Workato workspace via [`workato push`](</developing-connectors/sdk/cli/reference/cli-commands.html#workato-push>), this will be used as the default file for your connector's description.   
**settings.yaml.enc or settings.yaml** |  | Stores credentials used for testing the connector. See an example file and learn more [here](<#settings-yaml-enc-settings-yaml>).   

**Note** : If `secure` was selected during project setup, this will be a `.yaml.enc` file. Otherwise, this will be a `.yaml` file.   
**spec** | Via workato new | Stores RSpec test files. [RSpec](</developing-connectors/sdk/cli/guides/rspec/vcr.html>) is a Ruby testing tool that can be used in conjunction with the [SDK gem](</developing-connectors/sdk/cli.html>) to define, write, and run unit tests for your connector.   
**spec/connector_spec.rb** | Via workato new | Stores all unit test for the connector. This is the main RSpec file. See an example file and learn more [here](<#connector-spec-rb>).   

This file may be split into multiple files or folders if it helps you organize your tests. All spec tests can be run using the `bundle exec rspec` command.   
**spec/spec_helper.rb** | Via workato new | Stores all commands that should be set up prior to each RSpec run. See an example file and learn more [here](<#spec-helper-rb>).   
**tape_library** | via RSpec | Stores [VCR cassettes](<https://relishapp.com/vcr/vcr/v/6-0-0/docs/cassettes/cassette-format>), which are files that contain all info about recorded API requests and subsequent responses. These requests are essential for stable unit tests. Check out the [VCR docs](<https://relishapp.com/vcr/vcr/docs>) to learn more.   
**.github** | By you | **Applicable if using GitHub.** Stores information about your GitHub action workflows.   
**.gitignore** | Via workato new | Stores the names of files and/or directories that shouldn't be pushed to Git. See an example file and learn more [here](<#gitignore>).   

**Note** : If your project has a `master.key`, it should be added to this file as per our [security best practices](</developing-connectors/sdk/cli/guides/security-guidelines.html>).   
**.rspec** | Via workato new | Stores standard options to pass to RSpec when run. Some example flags:   

  * `--format documentation` \- Allows tests to be grouped 
  * `--color` \- Enables coloring in the RSpec output 
  * `--require spec_helper` \- Tells RSpec runs to require `spec_helper.rb` prior to every run 

* * *

## [#](<#connector-spec-rb>) connector_spec.rb

Created when `workato new` is run, the `connector_spec.rb` file contains the unit tests for your connector.

An example file might look something like this:
```bash
 
    # frozen_string_literal: true

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

          it 'returns response that is not excessively large' do
            # large Test responses might also cause connections to be evaluated wrongly
            expect(output.to_s.length).to be < 5000
          end
        end

        context 'given invalid credentials' do
          let(:settings) { Workato::Connector::Sdk::Settings.from_encrypted_file('invalid_settings.yaml.enc'}

          it 'establishes invalid connection' do
            expect { output }
              .to raise_error('500 Internal Server Error')
          end
        end
      end
    end


```

You can also use [`workato generate test`](</developing-connectors/sdk/cli/reference/cli-commands.html#workato-generate>) to generate RSpec test stubs for you. This handles most of the heavy lifting, such as such as instantiating your connector or settings.

It's ultimately up to you how you want to write your unit tests. If you'd like some help getting started, [check out this tutorial (opens new window)](<https://semaphoreci.com/community/tutorials/getting-started-with-rspec>).

* * *

## [#](<#fixtures>) fixtures

The `/fixtures` folders are used to store the input and output JSON files used to test parts of your connector. This includes actions, triggers, methods, and so on.

**Input** JSON files should be created and formed manually. You can design them yourself, or use the Cloud SDK's **Test code** tab to build them.

**Output** JSON files can be created from CLI commands by including the `--output` option. For example:
```ruby
 
    workato exec <PATH> --output


```

Your `/fixtures` folder might look something like this:
```ruby
 
    ├── fixtures
    │   ├── actions
    │   │   └── search_customers
    │   │       ├── input.json
    │   │       └── output.json
    │   ├── methods
    │   │   └── sample_method
    │   │       ├── input.json
    │   │       └── output.json
    │   ├── pick_lists
    │   │   └── dependent
    │   │       └── input.json
    │   └── triggers
    │       └── new_updated_object
    │           ├── customer_config.json
    │           ├── customer_input_poll.json
    │           ├── customer_input_poll_page.json
    │           ├── customer_output_fields.json
    │           ├── customer_output_poll.json
    │           └── customer_output_poll_page.json


```

* * *

## [#](<#gemfile>) GEMFILE
```bash
 
    # frozen_string_literal: true

    source 'https://rubygems.org'

    gem 'rspec'
    gem 'vcr'
    gem 'workato-connector-sdk'
    gem 'webmock'
    gem 'timecop'
    gem 'byebug'
    gem 'rubocop' # Only if you want to use rubocop. Not added by default.


```

* * *

## [#](<#settings-yaml-enc-settings-yaml>) settings.yaml.enc, settings.yaml

The `settings.yaml.enc`/`settings.yaml` file stores credentials used for testing. Data in this file must be valid YAML.

### [#](<#single-credential-set>) Single credential set

If you only have one set of credentials, they can be defined at the root level:
```ruby
 
    api_key: valid_key
    domain: valid_domain


```

### [#](<#multiple-credential-sets>) Multiple credential sets

If you have multiple sets of credentials, your settings file should be structured similarly to the following:
```ruby
 
    [one_connection_name]:
      api_key: valid_key
      domain: valid_domain
    [second_connection_name]:
      api_key: invalid_key
      domain: invalid_domain


```

* * *

## [#](<#spec-helper-rb>) spec_helper.rb

Created when `workato new` is run, the `spec_helper.rb` file stores common attributes to be used in RSpec runs.

This file should require, at a minimum:

  * `'bundler/setup'`
  * `'workato-connector-sdk'`
  * `'json'`

Learn more about additional RSpec configuration [here in the RSpec repository (opens new window)](<https://github.com/rspec/rspec-core>).

The following example shows the `spec_helper.rb` file that's created when the `secure` HTTP mocking behavior is selected for a project.

This file will encrypt all VCR recordings using the project's `master.key`.

However, by default the record mode for `secure` is `none`. This means that no new VCR cassettes will be recorded. To change this behavior, the `VCR_RECORD_MODE` environment variable to `once`.
```bash
 
    # frozen_string_literal: true

    require 'bundler/setup'
    require 'json'
    require "webmock/rspec"
    require "timecop"
    require "vcr"
    require "workato-connector-sdk"
    require "workato/testing/vcr_encrypted_cassette_serializer"
    require "workato/testing/vcr_multipart_body_matcher"

    RSpec.configure do |config|
      # Enable flags like --only-failures and --next-failure
      config.example_status_persistence_file_path = ".rspec_status"

      # Disable RSpec exposing methods globally on `Module` and `main`
      config.disable_monkey_patching!

      config.expect_with :rspec do |c|
        c.syntax = :expect
      end
    end

    VCR.configure do |config|
      config.cassette_library_dir = "tape_library"
      config.hook_into :webmock
      config.cassette_serializers[:encrypted] = Workato::Testing::VCREncryptedCassetteSerializer.new
      config.register_request_matcher :headers_without_user_agent do |request1, request2|
        request1.headers.except("User-Agent") == request2.headers.except("User-Agent")
      end
      config.register_request_matcher :multipart_body do |request1, request2|
        Workato::Testing::VCRMultipartBodyMatcher.call(request1, request2)
      end
      config.default_cassette_options = {
        record: ENV.fetch('VCR_RECORD_MODE', :none).to_sym,
        serialize_with: :encrypted,
        match_requests_on: %i[uri headers_without_user_agent body]
      }
      config.configure_rspec_metadata!
    end


```

* * *

## [#](<#gitignore>) .gitignore

The `.gitignore` file contains a list of files and/or directories that shouldn't be pushed via Git.

**Note** : If your project has a `master.key` file, you should add it to this file to ensure it isn't accidentally committed to a repository.
```ruby
 
    /.bundle/
    /.yardoc
    /_yardoc/
    /coverage/
    /doc/
    /pkg/
    /spec/reports/
    /tmp/
    master.key

    # rspec failure tracking
    .rspec_status


```
