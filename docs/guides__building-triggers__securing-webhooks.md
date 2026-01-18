# Workato SDK Documentation

> **Source**: https://docs.workato.com/en/developing-connectors/sdk/guides/building-triggers/securing-webhooks.html
> **Fetched**: 2026-01-18T02:50:01.654603

---

# [#](<#how-to-guides-securing-webhook-events>) How-to guides - Securing Webhook events

Webhook signature verification is a recommended practice that prevents malicious actors from spoofing events or allowing your connector to reject webhooks that were tampered with. There are many known signature verification methodologies which normally involve creating a signature from the webhook event and matching that against a signature in the webhook's headers. And this guide will show you one simple example of how to do so through [HubSpot's webhook V1 signature (opens new window)](<https://developers.hubspot.com/docs/api/webhooks/validating-requests#validate-requests-using-the-v1-request-signature>).

TIP

This guide assumes you know the basics of creating static or dynamic webhook triggers. Please review those guides if you have not done so.

## [#](<#sample-connector-hubspot-webhooks>) Sample Connector - HubSpot Webhooks
```ruby
 
          webhook_payload_type: "raw", # Workato does a JSON.parse on incoming webhooks but we need to calculate the signature based on the raw payload

          webhook_notification: lambda do |input, payload, extended_input_schema, extended_output_schema, headers, params, connection, webhook_subscribe_output|
            original_payload = payload
            client_secret = connection['client_secret'] 
            if client_secret.present?
              source_string = client_secret + original_payload # Build the string to SHA256 which is a concatenation of client secret + payload
              v1_signature = source_string.encode_sha256.encode_hex
            end

            # If condition below verifies that the signature we calculated is the same as the X-Hubspot-Signature we got in the webhook event
            if (client_secret.present? && v1_signature == headers['X-Hubspot-Signature']) 
              # Don't forget to parse the payload into JSON as we dictated that the payload would be `raw`
                { 
                  events: workato.parse_json(payload),
                  headers: headers,
                  webhook_validated: client_secret.present? ? true : false
                }
            end
          end,


```

[See the full connector in our community library (opens new window)](<https://app.workato.com/custom_adapters/543633/details?community=true>).

## [#](<#step-1-setting-the-webhook-payload-type-to-raw-if-needed>) Step 1 - Setting the webhook_payload_type to raw if needed

Workato's webhook gateway always attempts to parse incoming payloads as JSON. In some cases, this may cause some of the payload's details to be lost which may result in a wrong signature being created. To avoid this, you can use the key `webhook_payload_type` to force Workato to provide the raw payload to the `webhook_notification` lambda.

## [#](<#step-2-computing-the-webhook-signature>) Step 2 - Computing the Webhook signature

Another important part of verifying the authenticity of a webhook is to compute your own webhook signature from the incoming webhook event. This is often done through an encryption algorithm such as SHA256 or HMAC algorithms using the payload and a secret that is only known by you and the webhook provider.
```ruby
 
      original_payload = payload
      client_secret = connection['client_secret'] 
      if client_secret.present?
        source_string = client_secret + original_payload # Build the string to SHA256 which is a concatenation of client secret + payload
        v1_signature = source_string.encode_sha256.encode_hex
      end


```

In the case of HubSpot, we create the key to be encrypted from the payload and the client secret before encrypting it with SHA256.

## [#](<#step-3-comparing-the-generated-signature-with-the-provided-one-in-the-webhook-event>) Step 3 - Comparing the generated signature with the provided one in the webhook event

The next step would be to compare your generated signature in step 2 with the signature present in the webhook event. Normally, this would be contained in the header of the webhook event which you have access to in the `webhook_notification` lambda.
```bash
 
            # If condition below verifies that the signature we calculated is the same as the X-Hubspot-Signature we got in the webhook event
            if (client_secret.present? && v1_signature == headers['X-Hubspot-Signature']) 
              # Don't forget to parse the payload into JSON as we dictated that the payload would be `raw`
                { 
                  events: workato.parse_json(payload),
                  headers: headers,
                  webhook_validated: client_secret.present? ? true : false
                }
            end


```
