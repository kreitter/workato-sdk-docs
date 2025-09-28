#!/usr/bin/env python3
import re

# Test the fixed regex pattern
test_content = """[code]
    {
      title: 'Chargebee-demo',

      connection: {
        fields: [
          {
            name: 'api_key',
            control_type: 'password',
            hint: 'You can find your API key final change3' \\
              "under 'Settings'=>'Configure Chargebee'=>'API Keys and Webhooks'" \\
              " in Chargebee's web console.",
            label: 'Your API Key'
          },
          {
            name: 'domain',
            control_type: 'subdomain',
            url: 'chargebee.com'
          }
        ],

        authorization: {
          type: 'basic_auth',

          apply: lambda do |connection|
            user(connection['api_key'])
          end
        },

        base_uri: lambda do |connection|
          "https://#{connection['domain']}.chargebee.com"
        end
      },

      test: lambda do |_connection|
        get('/api/v2/plans', limit: 1)
      end,

      methods: {
        get_customers: lambda do
          get('/api/v2/customers')
        end,

        sample_method: lambda do |string1, string2|
          string1 + ' ' + string2
        end,
      },
    }
[/code]"""


def replace_code_block(match):
    content = match.group(1)
    # Default to ruby for Workato SDK docs
    return f"```ruby\n{content}\n```"


# Test the fixed regex pattern
result = re.sub(r"\[code\](.*?)\[/code\]", replace_code_block, test_content, flags=re.DOTALL)

print("FIXED REGEX RESULT:")
print(repr(result))
print("\nFORMATTED RESULT:")
print(result)
