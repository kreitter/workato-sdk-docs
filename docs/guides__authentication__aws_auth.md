# Workato SDK Documentation

> **Source**: https://docs.workato.com/en/developing-connectors/sdk/guides/authentication/aws_auth.html
> **Fetched**: 2026-01-18T02:49:30.710912

---

# [#](<#how-to-guides-aws-service-authentication>) How-to Guides - AWS Service Authentication

AWS services can be authenticated in two ways. Workato supports AWS libraries that simplify the authentication process by helping you to generate the AWS V4 Signature so you can focus on building actions and triggers.

This guide shows you how to implement dual authentication for both:

  * [Access key authentication (opens new window)](<https://docs.aws.amazon.com/general/latest/gr/signature-version-4.html>)
  * [IAM role authentication through AWS Security Token Service (opens new window)](<https://docs.aws.amazon.com/STS/latest/APIReference/API_AssumeRole.html>)

RECOMMENDED IAM ROLE FOR AUTHENTICATION

AWS and Workato both recommend using AWS IAM role authentication. We recommend that you make this the default authentication method for the users of your connector.

## [#](<#create-iam-role-and-arn-retrieval>) Create IAM role and ARN retrieval

Refer to the [IAM role-based authentication for AWS](</security/data-protection/secrets-management/iam-role-based-authentication-for-aws.html>) page for instructions on how to create an IAM role for Workato and retrieve your Amazon resource name (ARN).

## [#](<#sample-connector-generic-connector>) Sample connector - Generic connector
```ruby
 
    {
      title: "Sample AWS S3 Connector",

      connection: {
        fields: [
          {
            name: "aws_auth_type",
            label: "AWS Authorization type",
            control_type: "select",
            optional: false,
            pick_list: [
              ["IAM role", "aws_role_based"],
              ["Access key", "aws_key_secret"]
            ],
            default: "aws_role_based",
            hint: 'Learn more about Amazon S3 authorization support <a href="http://docs.workato.com/connectors/s3.html#connection-setup" target="_blank">here</a>.'
          },
          {
            name: "aws_assume_role",
            label: "IAM role ARN",
            optional: false,
            ngIf: 'input.aws_auth_type == "aws_role_based"',
            help: {
              title: "Using IAM Role authorization",
              text: <<~HELP
                Create an IAM role in your AWS account using the following data:
                <br/>&nbsp;- Use Workato AWS Account ID <b>{{ authUser.aws_iam_external_id }}</b>
                to generate the <b>Principal</b> for the role.
                <br/>&nbsp;- Use <b>{{ authUser.aws_workato_account_id }}</b> as the <b>External ID</b> for the role.
                <br/>&nbsp;- Set this field's value to the newly created role's ARN.
                <br/><a href="https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-user.html"
                target="_blank">Learn more</a>.
              HELP
            }
          },
          {
            name: "aws_api_key",
            label: "Access key ID",
            control_type: "password",
            optional: false,
            hint: "Go to <b>AWS account name</b> > <b>Security Credentials</b> > <b>Users</b>. Get API key from existing user or create new user.",
            ngIf: 'input.aws_auth_type == "aws_key_secret"'
          },
          {
            name: "aws_secret_key",
            label: "Secret access key",
            control_type: "password",
            optional: false,
            hint: "Go to <b>AWS account name</b> > <b>Security Credentials</b> > <b>Users</b>. Get secret key from existing user or create new user.",
            ngIf: 'input.aws_auth_type == "aws_key_secret"'
          },
          {
            name: "aws_region",
            optional: false,
            hint: "AWS service region. If your account URL is <b>https://eu-west-1.console.s3.amazon.com</b>, use <b>eu-west-1</b> as the region."
          }
        ],

        authorization: {
          type: "custom_auth"
        }
      },

      test: lambda do |connection|
        call(:list_buckets, connection)
      end,

       methods: {
        list_buckets: lambda do |connection|
          signature = aws.generate_signature(
            # The connection object defined earlier.
            connection: connection,
            # The internal name of the AWS service you are targeting
            service: "s3",
            # The AWS service region you are targeting.
            # For services with a globally unique endpoint such as IAM, use us-east-1.
            region: connection["aws_region"],
            # The host of the API url.
            # Optional and defaults to "#{service}.#{region}.amazonaws.com".
            # In some cases like AWS API Gateway and AWS IAM, your host may not follow this standard and require you to override the host.
            host: "s3.dualstack.#{connection['aws_region']}.amazonaws.com",
            # The relative path of the endpoint. Optional and defaults to "/"
            path: "/",
            # The verb used for the request. Optional and defaults to "GET"
            method: "GET",
            # The query parameters for the request. Optional and defaults to {}
            params: { "list-type" => 2, "max-keys" => 1000 },
            # The headers for the request. Optional and defaults to {}
            headers: {},
            # The payload for the request. Optional and defaults to ""
            payload: ""
          )
          url = signature[:url]
          headers = signature[:headers]

          response = get(url).headers(headers).response_format_xml

          files = response.dig("ListBucketResult", 0, "Contents")
          files = Array.wrap(files).map do |content|
            content.each_with_object({}) do |(k, v), obj|
              obj[k] = Array.wrap(v).dig(0, "content!")
            end
          end

          { "files" => files }
        end
      }
    }


```

## [#](<#step-1-defining-connection-fields>) Step 1 - Defining Connection fields

In the `connection` key, we define the input fields in the `fields` key in an array of hashes. Each hash in the array represents a single input field. Inside, we will be able to declare the name of the input field, hints that are displayed to the end user among other parameters. In this example, we're presenting two ways for users to authenticate which is decided by their input for the field `aws_auth_type`.

Based on this selection, we selectively show/hide the next fields for `aws_assume_role` or `aws_api_key` and `aws_secret_key`. This is done with the attribute `ngIf`.

TIP

Most AWS services have the same authentication, which allows you to use the same connection fields in the preceding example.

If you do choose to add more fields, you need to at least provide the `name` key. Additional attributes like `optional`, `hint` and `control_type` allow you to customize other aspects of these fields. For sensitive information like Client Secrets, remember to use the `control_type` as `password`.

Learn how to define [input fields in Workato](</developing-connectors/sdk/sdk-reference/connection.html#fields>).

## [#](<#step-2-generating-the-aws-signature>) Step 2 - Generating the AWS signature

Compared to other ways to authenticate, AWS requires a unique signature for each request as the current time is a component of the signature. As such, your connector should not use the `apply` lambda as there are no credentials to apply on a general basis.

Instead, you should use the `aws.generate_signature` method to get the valid URL and signature before making an API call. In our example, you can see that we have created a method `list_buckets` that makes a GET request to S3.
```ruby
 
        list_buckets: lambda do |connection|
          signature = aws.generate_signature(
            # The connection object defined earlier.
            connection: connection,
            # The internal name of the AWS service you are targeting
            service: "s3",
            # The AWS service region you are targeting.
            # For services with a globally unique endpoint such as IAM, use us-east-1.
            region: connection["aws_region"],
            # The host of the API url.
            # Optional and defaults to "#{service}.#{region}.amazonaws.com".
            # In some cases like AWS API Gateway and AWS IAM, your host may not follow this standard and require you to override the host.
            host: "s3.dualstack.#{connection['aws_region']}.amazonaws.com",
            # The relative path of the endpoint. Optional and defaults to "/"
            path: "/",
            # The verb used for the request. Optional and defaults to "GET"
            method: "GET",
            # The query parameters for the request. Optional and defaults to {}
            params: { "list-type" => 2, "max-keys" => 1000 },
            # The headers for the request. Optional and defaults to {}
            headers: {},
            # The payload for the request. Optional and defaults to ""
            payload: ""
          )
          url = signature[:url]
          headers = signature[:headers]

          response = get(url).headers(headers).response_format_xml

          files = response.dig("ListBucketResult", 0, "Contents")
          files = Array.wrap(files).map do |content|
            content.each_with_object({}) do |(k, v), obj|
              obj[k] = Array.wrap(v).dig(0, "content!")
            end
          end

          { "files" => files }
        end


```

## [#](<#step-3-testing-the-connection>) Step 3 - Testing the connection

With the method defined earlier, you'd be able to call this method in the test to verify the user's credentials.
```ruby
 
      test: lambda do |connection|
        call(:list_buckets, connection)
      end,


```

## [#](<#troubleshooting-tips>) Troubleshooting tips

Ensuring your AWS signature is correct may be hard to verify by testing your connection. Our recommendation is to wrap a simple API request in a method - like what we did with the example above - and stubbing the connection when you first start. This allows you to test an action
```ruby
 
    {
      title: "Sample AWS S3 Connector",

      connection: {
        fields: [
          #  Same fields as earlier
        ],

        authorization: {
          type: "custom_auth"
        }
      },

      test: lambda do |connection|
        true
      end,

      actions: {
        sample_action: {
          execute: lambda do |connection|
            call(:list_buckets, connection)
          end
        }
      },

      methods: {
        list_buckets: lambda do |connection|
          # Method from earlier
        end
      }
    }


```

By testing the "sample_action" action, you'll have better insight for debugging into the errors raised by the Workato SDK framework or the AWS API you are connecting to.

## [#](<#connections-sdk-reference>) Connections SDK reference

Learn about the available keys within the `connection` key in the [SDK reference](</developing-connectors/sdk/sdk-reference/connection.html>).
