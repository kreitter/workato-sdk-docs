# Workato SDK Documentation

> **Source**: https://docs.workato.com/en/developing-connectors/sdk/sdk-reference/streams.html
> **Fetched**: 2026-01-18T02:50:36.401590

---

# [#](<#sdk-reference-streams>) SDK Reference - `streams`

This section enumerates all the possible keys to define a streaming callback that enables you to create file stream producing actions. [Learn more about file streaming.](</developing-connectors/sdk/guides/building-actions/streaming.html>)

Quick overview

The `streams` key must be used in conjunction with an action or trigger. It enables you to download large amounts of data such as a CSV file or video in chunks from a compatible API. This allows you to build actions that can connect to Workato's ecosystem of file storage providers such as Workato Files, Google Cloud Storage, S3 and many more.

## [#](<#structure>) Structure
```ruby
 
        streams: {

          [Unique_stream_name]: lambda do |input, starting_byte_range, ending_byte_range, byte_size|
            Array
          end, 

          [Another_unique_stream_name]: lambda do |input, starting_byte_range, ending_byte_range, byte_size|
            Array
          end, 
        },


```

* * *

Attribute | Description  
---|---  
Key | `[Unique_stream_name]`  
Type | lambda function  
Description | This lambda function can be invoked by any streaming action using the `workato.stream.out` callback.  
Possible Arguments | `input` \- Hash representing user given inputs defined in `workato.stream.out`   
`starting_byte_range` \- Integer representing the requested start byte range for this particular chunk.   
`ending_byte_range`\- Integer representing the requested ending byte range for this particular chunk.   
`byte_size`\- Integer representing the exact amount of bytes for this particular chunk.  
Expected Output | Array of size 2. The first index represents the actual bytes for this particular chunk. The second index is a boolean value that tells the Workato framework whether this is the last chunk in the file.  
Creating a file stream

File streams on Workato are made by leveraging the common [HTTP RFC standard for `Range` headers (opens new window)](<https://datatracker.ietf.org/doc/html/rfc7233>). Below we have a simple download file action with file streaming.
```ruby
 
    actions: {
      download_file: {
        title: "Download file",

        input_fields: lambda do 
          [
            {
              name: "file_id",
              label: "File ID"
            }
          ]
        end,

        execute: lambda do
          {
            file_contents: workato.stream.out("download_file", { file_id: file_id })
          }
        end,

        output_fields: lambda do 
          [
            {
              name: "file_contents"
            } 
          ]
        end
      }
    }


```

The stream `download_file` defined in the `workato.stream.out` method is responsible for holding the code that retrieves a specific range of bytes requested by the platform - which will be sent over to a stream consumer to be uploaded into a downstream destination.

As such, the arguments passed to this callback provide you clear inputs that you can use in your HTTP requests to retrieve this range of bytes.

The output of the stream lambda is an array which expects the byte string in the first index and in the second index, a boolean value which should be true if this is the end of the file.
```ruby
 
    streams: {
        download_file: lambda do |input, starting_byte_range, ending_byte_range, byte_size|
          # Example starting_byte_range = 0
          # Example ending_byte_range = 10485759 
          # Example byte_size = 10485760 (10MB)
          # input passed from action can be assumed to be a friendly URL
          chunk = get("/#{input['file_id']}/download").
            headers("Range": "bytes=#{starting_byte_range}-#{ending_byte_range}").
            response_format_raw
          # if the chunk.size is smaller than the requested byte_size, 
          # then we know we are at the end of the file.
          [chunk, chunk.size < byte_size]
        end
    }


```

Take note that the `download_file` lambda is only executed when the datapill for `file_contents` is mapped to a downstream action.
