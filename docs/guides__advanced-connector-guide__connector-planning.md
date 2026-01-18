# Workato SDK Documentation

> **Source**: https://docs.workato.com/en/developing-connectors/sdk/guides/advanced-connector-guide/connector-planning.html
> **Fetched**: 2026-01-18T02:49:26.108788

---

# [#](<#connector-planning>) Connector planning

Before even beginning writing a single line of code, we highly recommend spending some time planning out all integration use cases for users of your custom connector on Workato. You’ll then be able to decompose them into the minimum set of actions and triggers in your connector to satisfy these use cases. This list of actions and triggers can always be expanded in the future.

Often, we’ve seen that connectors that are the most successful needn’t be the ones with the most actions or triggers but ones that power a wide range of business use cases from a prudent set of actions and triggers. If you’re building a connector to your platform as a way for your customers to integrate your services with the hundreds in Workato’s ecosystem, we would recommend going through this process with both a product manager and a developer to ensure the needs of your customers are met.

## [#](<#detailing-down-your-integration-use-cases>) Detailing down your integration use cases

Connectors can start small and grow big over time but it's always important to make sure that your connector can help you, your team or your customers find success in the integration use cases you have scouted out. This requires some time and effort thinking about how users would use your connector in recipes. First up, we highly recommend brainstorming to find out the exact use cases that you want to automate on Workato. For teams building connectors for internal use, this could be a tedious and manual process that you hope to automate. For teams building connectors on Workato to list on our platform so your customers can use Workato to include your application in their recipes, this should be something that you can foresee driving the most business value.

### [#](<#example-1>) Example 1:

As a developer from XYZ labs tasked to build a connector to Salesforce on Workato, my company sees ourselves manually importing new leads from Marketo daily into Salesforce and poor response times to new signups to our platform. Customer data and orders also have to be routinely exported from Salesforce into NetSuite, taking up a significant amount of the business analyst's team. Often, new deals also contain line items for products not present in NetSuite which are present in Salesforce.

To save time and lower the chance of human error, the integrations team has settled on 5 integration use cases to solve the problems above:

  1. Notifying your sales team in Slack about new leads in Salesforce
  2. Syncing account data in Salesforce with customers in NetSuite
  3. Syncing orders in Salesforce with sales receipts in NetSuite
  4. Creating leads in Salesforce when leads arrive through Marketo
  5. Syncing products in Salesforce with products in NetSuite

### [#](<#example-2>) Example 2:

XYZ lab’s main product is a cloud accounting software (XYZ accounting) that allows their customers to access and manage their financial accounts over any device. In order to expand the functionality of the platform, reduce customer churn and find new leads, the product team in XYZ labs is also looking to build an XYZ accounting connector on Workato. Users of XYZ accounting would then be able to use this connector to automate any of the tedious processes of exporting or importing accounting data out or into XYZ accounting.

After assessing the most heavily used portions of XYZ accounting as well as the variety of apps that people may use XYZ accounting with, a set of integration use cases were shortlisted as ones that would drive the most value for XYZ accounting customers.

  1. New closed-won opportunities in Salesforce create invoices in XYZ accounting
  2. New products in Salesforce create new products in XYZ accounting
  3. New payments in XYZ accounting update opportunities in Salesforce
  4. New vendors in XYZ accounting create new suppliers in Salesforce
  5. New approved expense reports in Expensify create an expense in XYZ accounting

## [#](<#defining-your-base-set-of-objects>) Defining your base set of objects

After deciding on what integration use cases you want to solve, this often translates into actions and triggers in a connector that we want to implement on certain objects.

As a start, we would recommend shortlisting 4 or 5 objects which you want to interact with through a recipe in Workato. For smaller applications, this could mean all objects. For large applications with over hundreds of objects, this could mean shortlisting 5 of them which meet your integration use cases. It's completely fine to keep your scope small and iterate over time.

### [#](<#example-3>) Example 3:

As an integration developer from XYZ labs, the integration use cases highlighted by the operations team revolves around multiple objects in Salesforce. Based on these use cases, it appears that support for `Orders`, `Leads`, `Accounts`, `Products` will allow my team to build the recipes they are looking for.

### [#](<#example-4>) Example 4:

As a developer tasked to build the connector to XYZ accounting, we can see that support should be prioritized for `Invoices`, `Products`, `Payments`, `Vendors` and `Expense reports`. When building a connector to your application for your customers, it's common to extend the number of objects supported when needed to ensure that a larger number of customers can use your connector beyond the use cases you have defined.

## [#](<#exploring-possible-actions>) Exploring possible actions

