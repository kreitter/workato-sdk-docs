# Workato SDK Documentation

> **Source**: https://docs.workato.com/en/developing-connectors/sdk/cli/guides/rspec/vcr.html
> **Fetched**: 2026-01-18T02:49:12.321097

---

# [#](<#how-to-guides-setting-up-vcr-for-your-unit-tests>) How-to guides - Setting up VCR for your unit tests

In this segment, we will be going through how you can set up VCR to record HTTP interactions for your unit tests.

## [#](<#why-do-i-need-vcr-for-my-unit-tests>) Why do I need VCR for my unit tests?

The VCR gem works hand in hand with RSpec tests to record any HTTP interactions (requests) that are sent out when you are running your test suite and play back the same responses if the test suite is run again.

This is critical for stable RSpec tests especially when you're working with an environments where data could be changing constantly. For example, for the same `GET` request, you might get a different response when later on, but VCR will be able to play your tests back with the same HTTP response it saw earlier, so your tests can make the same assertions.

This removes one aspect of variability in your tests and ensures that you're only testing for changes in your code and nothing else.

[Learn more about VCR (opens new window)](<https://relishapp.com/vcr/vcr/v/1-10-3/docs/getting-started>).

## [#](<#how-do-i-get-started>) How do I get started?

When you generate a connector project using the command `workato new [PATH]`, VCR will be set up automatically.

If you setup the project with the `secure` option, the VCR recordings are also encrypted. We recommend you use the `secure` option. In any case, your `spec_helper.rb` contains all information about your VCR recording configurations. Setting your project to `secure` ensures your VCR recordings are encrypted with your `master.key`. Below you can find an example of a `spec_helper.rb` which includes encryption.
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

TIP

**By default our record mode for secure is`none` which means no new VCR cassettes are recorded. To record new VCR cassettes, run the RSpec tests with the following command `VCR_RECORD_MODE=once bundle exec rspec spec/actions/test_action_spec.rb`.**

## [#](<#can-i-make-modifications-to-the-vcr-settings>) Can I make modifications to the VCR settings?

You can do so in `spec_helper.rb`. You can modify the spec_helper to suite your needs such as changing or relaxing the conditions as to how VCR matches your outgoing HTTP requests to previously recorded interactions.

Example: Relaxing VCR matching to accept different Authorization Headers by adjusting `spec_helper.rb`
```ruby
 
    config.register_request_matcher :headers_without_user_agent do |request1, request2|
      request1.headers.except('User-Agent', 'Authorization') == request2.headers.except('User-Agent', 'Authorization')
    end


```
