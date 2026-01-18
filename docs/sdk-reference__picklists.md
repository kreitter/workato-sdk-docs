# Workato SDK Documentation

> **Source**: https://docs.workato.com/en/developing-connectors/sdk/sdk-reference/picklists.html
> **Fetched**: 2026-01-18T02:50:32.686527

---

# [#](<#sdk-reference-pick-lists>) SDK Reference - `pick_lists`

Picklists are used in conjunction with some input fields to enumerate the possible options in a drop-down. Picklist options can be stored in the `pick_lists` key or defined directly in the input field hash. Input fields that use `pick_list` attribute have to be of the following `control_type`:

  * `select`
    * Allows the user to select a single input from the drop-down.
  * `multiselect`
    * Allows the user to select multiple inputs from the drop-down.
  * `tree`
    * Allows the user to select a single or multiple inputs from a hierarchical drop-down.

Quick Overview

Pick lists are a great way to make your connector easier to use when the API only accepts a certain set of values. Rather than having the user type it in manually, you should use picklists so they can easily select the value from a drop-down. The `pick_list` key is where you can store these options and refer to them when building your input fields.

## [#](<#structure>) Structure
```ruby
 
        pick_lists: {

          [Unique_pick_list_name]: lambda do |connection, pick_list_parameters|
            Array
          end,

          [Another_unique_pick_list_name]: lambda do |connection, pick_list_parameters|
            Array
          end
        },


```

* * *

Attribute | Description  
---|---  
Key | `[Unique_pick_list_name]`  
Type | lambda function  
Required | True  
Description | This lambda function is invoked whenever its parent object_definition's key is called in an action or trigger. It is able to make HTTP requests to dynamically build schema from metadata endpoints. The output of this lambda function should be an array of hashes that represents the input or output fields.  
Possible Arguments | `connection` \- Hash representing user given inputs defined in `connection`   
`pick_list_parameters` \- Used when defining dependent picklists.  
Expected Output | Array of Array  

Pick_lists outputs should be a 2D array in the following format:
```ruby
 
    [
      [ "Picklist Label", "Value" ],
      [ "Picklist Label", "Value" ],
      [ "Picklist Label", "Value" ],
      [ "Picklist Label", "Value" ]
    ]


```

\- pick_lists not allowed for connections fields

Example - options in connection fields

When defining enumerable values for connection fields, take note that you may not reference `pick_lists` defined in your connector.

Instead, you may define these fields statically and using the schema attribute - `options`
```ruby
 
    connection: {
      fields: [
        {
          name: 'environment',
          label: 'Instance environment',
          control_type: 'select',
          options: [
            ['Production', 'production'],
            ['Sandbox', 'Sandbox']
          ]
        }
      ]
    }


```

Example - pick_lists: - Static

Pick_lists can be static. When referenced, this definition would return the array stored in it. When an input field references this picklist, this array is returned and rendered on the front end as a drop-down.

![](/assets/img/static_picklist.5f9188f3.png)
```ruby
 
        input_fields: lambda do |object_definitions|
          [
            {
              name: 'event_category',
              control_type: 'select',
              pick_list: 'events'
            }
          ]
        end,


```
```ruby

        pick_lists: {
          events: lambda do |connection|
            [
              ["Meeting","meeting"],
              ["Webinar","webinar"],
              ["Cloud recording","recording"],
              ["User","user"],
            ]
          end
        },


```

Example - pick_lists: - dependent & static

Dependent pick lists allow you to change the contents of a pick list based on the value of another field. For example, rather than displaying all the cities in a single pick list, we can selectively display only cities from a country, selected in another field.

![](/assets/img/dependent_picklist.58a1fa9b.gif)
```ruby
 
        input_fields: lambda do |_object_definitions|
          [
            {
              name: 'country',
              control_type: 'select',
              pick_list: 'countries',
              optional: false
            },
            {
              name: 'city',
              control_type: 'select',
              pick_list: 'cities',
              pick_list_params: { country: 'country' },
              optional: false
            }
          ]
        end


```
```ruby

        pick_lists: {
          countries: lambda do |_connection|
          [
            ['United States', 'USA'],
            ['India', 'IND']
          ]
          end,

          cities: lambda do |_connection, country:|
          {
            'USA' => [
              ['New York City', 'NYC'],
              ['San Fransisco', 'SF']
            ],
            'IND' => [
              ['Bangalore', 'BNG'],
              ['Delhi', 'DLH']
            ]
          }[country]
          end
        }


```

