# Workato SDK Documentation

> **Source**: https://docs.workato.com/en/developing-connectors/sdk/cli/guides/troubleshooting.html
> **Fetched**: 2026-01-18T02:49:15.700405

---

# [#](<#troubleshooting-faq>) Troubleshooting - FAQ

Running the workato command in my terminal results in errors

Here is a quick checklist of things to verify:

  1. First check that you have installed a valid version of ruby. You can do this by typing `ruby -v` into your terminal. It should be ruby version `2.4.10` `2.5.X` or `2.7.X`. Our preferred version is `2.7.X`.
  2. Check that you have installed the SDK gem. You can do that by running `gem install workato-connector-sdk` in your terminal. You can also use `gem which workato-connector-sdk` to find out where the gem is installed.
  3. Run `bundle install` in your connector project to ensure you have all dependencies installed.
  4. Remove your gemfile.lock and run `bundle install`.

When I run a workato exec command, I get an error.

You may get this error if your connector receives a `400` bad request response from an API call. You may use options like `--verbose` to see the request, `--debug` to see the stacktrace of the SDK Gem and byebug to debug further.

When I try to use the workato push command, I get an error

The `workato push` command tries to release your connector on Workato. If there are syntax errors in your connector, the output of the command will relay that to you.
```ruby
 
    Unable to publish custom adapter Chargebee Demo1: Syntax [["method require not allowed", 1, 0, 1, 16]] and Publish Can not publish adapter with code errors


```

Where this is telling you that there is 1 error (denoted by 1 index in the root array) and the error is from line 1 position 0 to line 1 position 16.

When I run RSpec, VCR states that there is an VCR::Errors::UnhandledHTTPRequestError:

VCR records and matches HTTP requests based on your configurations in your `spec_helper.rb`. What RSpec is telling you is that it can't match the HTTP request you have sent to anything that has been recorded. There are a few reasons for this:

  1. If you've set up your connector project using `secure`, the default VCR recording mode is set to `none`. This means that when you run RSpec, no new HTTP interactions will be recorded but only previous ones will be played back. To run your unit tests to record all new HTTP interactions, you can use the command `VCR_RECORD_MODE=once bundle exec rspec`.
  2. Your previously recorded interactions may not match the ones your connector is currently attempting to make. This could be for a variety of reasons such as different headers due to a new access token in place of an earlier one. You can relax the matching for VCR recordings in the `spec_helper.rb`. [Learn more (opens new window)](<https://relishapp.com/vcr/vcr/v/1-6-0/docs/cassettes/request-matching>)

Example: Relaxing VCR matching to accept different Authorization Headers by adjusting `spec_helper.rb`
```ruby
 
    config.register_request_matcher :headers_without_user_agent do |request1, request2|
      request1.headers.except('User-Agent', 'Authorization') == request2.headers.except('User-Agent', 'Authorization')
    end


```
