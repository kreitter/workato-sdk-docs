# Workato SDK Documentation

> **Source**: https://docs.workato.com/en/developing-connectors/sdk/sdk-reference/test.html
> **Fetched**: 2026-01-18T02:50:37.518282

---

# [#](<#sdk-reference-test>) SDK Reference - `test`

This section enumerates all the possible keys available when testing your connection.

Quick Overview

The `test` lambda tells your connector how to check if the connection is valid. After it has taken the input from the user and executed the `authorization` block, this test verifies that the credentials supplied are valid via a simple HTTP request.

The `test` lambda is executed when a connection a user first clicks connect. The only exception is for OAuth2 authorization code grant connections, where the connection is marked as connected when Workato has successfully exchanged the authorization code for access tokens.

The `test` lambda is also executed for all types of connections upon recipe start and job rerun to ensure that the connection's credentials are still valid.

## [#](<#structure>) Structure
```ruby
 
        test: lambda do |connection|
          # see test: documentation for more information
        end


```

* * *

## [#](<#test>) `test`

Attribute | Description  
---|---  
Key | `test`  
Type | lambda function  
Required | True  
Description | A simple HTTP request that can verify that we have established a successful connection. This connection is marked as "Successful" when the HTTP response is 2XX.  
Example - test:

APIs normally provide an endpoint that returns information about the authenticated user. These endpoints are ideal for your connector to verify that connection has been established.
```ruby
 
        test: lambda do |connection|
          get('/api/v5/me')
        end


```

In cases where this is not available, you may also choose to use simple requests. Normally this could be to search for results in the target API. These requests should also allow you to verify that the connection is valid.
```ruby
 
        test: lambda do |connection|
          get("https://person.clearbit.com/v1/people/email/[[email protected]](</cdn-cgi/l/email-protection>)")
        end


```
