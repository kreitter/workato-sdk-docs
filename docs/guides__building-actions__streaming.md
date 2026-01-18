# Workato SDK Documentation

> **Source**: https://docs.workato.com/en/developing-connectors/sdk/guides/building-actions/streaming.html
> **Fetched**: 2026-01-18T02:49:50.156779

---

# [#](<#how-to-guides-file-streaming>) How-to guides - File Streaming

Utilizing Workato's file streaming library, you'll be able to build connectors that can transfer gigabytes of data between a source and destination. This is done by downloading a smaller chunk of the larger file, uploading that to the destination and looping over this process multiple times.

![File streaming](/assets/img/streaming-illustration.47a8ccdc.jpg)

Many of Workato's standard platform connectors to common file storage locations have streaming enabled such as S3, Google Cloud Storage and Azure Blob. [Find the full list here.](</features/file-streaming.html#file-streaming>)

ACTION TIMEOUT

SDK actions have a 180 second [timeout](</recipes/recipe-job-errors.html#timeouts>) limit.

You can use the `checkpoint!` method with file streaming actions to transfer files that exceed the timeout limit. Refer to the [Using our multistep framework to extend upload times](<#using-our-multistep-framework-to-extend-upload-times>) section for additional information.

## [#](<#prerequisites>) Prerequisites

  * Downloading files The API should respect the [HTTP RFC for Range headers (opens new window)](<https://datatracker.ietf.org/doc/html/rfc7233>) which allows us to download a specific byte range of the file.

  * Uploading the file The API should support ways to upload a file in multiple discrete chunks. This could be via [Content-Range headers (opens new window)](<https://www.ietf.org/rfc/rfc2616.txt>) or via any other form chunked uploads such as [Azure's multipart upload with block IDs. (opens new window)](<https://learn.microsoft.com/en-us/rest/api/storageservices/put-block>)

## [#](<#guides>) Guides

The guides below details out the various ways to build file streaming actions depending on the API's capabilities:

  1. [Download file via file streaming (Range headers)](</developing-connectors/sdk/guides/building-actions/streaming/download-stream.html>)
  2. [Upload file via file streaming (Content-Range headers)](</developing-connectors/sdk/guides/building-actions/streaming/upload-stream-content-range.html>)
  3. [Upload file via file streaming (Chunk ID)](</developing-connectors/sdk/guides/building-actions/streaming/upload-stream-chunk-id.html>)

## [#](<#what-happens-if-your-api-does-not-meet-the-prerequisites>) What happens if your API does not meet the prerequisites?

If the API you work with does not allow for chunked uploads or downloads, you can still download and upload files in-memory but subject to limitations of both time and size. **This is not recommended unless absolutely necessary.**
