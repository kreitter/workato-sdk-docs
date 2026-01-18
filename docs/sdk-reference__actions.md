# Workato SDK Documentation

> **Source**: https://docs.workato.com/en/developing-connectors/sdk/sdk-reference/actions.html
> **Fetched**: 2026-01-18T02:50:24.506262

---

# [#](<#sdk-reference-actions>) SDK Reference - `actions`

This section enumerates all the possible keys to define an action.

Quick Overview

The `actions` key can only be used in both recipes and the SDK **Test code** tab after you have created a successful connection. Actions receive data from earlier steps in a recipe via datapills, send a request to an endpoint and present the response as datapills.

## [#](<#structure>) Structure
```ruby
 
        actions: {

          [Unique_action_name]: {
            title: String,

            subtitle: String,

            description: lambda do |input, picklist_label|
              String
            end,

            help: lambda do |input, picklist_label|
              Hash
            end,

            display_priority: Integer,

            batch: Boolean,

            bulk: Boolean,

            deprecated: Boolean,

            config_fields: Array

            input_fields: lambda do |object_definitions, connection, config_fields|
              Array
            end,

            execute: lambda do |connection, input, extended_input_schema, extended_output_schema, continue|
              Hash
            end,

            output_fields: lambda do |object_definitions, connection, config_fields|
              Array
            end,

            sample_output: lambda do |connection, input|
              Hash
            end,

            retry_on_response: Array,

            retry_on_request: Array,

            max_retries: Int,

            summarize_input: Array,

            summarize_output: Array
          },

          [Another_unique_action_name]: {
            ...
          }
        },


```

* * *

## [#](<#title>) `title`

Attribute | Description  
---|---  
Key | `title`  
Type | String  
Required | Optional. Defaults to title built from labeled key.  
Description | This allows you to define the title of your action, which might differ from the name of the key assigned to it - Key = `search_object_query`, title = `"Search object via query"`  
Expected Output | `String`   
i.e. `"Search object via query"`  
UI reference | ![](/assets/img/title.48365f4d.png)  

TIP

In Workato, we generally advise the following structure "[Verb] [Object]" - "Create lead" or "Search object" rather than "Lead created".

* * *

## [#](<#subtitle>) `subtitle`

Attribute | Description  
---|---  
Key | `subtitle`  
Type | String  
Required | Optional. Defaults to subtitle inferred from connector name and action title.  
Description | This allows you to define the subtitle of your action.  
Expected Output | `String`   
i.e. `"Use complex queries to search objects in Percolate"`  
UI reference | ![](/assets/img/subtitle.9fbdfa1b.png)  

TIP

To make your subtitles meaningful, try to provide more information in here whilst keeping your titles concise. For example, your title could be "Create object" whereas your subtitle could be "Create objects like leads, customers, and accounts in Salesforce." When users search for a specific action, Workato also searches for matches in the subtitle.

* * *

## [#](<#description>) `description`

Attribute | Description  
---|---  
Key | `description`  
Type | lambda function  
Required | Optional. Defaults to description inferred from connector name and action title.  
Description | This allows you to define the description of your action when viewed in the recipe editor. This can be a static description or a dynamic one based on your needs.  
Possible Arguments | `input` \- Hash representing user given inputs defined in `input_fields`   
`picklist_label` \- Only applicable for picklists where a user's answer consist of both a picklist label and value. This Hash represents the label for a user's given inputs for picklist fields. See below for use cases.  
Expected Output | `String`   
i.e. `"Create a <span class='provider'>campaign</span> in <span class='provider'>Percolate</span>"` Add the `<span>` HTML tags to add weight to your description text.  
UI reference | ![](data:image/png;base64,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)  
Example - description:

For the `description` lambda function, you have access to two arguments to make your descriptions dynamic. This is useful when you want to change your description based on how a given user has configured the action. These changes can be incredibly useful for your users to ensure they know what this action is doing without having to click and view the action's configuration to understand what it does.
```ruby
 
        create_object: {
          description: lambda do |input, picklist_label|
            "Create a <span class='provider'>#{picklist_label['object'] || 'object'}</span> in " \
            "<span class='provider'>Percolate</span>"
          end,

          config_fields: [
            {
              name: 'object',
              control_type: 'select',
              pick_list: 'object_types',
              optional: false
            }
          ]

          # More keys to define the action
        }


```

