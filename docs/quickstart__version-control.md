# Workato SDK Documentation

> **Source**: https://docs.workato.com/en/developing-connectors/sdk/quickstart/version-control.html
> **Fetched**: 2026-01-18T02:50:22.301117

---

# [#](<#version-control>) Version control

Version control in the Workato SDK platform can be done directly through the UI. The source code of the latest version of your custom connector automatically displays in the code editor when you first enter a custom connector homepage. This represents the latest source code that you or anyone with access to your workspace has worked on and committed into a version.

Since the latest version of your custom connector may not be the version you want your active recipes to work off, we've also introduced the concept of releasing a specific version of your connector to be used by all recipes in your account.

This enables you to have a stable version of your custom connector released for use in all your recipes while you continue to improve your connector before releasing the next version.

CHECK THE VERSION

You can check the latest released version of a custom connector on the custom connector's homepage.

## [#](<#editing-the-latest-version>) Edit the latest version

The Workato SDK platform only allows you to edit the latest version of a custom connector's source code. By making changes directly in the code editor in the **Source code** tab, you can effectively edit the latest version. These changes are not saved until you click **Save changes** or test the code. The new custom connector source code is saved as the latest version when these changes are saved.

1

Click **Tools > Connector SDK**.

2

Select the custom connector you plan to edit.

3

Make your changes directly in the code editor on the **Source code** tab.

4

Click **Save**.

## [#](<#releasing-the-latest-version>) Release the latest version

You can only release the latest version of your custom connector on the SDK platform. Recipes in your Workato account using this custom connector begin using this version from the next job onwards when you release the latest version of a custom connector. Test thoroughly using the **Test code** tab before releasing a version to prevent any bugs from disrupting your active recipes.

Workato actively searches for errors in your code and prevents you from releasing a version with errors. This is to prevent your recipes from breaking. You are informed of the line of code which contains the error so you can fix it.

RELEASE TO ENABLE SEARCH

You must release a version of your connector before you can search for it while building your first connector. The currently released version of the connector displays on the custom connector homepage.

### [#](<#viewing-and-reverting-to-an-old-version>) Viewing and reverting to an old version

You can view and revert to an older version of your custom connector.

Navigate to the **Versions** tab of the custom connector homepage to view a table of versions. Clicking on any version will bring you to a page that contains a snapshot of the custom connector at that version.

1

Click **Tools > Connector SDK**.

2

Select the custom connector you plan to view or revert to.

3

Click the **Versions** tab and select a specific version to view.

![View old version](/assets/img/viewing-old-version.ef25cbdc.gif)_Select a specific version to view details about it and you can choose to revert to that specific version_

4

Optional. Click **Restore this version** to revert the version used in your recipes. This restores the version by creating a copy of the version's source code as a new latest version. You can begin editing or immediately release this version.

## [#](<#annotating-your-versions>) Annotate your versions

You can annotate different versions of your connector with notes as your connector grows in functionality (and versions). Annotation enables you and your team to know what changed in each version from the previous version, such as the addition of a new action or fixing a bug. This allows other developers to immediately know what state the connector is in and what work remains to be done.

![Version notes plain view](/assets/img/base-view-version-notes.7f5f9492.png) _Annotate your versions with crucial information such as milestones_

You can filter the list of versions to see only versions that have been released to your production recipes if they contain version notes or both. This allows you to strip away smaller intermediary versions that might clutter your view. We recommend that you annotate your versions after a round of enhancements to make it easier to collaborate with teammates to build robust and powerful connectors.

![Version notes plain view](/assets/img/filtered-view-version-notes.b3be4b92.png)_Version table when only those with version notes are chosen_

A popup displays to remind you to include any important notes before you release the latest version of your custom connector. This provides a simple and quick reminder to include what you have changed or added in this released version. This popup is optional and may be submitted without notes if you choose to do so.

![Version notes plain view](/assets/img/modal-popup-version-notes.9166b451.png) _When releasing versions, let people know what you're doing. Whether it's testing changes you made to the front end of your connector or introducing new functionality_
