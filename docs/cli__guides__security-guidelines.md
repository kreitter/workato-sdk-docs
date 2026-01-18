# Workato SDK Documentation

> **Source**: https://docs.workato.com/en/developing-connectors/sdk/cli/guides/security-guidelines.html
> **Fetched**: 2026-01-18T02:49:14.597497

---

# [#](<#securing-your-connector-project>) Securing Your Connector Project

When you build a connector locally, you bear all responsibility for securing credentials and application access. This is especially important if you push your code to git software, like GitHub.

Sounds scary, right? It doesn't have to be!

In this guide, we'll cover some tips that will help you mitigate risks when working with credentials or other sensitive information.

## [#](<#tip-1-always-use-a-sandbox>) Tip 1: Always use a sandbox

Whether you're building using the SDK gem or in Workato's cloud platform, **never use a production environment when developing.** We can't stress this enough.

You could make changes that negatively impact your business or potentially expose sensitive data. For this reason, always use a sandbox environment.

## [#](<#tip-2-always-use-encrypted-files>) Tip 2: Always use encrypted files

To ensure credentials remain secure, use encrypted files for storage.

The SDK gem includes a command that allows you to easily create and update encrypted files. This means you can encrypt your credentials, ensuring they can't be used or decrypted without your `master.key`.

To start working with encrypted files, use the [`workato edit`](</developing-connectors/sdk/cli/reference/cli-commands.html#workato-edit>) command to create the encrypted `master.key` file. If your project doesn't have this file, one will automatically be created the first time the command is run.

## [#](<#tip-3-always-use-encrypted-vcr-recordings>) Tip 3: Always use encrypted VCR recordings

VCR recordings are crucial for stable tests but also present a security risk. By default, VCR recordings record all aspects of your HTTP requests, such as tokens in headers and request or response data. If you decide to sync this data to the cloud, the best practice is to encrypt your VCR recordings.

The SDK gem makes it easy to do this when you set up your connector project.

After you run [`workato new`](</developing-connectors/sdk/cli/reference/cli-commands.html#workato-new>), select `secure` at the HTTP binding prompt:
```ruby
 
    Please select default HTTP mocking behavior suitable for your project?

    1 - secure. Cause an error to be raised for any unknown requests, all request recordings are encrypted.
                To record a new cassette you need set VCR_RECORD_MODE environment variable

                Example: VCR_RECORD_MODE=once bundle exec rspec spec/actions/test_action_spec.rb

    2 - simple. Record new interaction if it is a new request, requests are stored as plain text and expose secret tokens.


```

This option also creates a `spec_helper.rb` file, which comes pre-loaded with your VCR configurations and encryption. To learn more about VCR, [check out the VCR guides](</developing-connectors/sdk/cli/guides/rspec/vcr.html>).

## [#](<#tip-4-add-master-key-to-gitignore>) Tip 4: Add master.key to .gitignore

If your project contains a `master.key` file - [and we strongly recommend that it does](<#tip-2-always-use-encrypted-files>) \- it should never pushed to your Git repository.

To ensure you don't accidentally commit this file, add it to your project's `.gitignore`.

Additionally, if you need to share the info in `master.key` with your teammates, ensure you're doing so securely.

## [#](<#tip-5-use-repository-secrets-to-store-credentials-in-the-cloud>) Tip 5: Use repository secrets to store credentials in the cloud

To run your RSpec tests in the cloud while securely storing your credentials, we recommend adding secrets to your repository.

GITHUB SECRETS

Secrets are encrypted environment variables that you create in an organization, repository, or repository environment. Refer to GitHub's [Encrypted secrets (opens new window)](<https://docs.github.com/en/actions/reference/encrypted-secrets>) documentation for additional information.

Most git platforms support adding secrets to your repository, which is where we recommend storing your `master.key` for use during RSpec testing.
