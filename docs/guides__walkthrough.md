# Workato SDK Documentation

> **Source**: https://docs.workato.com/en/developing-connectors/sdk/guides/walkthrough.html
> **Fetched**: 2026-01-18T02:50:15.668316

---

# [#](<#build-your-first-connector>) Build your first connector

This guide demonstrates how to build a custom connector with the Connector SDK and the [Star Wars API (SWAPI) (opens new window)](<https://swapi.tech/>). SWAPI provides free access to information about Star Wars characters, vehicles, and other resources.

## [#](<#create-a-custom-connector>) Create a custom connector

Complete the following steps to create a new custom connector:

1

Sign in to your Workato account.

2

Go to **Tools > Connector SDK**.

![Navigating to SDK](/assets/img/Navigating-to-SDK.6b40667e.png) _Go to Tools > Connector SDK_

3

Click **Create connector** to open the Connector SDK wizard.

![Click Create connector](/assets/img/create-connector.a2642c32.png)_Click**Create connector**_

4

Select **Get guided from a Workato template** as your starting point, then click **Next**.

![Select your starting point](/assets/img/starting-point.506e3f8e.png)_Select your starting point_

5

Enter `Star Wars Information` in the **What application is this connector for?** field.

6

Drag and drop a PNG or JPG file to the **Add a logo** field, or click **upload from device**.

![Naming your custom connector](/assets/img/custom-connector-title-description.2fc1032a.png) _Fill in the name of your custom connector_

7

Click **Go to editor**.

After these steps, the Connector SDK opens, where you can define the connection details and configure your connector.

## [#](<#creating-a-connection>) Create a connection

To connect to an API, you must first identify its required authentication method. Since SWAPI doesn't require authentication, you can send requests to SWAPI without verifying your identity.

Complete the following steps to create a SWAPI connection:

1

Open the **Source code** tab.

2

Copy and paste the following code snippet into the code editor:
```ruby
 
    {
      title: 'Star Wars Information',

      connection: {
        fields: [
          {
            name: "object",
            hint: "Enter the object you plan to use to test your connection.",
          }
        ]
      },

      test: lambda do |connection|
        get("https://swapi.tech/api/#{connection["object"]}")
      end,

      # More code below but hidden for now!
    }


```

How does this code snippet work?

This code snippet includes the following keys:

  * `connection`
  * Defines the input fields that appear when users connect to your connector.
  * `fields`
  * Declares input fields. You can use the user input collected inside this key in other parts of the custom connector code.
  * `test`
  * Declares the test that runs when a user clicks **Connect**. This key allows Workato to provide feedback on whether the connection succeeds or fails.

What does this test do?

The SWAPI connector sends a `GET` request to a specified URL endpoint, and the test succeeds if the request returns a `200` status code. The `test` key defines this functionality, using the `get()` function to execute the request.

In this example, your input determines the target URL for the HTTP call. The snippet references your input through the `connection` key, specifically `connection["object"]`.

3

Enter a name in the **Connection name** field.

![Connection input field](/assets/img/Connection-input-fields.3c8dd1ea.png) _Example of input fields for connection setup_

4

Enter one of the following valid inputs in the **Object** field:

  * `films`
  * `people`
  * `planets`
  * `species`
  * `starships`
  * `vehicles`

5

Click **Connect** to establish the connection. A successful connection displays the following confirmation:

![successful-connection](/assets/img/successful-connection.0c160763.png) _Successful connection_

## [#](<#create-an-action>) Create an action

SWAPI allows you to retrieve information about Star Wars such as people, planets, and films. This example demonstrates how to build an action named `Get person by ID` that retrieves information about a Star Wars character. You can access and use the returned information in subsequent recipe steps with [datapills](</recipes/data-pills-and-mapping.html>).

![Action revealed to user](/assets/img/get-character-by-id-action.21ec9ed9.png) _Create the Get person by ID action_

Complete the following steps to create an action:

1

Replace the existing code in the **Source code** tab with the following snippet:
```ruby
 
    {
      title: 'Star Wars Information',

      connection: {
        fields: [
          {
            name: "object",
            hint: "Enter the object you plan to use to test your connection.",
          }
        ]
      },

      test: lambda do |connection|
        get("https://swapi.tech/api/#{connection["object"]}")
      end,

      actions: {
        get_person_by_id: {
          input_fields: lambda do
              [{
                name: 'id',
                label: 'Person ID',
                type: 'integer',
                default: '1',
                optional: false
              }]
            end,

          execute: lambda do | connection, input |
            get("https://swapi.tech/api/people/#{input["id"]}")
          end,

          output_fields: lambda do
              [{
                  name: "message",
                  label: "Message",
                  type: "string"
                },
                {
                  name: "result",
                  label: "Result",
                  type: "object",
                  properties: [{
                      name: "properties",
                      label: "Properties",
                      type: "object",
                      properties: [{
                          name: "height",
                          label: "Height",
                          type: "string"
                        },
                        {
                          name: "mass",
                          label: "Mass",
                          type: "string"
                        },
                        {
                          name: "hair_color",
                          label: "Hair color",
                          type: "string"
                        },
                        {
                          name: "skin_color",
                          label: "Skin color",
                          type: "string"
                        },
                        {
                          name: "eye_color",
                          label: "Eye color",
                          type: "string"
                        },
                        {
                          name: "birth_year",
                          label: "Birth year",
                          type: "string"
                        },
                        {
                          name: "gender",
                          label: "Gender",
                          type: "string"
                        },
                        {
                          name: "created",
                          label: "Date created",
                          type: "date_time"
                        },
                        {
                          name: "edited",
                          label: "Date edited",
                          type: "date_time"
                        },
                        {
                          name: "name",
                          label: "Person name",
                          type: "string"
                        },
                        {
                          name: "homeworld",
                          label: "Homeworld",
                          type: "string"
                        },
                        {
                          name: "url",
                          label: "URL",
                          type: "string"
                        }
                      ]
                    },
                    {
                      name: "description",
                      label: "Description",
                      type: "string"
                    },
                    {
                      name: "_id",
                      type: "string"
                    },
                    {
                      name: "uid",
                      type: "string"
                    },
                    {
                      name: "__v",
                      type: "integer"
                    }
                  ]
                }
              ]
            end,
        },
      }
    }


```

How does this code snippet work?

This code snippet includes the following keys:

  * `actions`
  * Declares a new action. Use indentation to ensure your code is readable.
  * `get_person_by_id`
  * Defines the **Get person by ID** action. The action name inherits this key, replacing underscores (`_`) with spaces. Ensure the key name accurately reflects the action's purpose. Don't use spaces in the key name.
  * `input_fields`
  * Declares the input fields that appear when users configure your action during recipe building. This example includes a single input field named `id`. The `label` variable defines the name displayed to users, while `type` specifies the data type. Setting `optional` to `false` makes this field mandatory.  
![Input fields](/assets/img/input-field-screen.d0f83522.png)
  * `execute`
  * Declares the HTTP request, target URL, and additional actions required for the recipe. The placeholder `#{input["id"]}` dynamically captures the user-provided ID, appending it to the target URL to retrieve the character's information.
  * `output_fields`
  * Declares the datapills returned by the action. These output fields should match the JSON object returned by the `GET` request specified in the `execute` key.  
![Output fields](/assets/img/output-field-screen.c24f928b.png)

How can I define a nested array or object?

To define an array, set the `type` to `array`. This tells Workato to expect a collection of multiple values. Use the `of` attribute to specify the data type of the array's items. For example, set `of` to `string` for arrays containing URLs.

## [#](<#testing-your-action>) Test your action

Complete the following steps to test your action:

1

Go to the **Test code** tab.

2

Select the **Get person by ID** action.

![Select the Get person by ID action](/assets/img/select-action.a1d93c7d.png)_Select the Get person by ID action_

3

Enter the ID of the Star Wars character you plan to retrieve information for in the **Person ID** field. For example, enter `1` to retrieve information about Luke Skywalker.

![Fill in the Person ID field](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAA6oAAAD8CAMAAABJnalbAAACW1BMVEUkQ08uTFgvTVg2Ul07V2FAW2VDXmhHX2tKYm1MZG9NZXBQZ3JSaXRUa3ZWbXdYb3lccnxedH5fdX9hd4BjeYdleYNne4RofIZqfodqfohsgIlugYpvg4xyhY50h5B1h5B2iZJ5i5R5jJR6jJV8jpZ8j5eAkpqCkpqDlaCElJyElp2FlZ2Glp6Hl5+ImJ+KmqGLmqKMnKONnaSOnaWPnqWQn6aQn6eRoKeToamToqmVpKuWpKuXpayXpq2Zp66bqK+bqbCcqrGdq7Ceq7KerLGfrbKgoKCisLWjsLWjsLmksbantLmptLmqt7ust7ytuL2uub6xu8CyvcGzvsK1wMS2wMW4uLi4wsa5wse6xMi6xMy8xcm8xc68xsq9x8u9x8++x8u/yMzAyczAyc3Bys7Cy87DzM/EzNDEzNPFztHGztLHz9LI0NTJ0dTK0tXL09bL09jN1djO1tnP1djP19rQ2NrR19rS2NvS2tzT2NvT2dzU2tzV297W3N7X3N/X3eDY3uDaOhva3+Ha4OLbRSnb4OTc4eTd4uTe4+bfVj7fWUHf5ObgX0jg5Obg5efh5ujiaVTicV3i5ujjdWHj5+jk6Ork6OvlfWrlgG7l6evl6uvm6uzniHfnkIHn6+3olIXplYbpoZXp7O7p7e7p7e/qn5Lq7u/rqZ7r7/Ds7/HtvbXtxL3t8PHt8fLuwLnuxr/uzMbu8fPvysXv8vPw1dHw1tLw2dXw29jw3drw8/Tw9PXx3tzx4N7x4uDx5OLx9PXy5+fy7Ozy8vPy9fb29/f8/Pz9/v7+/v7///+dJ5d1AAAH2klEQVR42u3ci5dUdQHA8bssC0abaK6lrEBk2pi9pIdEDwssnTLBDLamRSTCBinbsJIlS7ewrAxLkwJry9goKivbHkLZKrfXn9Xvd+/c3RlgaR8z7szh8zmHmfv73dndc/Z3vufeO3uHJAU6QOJXAFIFpApSBaQKSBWkCkgVkCpIFZAqIFWQKiBVkCogVUCqIFVAqoBUQaqAVAGpglQBqYJUAakCUgWpAlIFpApSBaQKSBWkCkgVkCpIFZAqSBWQKiBVkCogVUCqIFVAqoBUQarA+Zfqc3/4iwWC9k/1qZHHLRDMONVNr4pefd37d00092eHb7wmPq+N3/+qGwbuP9G4/ycjj1ggmHGqVyeFJZub+rPjN47PFxTff9ndUzt/+NNff3/kwO9/8fjfLBLMMtUkub2lqSbJmvHavj+PFH5pkWDGqW7b9pGNF8eWDrcm1aVbbromK/bdtX3P/+xAXuqP/mSRYMapZhtvCxt3ZFvH93x499F87+iRIyfTiT233BO2n7x708A3J7/uOx/fvL92kHzmyJFj4XH3rZ87fvZULwlP4zfEVr9e7H3hW7HUv1oimG2qh8PGO2Oo1+Qnq7+Kkz1Jsu/OxeG4mI6v64rT3becjPP35Ke1G7LB5iRZMbYmjnu+OG2qafr2MLGy2PvH7KD6lCWC2ab6dNh4czhaFteWy36bp3pjTHRV+vrignN9mH5fMbjoeJ7q4qX5uOfE9Kke606SJbWdpx4ZGfnNt0dGnrNGMMtU7wobt6Vpf3h6xfpV4XFjnmo8lPZseDJ2uHbdy5IlY2m6N06+/IrY8HV5qvFF3fFxy/SppivDTO2c+dSPR36XPnvge/+wRjC7VD8fq/xqui083hiG60N7tVS7BkJfO+O7T2Hi9n3hoTcMBsIBOB5K9+epdn10YnxjeH7rOVJdG2YeKHY/G/79/ZQlglmkumrVK7PT3tVpelWS9Mbp+8Pw0TzVT8bxffHy9Vj+JQ8XF52fCBvvyVPdGYbj8TXnSPWm2uuAuaVa0xsuPC8MF6nrojDek6W6PHvZyez4eu0X4vYdYfNjcWOiK17FZqnuj+PFSXL5OVJdV7wOmHuqSzfF68iuujsiBrJU+/PX7c0uRZNLHszfVMqaTZeFsOtSXXLuVOObxMctCsw51R07du6rndzWp/rp+lTTw6/L9nV9I90QnvbOPtWJsNVjTWDuqdYNwwnwFSdr0oZU03Ts5ngWfGW6o3in90RXdn07w1RvCxOXWhNoSqqvCcfNx6aGDamm6bHeJLkgPZjUktwSNt4701T3hSvZZLc1gaakemcYXvxE2HhsU0Oq48vfMBaeLsreIA6H3uTWNH0wHmS/MqNURz9zfZLdSQE0JdU03vzQtfqNl2VvAE+l+qYk6V65Nt7Tf204QMbsXro8Pl6fziDVwuKDlgSalOoTFxZhXV6f6mWTucVP33ywGF369CxSvfqoFYFmpZqe2JD9Wab7XUcbrlV35Amvzj9bc1826v5QNqhPdeU0qS5d8ZbPWg+Ye6pnc/CuXY+eOfvMvbvuHZscje351MN+wbCgqQJSBaQKUgWkClIFpApIFaQKSBWQKkgVkCogVZAqIFVAqiBVQKogVUCqgFRBqoBUAanC+ZPq6NBgBWidwaHRJqQ6OljZ7ncJrY11dP6pDlUeOtQKlcp/gVxlaP6pDm4fkyq0ONXB+adaqRySKrQ41YpUQapSBamCVKUKUpUqSBWkKlWQqlRBqiBVqYJUrQ9IFaQqVZAqSFWqIFWpglRBqlIFqUoVpApSlSpIVaogVZCqVEGqIFWpglSlClIFqUoVpCpVOH9S/efXfmABkWqbp/qvL79jUZL8xwoi1fZO9SVJ9G8riFSbkGq1Wi5XT58qlctTo3LdYFap9i5aJFWk2pxUy31R6cypvrzfaikblOd4rfpaqSLVZqRay7Kv7yxTWavFoCxVWMBUswirDSnmg1J+qC1nyZYbWpYqvNip1hqs1qVYN1Utuj00eT4sVViIVEt5idW6FMu1K9dsqmi4dNrlrFRhIVKtP2o2TBWplqUKC5lq3/SpZs/lqVT7pArtkGr5bKlWpQrtewJcanhv2AkwtEOqpdNSPeNtpapUYaFTrR01689vG6dqqU57D4RU4cVItfEWiFLtsXYLRNktENAuqdbfWJhnmYU7da/hPG4s/O7w8HB/knxpePjnFhGpNud2/WrdPUt1U/lBdo636/cnhX6LiFTn/SG48uSH4Oo26j4XVy6XqtVD80p1hUVEqv5vJZCqVEGqIFWpglSlClIFqUoVpApIFaQqVZAqSFWqIFWpglRBqlIFqUoVpAodbetWqUIHlPoBqULHlCpV6IhSpQodUapUoSNKlSp0RKlShY4oVarQ7qX6uyp0RKn+rgqdU6pUoSNKlSp0RKlShY4oVarQEaVKFdow1a2Nz1KFjiFVOG9SHdw+JlVocaqD8091qPKQVKHFqQ7NP9XRwQrQWoOj8081HR0SK7Q01KH/X+oMUgXagFRBqoBUQaqAVAGpglQBqQJSBakCUgWkClIFpApSBaQKSBWkCkgVkCpIFZAqIFWQKiBVkCogVUCqIFVAqoBUQaqAVAGpglQBqQJSBakCUgWpAlIFpApSBaQKSBWkCkgVkCpIFZAqSBWQKiBVkCogVUCqIFVAqoBUQaqAVAGpQqf4H5m7RBZ9+goBAAAAAElFTkSuQmCC)_Fill in the Person ID field_

4

Click **Test action**. The **Recent tests** tab opens.

5

Click the **Output** tab to view the output of the **Get person by ID** action. The following screenshot displays a successful test:

![View the output](/assets/img/test-code-output.8082b366.png)_View the output_

A successful test indicates that no errors occurred during recipe execution. However, it doesn't rule out the possibility of other issues, such as logic errors.

## [#](<#creating-a-recipe-using-your-new-custom-connector>) Use your custom connector in a recipe

You can now use the SWAPI connector and the action you created in any recipe. Search for the SWAPI connector when selecting an application to get started.

![Select the Star Wars Information connector](/assets/img/building-recipe.b6c63a03.png) _Select the Star Wars Information connector_
