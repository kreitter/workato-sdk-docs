# Workato SDK Documentation

> **Source**: https://docs.workato.com/en/developing-connectors/sdk/guides/authentication/on-prem.html
> **Fetched**: 2026-05-16T03:09:25.561369

---

[Connector SDK](</en/developing-connectors/sdk>)

[How-to guides](</en/developing-connectors/sdk/guides>)

[API authorization](</en/developing-connectors/sdk/guides/authentication>)

# How-to guide - OPA authentication [​](<#how-to-guide-opa-authentication>)

HTTP requests made in a custom adapter are sent from Workato [IP addresses](</security/ip-allowlists#traffic-from-workato>) by default. You can configure the adapter to instead route all requests through an [on-prem agent](</on-prem>).

Complete the following steps to enable OPA authentication in a custom connector:

1

Sign in to Workato.

2

Go to **Tools > Connector SDK**.

3

Select the connector you plan to modify, or click **\+ New connector** to [create a new connector](</developing-connectors/sdk/guides/walkthrough#create-a-custom-connector>).

4

Add `secure_tunnel` set to `true` as a top level property in your custom adapter code.

USE OPA FOR TLS CERTIFICATES

Configure TLS client certificates in the OPA connection profile instead of your SDK connector code. OPA terminates TLS to your target service, and the certificate must be configured in the HTTP profile. Refer to [On-prem agent – Connection profiles](</on-prem/agents/connection/profile#http-profile>) for instructions to configure TLS client certificates in OPA. The connection returns SSL errors if you configure the certificate in the SDK connector.

For example:

ruby
```ruby

    {
      title: 'On-prem example connector',
      secure_tunnel: true,

      connection: {
        fields: [{ name: 'profile', hint: 'On-prem example connector profile' }],
        authorization: { type: 'none'},
        apply: ->() {
          headers('X-Workato-Connector': 'enforce')
        }
      },

      test: ->(connection) {
        post("http://localhost/ext/#{connection['profile']}/computeDigest", { payload: 'test' })
      }
    }

```

ADD OPA TO AN EXISTING CONNECTOR

Use the `||` operator to specify the existing authentication method as the default when you add new authentication methods to an existing connector.

In the following example, the value left of the `||` operator, `auth_type`, is evaluated first. If the value is `nil` or `false`, the right value, `api_key`, is evaluated.

ruby
```ruby

    selected: lambda do |connection|
      connection["auth_type"] || 'api_key'
    end,

```

5

Click **Save > Release latest version**.

6

Summarize the changes you made to the connector in the **Confirm release** modal.

![Change summary and confirmation window](/assets/confirm-version-release-window.Co6Sj0jz.png)_Summarize your changes to the connector_

7

Click **Release** to release the new version of the connector in your workspace and allow it to be used in recipes.

The **New connection** page for your connector displays the **Connection type** drop-down menu after you set `secure_tunnel` to `true`. You can use this menu to select the [on-prem group](</on-prem/groups#on-prem-group>) you plan to use for your connection.

![Connection without option to use OPA](/assets/OPA-example-without-secure-tunnel.DwqWcAfP.png)_**New connection** page without `secure_tunnel` enabled_

![Connection with option to use OPA](/assets/OPA-example-with-secure-tunnel.-eQlwgum.png) _**New connection** page with `secure_tunnel` enabled_

## Next steps [​](<#next-steps>)

Refer to the [SDK reference](</developing-connectors/sdk/sdk-reference/connection>) guide for a list of available `connection` keys and parameters or refer to the following guides set up an on-prem agent:

  * [Create an on-prem group](</on-prem/groups/create-group>)
  * [Add an agent to a group](</on-prem/groups/add-agent>)
  * [Run an agent](</on-prem/agents/run>)

**Last updated:**