After you’ve decided on the objects, you now need to decide on what actions to support for your chosen objects. In most cases, we’ve found that starting with basic “Create”, “Read”, “Update”, “Delete” and “Search” (CRUDS) actions for your chosen objects cover most integration needs - especially when combined used together in recipes. Sometimes, we have seen users forgo “Delete” actions in cases as the deletion of data via an automated recipe might be undesirable.

Another possible type of action to support would be batch actions. Batch actions are actions that work with more than a single object but multiple ones and are often used in scenarios where multiple objects need to be synced in and out of an application. Consider if your users need this functionality to fulfill a core use case or if this can functionality added on later.

Another misstep that we often see with new users of Workato would be to overcomplicate actions. By keeping actions simple and always focused on handling one single thing, it makes recipes for your user’s easier to troubleshoot when errors do occur. For example, instead of creating an action - “Create a customer and attach the invoice to a customer”, this should be broken down into 2 actions - “Create a customer” and “Attach invoice”. This decoupling of actions makes them more general and allows your users to mix and match actions to achieve more.

API ACTION LIMITATIONS

Be aware of the functionalities and limitations of the API you plan to build a connector for.

Most well-designed APIs have endpoints to perform CRUD actions, and some also offer batch endpoints to support high-volume use cases.

## [#](<#exploring-possible-triggers>) Exploring possible triggers

Besides actions, we also recommend implementing object-based triggers to allow end-users of your user to trigger off events in your application. While Workato supports 3 types of triggers (polling, static webhooks and dynamic webhooks), it's often enough to implement a single type of trigger based on your integration use cases.

When deciding between polling triggers or webhook triggers, it's important to focus on how quickly your end-users would need to get their hands on new events. In time-sensitive situations - such as when a user requests for assistance on your website, webhooks might be the most appropriate to build recipes around to send help their way quickly. On the other hand, new sales in your CRM might not need to have webhook triggers where polling triggers might suffice.

API TRIGGER LIMITATIONS

Be aware of the functionalities and limitations of the API you plan to build a connector for.

Some APIs support webhook functionality. When webhooks are not available, [polling triggers](</developing-connectors/sdk/guides/building-triggers/poll.html>) can be a good alternative. If you are developing a connector for your own application, consider whether it should support webhook triggers.

For polling triggers, we often start with the basics such as triggers when objects are created or when objects created or updated.

## [#](<#exploring-other-actions-triggers-that-should-be-included-or-highlighted>) Exploring other actions/triggers that should be included or highlighted

For some applications, there may some special actions that aren’t included in your current shortlist of object-based actions and triggers. Review all integration use cases you and your team have set up to accomplish and take stock of any gaps in actions or triggers.

A great exercise would be to envision building recipes around the integration use cases you hope to accomplish and scout out any actions that may be missing. What we have found useful in Workato would be to draw a simple skeleton of the recipes that are needed to accomplish the use case.

### [#](<#example-5>) Example 5:

As the developer at XYZ labs building the XYZ connector on Workato, another important integration use case for our customers was the ability to use XYZ's integrated bank transfer functionality from a workplace messaging app like Slack. When drawing out the skeleton of the integration, we arrived at these steps:

Recipe: New command on Slackbot executes bank transfer on XYZ accounting | Action supported?  
---|---  
Trigger: New “Post bank transfer” command on Slack | Yes  
1\. Search for a supplier on XYZ accounting | Yes  
2\. Execute bank transfer on XYZ accounting using supplier ID | No  
3\. Post reply on Slack to notify user | Yes  

Using this skeleton, it’s easy to see that we’ve missed out on an “Execute bank transfer” action which would be critical in this use case.

CONNECTOR BUILDING IS AN ADVANCED FEATURE

Workato recommends gaining experience with recipe building before creating a custom connector. Refer to the [Getting started](</getting-started.html>) guide to learn the basics, or explore the [Use cases](</getting-started/workato-use-cases.html>) page for step-by-step walkthroughs of example recipes.

## [#](<#taking-stock-of-your-connector>) Taking stock of your connector

By the end of this exercise, you should have a list of actions and triggers that you plan to build. When placed into a table format, it should look something similar to this:

| New/updated trigger | Create action | Retrieve action | Update action | Delete action | Search action | Execute action  
---|---|---|---|---|---|---|---  
Invoices | Yes | Yes | Yes | Yes | Yes | Yes |   
Products | Yes | Yes | Yes | Yes | Yes | Yes |   
Payments | Yes | Yes | Yes | Yes | Yes | Yes |   
Vendors | Yes | Yes | Yes | Yes | Yes | Yes |   
Expense reports | Yes | Yes | Yes | Yes | Yes | Yes |   
Bank Transfer | Yes |  | Yes |  |  | Yes | Yes  

### [#](<#connector-building-time>) Connector building time

Now that you've sussed out what your connector generally looks like, its time to get building! The next chapter will go through how to organize and build your connector.
