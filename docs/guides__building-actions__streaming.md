# Workato SDK Documentation

> **Source**: https://docs.workato.com/en/developing-connectors/sdk/guides/building-actions/streaming.html
> **Fetched**: 2026-07-17T03:05:45.840357

---

[Connector SDK](</en/developing-connectors/sdk>)

[How-to guides](</en/developing-connectors/sdk/guides>)

Are you an LLM? You can read better optimized documentation at /en/developing-connectors/sdk/guides/building-actions/streaming.md for this page in Markdown format

# How-to guides - File Streaming [​](<#how-to-guides-file-streaming>)

Copy page

Utilizing Workato's file streaming library, you'll be able to build connectors that can transfer gigabytes of data between a source and destination. This is done by downloading a smaller chunk of the larger file, uploading that to the destination and looping over this process multiple times.

![File streaming](/assets/streaming-illustration.CyLcPq6_.jpg)

Many of Workato's standard platform connectors to common file storage locations have streaming enabled such as S3, Google Cloud Storage and Azure Blob. [Find the full list here.](</en/features/file-streaming#file-streaming>)

ACTION TIMEOUT

SDK actions have a 180 second [timeout](</en/recipes/recipe-job-errors#timeouts>) limit.

You can use the `checkpoint!` method with file streaming actions to transfer files that exceed the timeout limit. Refer to the [Using our multistep framework to extend upload times](</en/developing-connectors/sdk/guides/building-actions/streaming/upload-stream-chunk-id#using-our-multistep-framework-to-extend-upload-times>) section for additional information.

## Prerequisites [​](<#prerequisites>)

  * Downloading files The API should respect the [HTTP RFC for Range headers](<https://datatracker.ietf.org/doc/html/rfc7233>) which allows us to download a specific byte range of the file.

  * Uploading the file The API should support ways to upload a file in multiple discrete chunks. This could be via [Content-Range headers](<https://www.ietf.org/rfc/rfc2616.txt>) or via any other form chunked uploads such as [Azure's multipart upload with block IDs.](<https://learn.microsoft.com/en-us/rest/api/storageservices/put-block>)

## Guides [​](<#guides>)

The guides below details out the various ways to build file streaming actions depending on the API's capabilities:

  1. [Download file via file streaming (Range headers)](</en/developing-connectors/sdk/guides/building-actions/streaming/download-stream>)
  2. [Upload file via file streaming (Content-Range headers)](</en/developing-connectors/sdk/guides/building-actions/streaming/upload-stream-content-range>)
  3. [Upload file via file streaming (Chunk ID)](</en/developing-connectors/sdk/guides/building-actions/streaming/upload-stream-chunk-id>)

## What happens if your API does not meet the prerequisites? [​](<#what-happens-if-your-api-does-not-meet-the-prerequisites>)

If the API you work with does not allow for chunked uploads or downloads, you can still download and upload files in-memory but subject to limitations of both time and size. **This is not recommended unless absolutely necessary.**

**Last updated:**
