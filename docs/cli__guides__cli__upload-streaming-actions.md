# Workato SDK Documentation

> **Source**: https://docs.workato.com/en/developing-connectors/sdk/cli/guides/cli/upload-streaming-actions.html
> **Fetched**: 2026-06-16T03:13:01.595829

---

[Connector SDK](</en/developing-connectors/sdk>)

[CLI](</en/developing-connectors/sdk/cli>)

Guides

Are you an LLM? You can read better optimized documentation at /en/developing-connectors/sdk/cli/guides/cli/upload-streaming-actions.md for this page in Markdown format

# How-to guides - Running upload streaming actions/triggers on CLI [​](<#how-to-guides-running-upload-streaming-actions-triggers-on-cli>)

Copy page

In this segment, we will be going through how you can run and easily debug actions that utilize file streaming using the Workato Gem. File streaming can be differentiated into two main components that go together - download file actions and upload file actions. Below, we will go over the steps to execute an upload file action in the CLI.

## Prerequisites [​](<#prerequisites>)

  * You have installed and can run the Workato SDK Gem. Read our [getting-started guide](</en/developing-connectors/sdk/cli/guides/getting-started>) to know more.
  * You have an understanding of the mechanics of file streaming on the SDK. Read our [guides](</en/developing-connectors/sdk/guides/building-actions/streaming>) to learn more.

## Upload file - Sample connector - Upload file to url [​](<#upload-file-sample-connector-upload-file-to-url>)

We will be using the [generic upload file to url connector](</en/developing-connectors/sdk/guides/building-actions/streaming/upload-stream-content-range>) as an example.

### Running the `execute` lambda for the Upload file action [​](<#running-the-execute-lambda-for-the-upload-file-action>)

With upload file streaming actions, the definition of the input is important here as it has to contain information about an incoming file stream that the action will utilize. There are numerous options to simulate a file stream which we will go over.

ruby
```ruby

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

```

Alongside the execute lambda, you will also need a input JSON file such as `upload_file_input.json` when executing the upload file action in the SDK CLI. Below, we have an example of a mocked stream whose chunks are defined explicitly - each chunk is a separate key in the `chunks` hash.

JSON
```ruby

    {
        "file_name": "sample_file",
        "file": {
          # this hash simulates a file stream which is 
          # the output of a download file object
          "__stream__": true,
          "chunks": {
            "0": "abcd",
            "4": "efgh",
            "8": "ijkl",
            "12": "mn"
          }
        },
        "url": "https://www.friendly_upload_url.com"
    }

```

To run the upload file action, you give the same command as you would a standard action.

shell
```ruby

    workato exec actions.upload_to_url.execute --input='upload_file_input.json' --verbose

    SETTINGS
    {}
    INPUT
    {
        "file_name": "sample_file",
        "file": {
          "__stream__": true,
          "chunks": {
            "0": "abcd",
            "4": "efgh",
            "8": "ijkl",
            "12": "mn"
          }
        },
        "url": "https://www.friendly_upload_url.com"
    }

    RestClient.put "https://www.friendly_upload_url.com", "Content-Range"=>"bytes=0-3", "User-Agent"=>"rest-client/2.0.2 (darwin19.6.0 x86_64) ruby/2.4.10p364"
    # => 201 Created | 0 bytes, 1.46s    

    RestClient.put "https://www.friendly_upload_url.com", "Content-Range"=>"bytes=4-7", "User-Agent"=>"rest-client/2.0.2 (darwin19.6.0 x86_64) ruby/2.4.10p364"
    # => 201 Created | 0 bytes, 1.46s 

    RestClient.put "https://www.friendly_upload_url.com", "Content-Range"=>"bytes=8-11", "User-Agent"=>"rest-client/2.0.2 (darwin19.6.0 x86_64) ruby/2.4.10p364"
    # => 201 Created | 0 bytes, 1.46s 

    RestClient.put "https://www.friendly_upload_url.com", "Content-Range"=>"bytes=11-13", "User-Agent"=>"rest-client/2.0.2 (darwin19.6.0 x86_64) ruby/2.4.10p364"
    # => 201 Created | 0 bytes, 1.46s 

    RestClient.post "https://www.friendly_upload_url.com", "{\"commit\":true}", "Accept"=>"application/json", "Accept-Encoding"=>"gzip, deflate", "Content-Length"=>"88", "Content-Type"=>"application/json", "User-Agent"=>"rest-client/2.0.2 (darwin19.6.0 x86_64) ruby/2.4.10p364"
    # => 201 Created | 0 bytes, 1.46s   

    OUTPUT
    {
      "file_size": 13,
      "file_path": "/path/to/sample/file",
      "file_name": "file_name"
    }

```

### Variations to mock streams [​](<#variations-to-mock-streams>)

Beyond mocking streams by declaring chunks manually, you can mock streams in a variety of ways.

TIP

Take note that streams can take longer than your average actions to finish execution - depending on the size of the file and network. It is recommended to test with smaller files rather than production sizes.

Mock streams with each chunk explicitly

JSON
```ruby

    {
        "file": {
          "__stream__": true,
          "chunks": {
            "0": "abcd",
            "4": "efgh",
            "8": "ijkl",
            "12": "mn"
          }
        }
    }

```

Mock streams by utilizing a stream implemented for a download file action/trigger in the same connector

JSON
```ruby

    {
        "file": {
          "__stream__": true,
          "name": "stream_within_same_connector", # name of the stream in the connector
          "input": { # input that will be passed to the stream callback
            "file_path": "/path/to/sample/file"
          }
        },
    }

```

Mock streams by providing a static stream

JSON
```ruby

    {
        "file": {
          "data": "123456789",
          "eof": true
        },
    }

```

Mock streams by providing a string

JSON
```ruby

    {
        "file": "qwertyuiop[]"
    }

```

**Last updated:**