In the preceding example, the action is a generic object action that allows the user to choose between multiple object types when configuring the recipe. You can change the description of the object the user selects by referencing the `picklist_label` argument.

![](/assets/img/description-example.52d7ecb5.gif)

* * *

## [#](<#help>) `help`

Attribute | Description  
---|---  
Key | `help`  
Type | lambda function  
Required | Optional. No help is displayed otherwise.  
Description | The help text that is meant to guide your users as to how to configure this action. You can also point them to documentation.  
Possible Arguments | `input` \- Hash representing user given inputs defined in `input_fields`   
`picklist_label` \- Only applicable for picklists where a user's answer consist of both a picklist label and value. This Hash represents the label for a user's given inputs for picklist fields. See below for use cases.  
Expected Output | `Hash` or `String` See below for examples.  
UI reference | ![](data:image/png;base64,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)  
Example - help:

The output of the `help` lambda function can either be a simple String or a Hash. Below we go through the two examples:

  * String

```ruby
 
        help: lambda do |input, picklist_label|
          'Create an object in Percolate. First, select from a list of ' \
          'objects that we currently support. After selecting your object,' \
          ' dynamic input fields specific to your scope and object selected ' \
          'will be populated.' \
          ' Creating an approval denotes submitting a specified piece of content' \
          ' or campaign for a specific approval workflow.'
        end,


```

  * Hash

```ruby
 
        help: lambda do |input, picklist_label|
          {
            body: "First, filter by the object you want then fill up the input fields " \
            "which appear based on the object you have selected. Amongst other things, " \
            "you’ll be able to search for contacts in your company and cloud recordings from the past. ",
            learn_more_url: "https://docs.workato.com/connectors/zoom/event-actions.html#search-event-details",
            learn_more_text: "Learn more"
          }
        end,


```

![](/assets/img/help-example.bdfb4b3c.png)

* * *

## [#](<#display-priority>) `display_priority`

Attribute | Description  
---|---  
Key | `display_priority`  
Type | Integer  
Required | Optional. Defaults to zero, otherwise to the alphabetical ordering of actions titles.  
Description | This allows you to influence the ordering of the action in the recipe editor so that you can highlight top actions. The higher the integer, the higher the priority. If two actions have the same priority, they are ordered by their titles.  

* * *

## [#](<#batch>) `batch`

Attribute | Description  
---|---  
Key | `batch`  
Type | Boolean  
Required | Optional.  
Description | This presents a "Batch" tag next to your action to indicate that this action works with multiple records. Normally used in batch triggers or batch create/update/upsert actions where users can pass a list of records.  
UI reference | ![](data:image/png;base64,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)  

* * *

## [#](<#bulk>) `bulk`

Attribute | Description  
---|---  
Key | `bulk`  
Type | Boolean  
Required | Optional.  
Description | This presents a "Bulk" tag next to your action to indicate that this action works with a large flat file of records. Normally used bulk create/update/upsert actions where users pass a CSV of records.  
UI reference | ![](/assets/img/bulk.1d2a80e6.png)  

* * *

## [#](<#deprecated>) `deprecated`

Attribute | Description  
---|---  
Key | `deprecated`  
Type | Boolean  
Required | Optional.  
Description | This presents a "deprecated" tag next to your action to indicate that this action has been deprecated. Recipes which used to use this action will continue to work but future recipes will not be able to search and select this action.  
UI reference | ![](/assets/img/deprecated.3e09de36.png)  

TIP

Deprecation is a great way to move users to new actions when changes are not backwards compatible. This gives you more freedom to make your actions more usable or cater for upcoming API changes.

* * *

## [#](<#config-fields>) `config_fields`

Attribute | Description  
---|---  
Key | `config_fields`  
Type | Array  
Required | Optional.  
Description | This key accepts an array of hashes which show up as input fields shown to a user. Config fields are shown to a user before input fields are rendered and can be used to alter what set of input fields are shown to an end user. This is often used in generic object actions where config fields prompt a user to select the object and input fields are rendered based on that selection. To know more about how to define config fields in Workato, click [here.](</developing-connectors/sdk/sdk-reference/schema.html>)  
Expected Output | Array of hashes. Each hash in this array corresponds to a separate config field.  
UI reference | ![](/assets/img/config_fields.02e2eb97.gif)  

