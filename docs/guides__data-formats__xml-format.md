# Workato SDK Documentation

> **Source**: https://docs.workato.com/en/developing-connectors/sdk/guides/data-formats/xml-format.html
> **Fetched**: 2026-01-18T02:50:09.731650

---

# [#](<#how-to-guides-xml-data-format>) How-to guides - XML data format

XML data format can be specified using the following SDK methods:

Method | Description  
---|---  
`request_format_xml` | Convert request body to XML format  
`response_format_xml` | Expect response body in XML format  
`format_xml` | Convert request and expect response body in XML format  

## [#](<#forming-xml-payload-in-request>) Forming XML payload in request

Since custom connector actions receive data in the form of ruby hashes, you will have to convert these hashes into an XML by chaining one of the formatting methods to the end of the request. This example explores making requests to Intacct web services with XML data format.

According to the [Intacct documentation (opens new window)](<https://developer.intacct.com/wiki/web-services-api-30-calls>), all requests should be made to the same endpoint as a POST request: `https://api.intacct.com/ia/xml/xmlgw.phtml` where requests are expected to be in XML data formats.

### [#](<#sample-code-snippet>) Sample code snippet
```ruby
 
    <request>
      <control>
        <senderid>SENDER_ID</senderid>
        <password>PASSWORD</password>
        <controlid>testControlId</controlid>
        <uniqueid>false</uniqueid>
        <dtdversion>3.0</dtdversion>
      </control>
      <operation>
        <authentication>
          <login>
            <userid>USER_ID</userid>
            <companyid>COMPANY_ID</companyid>
            <password>PASSWORD</password>
          </login>
        </authentication>
        <content>
          <function controlid="testControlId">
            <inspect>
              <object>USERINFO</object>
            </inspect>
          </function>
        </content>
      </operation>
    </request>


```

Here is a sample action to retrieve GL Account information, **Get GL account**.
```ruby
 
    get_GL_account: {
      input_fields: lambda do
        [
          {
            name: "key",
            label: "Record ID",
            optional: false
          }
        ]
      end,

      execute: lambda do |connection, input|
        response = post("https://api.intacct.com/ia/xml/xmlgw.phtml").
          payload(
            "control": [
              {
                "senderid": [{ "content!": connection["sender_id"] }],
                "password": [{ "content!": connection["sender_password"] }],
                "controlid": [{ "content!": "testControlId" }],
                "uniqueid": [{ "content!": false }],
                "dtdversion": [{ "content!": 3.0 }]
              }
            ],
            "operation": [
              {
                "authentication": [
                  {
                    "login": [
                      {
                        "userid": [{ "content!": connection["login_username"] }],
                        "companyid": [{ "content!": connection["company_id"] }],
                        "password": [{ "content!": connection["login_password"] }]
                      }
                    ]
                  }
                ]
                "content": [
                  {
                    "function": [
                      {
                        "@controlid": "testControlId",
                        "get_list": [
                          {
                          "@object": "glaccount",
                          "@maxitems": "1"
                          }
                        ]
                      }
                    ]
                  }
                ]
              }
            ]).
            headers("Content-type": "x-intacct-xml-request").
            format_xml("request").
            dig("response", 0,
                "operation", 0,
                "result", 0,
                "data", 0,
                "glaccount", 0) || {}

        response.inject({}) do |hash (key, value)|
          hash.merge(
            {
              key => value.dig(0, "content!")
            })
        end
      end,

      output_fields: lambda do |object_definitions|
        object_definitions["budget"]
      end
    }


```

That is a handful! Let's break it down. Firstly, we define a POST to request to the appropriate endpoint:
```ruby
 
    post("https://api.intacct.com/ia/xml/xmlgw.phtml")


```

Next, we add a payload to the request in the form of a hash first:
```ruby
 
    .payload("control": [
             {
               "senderid": [{ "content!": connection["sender_id"] }],
               "password": [{ "content!": connection["sender_password"] }],
               "controlid": [{ "content!": "testControlId" }],
               "uniqueid": [{ "content!": false }],
               "dtdversion": [{ "content!": 3.0 }]
             }
           ],
           "operation": [
             {
               "authentication": [
                 {
                   "login": [
                     {
                       "userid": [{ "content!": connection["login_username"] }],
                       "companyid": [{ "content!": connection["company_id"] }],
                       "password": [{ "content!": connection["login_password"] }]
                     }
                   ]
                 }
               ],
               "content": [
                 {
                   "function": [
                     {
                       "@controlid": "testControlId",
                       "get_list": [
                         {
                           "@object": "glaccount",
                           "@maxitems": "1"
                         }
                       ]
                     }
                   ]
                 }
               ]
             }
           ])


```

Elements are represented by arrays of hashes, since XML elements can repeat without any extra notation. Element data is defined using the `content!` key and attributes using `@` prefix (example: `@object` and `@maxitems`).

The resultant XML body looks like this:
```ruby
 
    <control>
      <senderid>SENDER_ID</senderid>
      <password>PASSWORD</password>
      <controlid>testControlId</controlid>
      <uniqueid>false</uniqueid>
      <dtdversion>3.0</dtdversion>
    </control>
    <operation>
      <authentication>
        <login>
          <userid>USER_ID</userid>
          <companyid>COMPANY_ID</companyid>
          <password>PASSWORD</password>
        </login>
      </authentication>
      <content>
        <function controlid="testControlId">
          <get_list object="glaccount" maxitems="1"/>
        </function>
      </content>
    </operation>


```

Defining value for an XML element is done using the `content!` key. For example, to assign password to the `<senderid>` element, the hash looks like this:
```ruby
 
    {
      "senderid": [{ "content!": connection["sender_id"] }]
    }


```

Next, how do we form a complex XML element? First, let's form an XML element that has a single occurrence (object type). For example, the `<control>` element in the request body is a complex element type with a number of elements nested within. The resultant partial XML should look like this:
```ruby
 
    <control>
      <senderid>SENDER_ID</senderid>
      <password>PASSWORD</password>
      <controlid>testControlId</controlid>
      <uniqueid>false</uniqueid>
      <dtdversion>3.0</dtdversion>
    </control>


```

To form this, the equivalent hash should not have `content!` defined immediately in the `control` hash. Instead, define an array of a single hash that contains nested keys, one for each element that belongs in the `<control>` element.
```ruby
 
    "control": [
      {
        "senderid": [{ "content!": connection["sender_id"] }],
        "password": [{ "content!": connection["sender_password"] }],
        "controlid": [{ "content!": "testControlId" }],
        "uniqueid": [{ "content!": false }],
        "dtdversion": [{ "content!": 3.0 }]
      }
    ]


```

Notice that all elements immediately under the `<control>` element are primitive types. Each of these elements contain only a value and optionally, attributes.

Now, we know how to define values for primitive XML elements. What about XML attributes? Let's look at the `<content>` element in the XML body to see how it's done.
```ruby
 
    <content>
      <function controlid="testControlId">
        <get_list object="glaccount" maxitems="1"/>
      </function>
    </content>


```

This XML element has attributes defined in 2 elements. First, in a complex element `<function>` as well as a primitive element `<get_list>`. To form this XML, the equivalent hash structure looks like this:
```ruby
 
    "content": [
      {
        "function": [
          {
            "@controlid": "testControlId",
            "get_list": [
              {
                "@object": "glaccount",
                "@maxitems": "1"
              }
            ]
          }
        ]
      }
    ]


```

Attributes and nested elements in a complex XML element are defined with the same hierarchy, but with the `@` prefix to indicate an attribute. (`"get_list"` key for `<get_list>` element and `"@controlid"` key for `controlid` attribute)

Similarly, element value and attributes in a primitive XML element are defined with the same hierarchy. (`"content!"` key for value of `<get_list>` element and `"@object"` key for `object` attribute) In this example, the `<get_list>` element is not assigned a value. If we were to assign one, the equivalent hash will look like this:
```ruby
 
    "content": [
      {
        "function": [
          {
            "@controlid": "testControlId",
            "get_list": [
              {
                "@object": "glaccount",
                "@maxitems": "1",
                "content!": input["key"]
              }
            ]
          }
        ]
      }
    ]


```

Which will be converted into this XML:
```ruby
 
    <content>
      <function controlid="testControlId">
        <get_list object="glaccount" maxitems="1">KEY_VALUE<get_list>
      </function>
    </content>


```

Next, we add the necessary headers with the headers shorthand method:
```ruby
 
    .headers("Content-type": "x-intacct-xml-request")


```

Finally, we use the `format_xml` method (since we require both request and response in XML) and pass it the root element name as an argument, `<request>`)
```ruby
 
    .format_xml("request")


```

