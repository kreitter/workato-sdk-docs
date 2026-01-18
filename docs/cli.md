# Workato SDK Documentation

> **Source**: https://docs.workato.com/en/developing-connectors/sdk/cli.html
> **Fetched**: 2026-01-18T02:48:57.116215

---

# [#](<#sdk-cli>) SDK - CLI

Welcome to the SDK CLI! This section focuses on how you can use Workato's Connector SDK Ruby gem (SDK gem) to bring your connector development local.

## [#](<#what-is-the-sdk-gem>) What is the SDK gem?

The SDK Gem is a Ruby software package that emulates how Workato would parse and execute your connector code.

The gem is:

  * Easy to install
  * Can be run on the command line
  * Allows you to develop connectors from the comfort of your chosen IDE (integrated development environment)

## [#](<#prerequisites>) Prerequisites

To use the SDK gem, you should be familiar with:

  1. The [Connector SDK](</developing-connectors/sdk.html>) at an intermediate level
  2. Command line tools and how to use them
  3. RSpec for unit testing. Check out the [RSpec docs (opens new window)](<https://rspec.info/documentation/>) to learn more.
  4. VCR. Check out this [general guide (opens new window)](<https://dev.to/gathuku/testing-external-apis-with-vcr-in-rails-488m>) to learn more about VCR, or this [getting started guide (opens new window)](<https://relishapp.com/vcr/vcr/v/1-10-3/docs/getting-started>) to dive right in.

## [#](<#benefits-of-using-cli>) Benefits of using CLI

  * Develop in your chosen IDE by bringing connector development local
  * Enhanced debugging tools
  * Improved collaboration with teammates
  * Ability to implement unit tests and CI/CD processes, improving deployment stability
  * Ability to implement automated deployments

## [#](<#sdk-gem-features>) SDK gem features

Still not sure if the SDK gem is right for you? The following section describes the key differences between building a connector with the Cloud SDK **Test code** tab and the SDK gem.

| Cloud SDK Test code tab | SDK Gem  
---|---|---  
**Testing specificity** | Able to test connections, actions and triggers in their entirety | Able to test specific keys of a connector separately. For example: `execute` and `output_fields` can be tested separately   
**UI testing** | Able to test the exact look and feel of input and output fields. For example: Dynamic input and output fields | No UI, but able to quickly evaluate resultant Workato schema of input and output fields using CLI Utils  
**Unit testing** | Not available | Able to convert CLI commands into unit tests quickly  
**Test code tab properties and lookup tables** | No access to `account_properties` or lookup tables in Test code tab  | Able to store `account_properties` and credentials in encrypted/unencrypted formats. Able to store lookup tables in unencrypted format.  

As we continue to improve on the SDK Gem and its capabilities, more features will be added.

## [#](<#connector-development-with-the-cli>) Connector development with the CLI

So, what does connector development look like for a team?

Below is an example process, though it could always be modified to fit your team's specific needs and workflows.

![SLDC Connector with CLI](/assets/img/sldc_connector_cli.49750ce1.png)

Let's look at this step by step:

1

**Local development.** Run your connector locally. The SDK gem's handy [CLI commands](</developing-connectors/sdk/cli/reference/cli-commands.html>) can help you build, test, and debug your connector as you work.

2

**Test in your Workato workspace.** Ensuring functionality is important, but so is the UX of your connector. You can push your connector to your personal or team workspace, allowing you to test your connector in an actual recipe.

3

**Push to Git.** To collaborate with others, push your code to a Git repository. This might be GitHub, Gitlab, Bitbucket, or another provider.

4

**Review and test.** Review the changes made by your teammates and ensure the connector passes all unit tests.

5

**Automated push to DEV**. If desired, you can set up automated workflows in your repository to automatically push changes to your DEV workspace when pull requests are merged. This would allow you to trigger additional tests. For example: Recipe builders can conduct user acceptance testing to ensure the connector works as expected.

6

**Release to production.** Transition your connector through DEV > UAT > PROD environments through your standard recipe lifecycle management processes, ensuring that the connector - like your recipes - is fully tested before being released to production.

## [#](<#get-started>) Get started

Ready to start developing? Check out the [Getting Started](</developing-connectors/sdk/cli/guides/getting-started.html>) guide to get up and running!
