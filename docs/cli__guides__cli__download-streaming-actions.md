# Workato SDK Documentation

> **Source**: https://docs.workato.com/en/developing-connectors/sdk/cli/guides/cli/download-streaming-actions.html
> **Fetched**: 2026-01-18T02:48:59.395340

---

# [#](<#how-to-guides-running-streaming-download-actions-triggers-on-cli>) How-to guides - Running streaming download actions/triggers on CLI

In this segment, we will be going through how you can run and easily debug actions that utilize file streaming using the Workato Gem. File streaming can be differentiated into two main components that go together - download file actions and upload file actions. Below, we will go over the steps to a download file action in the CLI.

## [#](<#prerequisites>) Prerequisites

  * You have installed and can run the Workato SDK Gem. Read our [getting-started guide](</developing-connectors/sdk/cli/guides/getting-started.html>) to know more.
  * You have an understanding of the mechanics of file streaming on the SDK. Read our [guides](</developing-connectors/sdk/guides/building-actions/streaming.html>) to learn more.

## [#](<#download-file-sample-connector-egnyte>) Download file - Sample connector - Egnyte

We will be using the [Egnyte connector](</developing-connectors/sdk/guides/building-actions/streaming/download-stream.html>) as an example.

### [#](<#running-the-execute-lambda-for-the-download-file-action>) Running the `execute` lambda for the download file action

With download file actions, it is important to note that when the action/trigger is executed in a job, the actual downloading of the file contents (contained in the `streams` callback) is not triggered at that point in time. The `streams` callback of a download file action is only triggered when the datapill representing the file contents is used in a downstream action.

As such, in the SDK Gem, you may test your download file action as a normal action; and your `streams` callback separately. Let's go over the download file action first.
```ruby
 
    execute: lambda do |connection, input|
      file_path = input['file_path']&.gsub(/%2F/, '/')

      file_details = get("/pubapi/v1/fs/#{file_path}")

      file_details['file_contents'] = workato.stream.out("download_file_by_path", { file_path: file_path})

      file_details
    end,


```

Alongside the execute lambda, you will also need a input JSON file such as `egnyte_download_file_input.json` when executing the download file action in the SDK CLI.
```ruby
 
    {
        "file_path": "/path/to/sample/file"
    }


```

To run a download file action, you give the same command as you would a standard action.
```ruby
 
    workato exec actions.download_object.execute --input='egnyte_download_file_input.json' --verbose

    SETTINGS
    {
      "domain": "acme.egnyte.com",
      "client_id": "client_id",
      "client_secret": "client_secret",
      "access_token": "valid_access_token",
      "refresh_token": "valid_refresh_token",
      "expires_in": 3599,
      "token_type": "Bearer"
    }
    INPUT
    {
        "file_path": "/path/to/sample/file"
    }

    RestClient.get "https://acme.egnyte.com/pubapi/v1/fs/path/to/sample/file", "Accept"=>"application/json", "Accept-Encoding"=>"gzip, deflate", "Authorization"=>"Bearer valid_access_token", "Content-Length"=>"207", "Content-Type"=>"application/json", "User-Agent"=>"rest-client/2.0.2 (darwin19.6.0 x86_64) ruby/2.4.10p364"
    # => 200 OK | application/json 176 bytes       

    OUTPUT
    {
      "checksum": "abc123",
      "size": 1000,
      "path": "/path/to/sample/file",
      "name": "file",
      "file_contents": {
        "__stream__": true,
        "name": "stream",
        "input": {
          "file_path": "/path/to/sample/file"
      }
    }


```

Note that the actual downloading of the file from Egnyte has not actually happened at this point - only the evaluation of the `execute` lambda excluding the `download_file_by_path` stream has been done when calling the action via the CLI. The output of the `file_contents` is an artificial value for a file stream.

TIP

You can also use other options like `--output` to save the output of the function to a JSON file.

### [#](<#running-the-streams-lambda-used-in-the-download-file-action>) Running the `streams` lambda used in the download file action

Now, to debug and test the `streams` lambda directly, you can use the CLI to invoke the lambda directly.
```ruby
 
    streams: {
      download_file_by_path: lambda do |input, starting_byte_range, ending_byte_range, requested_byte_size|
        # Example starting_byte_range = 0
        # Example ending_byte_range = 10485759 
        # Example requested_byte_size = 10485760 (10MB)
        chunk = get("/pubapi/v1/fs-content/#{file_path}").
                  headers("Range": "bytes=#{starting_byte_range}-#{ending_byte_range}").
                  response_format_raw
        # if the chunk.size is smaller than the requested byte_size, 
        # then we know we are at the end of the file.
        [chunk, chunk.size < requested_byte_size]
      end
    }


```

With the SDK Gem, you are able to invoke the specific streaming callback lambda to simulate the download of a single chunk, or loop over the entire download process to download multiple chunks sequentially.

To read a single chunk, you can simply invoke the stream with 3 parameters
```ruby
 
    workato exec streams.download_file_by_path --input='egnyte_download_file_input.json' --from=0 --frame_size=256 --verbose

    SETTINGS
    {
      "domain": "acme.egnyte.com",
      "client_id": "client_id",
      "client_secret": "client_secret",
      "access_token": "valid_access_token",
      "refresh_token": "valid_refresh_token",
      "expires_in": 3599,
      "token_type": "Bearer"
    }
    INPUT
    {
        "file_path": "/path/to/sample/file"
    }

    RestClient.get "https://acme.egnyte.com/pubapi/v1/fs-content/path/to/sample/file", "Range"=>"bytes=0-255", "Accept"=>"application/json", "Accept-Encoding"=>"gzip, deflate", "Authorization"=>"Bearer valid_access_token", "Content-Length"=>"207", "User-Agent"=>"rest-client/2.0.2 (darwin19.6.0 x86_64) ruby/2.4.10p364"
    # => 206 PartialContent | text/csv 255 bytes, 1.85s       

    OUTPUT
    [
      "256_byte_string",
      false
    ]


```

To read all chunks, you can invoke the stream with the same 3 parameters but with a bang (`!`) method.
```ruby
 
    workato exec streams.download_file_by_path! --input='egnyte_download_file_input.json' --frame_size=256 --verbose


```

TIP

Take note that the `from` argument does not work with the bang (`!`) method. We advise that you test this on smaller files to avoid waiting for a long time for the download process to finish.