## [#](<#handling-xml-from-response>) Handling XML from response

Now, the response from the same request will be in this form:
```ruby
 
    <response>
      <control>
        <status>success</status>
        <senderid>SENDER_ID</senderid>
        <controlid>testControlId</controlid>
        <uniqueid>false</uniqueid>
        <dtdversion>3.0</dtdversion>
      </control>
      <operation>
        <authentication>
          <status>success</status>
          <userid>USER_ID</userid>
          <companyid>COMPANY_ID</companyid>
          <sessiontimestamp>2017-03-26T05:24:25-07:00</sessiontimestamp>
        </authentication>
        <result>
          <status>success</status>
          <function>get_list</function>
          <controlid>testControlId</controlid>
          <listtype start="0" end="0" total="107">glaccount</listtype>
          <data>
            <glaccount>
              <recordno>1</recordno>
              <glaccountno>1000</glaccountno>
              <title>Chase Operating Account</title>
              <normalbalance>debit</normalbalance>
              <accounttype>balancesheet</accounttype>
              <closingtype>closed to account</closingtype>
              <closingaccountno/>
              <whenmodified>06/03/2016 20:19:30</whenmodified>
              <status>active</status>
              <requiredept>false</requiredept>
              <requireloc>false</requireloc>
              <taxable>false</taxable>
              <taxcode/>
              <mrccode/>
              <alternativeaccount>None</alternativeaccount>
              <requireproject>false</requireproject>
              <requirecustomer>false</requirecustomer>
              <requirevendor>false</requirevendor>
              <requireemployee>false</requireemployee>
              <requireitem>false</requireitem>
            </glaccount>
          </data>
        </result>
      </operation>
    </response>


```