TIP

Config fields are powerful tools to introduce dynamic behavior to your actions. Use them to make your connector easier to use and discover new features. In the example gif above, you can see that the input "Event" actually causes more input fields to render. These input fields are rendered based on the selection of the value "Meeting".

* * *

## [#](<#input-fields>) `input_fields`

Attribute | Description  
---|---  
Key | `input_fields`  
Type | lambda function  
Required | True  
Description | This lambda function allows you to define what input fields should be shown to a user configuring this action in the recipe editor. Output of this lambda function should be an array of hashes, where each hash in this array corresponds to a separate input field. To know more about how to define input fields in Workato, click [here.](</developing-connectors/sdk/sdk-reference/schema.html>)  
Possible Arguments | `object_definitions` \- Allows you to reference an object definitions. Object definitions are stores of these arrays hashes which may be used to represent both input fields or output fields (datapills). These can be referenced by any action or trigger.   
`connection` \- Hash representing user given inputs defined in `connection`.   
`config_fields` \- Hash representing user given inputs defined in `config_fields`, if applicable.  
Expected Output | Array of hashes. Each hash in this array corresponds to a separate input field.  
UI reference | ![](/assets/img/input_fields.a652188c.png)  

* * *

## [#](<#execute>) `execute`

Attribute | Description  
---|---  
Key | `execute`  
Type | lambda function  
Required | True  
Description | This lambda function allows you to define what this action does with the inputs that have been passed to it from an end user. These inputs may be static values or datapills from upstream actions or the trigger. These are then used to send a HTTP request to retrieve data that can be presented as datapills.   

Optionally, you can also use the execute lambda function to do any pre-processing of input data before sending it as a request and post-processing of response data before passing it out as datapills.  
Possible Arguments | `connection` \- Hash representing user given inputs defined in `Connection`   
`input` \- Hash representing user given inputs defined in `input_fields`   
`extended_input_schema` \- See below for examples.   
`extended_output_schema` \- See below for examples   
`continue` \- Hash representing cursor from the previous invocation of execute. OPTIONAL and used for asynchronous actions. See below for examples.  
Expected Output | Hash representing the data to be mapped to the output datapills of this action.  
Example - execute: - extended_input_schema and extended_output_schema

Extended input and output schema is any schema from `object_definitions` that is used in your action. This information is often useful when you dynamically generate schema and you want to use it to do data pre- or post-processing. These arguments do not include config_fields.

For example, you may use extended_input_schema to know which inputs are datetimes and should be transformed to Epoch time which is accepted by the target API. In the same fashion, you may use extended_output_schema to take the response and transform Epoch variables into ISO8601 datetimes again.
```ruby
 
        create_object: {
          description: lambda do |input, picklist_label|
            "Create a <span class='provider'>#{picklist_label['object'] || 'object'}</span> in " \
            "<span class='provider'>Percolate</span>"
          end,

          config_fields: [
            {
              name: 'object',
              control_type: 'select',
              pick_list: 'object_types',
              optional: false
            }
          ],

          input_fields: lambda do |object_definitions, connection, config_fields|
            object = config_fields['object']
            object_definitions[object].ignored('id')
          end,

         execute: lambda do |connection, input, extended_input_schema, extended_output_schema|
           puts extended_input_schema
           # [
           #   {
           #     "type": "string",
           #     "name": "status",
           #     "control_type": "select",
           #     "label": "Status",
           #     "hint": "Status is required for creating Content",
           #     "pick_list": "post_statuses",
           #     "optional": false
           #   },
           #   ...
           # ]

           puts extended_output_schema
           # [
           #   {
           #     "type": "string",
           #     "name": "id",
           #     "control_type": "text",
           #     "label": "Content ID",
           #     "hint": "The Content ID, Example: <b>post:45565410</b>.",
           #     "optional": true
           #   },
           #   {
           #     "type": "string",
           #     "name": "status",
           #     "control_type": "select",
           #     "label": "Status",
           #     "hint": "Status is required for creating Content",
           #     "pick_list": "post_statuses",
           #     "optional": false
           #   },
           #   ...
           # ]
         end,

         output_fields: lambda do |object_definitions, connection, config_fields|
           object = config_fields['object']
           object_definitions[object]
          end,
        }


```

