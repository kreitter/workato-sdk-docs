# Workato SDK Documentation

> **Source**: https://docs.workato.com/en/developing-connectors/sdk/quickstart/FAQ.html
> **Fetched**: 2026-01-18T02:50:18.947047

---

# [#](<#connector-sdk-faqs>) Connector SDK FAQs

Get answers to frequently asked connector SDK questions.

How do I access Workato's Connector SDK platform?

You can access the [Connector SDK platform](</developing-connectors/sdk/quickstart.html#navigating-to-the-sdk-platform-homepage>) by navigating to the **Tools** tab on the main Workato recipes page and selecting **Connector SDK**. You can manage custom connectors that you've built or cloned.

I accidentally released an unstable version of my connector. How can I release the last version of my connector again?

[Restoring a stable version](</developing-connectors/sdk/quickstart/version-control.html#viewing-and-reverting-to-an-old-version>) of your connector is easy. Search your version history to find the version of your connector that was stable, using the **Released at** column to guide you. Restore that version and release it.

Why does an autosave occur before the release of a version or use of the Test code tab?

[Autosaves](</developing-connectors/sdk/quickstart/sharing.html>) only occur when there are any unsaved changes to your connector code. This ensures that any last-minute changes you make to your code without saving are picked up. We recommend that you use the SDK **Test code** tab to thoroughly test your changes before releasing a version.

Should I use the connector share link or packages to move my connector from my sandbox environment to my production environment?

[Packages](</developing-connectors/sdk/quickstart/sharing.html#exporting-packages-with-custom-connectors>) are only available on certain plans. While both share link and packages can accomplish the migration of your SDK connector, we highly recommend building and testing your custom connector and its associated recipes in your sandbox Workato environment. When you're ready, packages is the fastest way to bring your custom connector (and recipes) from your sandbox environment to production.

What happens to all my existing connectors that existed before an enhancement?

All existing connectors are backward compatible with enhancements. Your connectors contain a list of versions from before each release. You can see versions from the time your custom connector was created. If you create new versions, you must release them to use the changes in your recipes.

If I've cloned a custom connector and there is an update notification, what happens when I update?

Update notifications always use the [latest shared version](</developing-connectors/sdk/quickstart/sharing.html#released-versions-vs-shared-versions>) of its parent connector. Choosing to update creates a new version on top of your custom connector. Be sure to verify that the newly updated connector has changes that make sense to you before releasing it to your own workspace. You can make edits to the new connector code to suit your purposes.

How do I know what changes occur across each version and who created that version when working in a team workspace?

Our [version history](</developing-connectors/sdk/quickstart/version-control.html#version-control>) table gives you insight into the actions and triggers present in each version. Our versions table also displays the name of the user who created a connector version and who released a specific version of the connector.

How can I test a specific version of my custom connector in recipes before releasing it to all my active recipes?

You can create a dummy custom connector that hosts the same code as the latest stable version for [testing](</developing-connectors/sdk/quickstart/debugging.html#testing-a-connection>). You can add improvements to this dummy custom connector and test it separately with dedicated recipes. We suggest testing this new version on copies of both existing recipes that use the custom connector and new recipes to ensure that there are no regressions.

Is there a set way that I should use version notes?

[Version notes](</developing-connectors/sdk/quickstart/version-control.html#annotating-your-versions>) provide a free-form communication space to share version changes with others in your workspace as well as with those with whom you have shared your connector. We recommended updating the description of your connector each time you reach a new milestone, such as adding new actions or triggers.

What is the benefit of creating a connector using sample code?

Creating a connector using [sample code](</developing-connectors/sdk/quickstart.html#creating-a-connector-using-sample-code>) allows you to begin development using a pre-built template for applications like Calendly. The code includes comments that guide you on how to build authentication, actions, and triggers for your custom connector.

What code editor does Workato's SDK platform use, and what are the basic keyboard shortcuts available for editing code?

Workato's SDK platform uses [Code Mirror](</developing-connectors/sdk/quickstart.html#using-the-workato-code-editor>) for editing connector code. The platform provides real-time error highlighting. Some basic hotkeys include:

  * Persistent search

    * MacOS: press `command`+`f` to open the search box.
    * Windows: press `ctrl`+`f` to open the search box.
  * Replace

    * MacOS: press `command`+`option`+`f` to replace.
    * Windows: press `ctrl`+`shift`+`f` to replace.
  * Replace all (Shift-Ctrl-R or Shift-Cmd-Option-F)

    * MacOS: press `shift`+`command`+`option`+`f` to replace all.
    * Windows: press `shift`+`ctrl`+`r` to replace all.

How do I delete a custom connector in Workato, and what considerations should I keep in mind when doing so?

You can [delete a custom connector](</developing-connectors/sdk/quickstart.html#deleting-a-custom-connector>) in Workato, but you must first stop any active running recipes that use the connector. Deleting a custom connector doesn't affect its clones, as they are separate copies. Always ensure you have backups and understand the impact of deletion on your automations.
