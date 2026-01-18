# Workato SDK Documentation

> **Source**: https://docs.workato.com/en/developing-connectors/sdk/guides/authentication/on-prem.html
> **Fetched**: 2026-01-18T02:49:41.070978

---

# [#](<#how-to-guide-opa-authentication>) How-to guide - OPA authentication

HTTP requests made in a custom adapter are sent from Workato [IP addresses](</security/ip-allowlists.html#traffic-from-workato>) by default. You can configure the adapter to instead route all requests through an [on-prem agent](</on-prem.html>).

Complete the following steps to enable OPA authentication in a custom connector:

1

Sign in to Workato.

2

Go to **Tools > Connector SDK**.

3

Select the connector you plan to modify, or click **\+ New connector** to [create a new connector](</developing-connectors/sdk/guides/walkthrough.html#create-a-custom-connector>).

4

Add `secure_tunnel` set to `true` as a top level property in your custom adapter code.

USE OPA FOR TLS CERTIFICATES

Configure TLS client certificates in the OPA connection profile instead of your SDK connector code. OPA terminates TLS to your target service, and the certificate must be configured in the HTTP profile. Refer to [On-prem agent – Connection profiles](</on-prem/agents/connection/profile.html#http-profile>) for instructions to configure TLS client certificates in OPA. The connection returns SSL errors if you configure the certificate in the SDK connector.

For example:
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
```ruby
 
    selected: lambda do |connection|
      connection["auth_type"] || 'api_key'
    end,


```

5

Click **Save > Release latest version**.

6

Summarize the changes you made to the connector in the **Confirm release** modal.

![Change summary and confirmation window](/assets/img/confirm-version-release-window.561b4f2d.png)_Summarize your changes to the connector_

7

Click **Release** to release the new version of the connector in your workspace and allow it to be used in recipes.

The **New connection** page for your connector displays the **Connection type** drop-down menu after you set `secure_tunnel` to `true`. You can use this menu to select the [on-prem group](</on-prem/groups.html#on-prem-group>) you plan to use for your connection.

![Connection without option to use OPA](/assets/img/OPA-example-without-secure-tunnel.18090057.png)_**New connection** page without `secure_tunnel` enabled_

![Connection with option to use OPA](/assets/img/OPA-example-with-secure-tunnel.22653f76.png)_**New connection** page with `secure_tunnel` enabled_

## [#](<#next-steps>) Next steps

Refer to the [SDK reference](</developing-connectors/sdk/sdk-reference/connection.html>) guide for a list of available `connection` keys and parameters or refer to the following guides set up an on-prem agent:

  * [Create an on-prem group](</on-prem/groups/create-group.html>)
  * [Add an agent to a group](</on-prem/groups/add-agent.html>)
  * [Run an agent](</on-prem/agents/run.html>)