Example - pick_lists: - dependent & dynamic

In this example, accounts is an independent dynamic pick list while properties is a dependent dynamic pick list. When defining dynamic picklists, the response from the HTTP request should still be transformed into the same array of arrays.

In this example, we used the `.pluck` function to do the transformation.

![](/assets/img/dynamic_dependent_picklist.cc817402.gif)
```ruby
 
        input_fields: lambda do |_object_definitions|
          [
            {
              name: 'scope_id',
              label: 'Team',
              optional: false,
              control_type: 'select',
              pick_list: 'tenant_licenses'
            },
            {
              name: 'platform_id',
              control_type: 'select',
              pick_list: 'platforms',
              label: 'Platform',
              pick_list_params: { scope_ids: 'scope_id' },
              hint: 'Platform is required for creating Content'
            }
          ]
        end


```
```ruby

        pick_lists: {
          tenant_licenses: lambda do |connection|
            app_id = get("api/v5/client/client:#{connection['client_id']}")&.
                       dig('data', 'app_id')
            tenant_id = get("/api/v5/app/#{app_id}")&.dig('data', 'tenant_id')
            get('/api/v5/license/').
              params(tenant_id: tenant_id,
                     statuses: 'active')['data']&.
              select { |lic| lic['parent_id'].present? }&.
              pluck('name', 'id')
          end,

          platforms: lambda do |_connection, scope_ids:|
            get('/api/v5/platform/').
              params(scope_ids: scope_ids)['data']&.
              pluck('name', 'id')
          end,
        }


```

Example - pick_lists: - tree

Workato also allows for `tree` type picklists. Tree picklists are often used to model hierarchical structures in applications such as file/folder structures. When using tree picklists, traditional `pick_list_parameters` are ignored and replaced by a double splat variable.

To best explain this, we will use the concept of a file and folder structure, where folders might contain additional folders or files. All folders and files are considered nodes, while the main distinction is that folders might have child nodes whereas files may not. When you define a tree picklist, each time the user clicks on a folder node, the picklist is re-evaluated to build out the child nodes within it. The value of the folder node that the user clicked on can be found by `args&.[](:__parent_id)`. If this value is nil, this indicates that we are at the root node.
```ruby
 
        input_fields: lambda do |_object_definitions|
          [
            {
              name: 'path',
              label: 'File path',
              optional: false,
              control_type: 'tree',
              pick_list: "file_path"
            },
          ]
        end


```
```ruby

        pick_lists: {
          file_path: lambda do |_connection, **args|
            # Get sub folders
            if (folder_path = args&.[](:__parent_id)).presence
              path = []
              response = get("/pubapi/v1/fs#{folder_path}").params(list_content: true, sort_by: 'name')
              if response['is_folder']
                path << response['folders']&.map { |folder| [folder['name'].labelize, folder['path'].gsub(' ', '%20'), nil, true] }
                path << response['files']&.map { |file| [file['name'].labelize, file['path'].gsub(' ', '%20'), nil, false] } if response['files'].present?
                Array.wrap(path.compact).flatten(1)
              end
            else
              # Get root folders
              get('/pubapi/v1/fs/')['folders']&.map do |folder|
                [folder['name'].labelize, folder['path'].gsub(' ', '%20'), nil, true]
              end
            end
          end,
        }


```

![](/assets/img/tree-file-only.a2e08ad6.gif)

In the above case, we have wanted to only allow users to select files to be downloaded. However, in a variety of cases, you might want to allow users to also select folders (the nodes) as you want them to provide a path to a folder instead of a file. This can be configured like below:
```ruby
 
        input_fields: lambda do |_object_definitions|
          [
            {
              name: 'path',
              label: 'Folder path',
              optional: false,
              control_type: 'tree',
              pick_list: 'folder_path',
              tree_options: {
                selectable_folder: true
              }
            },
          ]
        end


```

Another variation is when you need to allow end users to select multiple folders. This can be configured like below:
```ruby
 
        input_fields: lambda do |_object_definitions|
          [
            {
              name: 'path',
              label: 'Folder path',
              optional: false,
              control_type: 'tree',
              pick_list: 'folder_path',
              tree_options: {
                selectable_folder: true,
                multi_select: true,
                force_selection_hierarchy: true # Setting this to true causes all child nodes to be selected when the parent is selected.
              }
            },
          ]
        end


```