Example - execute: - continue

When working with asynchronous APIs to kickstart a long running job or process in a target application, often times you'll send a request and expect an ID that corresponds to that job or process. Your action would then want to constantly check back with the API to see if the job is completed before retrieving results or moving on to the next step in the recipe.

For example, when you send a request to Google BigQuery to start a query, Google BigQuery might send you back the job ID. Your task would be to now regularly check back with Google BigQuery to see if the query is completed before retrieving the rows.

Rather than having the user configure this logic in the recipe, you can now embed this entire logic into a single action with "multi-step" actions on your custom connector. To use "multi-step" actions, the `continue` argument is used in conjunction with a dedicated method called `reinvoke_after`. Below, we go through some examples of what the `continue` argument might be.

To learn more about creating your "multistep" actions, read our guide [here](</developing-connectors/sdk/guides/building-actions/multistep-actions.html>).
```ruby
 
        multistep_action_sample: {
          input_fields: lambda do |object_definitions, connection, config_fields|

          end,

         execute: lambda do |connection, input, e_i_s, e_o_s, continue|

          if !continue.present? #continue is nil on the first invocation of the execute
            puts continue
            # nil
            reinvoke_after(seconds: 100, continue: { current_step: 1 })
          elsif continue['current_step'] == 1 #first reinvocation
            puts continue
            # {
            #   "current_step": 1
            # }
            reinvoke_after(seconds: 100, continue: { current_step: continue['current_step'] + 1 })
          else
            puts continue
            # {
            #   "current_step": 2
            # }
          end

         end,

         output_fields: lambda do |object_definitions, connection, config_fields|

          end,
        }


```

* * *

## [#](<#before-suspend>) `before_suspend`

Attribute | Description  
---|---  
Key | `before_suspend`  
Type | lambda function  
Required | False  
Description | This lambda function is exclusive to [Wait for resume actions](</developing-connectors/sdk/guides/building-actions/wait-for-resume-actions.html>). It is invoked after the `suspend` method is called in the `execute` lambda. It allows you to define an authenticated API request based on the `apply` to an external system to register a callback to resume the job.  
Possible arguments | 

  * `resume_token`: This token is specific to a particular job and is generated by the Workato framework. When the external system intends to resume a job, it must include this token in its resume request to the Resume job API.
  * `expires_at`: Timestamp in PST representing the time the job expires and resumes with a timeout.
  * `continue`: The `continue` hash passed from the `suspend` method. This can contain important information including the ID of the process in the external system.

Expected output | N/A  

* * *

## [#](<#before-resume>) `before_resume`

Attribute | Description  
---|---  
Key | `before_resume`  
Type | lambda function  
Required | False  
Description | This lambda function is exclusive to [Wait for resume actions](</developing-connectors/sdk/guides/building-actions/wait-for-resume-actions.html>). It is invoked after the external system has dispatched the API request to resume the job. It enables you to control the state of the `continue` hash, which is transmitted back to the `execute` lambda when the job resumes. Additionally, it grants access to the data value in the API request.  
Possible arguments | 

  * `data`: This represents the `data` value in the API request to resume the job.
  * `input`: The input that the recipe sends directly to the action.
  * `continue`: The `continue` hash passed from the `suspend` method. This can contain important information, including the ID of the process in the external system.

Expected output | N/A   
However, the lambda allows you to edit the value of the `continue` hash.  
Example- Edit the value of the continue hash

This example demonstrates how to edit the value of the `continue` hash.

If the `continue` method passed from the `suspend` method is:
```ruby
 
    {
      "state": "suspended",
      "job_id": "abc_123"
    }


```

and the `before_resume` lambda is:
```ruby
 
    before_resume: lambda do |data, input, continue|
      if continue["state"] == "suspended"
        continue["state"] = "resumed"
        continue["payload"] = "important data"
      else
        { "result" => "Unexpected state" }
      end
    end,


```

