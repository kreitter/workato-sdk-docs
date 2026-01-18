# Workato SDK Documentation

> **Source**: https://docs.workato.com/en/developing-connectors/sdk/cli/reference/cli-commands.html
> **Fetched**: 2026-01-18T02:49:16.854638

---

# [#](<#cli-command-reference>) CLI Command Reference

Learn more about the commands you can use in CLI after installing the SDK gem.

* * *

## [#](<#workato>) workato

Root command of the Workato gem. Synonymous with [`workato help`](<#workato-help>). 

### [#](<#usage>) Usage
```bash
 
    $ workato


```

### [#](<#output>) Output

Description of commands available in the Workato gem.

* * *

## [#](<#workato-edit>) workato edit

Creates or edits an encrypted file.

### [#](<#usage-2>) Usage
```bash
 
    $ workato edit <PATH>


```

### [#](<#input>) Input

Input | Description  
---|---  
**EDITOR** | The editor you'll use to edit the file. For example: `nano`  
**PATH** | The path to the file that should be created or updated, in dot notation.   

### [#](<#options>) Options

Option | Description  
---|---  
**\--key, -k** | The path to the encrypt/decrypt key.  

If this isn't provided, defaults to `master.key`.  

If a `master.key` file doesn't exist and no option is provided, a new `master.key` file is created.   

### [#](<#result>) Result

Encrypted file is created or updated. `master.key` is created if the file didn't previously exist and an option wasn't provided. 

### [#](<#example>) Example
```ruby
 
    For Windows:
      $ set EDITOR=notepad
      $ workato edit settings.yaml.enc
    For Mac:
      $ EDITOR="nano" workato edit settings.yaml.enc


```

* * *

## [#](<#workato-exec>) workato exec

Executes a specific lambda function in your connector for testing.

### [#](<#usage-3>) Usage
```bash
 
    $ workato exec <PATH> <OPTIONS>


```

### [#](<#input-2>) Input

Input | Description  
---|---  
**PATH** | The path to the lambda to execute, in dot notation. For example: `actions.search_customers.execute` would correspond to the action `search_customers` and the execute lambda. You may also simulate the entire action with the path `actions.search_customers`.   

### [#](<#options-2>) Options

Option | Description  
---|---  
**-c or --connector** | The path to the `connector.rb` file to execute. Defaults to `connector.rb` if not provided.   
**-s or --settings** | The path to the `settings.yaml` file that stores the credentials. Defaults to `settings.yaml.enc`, then `settings.yaml` if not provided.   
**-n or --connection** | The connection name in the `settings.yaml` file. Only required if there are multiple credential sets.   
**-i or --input** | The path to the JSON file that stores the input. Used for `execute`, `webhook_notification`, or `poll` lambdas.   
**\--closure** | The path to the JSON file that stores the closure. Used for `poll` lambdas to simulate polls after the initial poll.   
**-a or --args** | The path to the JSON file that stores arguments for a method or picklists. Used for `methods` or `pick_lists` lambdas to simulate their invocation. An error may arise if arguments were expected but not provided.   
**\--extended-input-schema and --extended-output-schema** | The path to the JSON file that stores the `extended_input_schema` and `extended_output_schema`. Used for `execute`, `webhook_notification`, or `poll` lambdas.   
**\--config-fields** | The path to the JSON file that stores the `config_fields` data. Used for `object_definitions`, `input_fields`, or `output_fields` lambdas.   
**\--continue** | The path to the JSON file that store the `continue` data. Used for `execute` lambdas that have multistep implemented.   
**\--from** | The starting byte range for a specific stream invocation. Used for `streams` lambdas.   
**\--frame_size** | The requested framesize in bytes for a specific stream invocation. Used for `streams` lambdas.   
**\--webhook-headers** | The path to the JSON file(s) that store incoming webhook header data. Used for `webhook_notification` lambdas.   
**\--webhook-params** | The path to the JSON files that store incoming webhook parameter data. Used for `webhook_notification` lambdas.   
**\--webhook-payload** | The path to the JSON files that store incoming webhook payload data. Used for `webhook_notification` lambdas.   
**\--webhook-url** | The path to the file that stores the webhook URL. Used for `webhook_subscribe` lambdas.   
**-o or --output** | The path to the file that saves the output of the lambda function.   
**\--oauth2-code** | The OAuth2 code used to invoke the `acquire` lambda function.   
**\--redirect-url** | The redirect-url used to invoke the `refresh` lambda function.   
**\--refresh-token** | The refresh-token used to invoke the `refresh` lambda function.   
**\--verbose** | Include this option to make the execution verbose. This means that all HTTP requests and request payloads will be shown. Response bodies won't be shown but can be inspected with `byebug`.   
**\--debug** | Include this option to show errors from the entire stacktrace, rather than just the last encountered error.   

### [#](<#result-2>) Result

The output of the lambda function. 

### [#](<#examples>) Examples

Invoke a specific method.
```bash
 
    $ workato exec methods.sample_method --args='input/sample_method_input.json'

```

Invoke the acquire lambda. Connector and settings are all specified.
```ruby
 
    workato exec connection.authorization.acquire --connector='zoominfo.rb' --settings='settings.yaml' --connection='My Valid Connection' --verbose

```

Invoke the test lambda. Connector and settings are all specified.
```ruby
 
    workato exec test --connector='zoominfo.rb' --settings='settings.yaml' --connection='My Valid Connection' --verbose

```

Invoke a specific action and pass it inputs.
```bash
 
    $ workato exec actions.search_customers.execute --input='input/search_customer_input.json' --verbose

```

Invoke a specific polling trigger and pass it inputs. This command simulates the trigger paginating through a series of records when `can_poll_more` is set to `true` in the closure.
```bash
 
    $ workato exec triggers.new_updated_customers.poll --input='input/new_updated_customers_input.json' --verbose

```

Invoke a specific polling trigger and pass it inputs. Output will be a single page of the poll. This command simulates a single trigger poll and returns only the first page.
```bash
 
    $ workato exec triggers.new_updated_customers.poll_page --input='input/new_updated_customers_input.json' --verbose

```

* * *

## [#](<#workato-generate>) workato generate

Generates Workato schema based on a given JSON or CSV or tests based on a given connector 

### [#](<#usage-4>) Usage
```bash
 
    $ workato generate <SUBCOMMAND>


```

### [#](<#input-3>) Input

Input | Description  
---|---  
**SUBCOMMAND** | The specific asset to be generated. Either `schema` or `test`.  

* * *

## [#](<#workato-generate-schema>) workato generate schema

Takes a given JSON or CSV file and converts it into Workato Schema for use in your connector 

### [#](<#usage-5>) Usage
```bash
 
    $ workato generate schema --api-token <API-TOKEN> <OPTIONS>


```

### [#](<#options-3>) Options

Option | Description  
---|---  
**\--json** | The path to the JSON file to convert into Workato Schema   
**\--csv** | The path to the CSV file to convert into Workato Schema   
**\--col-sep** | The column separators in the CSV file provided. Default: comma. Possible values: comma, space, tab, colon, semicolon, pipe   
**\--api-email** | DEPRECATED. API email and keys authentication has been succeeded with API Client authentication that is more secure. [Learn how to create an API client](<https://docs.workato.com/workato-api/api-clients.html#api-clients>). New versions of the SDK Gem will support deprecated API email and keys until 2023.   
**\--api-token** | REQUIRED. The API token of an API client with the proper permissions. API email and keys authentication has been succeeded with API Client authentication that is more secure. [Learn how to create an API client](<https://docs.workato.com/workato-api/api-clients.html#api-clients>).   

Required API Client permissions: 

  * POST /api/sdk/generate_schema/csv
  * POST /api/sdk/generate_schema/json

### [#](<#examples-2>) Examples

Convert sample JSON payload to Workato schema
```bash
 
    $ workato generate schema --api-token --json='fixtures/actions/search_customers/input.json'

```

Convert sample pipe delimited CSV file to Workato schema with
```bash
 
    $ workato generate schema --api-token --csv='fixtures/actions/report/input.csv' --col-sep=pipe

```

* * *

## [#](<#workato-generate-test>) workato generate test

Takes a given connector and generates RSpec tests for specified features. 

### [#](<#usage-6>) Usage
```bash
 
    $ workato generate test <OPTIONS>


```

### [#](<#options-4>) Options

Option | Description  
---|---  
**-c or --connector** | The path to the connector.rb file to execute. Defaults to connector.rb if not provided.   
**-a or --action** | The name of the specific Action to generate tests for. Generates tests for all features if not specified.   
**-t or --trigger** | The name of the specific Trigger to generate tests for. Generates tests for all features if not specified.   
**-p or --pick-list** | The name of the specific picklist to generate tests for. Generates tests for all features if not specified.   
**-o or --object-definition** | The name of the specific object_definition to generate tests for. Generates tests for all features if not specified.   
**-m or --method** | The name of the specific method to generate tests for. Generates tests for all features if not specified.   

### [#](<#examples-3>) Examples

Generate skeletal tests for all connector features
```bash
 
    $ workato generate test

```

Generate skeletal tests for specific action
```bash
 
    $ workato generate test action=get_customers

```

* * *

## [#](<#workato-help>) workato help

Displays help for a specified SDK gem command.

### [#](<#usage-7>) Usage
```bash
 
    $ workato help <COMMAND>


```

### [#](<#input-4>) Input

Input | Description  
---|---  
**COMMAND** | The command which you want to help displayed for. For example: `edit`  

### [#](<#output-2>) Output

Elaborated help for the specified SDK gem command.

### [#](<#example-2>) Example
```bash
 
    $ workato help edit
    Usage:
      workato edit PATH

    Options:
      -k, [--key=KEY]                  # Path to file with encrypt/decrypt key. NOTE: key from WORKATO_CONNECTOR_MASTER_KEY has higher priority
          [--verbose], [--no-verbose]

    Edit encrypted file, e.g. settings.yaml.enc


```

* * *

## [#](<#workato-new>) workato new

Creates a new connector project in your chosen directory.  

When you create a new connector project, you will be asked if you want to select `secure` or `simple` for your HTTP mocking behavior: 
```ruby
 
    Please select default HTTP mocking behavior suitable for your project?

    1 - secure. Cause an error to be raised for any unknown requests, all request recordings are encrypted.
                To record a new cassette you need set VCR_RECORD_MODE environment variable

                Example: VCR_RECORD_MODE=once bundle exec rspec spec/actions/test_action_spec.rb

    2 - simple. Record new interaction if it is a new request, requests are stored as plain text and expose secret tokens.


```

When you select `secure`, VCR recordings made for your unit tests are encrypted. **This is recommended.** You'll need to set your environment variable for `VCR_RECORD_MODE` as well. 

### [#](<#usage-8>) Usage
```bash
 
    $ workato new <PATH>


```

### [#](<#input-5>) Input

Input | Description  
---|---  
**PATH** | The path where the connector project should be created.   

### [#](<#result-3>) Result

Generates a new connector project. 

### [#](<#example-3>) Example
```bash
 
    $ workato new ~/Desktop/my-new-connector


```

* * *

## [#](<#workato-oauth2>) workato oauth2

GEM VERSION REQUIREMENT

The command `workato oauth2` requires SDK Gem version 0.1.2 and above.

Use this to implement the OAuth2 Authorization code grant flow for applicable connectors. Applicable connectors are ones where the connection hash has `type: 'oauth2`. For more information, check out this handy [Okta article](<https://developer.okta.com/blog/2018/04/10/oauth-authorization-code-grant-type>). 

### [#](<#usage-9>) Usage
```bash
 
    $ workato oauth2 <OPTIONS>


```

### [#](<#options-5>) Options

Option | Description  
---|---  
**-c or --connector** | The path to the connector source code. Defaults to `connector.rb` if not provided.   
**-s or --settings** | The path to the `settings.yaml` file that stores the credentials. Defaults to `settings.yaml.enc`, then `settings.yaml` if not provided.   
**-n or --connection** | The connection name in the `settings.yaml` file. Only required if there are multiple credential sets.   
**\--key, -k** | The path to the encrypt/decrypt key.  

If this isn't provided, defaults to `master.key`.  

If a `master.key` file doesn't exist and no option is provided, a new `master.key` file is created.   
**\--port** | By default, the SDK Gem spins up a webserver at "http://localhost:45555/oauth/callback" which is used to receive the OAuth callback. Use this option to change the port. i.e. --port='3010' will spin up the webserver at "http://localhost:3010/oauth/callback" This is useful when your OAuth app is configured to a specific redirect uri.   
**\--ip** | Allows you to override the default ip address. Defaults to "127.0.0.1"   
**\--https, --no-https** | Allows you to start the webserver with a self-signed certificate. Required in cases where the OAuth App requires a redirect uri with a "https://" prefix.   
**\--verbose** | Include this option to make the execution verbose. This means that all HTTP requests and request payloads will be shown. Response bodies won't be shown but can be inspected with `byebug`.   

### [#](<#result-4>) Result

Emulates the OAuth2 Authorization Code Grant Flow on Workato. Applicable connectors are ones where the connection hash has `type: 'oauth2`. For more information, check out this handy [Okta article](<https://developer.okta.com/blog/2018/04/10/oauth-authorization-code-grant-type>). 

### [#](<#example-4>) Example
```bash
 
    $ workato oauth2


```

* * *

## [#](<#workato-push>) workato push

PUSH TO A SPECIFIC FOLDER

The `workato push` command does not push to a specific folder in your Workato workspace unless you use the `--folder` parameter. For example: `workato push --folder <folder ID>`.

VIRTUAL PRIVATE WORKATO (VPW) CUSTOMERS

This feature requires configuration steps that are specific to your Virtual Private Workato (VPW) instance. If you are a VPW customer, refer to your VPW private documentation for the configuration details for your instances.

Creates a new connector project in your chosen Workato folder.

### [#](<#usage-10>) Usage
```bash
 
    $ workato push --api-token <API-TOKEN> <OPTIONS>


```

### [#](<#options-6>) Options

Option | Description  
---|---  
**\--api-email** | DEPRECATED. API email and keys authentication has been succeeded with API Client authentication that is more secure. [Learn how to create an API client](<https://docs.workato.com/workato-api/api-clients.html#api-clients>). New versions of the SDK Gem will support deprecated API email and keys until 2023.   
**\--api-token** | REQUIRED. The API token of an API client with the proper permissions. API email and keys authentication has been succeeded with API Client authentication that is more secure. [Learn how to create an API client](<https://docs.workato.com/workato-api/api-clients.html#api-clients>).   

Required API Client permissions: 

  * GET /api/users/me
  * GET /api/packages/:id
  * POST /api/packages/import/:id

**\--folder** | The ID of the folder in your Workato workspace where you plan to push the connector. By default, the connector is not pushed to a specific folder unless you add the `--folder` parameter and folder ID.  

Folder IDs are located in the URL when you're viewing the folder. For example: if the URL is `https://app.workato.com/?fid=106070#assets`, the folder ID is `106070`.   
**-t or --title** | The title of your connector. Defaults to the title key in your connector code if not provided.   
**-d or --description** | The path to your connector's description, which could be a Markdown or plain text file. Defaults to `README.md` if not provided.   
**-l or --logo** | The link to the `png` or `jpeg` of your connector's logo. Defaults to `logo.png` if not provided.   
**-n or --notes** | The version notes attached to this uploaded version.   
**-c or --connector** | The path to the connector source code. Defaults to `connector.rb` if not provided.   
**\--environment** | Use this data center-specific URL to push connector code. Defaults to the WORKATO_BASE_URL environment variable if not set. For example: \- `https://app.workato.com` \- `https://app.eu.workato.com` \- `https://app.jp.workato.com` \- `https://app.sg.workato.com` \- `https://app.au.workato.com` \- `https://app.il.workato.com` \- `https://app.trial.workato.com`   

### [#](<#example-5>) Example
```ruby
 
    workato push --api-token


```
