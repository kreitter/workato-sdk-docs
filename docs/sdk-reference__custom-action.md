# Workato SDK Documentation

> **Source**: https://docs.workato.com/en/developing-connectors/sdk/sdk-reference/custom-action.html
> **Fetched**: 2026-01-18T02:50:28.091263

---

# [#](<#sdk-reference-custom-action>) SDK Reference - `custom_action`  

This section enumerates all the possible keys to define a custom action.

Quick Overview

The `custom_action` key allows you to quickly define custom actions to unblock users of your connector when no standard action is available to them. Keep in mind that these actions require users to understand certain API concepts like how to find the relevant API endpoints and payload schema.

## [#](<#structure>) Structure
```ruby
 
        custom_action: Boolean,

        custom_action_help: {
          learn_more_url: String,

          learn_more_text: String,

          body: String
        }


```

* * *

## [#](<#custom-action>) `custom_action`

Attribute | Description  
---|---  
Key | `custom_action`  
Type | Boolean  
Required | Optional. Defaults to false where no custom action is added to your connector. Set to true to add custom actions as an option for your users.  
Description | This adds a custom action to your connector.  
Expected Output | `Boolean`   
i.e. `true`  
UI reference | ![](/assets/img/custom_action.981c720d.png)  

* * *

## [#](<#custom-action-help>) `custom_action_help`

Attribute | Description  
---|---  
Key | `custom_action_help`  
Type | Hash  
Required | Optional. If custom_action is `true`, then this hash allows you to customize the help text in your action.  
Description | Allows you to configure the help body, help button url and label.  
Expected Output | `Hash` See below for more information  
UI reference | ![](/assets/img/custom_action_help.125b64ae.png)  

TIP

Custom action help is important to guide users to the proper websites to collect information such as API documentation.

* * *

## [#](<#learn-more-url>) `learn_more_url`

Attribute | Description  
---|---  
Key | `learn_more_url`  
Type | String  
Required | Optional.  
Description | Defines the URL to send users when they click on the help link in the custom action.  
Expected Output | `'www.api-reference.com'`  

* * *

## [#](<#learn-more-text>) `learn_more_text`

Attribute | Description  
---|---  
Key | `learn_more_text`  
Type | String  
Required | Optional.  
Description | The label for the hyperlink text in the help.  
Expected Output | `'API documentation'`  

* * *

## [#](<#body>) `body`

Attribute | Description  
---|---  
Key | `body`  
Type | String  
Required | Optional.  
Description | The main help text body that appears above the learn more button. This body is HTML compatible.  
Expected Output | `'<p>Build your own Chargebee action with a HTTP request. <b>The request will be authorized with your Chargebee Hana connection.</b></p>`
