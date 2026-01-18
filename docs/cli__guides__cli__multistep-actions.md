# Workato SDK Documentation

> **Source**: https://docs.workato.com/en/developing-connectors/sdk/cli/guides/cli/multistep-actions.html
> **Fetched**: 2026-01-18T02:49:01.774238

---

# [#](<#how-to-guides-running-multistep-actions-on-cli>) How-to guides - Running multistep actions on CLI

In this segment, we will be going through how you can run and easily debug multistep actions using the Workato Gem.

## [#](<#prerequisites>) Prerequisites

  * You have installed and can run the Workato SDK Gem. Read our [getting-started guide](</developing-connectors/sdk/cli/guides/getting-started.html>) to know more.
  * You have a working connector with at least 1 multistep action.
  * You have a working set of credentials. If you are using a sample connector code, ensure that you have the appropriate credentials for the connector.

## [#](<#sample-connector-google-bigquery>) Sample connector - Google BigQuery

For this example we will be using the BigQuery connector example [here](</developing-connectors/sdk/guides/building-actions/multistep-actions.html#sample-connector-google-bigquery>).

Credentials in `settings.yaml.enc` .
```ruby
 
    iss: [[email protected]](</cdn-cgi/l/email-protection>)
    private_key: "-----BEGIN PRIVATE KEY-----...-----END
      PRIVATE KEY-----\\n"
    access_token: valid_access_token
    expires_in: 3599
    token_type: Bearer


```

TIP

If you're using an encrypted settings.yaml file, you will need to use `workato edit <PATH>` to edit or create the file. Find out more [here](</developing-connectors/sdk/cli/reference/cli-commands.html#workato-edit>).

With the SDK Gem, you'll be able to invoke individual lambda functions in your action and gain greater control over how each part of your action works. For example, you may run your `execute` lambda function independently from your `input_fields` lambda. Check out the guide [here](</developing-connectors/sdk/cli/guides/cli/actions.html>) to understand about running your `input_fields` and `output_fields` lambdas.

## [#](<#running-your-execute-lambda-for-multistep-actions>) Running your execute lambda for multistep actions

With multistep actions, we need to take note that special methods like `reinvoke_after` will cause the job in Workato to be put to sleep for a defined amount of time.
```ruby
 
    reinvoke_after(seconds: 10, continue: { current_step: current_step + 1, jobid: continue['jobid']})


```

TIP

On the Workato platform, step time is set to be a minimum of 60 seconds. On the SDK Emulator, however, the step time between checks can be set to be lower for debugging purposes.

The above method call in your `execute` lambda will results in the job being put to sleep for 10 seconds before being awoken again where execution begins at the **start of the execute block**. The SDK Gem emulates this behavior so you'll be able to examine how your action might behave on Workato.

In this case, the contents of the file `bigquery_input.json` contains
```ruby
 
    {
        "project_id": "named-reporter-237205",
        "query": "SELECT * FROM `named-reporter-237205.Lead_data.2mill_table` t1",
        "wait_for_query": "true"
    }


```

To run a multistep action, you give the same command as you would a standard action.
```ruby
 
    workato exec actions.query.execute --input='bigquery_input.json' --verbose

    SETTINGS
    {
      "iss": "[[email protected]](</cdn-cgi/l/email-protection>)",
      "private_key": "-----BEGIN PRIVATE KEY-----...-----END
      PRIVATE KEY-----\\n",
      "access_token": "valid_access_token",
      "expires_in": 3599,
      "token_type": "Bearer"
    }
    INPUT
    {
      "project_id": "named-reporter-237205",
      "query": "SELECT * FROM `named-reporter-237205.Lead_data.2mill_table` t1",
      "wait_for_query": "true"
    }

    RestClient.post "https://bigquery.googleapis.com/bigquery/v2/projects/named-reporter-237205/queries", "{\"query\":\"SELECT * FROM `named-reporter-237205.Lead_data.2mill_table` t1 left join `named-reporter-237205.Lead_data.2mill_table` t2 on t1.start_time = t2.start_time\",\"timeoutMs\":\"25000\",\"useLegacySql\":false}", "Accept"=>"application/json", "Accept-Encoding"=>"gzip, deflate", "Authorization"=>"Bearer ya29.c.Kp8BFQgUT1EOcK5YBwTEv60KokPYvLLWJRFsbfd9S0oGEB3cW5cp1pXTJRZreYPB4B06Z1_YdvhLQByhe9fP_FjziQc6rCtEfGs9zZdMZpXKUFHWEqzG44qxni-jibwaLEgWLw3zaqv42y00x28jUmZQdP3AQilOPdn1xRwf6s-gWi_95d1t0qDe478VnclTIrZ_SmCMtDTTbdU1yvkA80TQ...", "Content-Length"=>"207", "Content-Type"=>"application/json", "User-Agent"=>"rest-client/2.0.2 (darwin19.6.0 x86_64) ruby/2.4.10p364"
    # => 200 OK | application/json 176 bytes       

    RestClient.get "https://bigquery.googleapis.com/bigquery/v2/projects/named-reporter-237205/jobs/job_LnXWC2bcE64hzeBlYMPWNCsMwavn", "Accept"=>"application/json", "Accept-Encoding"=>"gzip, deflate", "Authorization"=>"Bearer ya29.c.Kp8BFQgUT1EOcK5YBwTEv60KokPYvLLWJRFsbfd9S0oGEB3cW5cp1pXTJRZreYPB4B06Z1_YdvhLQByhe9fP_FjziQc6rCtEfGs9zZdMZpXKUFHWEqzG44qxni-jibwaLEgWLw3zaqv42y00x28jUmZQdP3AQilOPdn1xRwf6s-gWi_95d1t0qDe478VnclTIrZ_SmCMtDTTbdU1yvkA80TQ...", "User-Agent"=>"rest-client/2.0.2 (darwin19.6.0 x86_64) ruby/2.4.10p364"
    # => 200 OK | application/json 2062 bytes

    OUTPUT
    {
      "jobId": "abc123",
      "totalRows": 1000,
      "pageToken": "123abc",
      "rows": [
        ...rows...
      ],
      "manualLink": "https://www.example.com"
    }


```

Note that we have used `--verbose` so the SDK gem has printed out more information including the API requests and responses. This also allows you to see the multistep in action, where the Gem allows you to wait before executing a request to check on the job execution.

TIP

You can also use other options like `--output` to save the output of the function to a JSON file.
