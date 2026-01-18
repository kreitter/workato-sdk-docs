# Workato SDK Documentation

> **Source**: https://docs.workato.com/en/developing-connectors/sdk/guides/advanced-connector-guide/introduction.html
> **Fetched**: 2026-01-18T02:49:27.251205

---

# [#](<#workato-advanced-connector-building-guide>) Workato advanced connector building guide

Here is a final guide that focuses on the usability and the code quality of a connector. We will be going through exercises that can help you plan out robust connectors as well as guidelines on writing connector code. At this point, we assume that you have read through the basics of connector building found over [here.](</developing-connectors/sdk.html>)

In this guide, we introduce the concept of object-based connectors, something that you should have seen before if you have used NetSuite, Salesforce, or numerous other connectors on Workato. Object-based connectors are ones that reduce the amount of clutter by allowing users to first select a verb such as “Create” or “Update” before selecting the object they want to create or update.

## [#](<#what-should-i-expect-to-gain-from-this-guide>) What should I expect to gain from this guide?

This guide should help organize your thoughts around building connectors that are usable by a wide audience. While custom connectors could be used as a quick way for your team to connect to unsupported web APIs on Workato, this guide looks at a sustainable approach of connector building. Workato also allows users from our community to promote their custom connectors to become platform-wide connectors - ones that can be found and used by anyone on the platform.

If you're reading this guide to build a connector on Workato to your own web API, one great resource would be this guide by google over [here (opens new window)](<https://cloud.google.com/apis/design/>) which goes through resource-oriented API designs. Well built APIs greatly ease the connector building experience as well as integration experience for users of your application when creating recipes on Workato.

## [#](<#looking-to-submit-your-custom-connector-to-our-platform>) Looking to submit your custom connector to our platform?

If you're building this connector to be accessible by our active community of Workato chefs, head over to our [support site to submit a ticket (opens new window)](<https://support.workato.com/support/tickets/new>). We'll route you to the proper channels and also set up some time to review your connector.

**Expect to see the following benefits:**

  1. Increased usage of your API for your customers as they integrate with Workato
  2. More leads for your services as users on Workato are constantly searching for new business applications that make their lives easier
  3. Greater exposure to integration use cases from our fantastic community

## [#](<#object-based-connectors>) Object-based connectors

You may find yourself wondering what object-based connectors are in the first place but before that we must first clarify what resources and procedures are in applications.

When looking at a cloud based application, we often see that most applications have several resources at their core. These resources hold data in structures that users of the application can interact with and appreciate. For example, a resource in a banking application could be a `Customer` which contains all relevant information to a customer in the bank.

On the other hand, applications also provide a whole host of other services beyond holding data in certain organized resources for their users. These processes that applications perform on resources in their systems also create large amounts of business value for their users. For example, a process in the same banking application could be a `Bank Transfer`. This process could also include certain validations such a checking the balance of each account as well as ensuring the atomicity of the operation.

When building connectors in Workato, we've found that object-based connectors can encompass **both** but often, we see that working with resources is often the foundation of a connector before moving on to specific processes.

In the next chapter, we will go through thought exercises that can better help you plan out your connectors.
