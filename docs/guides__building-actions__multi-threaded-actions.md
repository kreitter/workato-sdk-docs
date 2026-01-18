# Workato SDK Documentation

> **Source**: https://docs.workato.com/en/developing-connectors/sdk/guides/building-actions/multi-threaded-actions.html
> **Fetched**: 2026-01-18T02:49:47.931159

---

# [#](<#how-to-guides-multi-threaded-actions>) How-to guides - Multi-threaded actions

In this segment, we will be going through the creation of actions that allow you to send requests in parallel across multiple threads. Data throughput can be a key concern for users and in some cases, APIs themselves may only support singleton ingestion endpoints or the batch sizes for requests are simply too low!

For example, imagine that you have thousands of contacts you want to sync into an app like [Intercom (opens new window)](<https://developers.intercom.com/intercom-api-reference/reference#create-contact>) but the API only supports inserting a single contact at a time. You could ask the recipe builder to loop over these contacts and ingest them 1 by 1 but that may lead to slow record ingestion times.

Rather than looping over thousands of contacts, you can use Multi-threaded actions to process them in batches (for example, of batch size 1000) and send API requests in parallel to increase overall throughput and reduce execution time.

NOTE

When you build multi-threaded actions on the SDK CLI tool, take note that requests will be sent sequentially instead of across parallel threads.

This allows you to inspect requests individually for easier debugging.

ACTION TIMEOUT

SDK actions have a 180 second [timeout](</recipes/recipe-job-errors.html#timeouts>) limit.

## [#](<#sample-connector-intercom>) Sample connector - Intercom
```ruby
 
    {
      title: 'My Intercom connector',

      # More connector code here
      actions: {
        create_contact: {
            title: "Create contacts",

            subtitle: "Creates multiple contacts in Intercom",

            description: "Create contacts in Intercom",

            input_fields: lambda do 
              [
                {
                  name: "contacts",
                  type: "array",
                  of: "object",
                  properties: [
                    {
                      control_type: "text",
                      label: "Role",
                      type: "string",
                      name: "role"
                    },
                    {
                      control_type: "text",
                      label: "External ID",
                      type: "string",
                      name: "external_id"
                    },
                    {
                      control_type: "text",
                      label: "Email",
                      type: "string",
                      name: "email"
                    },
                    {
                      control_type: "text",
                      label: "Phone",
                      type: "string",
                      name: "phone"
                    },
                    {
                      control_type: "text",
                      label: "Name",
                      type: "string",
                      name: "name"
                    }
                  ]
                }
              ]
            end,

            execute: lambda do |connection, input, eis, eos|
              # Pre-processing of the data. 
              # For multithreading, we need to create an array of requests which we do over here.
              number_of_batches = input['contacts'].size
              batches = input['contacts'].map do |contact|
                post("contacts", contact)
              end

              # Sending of the requests in simultaneously using the parallel method
              # The output of a method is an array with 3 indexes.
              # The first index is a boolean to indicate that all requests were successful.
              # The second index is an array of the successful responses. Failed requests are indicated
              results = parallel(
                  batches, # Each index in the batch array represents a single request
                  threads: 20, # The max number of threads. Defaults to 1 and max is 20
                  rpm: 100, # How many requests to send per minute
                  )

              # Post-processing
              # Boolean to tell the user that all records were successful
              success = results[0] 
              # An array of all the responses for successful records
              records_ingested = results[1].compact
              # Collecting all the failed records into an array
              records_failed = []
              results[2].each_with_index do |item, index|
                next unless item 
                failed_record = {
                  code: item,
                  record: input['contacts'][index]
                }
                records_failed << failed_record
              end

              {
                success: success,
                records_ingested: records_ingested,
                records_failed: records_failed
              }
            end,

            output_fields: lambda do |object_definitions, config_fields|
              object_definitions['insert_contacts_output']
            end

          },
    }


```

## [#](<#step-1-action-title-subtitle-description-and-help>) Step 1 - Action title, subtitle, description, and help

The first step to making a good action is to properly communicate what the actions does, how it does it and to provide additional help to users. To do so, Workato allows you to define the title, description, and provide hints for an action. Quite simply, the title is the title of an action and the subtitle provides further details of the action. The description of the action then contains specifications and explanation on what the action accomplishes and in the context of the application it connects to. Finally, the help segment provides users any additional information required to make the action work.

To know more about this step, take a look at our [SDK reference](</developing-connectors/sdk/sdk-reference/actions.html#title>)

## [#](<#step-2-define-input-fields>) Step 2 - Define input fields

This component tells Workato what fields to show to a user trying to execute the insert batch action. In the case of inserting a batch of contacts in Intercom for example, the user has to provide us with an array (list) of contacts.
```ruby
 
      input_fields: lambda do 
        [
          {
            name: "contacts",
            type: "array",
            of: "object",
            properties: [
              {
                control_type: "text",
                label: "Role",
                type: "string",
                name: "role"
              },
              {
                control_type: "text",
                label: "External ID",
                type: "string",
                name: "external_id"
              },
              {
                control_type: "text",
                label: "Email",
                type: "string",
                name: "email"
              },
              {
                control_type: "text",
                label: "Phone",
                type: "string",
                name: "phone"
              },
              {
                control_type: "text",
                label: "Name",
                type: "string",
                name: "name"
              }
            ]
          }
        ]
      end,


```

## [#](<#step-3-defining-the-execute-lambda>) Step 3 - Defining the execute lambda

The execute lambda is responsible for

  1. Preparing the series of requests to send in parallel to the API
  2. The actual sending of the request
  3. Any post-processing of the data.

### [#](<#_1-preparing-the-series-of-requests-to-send-in-parallel-to-the-api>) 1\. Preparing the series of requests to send in parallel to the API

In the first part of the execute lambda, we first create an array of requests with a single request for each contact. Take note that the requests are not actually sent out at this point but only when the array of requests is passed to the `parallel` method.
```bash
 
      # Pre-processing of the data. 
      # For multithreading, we need to create an array of requests which we do over here.
      number_of_batches = input['contacts'].size
      batches = input['contacts'].map do |contact|
        post("contacts", contact)
      end


```

### [#](<#_2-sending-of-the-request>) 2\. Sending of the request

In the next step we call the parallel method which takes in the array of requests as well as parameters for the execution like the total number of threads and any throttling of requests required. Take note that `rpm` is optional and excluding it will result in no throttling of requests.
```ruby
 
    results = parallel(
        batches, # Each index in the batch array represents a single request
        threads: 20, # The max number of threads. Defaults to 1 and max is 20
        rpm: 100, # How many requests to send per minute
        )


```

### [#](<#_3-post-processing-of-the-data>) 3\. Post-processing of the data

The output of the parallel method is an array which describes the successful and failed requests in the batch. This is done in the second and third index of the array which correspond to successful responses and failed responses for requests respectively. Take note that `null` values in either array indicate a value in the same position in its counterpart.

**Sample output of the parallel method**
```ruby
 
    [
      false, # Boolean that indicates all requests were successful
      [
        null, # null indicates that this request was unsuccesful
        { ... }, # The response from a successful API call
        # ...
      ],
      [
        "409 Conflict", # the error message from a failed request
        null, # null indicates the request was successful
        # ...
      ],
    ]


```

Lastly, we need to do some transformations to ensure that the output of this action contains both the successfully ingested records and the failed records so the user can retry these failed records or store this somewhere.
```bash
 
      # Post-processing
      # Boolean to tell the user that all records were successful
      success = results[0] 
      # An array of all the responses for successful records
      records_ingested = results[1].compact
      # Collecting all the failed records into an array
      records_failed = []
      results[2].each_with_index do |item, index|
        next unless item 
        failed_record = {
          code: item,
          record: input['contacts'][index]
        }
        records_failed << failed_record
      end

      {
        success: success,
        records_ingested: records_ingested,
        records_failed: records_failed
      }


```

## [#](<#step-4-defining-output-fields>) Step 4 - Defining output fields

This section tells us what datapills to show as the output of the trigger. The `name` attributes of each datapill should match the keys in the output of the `execute` key.
```ruby
 
    output_fields: lambda do |object_definitions, config_fields|
      object_definitions['insert_contacts_output']
    end


```
