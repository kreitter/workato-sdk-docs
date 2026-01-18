# Workato SDK Documentation

> **Source**: https://docs.workato.com/en/developing-connectors/sdk/guides/data-formats/form-url-encoded.html
> **Fetched**: 2026-01-18T02:50:06.212231

---

# [#](<#how-to-guides-url-encoded-form>) How-to guides - URL Encoded Form

This request format can be declared in any keys (`execute`, `acquire`, `fields` etc.) in your custom connector code.

## [#](<#sample-code-snippet>) Sample code snippet

Let's use the submit data to a form endpoint in [HubSpot API (opens new window)](<https://developers.hubspot.com/docs/methods/forms/submit_form>) as an example. This endpoint accepts form data in form urlencoded format.

A cURL example looks like this:
```ruby
 
    curl \
      https://forms.hubspot.com/uploads/form/v2/12345/67890 \
      -X POST \
      -H 'Content-Type: application/x-www-form-urlencoded' \
      -d 'firstname=TestContact&lastname=FormSub&[[email protected]](</cdn-cgi/l/email-protection>)&newcustomproperty=testing&hs_context=%7B%22hutk%22%3A%2260c2ccdfe4892f0fa0593940b12c11aa%22%2C%22ipAddress%22%3A%22192.168.1.12%22%2C%22pageUrl%22%3A%22http%3A%2F%2Fdemo.hubapi.com%2Fcontact%2F%22%2C%22pageName%22%3A%22Contact%2BUs%22%2C%22redirectUrl%22%3A%22http%3A%2F%2Fdemo.hubapi.com%2Fthank-you%2F%22%7D'


```

This cURL command can be replicated in Workato:
```ruby
 
    {
      title: "HubSpot",

      connection: {
        # Some code here
      },

      test: {
        # Some code here
      },

      actions: {
        submit_form: {
          input_fields: lambda do
            [
              {
                name: "portal_id",
                type: "string"
              },
              {
                name: "form_guid",
                type: "string"
              },
              {
                name: "hutk",
                type: "string"
              },
              {
                name: "ipAddress",
                type: "string"
              },
              {
                name: "pageUrl",
                type: "string"
              },
              {
                name: "pageName",
                type: "string"
              },
              {
                name: "redirectUrl",
                type: "string"
              }
            ]
          end,

          execute: lambda do |connection, input|
            post("https://forms.hubspot.com/uploads/form/v2/#{input['portal_id']}/#{input['form_guid']}").
              request_body(
                input.reject { |k,v| k == 'portal_id' || k == 'form_guid' }
              ).
              request_format_www_form_urlencoded

          end
        },

        output_fields: { ... }
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

## [#](<#components>) Components

cURL | Workato  
---|---  
`curl https://forms.hubspot.com/uploads/form/v2/{portal_id}/{form_guid} -X POST` | `post("https://forms.hubspot.com/uploads/form/v2/#{input['portal_id']}/#{input['form_guid']}")`  
`-H 'Content-Type: application/x-www-form-urlencoded'` | `.request_format_www_form_urlencoded`  
`-d '{data}'` | `.request_body(input.reject { |k,v| k == 'portal_id' || k == 'form_guid' })`