Then the `continue` argument passed to the `execute` lambda looks like this:
```ruby
 
    {
      "state": "resumed",
      "job_id": "abc_123",
      "payload": "important data"
    }


```

* * *

## [#](<#before-timeout-resume>) `before_timeout_resume`

Attribute | Description  
---|---  
Key | `before_timeout_resume`  
Type | lambda function  
Required | False  
Description | This lambda function is exclusive to [Wait for resume actions](</developing-connectors/sdk/guides/building-actions/wait-for-resume-actions.html>). It is invoked when the `expires_at` time has passed and Workato has not received an API request to resume the job. It allows you to manage the state of the `continue` hash which is passed back to the `execute` lambda when the job resumes.  
Possible arguments | 

  * `input`: The input that the recipe sends directly to the action.
  * `continue`: The `continue` hash passed from the `suspend` method. This can contain important information, including the ID of the process in the external system.

Expected output | N/A  
However, the lambda allows you to edit the value of the `continue hash`. Refer to the `before_resume` example to learn more.  

* * *

## [#](<#output-fields>) `output_fields`

Attribute | Description  
---|---  
Key | `output_fields`  
Type | lambda function  
Required | True  
Description | This lambda function allows you to define what output fields (datapills) should be shown to a user configuring this action in the recipe editor. The output of this lambda function should be an array of hashes, where each hash in this array corresponds to a separate output field (datapill). To know more about how to define input fields in Workato, click [here.](</developing-connectors/sdk/sdk-reference/schema.html>)  
Possible Arguments | `object_definitions` \- Allows you to reference an object definitions. Object definitions are stores of these arrays which can represent either input and output fields. These can be referenced by any action or trigger.   
`connection` \- Hash representing user given inputs defined in `connection`.   
`config_fields` \- Hash representing user given inputs defined in `config_fields`, if applicable.  
Expected Output | Array of hashes. Each hash in this array corresponds to a separate input field.  
UI reference | ![](/assets/img/output_fields.ea775e7c.png)  
Example - output_fields:

Output fields relate directly to the datapills that users see in the recipe editor. The definition of these output fields are mapped to the output of the `execute` lambda function which is a hash.
```ruby
 
        create_object: {
         execute: lambda do |connection, input, extended_input_schema, extended_output_schema|
           post("/object/create", input)
           # JSON response passed out of the execute: lambda function.
           #  {
           #    "id": 142414,
           #    "title": "Newly created object",
           #    "description": "This was created via an API"
           #  }
         end,

         output_fields: lambda do |object_definitions, connection, config_fields|
           [
             {
               name: "id",
               type: "integer"
             },
             {
               name: "title",
               type: "string"
             },
             {
               name: "description",
               type: "string"
             }
           ]
          end,
        }


```

* * *

## [#](<#sample-output>) `sample_output`

Attribute | Description  
---|---  
Key | `sample_output`  
Type | lambda function  
Required | False.  
Description | This lambda function allows you to define a sample output that is displayed next to your output fields (datapills).  
Possible Arguments | `connection` \- Hash representing user given inputs defined in `connection`.   
`input` \- Hash representing user given inputs defined in `input_fields`  
Expected Output | Hash. This hash should be a stubbed output of the `execute` lambda function.  
UI reference | ![](/assets/img/sample_output.1785f345.png)  

* * *

## [#](<#retry-on-response>) `retry_on_response`

Attribute | Description  
---|---  
Key | `retry_on_response`  
Type | Array  
Required | False.  
Description | **Used in conjunction with retry_on_request: and max_retries:**   

Use this declaration to implement a retry mechanism for certain HTTP methods and responses. This guards against APIs which may sometime return errors due to server failure such as 500 Internal Server Error codes.   

When supplying this array, we will accept what error codes to retry on as well as entire string or regex expressions.   

In cases where no error code is defined, Workato will only search the message body for any given regex or plain string IF the error codes fall under a default list of codes: (429, 500, 502, 503, 504, 507). When supplying an entire string instead of regex, this will give only retry if the entire response matches exactly.   

