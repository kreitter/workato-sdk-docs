# Workato SDK Documentation

> **Source**: https://docs.workato.com/en/developing-connectors/sdk/sdk-reference/whitelist-removal.html
> **Fetched**: 2026-01-18T02:50:39.889139

---

# [#](<#removal-of-ruby-whitelist-for-sdk>) Removal of Ruby whitelist for SDK

Following the migration of custom connector code execution to **isolated containers** , **Ruby whitelisting** is removed from the connector SDK. This change significantly expands the range of capabilities SDK developers can use within the platform. Developers can now leverage the **full functionality of Ruby 2.7** , including built-in libraries and Ruby gems available in the SDK container.

## [#](<#key-capabilities>) Key capabilities

With the removal of Ruby whitelisting, developers can now access the full functionality of Ruby 2.7, including built-in libraries and Ruby gems available in the SDK container.

  * **Access to Ruby 2.7 standard methods**

Developers now have access to the full range of Ruby 2.7 standard methods. Developers can also use Ruby’s `require` method to import built-in libraries, such as JSON, CSV, socket, and others.

  * **Pre-installed Ruby Gems**

Developers can now directly use a selection of pre-installed Ruby gems without restrictions:

    * `activesupport` (5.2.8.1)
    * `aws-sigv4` (1.2.4)
    * `charlock_holmes` (0.7.7)
    * `concurrent-ruby` (1.2.3)
    * `gyoku` (1.3.1)
    * `i18n` (0.9.5)
    * `jwt` (2.1.0)
    * `loofah` (2.21.3)
    * `mime-types` (3.5.2)
    * `nokogiri` (1.15.6)
    * `rails-html-sanitizer` (1.4.4)
    * `rest-client` (2.1.0)
    * `ruby_rncryptor` (3.0.2)
  * **TCP sockets**

Developers can now leverage TCP sockets for low-level TCP connections. [Learn more (opens new window)](<https://ruby-doc.org/stdlib-2.7.0/libdoc/socket/rdoc/TCPSocket.html>).

    * Example use case: Implement MQTP protocol over UDP or WebSocket connections.
  * **Classes and modules**

Developers can now define classes and modules, improving code reusability, organization, and maintainability.

  * **Dynamic code execution**

Using the `eval` method, developers can now dynamically load and execute code. Code can be generated on the fly based on runtime data and executed immediately.

  * **Multi-threaded and concurrent code**

Developers can now write multi-threaded and concurrent code.

## [#](<#example-connector-ideas>) Example connector ideas

  * **E-commerce data scraper**

A connector that uses `nokogiri` to scrape product data from various e-commerce websites, transforms the data using `gyoku`, and uploads it to a central database for analysis.

  * **Secure API Gateway**

A connector that uses `jwt` for secure API authentication and `rest-client` to interact with multiple third-party APIs, aggregating data and providing a unified interface.

  * **Amazon S3 file manager**

A connector that uses `aws-sigv4` to securely upload and download files from Amazon S3, with MIME type handling using `mime-types` to ensure correct file processing.

  * **HTML sanitization**

A connector that uses `loofah` and `rails-html-sanitizer` to sanitize HTML content, removing potentially harmful elements and ensuring data integrity.

  * **Real-time data processor**

A connector that uses `concurrent-ruby` to process multiple data streams in parallel, such as Internet of Things sensor data, performing real-time analysis and actions.

  * **Concurrent processing**

A connector that uses `concurrent-ruby` to handle concurrent tasks, improving the performance and responsiveness of connectors.

  * **JWT authentication**

A connector that uses the `jwt` gem to create and verify JSON web tokens for secure API authentication.

  * **XML and HTML data handling**

A connector that uses `nokogiri` and `gyoku` for parsing, transforming, and generating XML and HTML data. This can be useful for integrating with systems that use XML-based APIs or for web scraping tasks.
