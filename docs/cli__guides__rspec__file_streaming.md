# Workato SDK Documentation

> **Source**: https://docs.workato.com/en/developing-connectors/sdk/cli/guides/rspec/file_streaming.html
> **Fetched**: 2026-01-18T02:49:11.193396

---

# [#](<#how-to-guides-writing-tests-for-streaming-triggers-actions>) How-to guides - Writing tests for streaming triggers/actions

In this segment, we will be going through how you can write tests for actions that utilize Workato's file streaming capabilities. To do this, we will be using the generic upload file to url connector example [here](</developing-connectors/sdk/guides/building-actions/streaming/upload-stream-content-range.html>).

## [#](<#generating-your-tests>) Generating your tests

You can create a separate spec file for each action or generate your tests based on your connector by using the `workato generate test` command. This will generate a spec file which will include most of the necessary stubs for your to start writing tests.

### [#](<#sample-rspec-contents>) Sample RSpec contents
```ruby
 
    RSpec.describe 'actions/upload_file_to_url', :vcr do

      let(:connector) { Workato::Connector::Sdk::Connector.from_file('connector.rb', settings) }
      let(:settings) { Workato::Connector::Sdk::Settings.from_default_file }

      before do
        stub_const('Workato::Connector::Sdk::Stream::Reader::DEFAULT_FRAME_SIZE', 5.kilobytes)
      end

      let(:action) { connector.actions.upload_file_to_url }

      describe 'execute' do
        subject(:output) { action.execute(settings, input) }

        let(:input) do
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
              "url": "https://www.friendly_s3_url.com/upload"
          }
        end

        it 'given simple stream' do
          it 'produces a file' do
            is_expected.to include(:file_size)
            expect(output.file_size).to eq(13)

            is_expected.to include(:file_path)

            is_expected.to include(:file_name)
          end
        end
      end

    end


```

## [#](<#step-1-define-your-connector-instance>) Step 1 - Define your connector instance

To begin testing, you need to use the Workato SDK Gem to create an instance of your connector.
```ruby
 
      let(:connector) { Workato::Connector::Sdk::Connector.from_file('connector.rb', settings) }


```

## [#](<#step-2-define-your-settings-instance>) Step 2 - Define your settings instance

Next, you need to use the Workato SDK Gem to create an instance of your settings. This is synonymous with your connection on Workato. Take note that, your connector instance previously defined also uses this settings instance.
```ruby
 
      let(:settings) { Workato::Connector::Sdk::Settings.from_default_file }


```

## [#](<#step-3-define-your-action>) Step 3 - Define your action

After creating the related instances, we instantiate the `action` so we can reference it more easily in the rest of the tests.
```ruby
 
      let(:action) { connector.actions.upload_file_to_url }


```

## [#](<#step-3-describe-your-tests-define-your-subject-and-input>) Step 3 - Describe your tests, define your subject and input

Here, we describe the "family" of tests we are hoping to run. In this case, we use the keyword `execute`. Next, we make the subject the output which is the outcome of the execution of the action. Lastly, we declare the `input` which is a simple stream.
```ruby
 
      describe 'execute' do
        subject(:output) { action.execute(settings, input) }

        let(:input) do
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
              "url": "https://www.friendly_s3_url.com/upload"
          }
        end


```

## [#](<#step-4-declare-your-assertions-for-individual-tests>) Step 4 - Declare your assertions for individual tests

For a test to pass or fail, there needs to be a declared comparison.

Over here, we are declaring that we "expect" the output of the `execute` lambda to include keys `file_size`, `file_path` and `file_name`. Furthermore, we expect the `file_size` value to be 13.
```ruby
 
      it 'given simple stream' do
        it 'produces a file' do
          is_expected.to include(:file_size)
          expect(output.file_size).to eq(13)

          is_expected.to include(:file_path)

          is_expected.to include(:file_name)
        end
      end


```

## [#](<#variations-to-mock-streams-in-rspec>) Variations to mock streams in RSpec

Alongside mocking simple streams within your RSpec tests, you have the ability mock other variations as well.

Mock streams with each chunk explicitly
```ruby
 
    let(:input) do
      {
          file_name: 'sample_file',
          file: {
            __stream__: true,
            chunks: {
              0 => 'abcd',
              4 => 'efgh',
              8 => 'ijkl',
              12 => 'mn'
            }
          },
          url: 'https://www.friendly_s3_url.com/upload'
      }
    end


```

Mock streams by utilizing a stream implemented for a download file action/trigger in the same connector
```ruby
 
    let(:input) do
      {
          file_name: 'sample_file',
          file: {
            __stream__: true,
            name: 'global_stream',
            input: {
              file_path: '/path/to/sample/file'
            }
          },
          url: 'https://www.friendly_s3_url.com/upload'
      }
    end


```

Mock streams by providing the inline definition of a stream with its own authentication

TIP

Advanced mocks like these are only available in RSpec tests and not in CLI execution.
```ruby
 
    let(:input) do
      {
          file_name: 'sample_file',
          file: {
            __stream__: true,
            name: 'mock_advanced_stream',
            input: {
              file_path: '/path/to/sample/file'
            },
            settings: {
              # optional
              # A connection settings for stream mock application
              # if the mock makes authorized requests to external apps
              # Also can use Workato::Connector::Sdk::Settings.from_file
              domain: 'acme.egnyte.com',
              api_key: 'api_key'
            },
            connection: {
              # optional
              # A connection definition for stream source applications
              # if the mock makes authorized requests to external apps
              # It supports the same blocks as connector's connection definition
              authorization: {
                type: 'api_key',

                apply: lambda do |connection|
                  headers(api_key: connection['api_key'])
                end
            },
            },
            chunks: lambda do |input, _first_byte, last_byte, size|
              chunk = get("/pubapi/v1/fs-content/#{file_path}").
                  headers("Range": "bytes=#{starting_byte_range}-#{ending_byte_range}").
                  response_format_raw

              [chunk, chunk.size < requested_byte_size]
            end
          },
          url: 'https://www.friendly_s3_url.com/upload'
      }
    end


```

Mock streams by providing a static stream
```ruby
 
    let(:input) do
      {
          file_name: 'sample_file',
          file: {
            data: '1234567890',
            oef: true
          },
          url: 'https://www.friendly_s3_url.com/upload'
      }
    end


```

Mock streams by providing a string
```ruby
 
    let(:input) do
      {
          file_name: 'sample_file',
          file: 'qwertyuiop[]',
          url: 'https://www.friendly_s3_url.com/upload'
      }
    end


```