If entire strings or regex match and error codes are defined, both the error codes and strings must match for retries to be triggered  
Expected Output | Array. For example, `[500]` or `[500,/error/]` or `[‘“error”’, 500]`  

* * *

## [#](<#retry-on-request>) `retry_on_request`

Attribute | Description  
---|---  
Key | `retry_on_request`  
Type | Array  
Required | False.  
Description | **Used in conjunction with retry_on_request: and max_retries:**   

Use this declaration to implement a retry mechanism for certain HTTP methods and responses. This guards against APIs which may sometime return errors due to server failure such as 500 Internal Server Error codes.   

Optional. When not defined, it defaults to only “GET” and “HEAD” HTTP requests.  
Expected Output | Array. For example, `[“GET”]` or `[“GET”, “HEAD”]`  

* * *

## [#](<#max-retries>) `max_retries`

Attribute | Description  
---|---  
Key | `max_retries`  
Type | Int  
Required | False.  
Description | **Used in conjunction with retry_on_request: and max_retries:**   

Use this declaration to implement a retry mechanism for certain HTTP methods and responses. This guards against APIs which may sometime return errors due to server failure such as 500 Internal Server Error codes.   

The number of retries. A maximum of 3 allowed. If more than 3, action retries 3 times.   

Workato waits 5 seconds for the first retry and increases the interval by 5 seconds for each subsequent retry.  
Expected Output | Int. For example, `1` or `2`  

TIP

  * We recommend using only one HTTP method per action if possible
  * Multiple GET requests within a single action are also possible
  * Since we retry on an action level, actions should be defined to only at most only one POST request. This guards against cases where the first post request succeeds and the second post request fails.

Example - Implementing the retry mechanism

Retrying an API request is very useful in ensuring that your actions (and recipes) are tolerant to any inconsistencies in the target App. To implement this, you will need to use a combination of the retry_on_response:, retry_on_request: and max_retries: keys.
```ruby
 
        actions: {
          custom_http: {
            input_fields: lambda do |object_definitions|
              [{ name: 'url', optional: false }]
            end,

            execute: lambda do |_connection, input|
              {
                results: get(input['url'])
              }
            end,

            output_fields: lambda do |object_definitions|
              []
            end,

            retry_on_response: [500, /error/] # contains error codes and error message match rules

            retry_on_request: ["GET", "HEAD"],

            max_retries: 3
          }
        }


```

* * *

## [#](<#summarize-input>) `summarize_input`

Attribute | Description  
---|---  
Key | `summarize_input`  
Type | Array  
Required | False.  
Description | Use this to summarize your input which contain long lists. Summarizing your input is important to keep the jobs page lightweight so it can load quickly. In general, when your input has lists that are longer than 100 lines, they should be summarized.  
Expected Output | Array. For example, `['leads']` or `['report.records', 'report.description']`  

* * *

## [#](<#summarize-output>) `summarize_output`

Attribute | Description  
---|---  
Key | `summarize_output`  
Type | Array  
Required | False.  
Description | Use this to summarize your actions output which contain long lists. Summarizing your output is important to keep the jobs page lightweight so it can load quickly. In general, when your output has lists that are longer than 100 lines, they should be summarized.  
Expected Output | Array. For example, `['leads']` or `['report.records', 'report.description']`  
UI reference | ![](/assets/img/job_input_summarized.631f2b8f.png)  
Example - Summarizing inputs and outputs in job data

When working with large arrays or data, Workato tries to show all the data in the input and output tabs of the job for each action. Sometimes, this can get confusing when we are working with a large numbers of records or large strings. You can use the `summarize_input` and `summarize_output` keys to summarize the data in your job input and output tabs to make it more human readable for users of your connector.
```ruby
 
        input_fields: lambda do
          [
            {
              name: 'report',
              type: 'object',
              properties: [
                {
                  name: 'records',
                  type: :array,
                  of: :object,
                  properties: [
                    {
                      name: 'item_name',
                      type: 'string'
                    }
                  ]
                },
                {
                  name: 'description',
                  type: 'string'
                },
                {
                  name: 'comment',
                  type: 'string'
                }
              ],
            }
          ]
        end,

        summarize_input: ['report.records', 'report.description'],


```
