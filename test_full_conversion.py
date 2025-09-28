#!/usr/bin/env python3
import re

import html2text
from bs4 import BeautifulSoup

# Test the full conversion process
test_html = """<div class="content">
<h2>Sample connector - Chargebee</h2>
<p>The code in <code>connector.rb</code>.</p>
<pre><code>{
  title: 'Chargebee-demo',

  connection: {
    fields: [
      {
        name: 'api_key',
        control_type: 'password',
        hint: 'You can find your API key final change3' \
          "under 'Settings'=>'Configure Chargebee'=>'API Keys and Webhooks'" \
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
}</code></pre>
</div>"""

# Simulate the converter
h2t = html2text.HTML2Text()
h2t.body_width = 0  # No line wrapping
h2t.protect_links = True
h2t.wrap_links = False
h2t.skip_internal_links = False
h2t.inline_links = True
h2t.ignore_images = False
h2t.images_to_alt = False
h2t.mark_code = True

# Extract main content (simplified)
soup = BeautifulSoup(test_html, "html.parser")
main_content = soup.find("div", class_="content")
if main_content:
    main_html = str(main_content)
else:
    main_html = test_html

# Convert to markdown
markdown = h2t.handle(main_html)


# Post-process markdown (our fix)
def post_process_markdown(markdown_content):
    lines = markdown_content.split("\n")
    processed_lines = []

    # Add header with source URL
    processed_lines.append("# Workato SDK Documentation")
    processed_lines.append("")
    processed_lines.append(
        "> **Source**: https://docs.workato.com/en/developing-connectors/sdk/cli/guides/cli/"
        "methods.html"
    )
    processed_lines.append("> **Fetched**: 2025-09-27T02:27:57.918629")
    processed_lines.append("")
    processed_lines.append("---")
    processed_lines.append("")

    # Process the content
    for line in lines:
        # Skip empty lines at the beginning
        if not processed_lines and not line.strip():
            continue
        processed_lines.append(line)

    # Join and clean up
    markdown_content = "\n".join(processed_lines)

    # Fix common conversion issues
    markdown_content = re.sub(r"\n{3,}", "\n\n", markdown_content)  # Max 2 consecutive newlines
    markdown_content = re.sub(
        r"^\s+$", "", markdown_content, flags=re.MULTILINE
    )  # Clean empty lines with spaces

    # Replace [code] markers with proper markdown code blocks
    def replace_code_block(match):
        content = match.group(1)
        # Default to ruby for Workato SDK docs
        return f"```ruby\n{content}\n```"

    # Match [code] blocks that span multiple lines - fixed regex pattern
    markdown_content = re.sub(
        r"\[code\](.*?)\[/code\]", replace_code_block, markdown_content, flags=re.DOTALL
    )

    # Clean up any remaining [/code] tags that might be orphaned
    markdown_content = re.sub(r"\[/code\]", "", markdown_content)

    # Handle inline code (single line between [code] tags)
    markdown_content = re.sub(r"\[code\]\s*([^\n\[]+?)\s*\[/code\]", r"`\1`", markdown_content)

    return markdown_content


# Apply post-processing
final_markdown = post_process_markdown(markdown)

print("FINAL MARKDOWN RESULT:")
print(final_markdown)
