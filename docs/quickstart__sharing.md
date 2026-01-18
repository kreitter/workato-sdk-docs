# Workato SDK Documentation

> **Source**: https://docs.workato.com/en/developing-connectors/sdk/quickstart/sharing.html
> **Fetched**: 2026-01-18T02:50:21.181468

---

# [#](<#sharing-your-connector>) Share a connector

You can share your connector with other users in the **Share** tab after you build your custom connector. You can share your connector with open or closed source code [through the community library](<#sharing-your-connector-with-the-community>) or [using a link](<#closed-source-code>).

## [#](<#released-versions-vs-shared-versions>) Released versions and shared versions

Shared version | Released version  
---|---  
Your connector's _shared_ version is the version which others receive when they install your connector for the first time. When you share a new version, everyone who installed your connector receives an option to update their connectors as well, including child connectors. | Your connector's _released_ version is the version all your recipes use. When you release a new version of your connector, all recipes using this connector update to use this version immediately.  

## [#](<#sharing-your-connector-with-the-community>) Upload a connector to the community library

Upload your connector to the community library

Complete the following steps to upload a connector to the community library:

1

Go to **Tools > Connector SDK**.

2

Select the connector you plan to upload.

![Click the connector](/assets/img/select-connector.099d7e40.png)_Click the connector you plan to upload_

3

Go to the **Share** tab, then click **Share version**.

![Click Share version](/assets/img/share-connector.d5c82070.png)_Click**Share version**_

4

Click **Publish connector** to open the **List on community library** dialog.

![Click Publish connector](/assets/img/publish-connector.2af4756e.png)_Click**Publish connector**_

5

Enter the name of the **App** this connector is built for. This field is case-sensitive. It will take longer to review your connector if its associated app is not listed in the drop-down menu, as Workato needs time to verify new apps.

![The Add details section](/assets/img/add-details.2f479264.png)_The**Add details** section_

6

Select any relevant tags in the **Category tags** drop-down menu.

7

Enter up to three **Search keywords** separated by commas.

8

Click the **Prevent direct installation** toggle if you plan to hide the connector's source code and redirect visitors to your landing page to request connector access.

9

Provide a **Landing Page URL** if you enabled **Prevent direct installation**. The page you link should showcase the connector and provide a clear path to your private sharing link. Go to the **Sharing privately using a link** section of your connector's **Share** tab to access your private sharing link.

10

Read the Workato developer agreement and click the checkbox to accept the terms and conditions.

![Read the Workato developer agreement](/assets/img/developer-agreement.96cfdd52.png)_Read the Workato developer agreement_

11

Click **List connector** to submit your connector for review.

12

Wait one business day for your connector to be reviewed. You can monitor the status of your submission in your connector's **Share** tab. Workato will notify you through your community profile's email when your connector has been reviewed.

![Monitor your connector's status](/assets/img/connector-approval.09c7c90d.png)_Monitor your connector's status_

REQUIRED PERMISSIONS

Uploading connectors to the community library requires [full access to the Connector SDK](</user-accounts-and-teams/role-based-access/new-model/privileges-reference.html#connector-sdk>). If you don't have the required permissions, contact your workspace admin to help you upload the connector.

## [#](<#closed-source-code>) Share a connector with a link 

FEATURE AVAILABILITY

Closed code source connector sharing is subject to the following limitations:

  * Collaborating workspaces must use the same data center as the custom connector's developer. Refer to [Share data between regions](</datacenter/datacenter-overview.html#share-data-between-regions>) for more information on cross-region collaboration.
  * Partners must be given access to this feature. Contact your Customer Success Representative to learn more.

Complete the following steps to share your custom connector with a link:

1

Go to **Tools > Connector SDK**.

2

Select the connector you plan to share.

![Select a connector](/assets/img/select-connector.099d7e40.png)_Select a connector_

3

Go to the **Share** tab.

4

Click **Set up connector sharing** to open the configuration module.

5

If your workspace has access to closed source connector sharing, you can decide to share your connector as open or closed source:

1

Keep the **Share without source code** toggle off to make your source code visible to all users.

![Share your connector as open source](/assets/img/set-up-connector-sharing.59965fd1.png)_Share your connector as open source_

2

Click **Start sharing** to make your source code visible and allow any workspace to view, install, or share your connector.

1

Click the **Share without source code** toggle to keep the source code of your connector private.

![Share your connector without source code](/assets/img/set-up-connector-sharing-closed-source.67139e29.png)_Share your connector without source code_

2

Enter the email addresses of workspaces that require access to your connector. Separate each email with a comma. These workspaces can view and install your custom connector but will not have access to your connector's source code.

3

Click **Start sharing**.

6

Click the **Enable shareable link** toggle to share your custom connector with others through a link.

If your connector is closed source, your source code is hidden and only workspaces granted access to your connector can use this link. ![Closed source shareable link](/assets/img/enable-shareable-link-closed.80b233a6.png)_Closed source shareable link_

If your connector is open source, your source code is visible and any workspace can view, install, or share your connector. ![Open source shareable link](/assets/img/enable-shareable-link-open.943f0aa7.png)_Open source shareable link_

### [#](<#manage-closed-source-connector-access>) Manage closed source connector access

Complete the following steps to manage access to your closed source connector:

1

Go to **Tools > Connector SDK**.

2

Select the connector you plan to manage, then go to the **Share** tab.

![Select a connector](/assets/img/select-connector.099d7e40.png)_Select a connector_

3

Click **Manage access**.

![Managed access](/assets/img/closed-source-manage-access.7d988553.png)_Closed source managed access_

4

Add or remove workspace email addresses to manage the workspaces that can view and install your connector. Separate each email with a comma. These workspaces do not have access to your connector's source code.

![Manage access to your connector](/assets/img/manage-access-list.fe013f38.png)_Manage access to your connector_

5

Click the **Notify primary admins about the connector’s availability via email** toggle if you plan to notify primary admins about the changes.

6

Click **Save changes**.

### [#](<#switch-between-open-source-and-closed-source>) Switch between open source and closed source

Switching your connector between open and closed source has the following effects:

  * The connector becomes exclusively visible and installable [via shareable link](<#closed-source-code>) by workspaces [you grant access to](<#manage-closed-source-connector-access>).

  * The current sharing link is revoked.

  * If the connector is published on the community, the listing is taken down.

  * Your connector's source code becomes hidden. If other users have already installed your connector, the source code will remain visible to them until they update the connector to a new version.

  * The connector and its source code become visible, installable, and shareable to all workspaces. If other users have already installed your connector, the source code will remain hidden to them until they update the connector to a new version.

  * The connector's sharing link is revoked.

Complete the following steps to switch your connector between open source and closed source:

1

Go to the **Share** tab of the connector you plan to modify.

2

Click **Change to show source code** or **Change to hide source code**. ![Change source code button](/assets/img/change-source-code-access.9a6c9297.png)_Change source code button_

3

Click **Update connector**. ![Update connector](/assets/img/change-source-code-status.4814c0d1.png)_Click**Update connector**_

## [#](<#exporting-packages-with-custom-connectors>) Export packages with custom connectors

You can use the [Recipe lifecycle management](</recipe-development-lifecycle.html>) tool to export and import entire folders of recipes from a sandbox environment to a production environment in Workato. Recipes that you plan to export from one account and import into another often contain custom connectors that you have built or cloned. Workato helps to export custom connectors in the manifests when you export these recipes.

The **latest released version** and the attached version note of your custom connector used in recipes are included in the manifest export. [Find out more about exporting here](</recipe-development-lifecycle/export.html>).

## [#](<#importing-a-manifest-with-custom-connectors>) Import a manifest with custom connectors

Workato first checks for an existing copy of the custom connector when you import a manifest. If no existing copy is found, a new custom connector is created with the latest released version as version 1. If an existing copy is found, a new latest version is created instead. In both cases, importing a manifest immediately releases the latest version of the custom connector for you because the recipes you are importing use that latest version. [Find out more about importing here](</recipe-development-lifecycle/import.html>).

EXPLORE RECIPE DEPENDENCIES

Be sure to explore dependencies in the existing recipes in your production account when importing a manifest that overwrites a connector.
