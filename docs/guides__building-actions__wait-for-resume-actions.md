# Workato SDK Documentation

> **Source**: https://docs.workato.com/en/developing-connectors/sdk/guides/building-actions/wait-for-resume-actions.html
> **Fetched**: 2026-01-18T02:49:55.998402

---

# [#](<#wait-for-resume-actions>) Wait for resume actions

This article describes how to configure Wait for resume actions. This feature allows you to build actions capable of executing the following tasks:

  * Send an API request to an external system to start a long-running process. For example, you can start a batch processing job or send a document for approval.
  * Suspend the job in Workato after the request is sent.
  * Wait for the external system to send an authenticated request back to Workato with a payload.
  * Resume the job with the payload to continue downstream recipe steps.

ACTION TIMEOUT

SDK actions have a 180 second [timeout](</recipes/recipe-job-errors.html#timeouts>) limit.

## [#](<#example-use-cases>) Example use cases

You can use Wait for resume actions to achieve the following use cases:

  * Simulate a chat flow within a single recipe. This is similar to Workbot's "Wait for user input/action" feature.
  * Wait for document approvals in an external system. When approved, the recipe continues immediately.
  * Build process flows for records in an external system. For example, you can build a workflow that gathers leads from Marketo, and only proceeds when data collection is complete.

## [#](<#prerequisites>) Prerequisites

If you plan to use this action to send a request to an external system, the external system you choose must be able to send an authenticated request back to Workato's developer APIs.

Additionally, the external system must be able to store a resume token, which is sent alongside the authenticated request to Workato's developer APIs. This token indicates which job Workato should resume.

## [#](<#how-to-implement-wait-for-resume-actions>) How to implement Wait for resume actions

Two crucial components facilitate the functionality of Wait for resume actions:

  * [SDK code](<#sdk-code>): Use SDK code within actions to suspend and resume recipe workflows.
  * [API requests](<#api-requests>): Send API requests from third-party applications to Workato's developer APIs to resume jobs.

### [#](<#sdk-code>) SDK code

On the SDK level, there are new callbacks in actions that enable you to suspend and resume calls. Learn how it works in this [sample custom connector (opens new window)](<https://app.workato.com/custom_adapters/497423/details?token=a0fc7274b82f4a75fc5f6867608cff1850fd32b29f99ea051df3677c5176f450>).

Sample custom connector code
```ruby
 
    {
      actions: {
        wait_for_webhook: {
          config_fields: [
            {
              name: 'url',
              label: 'API endpoint',
              hint: 'We will send a POST request to this endpoint with the resume token',
              optional: false
            },
            {
              name: 'payload_schema',
              optional: true,
              sticky: true,
              schema_neutral: true,
              control_type: 'schema-designer',
              sample_data_type: 'json_input',
            }
          ],      
          execute: lambda do |_connection, input, _input_schema, _output_schema, continue|
            if continue.blank?
              # Calling suspend will put the job to sleep, after the request in the proc is executed. 
              # in this case we send a POST request to the URL provided by the recipe builder
              # expires_at is configurable and once the time is reached, the job is resumed
              suspend(continue: { "state" => "suspended", "url" => input['url']}, expires_at: 10.minutes.from_now)
            elsif continue["state"] == "resumed" 
              { "result" => "resumed", "payload" =>  continue["payload"]}
            elsif continue["state"] == "suspend_timeout"
              { "result" => "suspend_timeout" }
            else
              { "result" => "Unexpected state" }
            end
          end,
          # When suspend is called, this lambda is executed to suspend the job
          # The lambda receives 3 arguments
          # The resume token is an opaque token that must be stored in the external system. This will be used to identify the job to resume
          # expires_at is the time when the job resumes with a timeout
          # continue is the argument passed
          before_suspend: lambda do |resume_token, expires_at, continue|
            response = post(continue['url'], { expires_at: expires_at, resume_token: resume_token } )      
          end,
          # Allows you to manipulate or add data before the resume.
          # We change the state of the "continue" argument
          # We also add the payload data into the "continue" argument
          # After this lambda is called, the "execute" lambda is called with the "continue" argument
          before_resume: lambda do |data, input, continue|
            if continue["state"] == "suspended"
              continue["state"] = "resumed"
              continue["payload"] = data
            else
              { "result" => "Unexpected state" }
            end
          end,
          # Allows you to manipulate or add data before the resume due to a timeout
          # We change the state of the "continue" argument
          # After this lambda is called, the "execute" lambda is called with the "continue" argument
          before_timeout_resume: lambda do |input, continue|
            if continue["state"] == "suspended"
              continue["state"] = "suspend_timeout"
            else
              { "result" => "Unexpected state" }
            end
          end,
          output_fields: lambda do |object_definition|
            object_definition['output']
          end
        }
      }
    }


```

This guide does not elaborate on the details of the standard attributes of the action. Refer to our [SDK actions reference](</developing-connectors/sdk/sdk-reference/actions.html>) documentation to learn about the basic structure of actions.

There are four lambdas in the action hash that are foundational for Wait for resume actions:

#### [#](<#execute>) `execute`

This lambda operates similarly to standard [Multistep actions](</developing-connectors/sdk/guides/building-actions/multistep-actions.html>). Its primary purpose is to preprocess data from user input and determine the final output of the action when it resumes. This is facilitated by the `continue` argument, which is `nil` the first time the action is invoked. The `continue` argument also contains the output of either the `before_resume` or `before_timeout_resume` lambdas when resumed.

For the Wait for resume action to function properly, the execute lambda must invoke the `suspend` method, which initiates the suspension of the job.

Refer to our [suspend method reference](</developing-connectors/sdk/sdk-reference/ruby_methods.html#suspend>) documentation for more information.

#### [#](<#before-suspend>) `before_suspend`

This lambda is specific to Wait for resume actions and is invoked when the suspend method is called. It primarily registers the resume token with the external application, guiding it on how to resume this specific job.

View our [key reference](</developing-connectors/sdk/sdk-reference/actions.html#before-suspend>) documentation for more information.

#### [#](<#before-resume>) `before_resume`

This lambda is specific to Wait for resume actions and is invoked when Workato receives an API request to resume the job. Its primary purpose is to offer you a hook to manipulate data if necessary and manage the state of the `continue` argument before transferring execution to the `execute` lambda.

View our [key reference](</developing-connectors/sdk/sdk-reference/actions.html#before-resume>) documentation for more information.

#### [#](<#before-timeout-resume>) `before_timeout_resume`

This lambda is specific to Wait for resume actions and is invoked when the `expires_at` time passes before Workato receives an API request to resume the job. Its primary purpose is to offer you a hook to manipulate data if necessary and manage the state of the `continue` argument before transferring execution to the `execute` lambda.

View our [key reference](</developing-connectors/sdk/sdk-reference/actions.html#before-timeout-resume>) documentation for more information.

### [#](<#api-requests>) API requests

To resume the job from the external system, the external system must be capable of dispatching an authenticated API request to Workato's [developer API](</workato-api.html>).

#### [#](<#resume-job>) Resume job

The Resume job endpoint resumes a suspended job based on the `resume_token` you provide. The endpoint returns `204` responses with no content.

View our [Resume job](</workato-api/jobs.html#job-resume>) API documentation to learn how to use this endpoint.

## [#](<#limitations>) Limitations

  * API requests in the `execute` lambda must be called with `.presence`. Because API requests are lazy-loaded in the `execute` lambda, any request defined before the `suspend` method must be forced to execute using `.presence` chained after the request.

  * Maximum time to suspend: The maximum time you can suspend a job is 60 days.

  * Rate limits: The developer API has a rate limit of 100 requests each minute for this action.

  * Resume payload maximum size: The maximum payload size is 50MB.
