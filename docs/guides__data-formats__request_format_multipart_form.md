# Workato SDK Documentation

> **Source**: https://docs.workato.com/en/developing-connectors/sdk/guides/data-formats/request_format_multipart_form.html
> **Fetched**: 2026-01-18T02:50:08.459686

---

# [#](<#how-to-guides-multipart-form>) How-to guides - Multipart Form

[Multipart form request (opens new window)](<https://www.w3.org/TR/html401/interact/forms.html#h-17.13.4.2>) is typically used to send large files and data to a server.

This request format can be declared in any keys (`execute`, `acquire`, `fields` etc.) in your custom adapter code. This is done by embedding the data format inside the `Content-Type` header.

## [#](<#sample-code-snippet>) Sample code snippet

Let's use the Convert document endpoint in [IBM Watson API (opens new window)](<https://www.ibm.com/watson/developercloud/document-conversion/api/v1/#convert-document>) as an example. This endpoint accepts a document in multipart/form-data format.

A cURL example looks like this:
```ruby
 
    curl \
      https://gateway.watsonplatform.net/document-conversion/api/v1/convert_document?version=2015-12-15 \
      -X POST \
      -u "{username}":"{password}" \
      -F config="{\"conversion_target\":\"answer_units\"}" \
      -F "[[email protected]](</cdn-cgi/l/email-protection>);type=application/pdf"


```

Workato:
```ruby
 
    {
      title: "IBM Watson",

      connection: {
        # Some code here
      },

      test: {
        # Some code here
      },

      actions: {
        upload_file: {
          input_fields: lambda do
            [
              { name: "file_name", type: "string" },
              { name: "file_data", type: "string" },
              { name: "conversion_target", type: "string" }
            ]
          end,

          execute: lambda do |connection, input|
            post("https://gateway.watsonplatform.net/document-conversion/api/v1/convert_document").
              params(version: "2015-12-15").
              request_format_multipart_form.
              payload(file: [input['file_data'], 'application/pdf'],
                      file_name: input['file_name'],
                      config: "{\"conversion_target\":\"#{input['conversion_target']}\"}")
          end
        },

        output_fields: {
          # Some code here
        }
      },

      triggers: {
        # Some code here
      },
      object_definitions: {
        # Some code here
      },
      pick_lists: {
        # Some code here
      },
      methods: {
        # Some code here
      }


```

In the SDK, notice that the `file` key in the payload takes an array of length 2. This defines the request as form data. The first item in the array is the file data and the second item is the media type (MIME type) of the input file.

## [#](<#components>) Components

cURL | Workato  
---|---  
`curl https://gateway.watsonplatform.net/document-conversion/api/v1/convert_document?version=2015-12-15 -X POST` | `post("https://gateway.watsonplatform.net/document-conversion/api/v1/convert_document")`  
`.params(version: "2015-12-15")`  
`-u "{username}":"{password}"` | This is defined in the [connection](../authentication/basic-authentication.md) key and is automatically added onto the outgoing request.  
`-F config="{\"conversion_target\":\"answer_units\"}"`  
`-F "[[email protected]](</cdn-cgi/l/email-protection>);type=application/pdf"` | `.request_format_multipart_form`  
`.payload(`  
`file: [input['file_data'], 'application/pdf'], `  
`file_name: input['file_name'],`  
`config: "{\"conversion_target\":\"#{input['conversion_target']}\"}")`  

## [#](<#variations>) Variations

Sometimes, the name of the file must be explicitly stated in the multipart form as part of the file payload, instead of a separate key-value pair, like the previous example. To satisfy this, you can adjust your payload to this.

FILE_NAME IS DIFFERENT FROM FILE

`file_name` in the following example is different from the payload key (`file`).
```ruby
 
    execute: lambda do |connection, input|
      post("https://gateway.watsonplatform.net/document-conversion/api/v1/convert_document").
        params(version: "2015-12-15").
        request_format_multipart_form.
        payload(file: [input['file_data'], 'application/pdf', input['file_name']],
                config: "{\"conversion_target\":\"#{input['conversion_target']}\"}")
    end


```
