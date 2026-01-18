# Workato SDK Documentation

> **Source**: https://docs.workato.com/en/developing-connectors/sdk/guides.html
> **Fetched**: 2026-01-18T02:49:20.360405

---

# [#](<#connector-how-to-guides>) Connector how-to guides

The guides in this section help you cover various parts of building a connector from authentication to building actions or triggers. Take a look at the examples to get a sensing of how you can build your connector! Here are some basics to get you started:

## [#](<#the-basics>) The basics

In Workato, we allow you to build custom connectors on our SDK using ruby (a coding language). Some basic coding knowledge in any language is recommended but we believe our SDK (Software Development Kit) has been built such that users at any level will be able to build custom connectors. The custom connectors you build can be used in any number of your recipes and you'll also able to share them with your coworkers, friends, or even the community at large.

Through out the whole process, you'll be able to build, test, and push out your custom connector directly from Workato's platform. This means working directly from the browser you have open right now and never having to install anything onto your computer. Pretty neat right?

Connector source code which you write on the SDK platform will be hosted in Workato's servers and is executed whenever a recipe using that connector is triggered. To find out more about the features of the Connector SDK console, check out our [Platform Quick Start](</developing-connectors/sdk/quickstart/quickstart.html>).

## [#](<#connector-definition-overview>) Connector definition overview

A custom connector on Workato always starts off with curly braces that encapsulates all code (Curly braces look like this `{}`). Inside the curly braces, each connector has numerous root keys that are responsible for different aspects of the connector. For example, the code `connection: { ... }` is referred to as the `connection` key. To find out more information about Connector definitions, check out our [SDK reference](</developing-connectors/sdk/sdk-reference.html>)

Take note that these key names are strictly defined and must be spelled exactly. Our framework uses these keys to know where to refer when looking to perform authorizations or execute any triggers or actions. Inside each object, there will be further nested keys that allow you to declare input fields for connections, actions, and triggers which we will cover later on.

## [#](<#sdk-cheat-sheet>) SDK cheat sheet

Read and download our [SDK cheat sheet (opens new window)](<https://public-workato-files.s3.us-east-2.amazonaws.com/Uploads/workato_connector_sdk_cheat_sheet.pdf>) to get started with the connector SDK quickly.
