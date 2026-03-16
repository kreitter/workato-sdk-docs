# Workato SDK Documentation

> **Source**: https://docs.workato.com/en/developing-connectors/sdk/quickstart/sharing.html
> **Fetched**: 2026-03-16T03:09:01.635561

---

# [#](<#sharing-your-connector>) Share a connector

You can share your connector with other users in the **Share** tab after you build your custom connector. You can share your connector as open-source or closed-source [using a link](<#closed-source-code>) or [through the community library](<#sharing-your-connector-with-the-community>).

## [#](<#released-versions-vs-shared-versions>) Released versions and shared versions

Version type | Description  
---|---  
Released version | Determines which connector version your recipes use. All recipes that use this connector update immediately when you release a new version.  
Shared version | Determines which connector version other users install. Users who installed your connector can choose to update their connectors, including child connectors, when you share a new version.  

## [#](<#open-source-vs-closed-source>) Open-source and closed-source connectors

You can share your connector as open-source or closed-source. An open-source connector makes the connector's source code available for anyone to view, modify, and distribute. A closed-source connector keeps its source code private. Users can't view, modify, or distribute the source code after installation.

FEATURE AVAILABILITY

Closed code source connector sharing is subject to the following limitations:

  * Collaborating workspaces must use the same data center as the custom connector's developer. Refer to [Share data between regions](</datacenter/datacenter-overview.html#share-data-between-regions>) for more information on cross-region collaboration.
  * Partners must be given access to this feature. Contact your Customer Success Representative to learn more.

### [#](<#switch-between-open-source-and-closed-source>) Switch between open-source and closed-source

Switching your connector between open-source and closed-source changes its visibility, sharing behavior, and source code access.

Workato restricts visibility and hides the connector's source code when you switch to closed-source:

  * Workato revokes the current sharing link.
  * Workato hides the connector's source code. Users who already installed the connector can still view it until they update to a newer version.

Workato makes the connector and its source code publicly accessible when you switch to open-source:

  * The connector and its source code become visible, installable, and shareable to all workspaces.
  * Workato revokes the existing sharing link.
  * Users who already installed the connector continue to see the source code as hidden until they update to a newer version.

Complete the following steps to switch your connector between open-source and closed-source:

1

Go to the **Share** tab of the connector you plan to modify.

2

Click **Make source code hidden** or **Make source code visible**.

![Change source code button](/assets/img/change-source-code-access.fac6a25a.png)_Change source code button_

3

Click **Update connector**.

![Update connector](/assets/img/change-source-code-status.2c5887dc.png)_Click**Update connector**_

## [#](<#closed-source-code>) Share a connector with a link

You can use a shareable link to distribute your connector directly to specific workspaces.

Complete the following steps to generate a shareable link:

1

Go to **Tools > Connector SDK**, select the connector you plan to share, and open the **Share** tab.

![Select a connector](/assets/img/select-connector.099d7e40.png)_Select a connector_

2

Click the **Enable shareable link** toggle.

3

Copy the generated link and share it with the appropriate workspaces.

The behavior of the shareable link depends on whether your connector is open-source or closed-source. Refer to [Open-source and closed-source connectors](<#open-source-vs-closed-source>) for more details.

### [#](<#manage-closed-source-connector-access>) Manage closed-source connector access

This section applies only to closed-source connectors that you share using a link. Refer to [Open-source and closed-source connectors](<#open-source-vs-closed-source>) for an overview of closed-source behavior.

Complete the following steps to manage access to your closed-source connector:

1

Go to **Tools > Connector SDK**.

2

Select the connector you plan to manage, then go to the **Share** tab.

![Select a connector](/assets/img/select-connector.099d7e40.png)_Select a connector_

3

Click **Manage access**.

![Managed access](/assets/img/closed-source-manage-access.9ec89043.png)_Closed source managed access_

4

Add workspace email addresses. Separate each email with a comma.

These workspaces can view and install the connector but can't access the source code.

![Manage access to your connector](/assets/img/manage-access-list.e38a123f.png)_Manage access to your connector_

5

Click the **Notify primary admins about the connector’s availability via email** toggle if you plan to notify primary admins about the changes.

6

Click **Save changes**.

## [#](<#sharing-your-connector-with-the-community>) Share a connector to the community library

Complete the following steps to share a connector to the community library:

1

Go to **Tools > Connector SDK**.

2

Select the connector you plan to share.

![Click the connector](/assets/img/select-connector.099d7e40.png)_Click the connector you plan to upload_

3

Go to the **Share** tab, then click **Share version**.

![Click Share version](/assets/img/share-connector.d5c82070.png)_Click**Share version**_

4

Optional. Click the **Make source code hidden** button if you plan to publish a closed-source connector. This ensures your connector code isn't visible or editable by others. You can't change this setting after publishing unless you unpublish the connector.

![Choose to hide your source code](/assets/img/change-source-code-hidden.b6abbb70.png)_Choose to hide your source code_

5

Click **Edit** in the connector description and ensure the description includes a clear way for users to contact support, such as a support email, documentation link, or help center. Submissions without support contact information may be rejected during review.

![Edit connector description](/assets/img/edit-connector-description.01da6c7f.png)_Edit connector description_

6

Click **Publish connector** to open the **List on community library** dialog.

![Click Publish connector](/assets/img/publish-connector.2af4756e.png)_Click**Publish connector**_

7

Enter the **App** name. This field is case-sensitive.

![The Add details section](/assets/img/add-details.ff37aff4.png)_The**Add details** section_

8

Select any relevant tags in the **Category tags** drop-down menu.

9

Enter up to three **Search keywords** , separated by commas.

10

Optional. Click the **Prevent direct installation** toggle if you plan to redirect visitors to a landing page to request access.

The following occurs when this option is enabled:

  * End users can't install the connector directly from the community listing.
  * Users can install the connector only through your private sharing link. Go to the **Sharing privately using a link** section of your connector's **Share** tab to obtain the link. Refer to [Share a connector with a link](</developing-connectors/sdk/quickstart/sharing.html#closed-source-code>) to learn how to grant access to users.
  * You must provide a **Landing Page URL** and a clear path.

Any workspace can install the connector directly from the community listing if you don't enable this toggle. Closed-source connectors hide the source code but don't restrict installation.

11

Provide a **Landing Page URL** if you enabled **Prevent direct installation**. The page you link to should showcase the connector and provide a clear path on how to obtain the private sharing link of the connector.

12

Read the Workato developer agreement and click the checkbox to accept the terms and conditions.

![Read the Workato developer agreement](/assets/img/developer-agreement.96cfdd52.png)_Read the Workato developer agreement_

13

Click **List connector** to submit your connector for review.

14

Workato notifies you through your community profile's email when your connector has been reviewed.

![Monitor your connector's status](/assets/img/connector-approval.09c7c90d.png)_Monitor your connector's status_

REQUIRED PERMISSIONS

Sharing connectors to the community library requires [full access to the Connector SDK](</user-accounts-and-teams/role-based-access/new-model/privileges-reference.html#connector-sdk>). If you don't have the required permissions, contact your workspace admin to help you share the connector.

## [#](<#exporting-packages-with-custom-connectors>) Export packages with custom connectors

You can use the [Recipe lifecycle management](</recipe-development-lifecycle.html>) tool to export and import entire folders of recipes from a sandbox environment to a production environment in Workato. Recipes that you plan to export from one account and import into another often contain custom connectors that you have built or cloned. Workato helps to export custom connectors in the manifests when you export these recipes.

The **latest released version** and the attached version note of your custom connector used in recipes are included in the manifest export. Refer to [Exporting recipes](</recipe-development-lifecycle/export.html>) for more information.

## [#](<#importing-a-manifest-with-custom-connectors>) Import a manifest with custom connectors

Workato first checks for an existing copy of the custom connector when you import a manifest. If no existing copy is found, a new custom connector is created with the latest released version as version 1. If an existing copy is found, a new latest version is created instead. In both cases, importing a manifest immediately releases the latest version of the custom connector for you because the recipes you are importing use that latest version. Refer to [Importing recipes](</recipe-development-lifecycle/import.html>) for more information.

EXPLORE RECIPE DEPENDENCIES

Be sure to explore dependencies in the existing recipes in your production account when importing a manifest that overwrites a connector.