Because `format_xml` was called in the request, Workato SDK returns an equivalent hash. Similar to request:

  * elements are represented by arrays of hashes, since XML elements can repeat without any extra notation
  * elements attributes has `@` prefixed with the same hierarchy as nested elements and element values
  * element values are passed as values of the `"content!"` key

```ruby
 
    {
      "response"=>[
        {
          "control"=>[
            {
              "status"=>[{ "content!"=>"success" }],
              "senderid"=>[{ "content!"=>"SENDER_ID" }],
              "controlid"=>[{ "content!"=>"testControlId" }],
              "uniqueid"=>[{ "content!"=>"false" }],
              "dtdversion"=>[{ "content!"=>"3.0" }]
            }
          ],
          "operation"=>[
            {
              "authentication"=>[
                {
                  "status"=>[{ "content!"=>"success" }],
                  "userid"=>[{ "content!"=>"USER_ID" }],
                  "companyid"=>[{ "content!"=>"COMPANY_ID" }],
                  "sessiontimestamp"=>[{ "content!"=>"2017-03-26T08:25:12-07:00" }]
                }
              ],
              "result"=>[
                {
                  "status"=>[{ "content!"=>"success" }],
                  "function"=>[{ "content!"=>"get_list" }],
                  "controlid"=>[{ "content!"=>"testControlId" }],
                  "listtype"=>[
                    {
                      "@start"=>"0",
                      "@end"=>"0",
                      "@total"=>"107",
                      "content!"=>"glaccount"
                    }
                  ],
                  "data"=>[
                    {
                      "glaccount"=>[
                        {
                          "recordno"=>[{ "content!"=>"1" }],
                          "glaccountno"=>[{ "content!"=>"1000" }],
                          "title"=>[{ "content!"=>"Chase Operating Account" }],
                          "normalbalance"=>[{ "content!"=>"debit" }],
                          "accounttype"=>[{ "content!"=>"balancesheet" }],
                          "closingtype"=>[{ "content!"=>"closed to account" }],
                          "closingaccountno"=>[{}],
                          "whenmodified"=>[{ "content!"=>"06/03/2016 20:19:30" }],
                          "status"=>[{ "content!"=>"active" }],
                          "requiredept"=>[{ "content!"=>"false" }],
                          "requireloc"=>[{ "content!"=>"false" }],
                          "taxable"=>[{ "content!"=>"false" }],
                          "taxcode"=>[{}],
                          "mrccode"=>[{}],
                          "alternativeaccount"=>[{ "content!"=>"None" }],
                          "requireproject"=>[{ "content!"=>"false" }],
                          "requirecustomer"=>[{ "content!"=>"false" }],
                          "requirevendor"=>[{ "content!"=>"false" }],
                          "requireemployee"=>[{ "content!"=>"false" }],
                          "requireitem"=>[{ "content!"=>"false" }]
                        }
                      ]
                    }
                  ]
                }
              ]
            }
          ]
        }
      ]
    }


```

Hence, we will need to extract the desired data using the `dig` method.
```ruby
 
    .dig("response", 0,
         "operation", 0,
         "result", 0,
         "data", 0,
         "glaccount", 0)


```

This returns us the hash:
```ruby
 
    {
      "recordno"=>[{ "content!"=>"1" }],
      "glaccountno"=>[{ "content!"=>"1000" }],
      "title"=>[{ "content!"=>"Chase Operating Account" }],
      "normalbalance"=>[{ "content!"=>"debit" }],
      "accounttype"=>[{ "content!"=>"balancesheet" }],
      "closingtype"=>[{ "content!"=>"closed to account" }],
      "closingaccountno"=>[{}],
      "whenmodified"=>[{ "content!"=>"06/03/2016 20:19:30" }],
      "status"=>[{ "content!"=>"active" }],
      "requiredept"=>[{ "content!"=>"false" }],
      "requireloc"=>[{ "content!"=>"false" }],
      "taxable"=>[{ "content!"=>"false" }],
      "taxcode"=>[{}],
      "mrccode"=>[{}],
      "alternativeaccount"=>[{ "content!"=>"None" }],
      "requireproject"=>[{ "content!"=>"false" }],
      "requirecustomer"=>[{ "content!"=>"false" }],
      "requirevendor"=>[{ "content!"=>"false" }],
      "requireemployee"=>[{ "content!"=>"false" }],
      "requireitem"=>[{ "content!"=>"false" }]
    }


```

