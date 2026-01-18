# Workato SDK Documentation

> **Source**: https://docs.workato.com/en/developing-connectors/sdk/guides/building-actions/streaming/download-stream.html
> **Fetched**: 2026-01-18T02:49:51.356435

---

# [#](<#how-to-guides-download-file-via-file-streaming-range-headers>) How-to guides - Download file via file streaming (Range headers)

In this segment, we will be going through the creation of actions that download files in a target application through file streaming.

ACTION TIMEOUT

SDK actions have a 180 second [timeout](</recipes/recipe-job-errors.html#timeouts>) limit.

You can use the [checkpoint!](</developing-connectors/sdk/sdk-reference/ruby_methods.html#checkpoint>) method with file streaming actions to transfer files that exceed the timeout limit. The `checkpoint!` method checks the duration of an action's execution. If it exceeds 120 seconds, Workato refreshes the timeout with a slight delay to ensure fair processing.

## [#](<#sample-connector-egnyte>) Sample connector - Egnyte
```ruby
 
    {
      title: 'My Egnyte connector',

      # More connector code here
      actions: {
        download_object: {
          title: 'Download file from selected folder',

          description: lambda do |input, picklist_label|
            "Download <span class='provider'>file</span> in <span class='provider'>Egnyte</span>"
          end,

          help: 'Download file contents from selected folder in Egnyte.',

          input_fields: lambda do |object_definitions|
            [
              {
                name: 'file_path',
                label: 'File path',
                hint: 'Select path of file.',
                optional: false,
                control_type: 'tree',
                pick_list: 'file_path',
                toggle_hint: 'Select file',
                toggle_field: {
                  name: 'file_path',
                  type: 'string',
                  control_type: 'text',
                  label: 'File path',
                  optional: false,
                  toggle_hint: 'Use file path',
                  hint: "Provide complete path of file. Example: <b>/Private/Sample/file.csv</b>"
                }
              }
            ]
          end,

          execute: lambda do |connection, input|
            file_path = input['file_path']&.gsub(/%2F/, '/')

            # This API call retrieves metadata about the file. Not the file itself. 
            file_details = get("/pubapi/v1/fs/#{file_path}")

            file_details['file_contents'] = workato.stream.out("download_file_by_path", { file_path: file_path, file_size: file_details['size'] })

            file_details
          end,

          output_fields: lambda do |object_definitions|
            [
              { name: 'path' },
              { name: 'name' },
              { name: 'size' },
              { name: 'file_contents' }
            ]
          end
        },
      }

      streams: {
        download_file_by_path: lambda do |input, starting_byte_range, ending_byte_range, requested_byte_size|
          # Example starting_byte_range = 0
          # Example ending_byte_range = 10485759 
          # Example requested_byte_size = 10485760 (10MB)
          chunk = get("/pubapi/v1/fs-content/#{input['file_path']}").
                    headers("Range": "bytes=#{starting_byte_range}-#{ending_byte_range}").
                    response_format_raw
          # The output of the streaming callback should be an array.
          # Firstly, passing the chunk of file
          # Secondly, a boolean value that indicates if this is the final chunk
          [chunk, ending_byte_range >= input['file_size']]
        end
      }

      # More connector code here
    }


```

## [#](<#step-1-action-title-subtitle-description-and-help>) Step 1 - Action title, subtitle, description, and help

The first step to making a good action is to properly communicate what the actions does, how it does it and to provide additional help to users. To do so, Workato allows you to define the title, description, and provide hints for an action. Quite simply, the title is the title of an action and the subtitle provides further details of the action. The description of the action then contains specifications and explanation on what the action accomplishes and in the context of the application it connects to. Finally, the help segment provides users any additional information required to make the action work.

To know more about this step, take a look at our [SDK reference](</developing-connectors/sdk/sdk-reference/actions.html#title>)

## [#](<#step-2-define-input-fields>) Step 2 - Define input fields
```ruby
 
      input_fields: lambda do |object_definitions|
        [
          {
            name: 'file_path',
            label: 'File path',
            hint: 'Select path of file.',
            optional: false,
            control_type: 'tree',
            pick_list: 'file_path',
            toggle_hint: 'Select file',
            toggle_field: {
              name: 'file_path',
              type: 'string',
              control_type: 'text',
              label: 'File path',
              optional: false,
              toggle_hint: 'Use file path',
              hint: "Provide complete path of file. Example: <b>/Private/Sample/file.csv</b>"
            }
          }
        ]
      end


```

![Download file input fields](/assets/img/download_file_input.0581e3c0.png) _Download file input fields_

This component tells Workato what fields to show to a user trying to retrieve an object. In the case of finding a file in Egnyte for example, the user has to input the `file_path` of the file that a user wishes to download.

Object definitions

Note that `object_definitions` is passed in as an argument. Workato allows connector builders to supply the definitions of an object separately in the `object_definitions` key. This key is used when the definitions of an object are large and/or can be dynamically obtained.

To know more about this, take a look at our [SDK reference](</developing-connectors/sdk/sdk-reference/object_definitions.html>)

## [#](<#step-3-defining-the-execute-lambda>) Step 3 - Defining the execute lambda

The execute lambda contains the code that is invoked when the job execution reaches this particular step. In the case of file download actions, there are two main objectives - retrieving the relevant file details (such as name, path and file size) and instantiating a file stream that represents the actual stream of the file contents.

In our example, we first take the `file_path` given from the input and format it by replacing any URL encoded value with the actual intended character, in this case, we replace `%2F` with `/`. Next, we retrieve the `file_details` by sending a request to the `/pubapi/v1/fs/#{file_path}` endpoint. This retrieves all the relevant information we need about this particular file.

Next we add one more attribute to the `file_details` output called `file_contents` which is the instantiated file stream using the `workato.stream.out` method. In this method, we define the `stream` lambda function we want to use - `download_file_by_path` \- as well as pass it a hash `{ file_path: file_path, file_size: file_details['size'] }` which will be passed as the input to the lambda function.
```ruby
 
      execute: lambda do |connection, input|
        file_path = input['file_path']&.gsub(/%2F/, '/')

        # This API call retrieves metadata about the file. Not the file itself. 
        file_details = get("/pubapi/v1/fs/#{file_path}")

        file_details['file_contents'] = workato.stream.out("download_file_by_path", { file_path: file_path, file_size: file_details['size'] })

        file_details
      end,


```

## [#](<#step-4-defining-output-fields>) Step 4 - Defining output fields

This section tells us what datapills to show as the output of the trigger. The `name` attributes of each datapill should match the keys in the output hash of the `execute` lambda function.
```ruby
 
      output_fields: lambda do |object_definitions|
        [
          { name: 'path' },
          { name: 'name' },
          { name: 'size' },
          { name: 'file_contents' }
        ]
      end


```

To know more about the output fields key, take a look at our [SDK reference](</developing-connectors/sdk/sdk-reference/actions.html#output-fields>)

Object definitions

Note that `object_definitions` is passed in as an argument. Workato allows connector builders to supply the definitions of an object separately in the `object_definitions` key. This key is used when the definitions of an object are large and/or can be dynamically obtained.

To know more about this, take a look at our [SDK reference](</developing-connectors/sdk/sdk-reference/object_definitions.html>)

## [#](<#step-5-defining-the-streaming-lambda-function>) Step 5 - Defining the streaming lambda function

The instantiation of a file stream using `workato.stream.out` now needs to be coupled with the specified streaming callback `download_file_by_path`. This is a lambda function defined in the `streams` hash and the main objective of this lambda function is to download a specific chunk of the file given arguments passed to it. We utilize a GET request to the `/pubapi/v1/fs-content/#{file_path}` where we add the headers for `Range` to be from the `starting_byte_range` to the `ending_byte_range`. You must also add `response_format_raw` if the data sent back from the server is the pure binary data and not a JSON response.

Lastly, the output of the streaming callback should be an array of size 2:

  1. The first index is the binary data
  2. The second index is a boolean value that denotes the end of file. In this case, since we can retrieve the expected size (in bytes) of the file, we know that if the ending_byte_range is larger than the file's size, we are at the end of the file.

```ruby
 
      streams: {
        download_file_by_path: lambda do |input, starting_byte_range, ending_byte_range, requested_byte_size|
          # Example starting_byte_range = 0
          # Example ending_byte_range = 10485759 
          # Example requested_byte_size = 10485760 (10MB)
          chunk = get("/pubapi/v1/fs-content/#{input['file_path']}").
                    headers("Range": "bytes=#{starting_byte_range}-#{ending_byte_range}").
                    response_format_raw
          # The output of the streaming callback should be an array.
          # Firstly, passing the chunk of file
          # Secondly, a boolean value that indicates if this is the final chunk
          [chunk, ending_byte_range >= input['file_size']]
        end
      }


```

TIP

Understanding the streaming callback makes most sense when thinking about it alongside a stream consumer. Stream consumers control the streaming callback where it first requests a single chunk of data, uploads it to the downstream system, before reiterating on the process over and over until the entire file is streamed over. As such, the `starting_byte_range` and `ending_byte_range` represent the byte range requested from the streaming consumer. The `requested_byte_size` is a synthetic argument that is useful for comparing the stream producing endpoint has simply no more bytes to provide, indicating the end of file. This signal will be sent over to the stream consumer to continue on with the recipe.
