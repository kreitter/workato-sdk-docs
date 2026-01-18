# Workato SDK Documentation

> **Source**: https://docs.workato.com/en/developing-connectors/sdk/guides/building-actions/streaming/upload-stream-content-range.html
> **Fetched**: 2026-01-18T02:49:53.669709

---

# [#](<#how-to-guides-upload-file-via-file-streaming-content-range-headers>) How-to guides - Upload file via file streaming (Content-Range headers)

In this segment, we will be going through the creation of actions that uploads files in a target application through file streaming and utilizing Content-Range Headers.

ACTION TIMEOUT

SDK actions have a 180 second [timeout](</recipes/recipe-job-errors.html#timeouts>) limit.

You can use the `checkpoint!` method with file streaming actions to transfer files that exceed the timeout limit. Refer to the [Using our multistep framework to extend upload times](<#using-our-multistep-framework-to-extend-upload-times>) section for additional information.

## [#](<#sample-connector>) Sample connector
```ruby
 
    {
      title: 'Upload file to URL',

      # More connector code here
      actions: {
        upload_to_url: {
          input_fields: lambda do |_object_definitions|
            [
              { name: "file_name", type: "string" },
              { name: "file", type: "stream" }, # field type must be stream
              { name: "url", label: "Any friendly URL" }
            ]
          end,

          execute: lambda do |_connection, input, _input_schema, _output_schema, closure|
            # Calling workato.stream.in runs in a loop where the input should be file. 
            # It can accept both entire files or the output of a streaming-enabled download file action
            workato.stream.in(input["file"]) do |chunk, starting_byte_range, ending_byte_range, eof, next_starting_byte_range| 
              put(input['url']).
                headers("Content-Range": "bytes #{starting_byte_range}-#{ending_byte_range}/*").
                request_body(chunk).presence
            end

            # This commits the upload
            post(input['url'], { "commit": true } )

          end,

          output_fields: lambda do |object_definitions|
            [
              { name: "file_name", type: "string" },
              { name: "file_path", type: "string" },
              { name: "file_size", type: "integer" }
            ]
          end
        }
      }
      # More connector code here
    }


```

## [#](<#step-1-action-title-subtitles-description-and-help>) Step 1 - Action title, subtitles, description, and help

The first step to making a good action is to properly communicate what the actions does, how it does it and to provide additional help to users. To do so, Workato allows you to define the title, subtitles, description, and provide hints for an action. Quite simply, the title is the title of an action and the subtitle provides further details of the action. The description of the action then contains specifications and explanation on what the action accomplishes and in the context of the application it connects to. Finally, the help segment provides users any additional information required to make the action work.

To know more about this step, take a look at our [SDK reference](</developing-connectors/sdk/sdk-reference/actions.html#title>)

## [#](<#step-2-define-input-fields>) Step 2 - Define input fields
```ruby
 
      input_fields: lambda do |object_definitions|
        [
          { name: "file_name", type: "string" },
          { name: "file", type: "stream" }, # field type must be stream
          { name: "url", label: "Any friendly URL" }
        ]
      end,


```

This component tells Workato what fields to show to a user trying to upload an object. In the case of this connector, we collect the `file_name`, the `file` which must be defined with `type` as `stream` and the `url` input for a friendly URL that we can upload this file to.

## [#](<#step-3-defining-the-execute-key>) Step 3 - Defining the execute key

In the execute action, we define the `workato.stream.in` which takes in the `file` stream input.

After calling `workato.stream.in` you're required to define a block that signifies how to upload this particular chunk of data received. In this block, we send a PUT request to the URL alongside standard `Content-Range` headers to denote the part of the file we are uploading. `workato.stream.in` continues to loop over this block until the `stream` consumer dictates that the file has ended.

After the stream is consumed, we send a POST request to commit the entire upload as a new file.
```ruby
 
      execute: lambda do |_connection, input, _input_schema, _output_schema, closure|
        # Calling workato.stream.in runs in a loop where the input should be file. 
        # It can accept both entire files or the output of a streaming-enabled download file action
        workato.stream.in(input["file"]) do |chunk, starting_byte_range, ending_byte_range, eof, next_starting_byte_range| 
          put(input['url']).
            headers("Content-Range": "bytes #{starting_byte_range}-#{ending_byte_range}/*").
            request_body(chunk).
            presence # presence is required as a way to force the HTTP request to be sent. 
        end

        # This commits the upload
        post(input['url'], { "commit": true } )

      end,


```

NOTE

Take note that we assume the API accepts `*` as a wildcard range, indicating that the total file size is not yet known. In some cases, APIs may not accept a wildcard range and you should add an input field to collect the total file size from the recipe builder.

## [#](<#step-4-defining-output-fields>) Step 4 - Defining output fields

This section tells us what datapills to show as the output of the trigger. The `name` attributes of each datapill should match the keys in the output of the `execute` key. Here, we assume the response from the final POST request returns the `file_name`, `file_path` and `file_size`.
```ruby
 
      output_fields: lambda do |object_definitions|
        [
          { name: "file_name", type: "string" },
          { name: "file_path", type: "string" },
          { name: "file_size", type: "integer" }
        ]
      end


```

## [#](<#variations>) Variations

### [#](<#using-our-multistep-framework-to-extend-upload-times>) Using our multistep framework to extend upload times

When defining the `workato.stream.in` method, you are able to define an additional named parameter for `from`, which can be used in conjunction with the `checkpoint!` method to extend the timeout of your upload action beyond Workato's limit of 180 seconds.

When `checkpoint!` is called, it checks if action's current execution time is larger than 120 seconds, and if so, refreshes the action timeout after a short waiting period. This can be used in conjunction with the `from` argument to tell Workato's streaming library where to continue from the last byte offset.
```ruby
 
      execute: lambda do |_connection, input, _input_schema, _output_schema, closure|
        next_from = closure["next_from"].presence || 0
        # Calling workato.stream.in runs in a loop where the input should be file. 
        # It can accept both entire files or the output of a streaming-enabled download file action
        workato.stream.in(input["file"], from: next_from) do |chunk, starting_byte_range, ending_byte_range, eof, next_starting_byte_range| 
          put(input['url']).
            headers("Content-Range": "bytes #{starting_byte_range}-#{ending_byte_range}/*").
            request_body(chunk).
            presence # presence is required as a way to force the HTTP request to be sent. 

            # Call checkpoint unless it is the end of file.
            checkpoint!(continue: { next_from: next_starting_byte_range }) unless eof
        end

        # This commits the upload
        post(input['url'], { "commit": true } )

      end


```

### [#](<#adjusting-the-default-10mb-chunk-size>) Adjusting the default 10MB chunk size

When Workato attempts to retrieve a file chunk from an API, it defaults to requesting a 10MB chunk. In some cases, your API may require a larger minimum chunk size and you can override this default by declaring your own chunk size using the `frame_size` argument.

Take note that this does not guarantee that you will receive a chunk size of 20MB from all producers. You can make necessary precautions by storing a temporary buffer as well.
```ruby
 
      execute: lambda do |_connection, input, _input_schema, _output_schema, closure|
        # 20MB in bytes
        frame_size = 20971520 
        next_from = closure["next_from"].presence || 0
        buffer = ""
        # Calling workato.stream.in runs in a loop where the input should be file. 
        # It can accept both entire files or the output of a streaming-enabled download file action
        workato.stream.in(input["file"], from: next_from, frame_size: frame_size) do |chunk, starting_byte_range, ending_byte_range, eof, next_starting_byte_range| 
          # save chunk to buffer
          buffer << chunk

          # If not end of file and buffer is less than require size, skip to next iteration
          if !eof && buffer.size < frame_size
            next
          end
          put(input['url']).
            headers("Content-Range": "bytes #{starting_byte_range}-#{ending_byte_range}/*").
            request_body(buffer).
            presence # presence is required as a way to force the HTTP request to be sent. 

          #reset buffer
          buffer = ""

          # Call checkpoint unless it is the end of file.
          checkpoint!(continue: { next_from: next_starting_byte_range }) unless eof
        end

        # This commits the upload
        post(input['url'], { "commit": true } )

      end


```