Lastly, we convert the hash here back to a recipe-friendly output schema:
```ruby
 
    response.inject({}) do |hash, (key, value)|
      hash.merge(
        {
          key => value.dig(0, "content!")
        })
    end


```

The output of this action is then:
```ruby
 
    {
      "recordno": "1",
      "glaccountno": "1000",
      "title": "Chase Operating Account",
      "normalbalance": "debit",
      "accounttype": "balancesheet",
      "closingtype": "closed to account",
      "closingaccountno": null ,
      "whenmodified": "06/03/2016 20:19:30",
      "status": "active",
      "requiredept": "false",
      "requireloc": "false",
      "taxable": "false",
      "taxcode": null ,
      "mrccode": null ,
      "alternativeaccount": "None",
      "requireproject": "false",
      "requirecustomer": "false",
      "requirevendor": "false",
      "requireemployee": "false",
      "requireitem": "false"
    }


```

## [#](<#example-action-in-action>) Example action in action

### [#](<#request>) Request
```ruby
 
    POST https://api.intacct.com/ia/xml/xmlgw.phtml
    Accept  application/xml
    Accept-Encoding gzip, deflate
    Content-Type  application/xml
    Authorization Bearer
    Content-type  x-intacct-xml-request


```

Request body:
```ruby
 
    <request>
      <control>
        <senderid>SENDER_ID</senderid>
        <password>PASSWORD</password>
        <controlid>testControlId</controlid>
        <uniqueid>false</uniqueid>
        <dtdversion>3.0</dtdversion>
      </control>
      <operation>
        <authentication>
          <login>
            <userid>USER_ID</userid>
            <companyid>COMPANY_ID</companyid>
            <password>PASSWORD</password>
          </login>
        </authentication>
        <content>
          <function controlid="testControlId">
            <get_list object="glaccount" maxitems="1"></get_list>
          </function>
        </content>
      </operation>
    </request>


```

### [#](<#response>) Response

Status: `200 OK`

Response body:
```ruby
 
    <?xml version="1.0" encoding="UTF-8"?>
    <response>
      <control>
        <status>success</status>
        <senderid>SENDER_ID</senderid>
        <controlid>testControlId</controlid>
        <uniqueid>false</uniqueid>
        <dtdversion>3.0</dtdversion>
      </control>
      <operation>
        <authentication>
          <status>success</status>
          <userid>USER_ID</userid>
          <companyid>COMPANY_ID</companyid>
          <sessiontimestamp>2017-03-26T05:24:25-07:00</sessiontimestamp>
        </authentication>
        <result>
          <status>success</status>
          <function>get_list</function>
          <controlid>testControlId</controlid>
          <listtype start="0" end="0" total="107">glaccount</listtype>
          <data>
            <glaccount>
              <recordno>1</recordno>
              <glaccountno>1000</glaccountno>
              <title>Chase Operating Account</title>
              <normalbalance>debit</normalbalance>
              <accounttype>balancesheet</accounttype>
              <closingtype>closed to account</closingtype>
              <closingaccountno/>
              <whenmodified>06/03/2016 20:19:30</whenmodified>
              <status>active</status>
              <requiredept>false</requiredept>
              <requireloc>false</requireloc>
              <taxable>false</taxable>
              <taxcode/>
              <mrccode/>
              <alternativeaccount>None</alternativeaccount>
              <requireproject>false</requireproject>
              <requirecustomer>false</requirecustomer>
              <requirevendor>false</requirevendor>
              <requireemployee>false</requireemployee>
              <requireitem>false</requireitem>
            </glaccount>
          </data>
        </result>
      </operation>
    </response>


```

Which is extracted and converted into:
```ruby
 
    {
      "recordno": "1",
      "glaccountno": "1000",
      "title": "Chase Operating Account",
      "normalbalance": "debit",
      "accounttype": "balancesheet",
      "closingtype": "closed to account",
      "closingaccountno": null ,
      "whenmodified": "06/03/2016 20:19:30",
      "status": "active",
      "requiredept": "false",
      "requireloc": "false",
      "taxable": "false",
      "taxcode": null ,
      "mrccode": null ,
      "alternativeaccount": "None",
      "requireproject": "false",
      "requirecustomer": "false",
      "requirevendor": "false",
      "requireemployee": "false",
      "requireitem": "false"
    }


```
