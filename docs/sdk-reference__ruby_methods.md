# Workato SDK Documentation

> **Source**: https://docs.workato.com/en/developing-connectors/sdk/sdk-reference/ruby_methods.html
> **Fetched**: 2026-01-18T02:50:34.125656

---

# [#](<#available-ruby-methods>) Available Ruby methods

Workato implements a subset of Ruby's public instance methods within its SDK framework. This document lists the Ruby methods that are available when building your connectors. You can request to add additional methods to this list using the [Workato feedback widget (opens new window)](<https://ideas.workato.com/app/#/login>).

WHITELIST REMOVAL

Workato has removed whitelisting for its SDK framework, starting March 2025. This means that developers can now access the full functionality of Ruby 2.7, including built-in libraries, and any available Ruby gems in the SDK container. This change significantly expands the range of capabilities SDK developers can leverage within the platform.

[Learn more](</developing-connectors/sdk/sdk-reference/whitelist-removal.html>) about the capabilities available with the removal of ruby whitelisting.

This enhancement doesn't apply to the Ruby code connector.

PERSONAL REUSABLE METHODS

You can declare personal reusable methods to use in any block when using Workato SDK.

* * *

## [#](<#at>) at

Creates a new time object with the given argument.

See [at (opens new window)](<https://apidock.com/ruby/Time/at/class>) method definition.

* * *

## [#](<#abs>) abs

Returns the absolute value of a number.

* * *

## [#](<#account-property>) account_property

Returns the value for a specific account property in the user's workspace.
```ruby
 
    client_secret = account_property('hubspot_webhook_client_secret')


```

Note that you can only invoke this method from the following lambdas within the `connection` hash:

  * `authorization_url`
  * `token_url`
  * `acquire`
  * `base_uri`

Also, other lambdas within `actions`, `triggers`, `methods`, `object_definitions`, and `pick_lists`.

* * *

## [#](<#aes-cbc-encrypt>) aes_cbc_encrypt

AES encryption with CBC mode. Accepts 128, 192, and 256-bit keys.
```ruby
 
    key128 = workato.pbkdf2_hmac_sha1("password", workato.random_bytes(8))
    workato.aes_cbc_encrypt("text_to_encrypt", key128)


```

* * *

## [#](<#aes-cbc-decrypt>) aes_cbc_decrypt

AES decryption with CBC mode. Accepts 128, 192, and 256-bit keys.
```ruby
 
    workato.aes_cbc_decrypt("text_to_decrypt", key128)


```

* * *

## [#](<#aes-gcm-encrypt>) aes_gcm_encrypt

Returns an AES encrypted string and auth tag using GCM mode. The initialization vector (IV) key size must be 12 bytes. Accepts 128, 192, and 256-bit keys.
```bash
 
    # Generate a salt for key derivation
    salt = workato.random_bytes(8)

    # Derive a key using PBKDF2 with HMAC-SHA1
    key128 = workato.pbkdf2_hmac_sha1("password", salt)

    # Initialize an IV (initialization vector)
    iv = "init_vector0"

    # Encrypt the text
    encrypted_data = workato.aes_gcm_encrypt("text_to_encrypt", key128, iv)  # [0x3040ffe9e51d4a929605fe0a262eea, 0x0f7e0a05eb25512c03ffafca43418a12]


```

You can also provide `auth_data`, which accepts a string value:
```ruby
 
    auth_data = "my_auth_data"

    # Generate a salt for key derivation
    salt = workato.random_bytes(8)

    # Derive a key using PBKDF2 with HMAC-SHA1
    key128 = workato.pbkdf2_hmac_sha1("password", salt)

    # Initialize an IV (initialization vector)
    iv = "init_vector0"

    # Encrypt the text
    encrypted_data = workato.aes_gcm_encrypt("text_to_encrypt", key128, iv, auth_data)  # [0x3040ffe9e51d4a929605fe0a262eea, 0x0f7e0a05eb25512c03ffafca43418a12]


```

The result is an array in the form `[encrypted_string, auth_tag]`. Use the [`.first`](<#first>) and [`.last`](<#last>) formulas to retrieve these values individually.

* * *

## [#](<#aes-gcm-decrypt>) aes_gcm_decrypt

Returns an AES decrypted string using GCM mode. The initialization vector (IV) key size must be 12 bytes. Accepts 128, 192, and 256-bit keys.
```ruby
 
    decrypted_string = workato.aes_gcm_decrypt(encrypted_string, key128, auth_tag, iv)  # 0x746578745f746f5f656e6372797074


```

If you encrypted with `auth_data`, you must include it in the formula:
```ruby
 
    decrypted_string = workato.aes_gcm_decrypt(encrypted_string, key128, auth_tag, iv, auth_data)  # 0x746578745f746f5f656e6372797074


```

The output is a raw byte sequence in hexadecimal format. You can append the [`.as_utf8`](<#as_utf8>) formula to decode it into a UTF-8 string:
```ruby
 
    decrypted_string =  workato.aes_gcm_decrypt(encrypted_string, key128, auth_tag, iv, auth_data).as_utf8  # "text_to_encrypt"


```

* * *

## [#](<#after-error-response>) after_error_response

Can be chained with an HTTP request to rescue a failed request. See [Error handling](</developing-connectors/sdk/guides/error-handling.html>).

* * *

## [#](<#after-response>) after_response

Can be chained with an HTTP request to utilize the response's headers, and so on. See [Error handling](</developing-connectors/sdk/guides/error-handling.html>).

* * *

## [#](<#ago>) ago

Go back in time. Returns timestamp.
```ruby
 
    2.days.ago #2017-01-15T12:30:00.000000-07:00 if time now is 2017-01-17T12:30:00.000000-07:00
    30.minutes.ago #2017-01-15T12:30:00.000000-07:00 if time now is 2017-01-15T13:00:00.000000-07:00
    30.seconds.ago #2017-01-15T12:30:00.000000-07:00 if time now is 2017-01-15T12:30:30.000000-07:00


```

See [ago (opens new window)](<https://apidock.com/rails/ActiveSupport/Duration/ago>) method definition.

* * *

## [#](<#all>) all?

Passes each element of the collection to the given block. The method returns true if the block never returns false or nil.
```ruby
 
    %w[ant bear cat].all? { |word| word.length >= 3 } #=> true


```

See [all?](<hhttps://apidock.com/ruby/Enumerable/all%3F>) method definition.

* * *

## [#](<#as-string>) as_string

Decode byte sequence as a string in the given encoding.
```ruby
 
    "0J/RgNC40LLQtdGC\n".decode_base64.as_string('utf-8')


```

* * *

## [#](<#as-utf8>) as_utf8

Decode byte sequence as a UTF-8 string.
```ruby
 
    "0J/RgNC40LLQtdGC\n".decode_base64.as_utf8


```

* * *

## [#](<#aws-generate-signature>) aws.generate_signature

Generates an AWS V4 Signature for AWS services and returns a hash that contains the URL and signature for you to formulate the request.
```ruby
 
    aws.generate_signature(
       connection: connection,
       service: "s3",
       region: connection["aws_region"],
       host: "s3.dualstack.#{connection['aws_region']}.amazonaws.com",
       method: "GET",
       path: "/demo",
       params: {
         "list-type": 2,
         "max-keys": 1000
       }.compact,
       headers: {
         Test: "hello!"
       },
       payload: {
         hello: "world"
       }.to_json
     )


```

See [AWS authentication](</developing-connectors/sdk/guides/authentication/aws_auth.html>).

* * *

## [#](<#blank>) blank?

Returns true if value is null or an empty string, otherwise false.

* * *

## [#](<#binary>) binary?

Returns true if value is a binary array.

* * *

## [#](<#beginning-of-hour>) beginning_of_hour

Returns timestamp for top-of-the-hour for given timestamp.
```ruby
 
    "2017-06-01T16:56:00.000000-07:00".to_time.beginning_of_hour #2017-06-01T16:00:00.000000 +0000


```

* * *

## [#](<#beginning-of-day>) beginning_of_day

Returns timestamp for midnight for given timestamp.
```ruby
 
    "2017-06-08T22:30:10.000000-07:00".to_time.beginning_of_day #2017-06-08T00:00:00.000000 +0000


```

* * *

## [#](<#beginning-of-week>) beginning_of_week

Returns timestamp for midnight at the start of the week (Mon) for the given timestamp.
```ruby
 
    "2017-08-18T00:00:00.000000-07:00".to_time.beginning_of_week #2017-08-14T00:00:00.000000 +0000


```

* * *

## [#](<#beginning-of-month>) beginning_of_month

Returns timestamp for midnight for the start of the month for the given timestamp.
```ruby
 
    "2017-01-30T22:35:00.000000-07:00".to_time.beginning_of_month #2017-01-01T00:00:00.000000 +0000


```

* * *

## [#](<#beginning-of-year>) beginning_of_year

Returns timestamp for midnight for the start of the year for a given timestamp.
```ruby
 
    "2017-01-30T22:35:00.000000 -07:00".to_time.beginning_of_year #2017-01-01T00:00:00.000000 +0000


```

* * *

## [#](<#bytes>) bytes

Returns an array of bytes for a given string.
```ruby
 
    "Hello".bytes # ["72","101","108","108","111"]


```

* * *

## [#](<#bytesize>) bytesize

Returns the length of a given string in bytes.
```ruby
 
    "Hello".bytesize # 5


```

* * *

## [#](<#byteslice>) byteslice

Returns a substring of specified bytes instead of length. In some cases, non-ASCII characters (for example, Japanese and Chinese characters) may use multiple bytes.
```ruby
 
    "abc漢字".byeslice(0,4) # "abc漢"


```

See [byteslice (opens new window)](<https://apidock.com/ruby/String/byteslice>) method definition.

* * *

## [#](<#capitalize>) capitalize

Capitalizes the first character of the string.

* * *

## [#](<#case-sensitive-headers>) case_sensitive_headers

Can be chained with HTTP methods to introduce headers that are case-sensitive. By default, Workato does not respect case sensitivity for headers, as per RFC specification.
```ruby
 
    get("https://www.example.com").case_sensitive_headers("HeLlo": "world")


```

* * *

## [#](<#checkpoint>) checkpoint!

Similar to `reinvoke_after`, the `checkpoint!` method is used with file stream consuming actions. When invoked, Workato checks the duration of the action's execution. If it exceeds 120 seconds, Workato refreshes the action level timeout with a slight delay to ensure fair processing.

This allows you to transfer files that exceed the current 180-second timeout limit.

* * *

## [#](<#chunk>) chunk

Enumerates over the items, chunking them together based on the return value of the block.

See [chunk (opens new window)](<https://apidock.com/ruby/Enumerable/chunk>) method definition.

* * *

## [#](<#chunk-while>) chunk_while

Creates an enumerator for each chunked element. The beginnings of chunks are defined by the block.

See [chunk_while (opens new window)](<https://apidock.com/ruby/Enumerable/chunk_while>) method definition.

* * *

## [#](<#collect>) collect

Returns a new array with the results of running block once for every element in enum.

See [collect (opens new window)](<https://apidock.com/ruby/Array/collect>) method definition.

* * *

## [#](<#collect-concat>) collect_concat

Returns a new array with the concatenated results of running block once for every element in enum.

See [collect_concat (opens new window)](<https://apidock.com/ruby/Enumerable/collect_concat>) method definition.

* * *

## [#](<#compact>) compact

Returns a hash with non nil values.

See [compact (opens new window)](<https://apidock.com/rails/Hash/compact>) method definition.

* * *

## [#](<#count>) count

Returns the number of elements in an array that match the given value.
```ruby
 
    ["apple", "orange", "apple", "banana", "apple"].count("apple")


```

For more details, refer to the [count (opens new window)](<https://apidock.com/ruby/Array/count>) method definition.

* * *

## [#](<#csv-parse>) csv.parse

Allows you to parse a CSV string into a JSON array that makes it easy to display as datapills.
```ruby
 
    workato.csv.parse("blue;1\nwhite;2\n", headers: "color;count", col_sep: ";")


```

Takes seven arguments:

  * string

  * The first position of the method which represents the CSV string to parse.

  * headers

  * Either `true` (First row of actual CSV will be used as headers), `array` of `string` (corresponding to each column header) or `string` (Artificial first row of the CSV with appropriate column separator).

  * col_sep

  * The column separator in the CSV. Defaults to `,`.

  * row_sep

  * The row separator in the CSV. Defaults to `\n`.

  * quote_char

  * The quoting character in the CSV. Defaults to double quotes `"`.

  * skip_blanks

  * Boolean that indicates whether blank lines in the string input should be ignored. Defaults to false.

  * skip_first_line

  * Boolean that indicates if we should skip the first line. Useful when `headers` is true.

**Limits:** File size must be less than 30 MB and CSV lines fewer than 65K.

* * *

## [#](<#csv-generate>) csv.generate

Allows you to generate a CSV string from a JSON array so you can send it to a downstream system as a file.
```ruby
 
    workato.csv.generate(headers: ["color", "amount"], col_sep: ";") do |csv|
      csv << [:blue, 1]
      csv << [:white, 2]
    end


```

Takes five arguments:

  * headers

  * Either `true` (First row of actual CSV will be used as headers), `array` of `string` (corresponding to each column header) or `string` (Artificial first row of the CSV with appropriate column separator).

  * col_sep

  * The column separator in the CSV. Defaults to `,`.

  * row_sep

  * The row separator in the CSV. Defaults to `\n`.

  * quote_char

  * The quoting character in the CSV. Defaults to double quotes `"`.

  * force_quotes

  * Boolean that determines whether each output field should be quoted.

Finally, one lambda that allows you to append individual rows to this CSV as an array of strings.

* * *

## [#](<#cycle>) cycle

Cycles through an array for a specified number of times and calls a block for each element.

See [cycle (opens new window)](<https://apidock.com/ruby/v2_5_5/Enumerable/cycle>) method definition.

* * *

## [#](<#decode-base64>) decode_base64

Decode using Base64 algorithm.

* * *

## [#](<#decode-hex>) decode_hex

Decode hexadecimal into binary string.

* * *

## [#](<#decode-url>) decode_url

URL decode a string. This formula uses `CGI.unescape` to URL decoding.

* * *

## [#](<#decode-urlsafe-base64>) decode_urlsafe_base64

Decode using URL-safe modification of Base64 algorithm.

* * *

## [#](<#decrypt>) decrypt

Decrypt the encrypted string using AES-256-CBC algorithm. Input should be in RNCryptor V3 format.

This method returns a byte array instead of a string. You can convert the decrypt method output to a string by appending the [`.as_string()`](<#as-string>) or [`.as_utf8`](<#as-utf8>) function to your formula.

* * *

## [#](<#deep-merge>) deep_merge

Merges a hash with another hash, including nested child hashes.

See [deep_merge (opens new window)](<https://apidock.com/rails/Hash/deep_merge>) method definition.

* * *

## [#](<#delete-at>) delete_at

Delete elements in an array.

See [delete_at (opens new window)](<https://apidock.com/ruby/Array/delete_at>) method definition.

* * *

## [#](<#detect>) detect

Passes each element in an array to a block. Returns the first element that satisfies a block.

See [detect (opens new window)](<https://apidock.com/ruby/v2_5_5/Enumerable/detect>) method definition.

* * *

## [#](<#dig>) dig

Retrieves the value object corresponding to the index passed in.

The `dig` method is often used to strip away layers in nested arrays/hashes. For example, we use the `dig` method often when dealing with XML data formats.

See [dig (opens new window)](<https://apidock.com/ruby/Array/dig>) method definition.

* * *

## [#](<#drop>) drop

Drops first N elements from an Enumerator and returns the rest of the elements in an array.
```ruby
 
    [1, 2, 3, 4, 5, 0].drop(3) #=> [4, 5, 0]


```

See [drop (opens new window)](<https://apidock.com/ruby/v2_5_5/Enumerable/drop>) method definition.

* * *

## [#](<#drop-while>) drop_while

Drops elements up to, but not including, the first element of an array for which the block returns nil or false.

See [drop_while (opens new window)](<https://apidock.com/ruby/v2_5_5/Enumerable/drop_while>) method definition.

* * *

## [#](<#dst>) dst?

Returns true if the time is within Daylight Savings Time for the specified time zone.

* * *

## [#](<#each>) each

Basic iterator.
```ruby
 
    [1, 2, 3].each { |i| puts i }


```

* * *

## [#](<#each-byte>) each_byte

Passes each byte in a given string to the given block, or returns an enumerator if no block is given.

See [each_byte (opens new window)](<https://apidock.com/ruby/v2_5_5/String/each_byte>) method definition.

* * *

## [#](<#each-char>) each_char

Passes each character in a given string to the given block. Returns an enumerator if no block is given.

See [each_char (opens new window)](<https://apidock.com/ruby/String/each_char>) method definition.

* * *

## [#](<#each-cons>) each_cons

Iterates the given block for each array of consecutive N elements. If no block is given, returns an enumerator.

See [each_cons (opens new window)](<https://apidock.com/ruby/v2_5_5/Enumerable/each_cons>) method definition.

* * *

## [#](<#each-entry>) each_entry

Iterates over an array and returns each element in the block.

See [each_entry (opens new window)](<https://apidock.com/ruby/v2_5_5/Enumerable/each_entry>) method definition.

* * *

## [#](<#each-slice>) each_slice

Iterates the given block for each slice of N elements. If no block is given, returns an enumerator.

See [each_slice (opens new window)](<https://apidock.com/ruby/v2_5_5/Enumerable/each_slice>) method definition.

* * *

## [#](<#each-with-index>) each_with_index

Iterator returned with an index.
```ruby
 
    [1, 2, 3].each_with_index { |item, index| puts "#{index}:#{item}" }


```

See [each_with_index (opens new window)](<https://apidock.com/ruby/Enumerator/each_with_index>) method definition.

* * *

## [#](<#each-with-object>) each_with_object

Iterator returned with an object which you can define.
```ruby
 
    [%w(foo bar)].each_with_object({}) { |str, hsh| hsh[str] = str.upcase }
    # => {'foo' => 'FOO', 'bar' => 'BAR'}


```

See [each_with_object (opens new window)](<https://apidock.com/rails/Enumerable/each_with_object>) method definition.

* * *

## [#](<#encode-hex>) encode_hex

Converts binary string to its hex representation.
```ruby
 
    "0J/RgNC40LLQtdGC\n".decode_base64.encode_hex


```

* * *

## [#](<#encode-sha256>) encode_sha256

Encode using SHA256 algorithm. The output is a binary string. Use `encode_hex` to convert to a hex representation.
```ruby
 
    "hello".encode_sha256 #=> 0x2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824
    "hello".encode_sha256.encode_hex #=> 2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824


```

* * *

## [#](<#encode-sha512>) encode_sha512

Encode using SHA512 algorithm. The output is a binary string. Use `encode_hex` to convert to a hex representation.
```ruby
 
    "hello".encode_sha512 #=> 0x9b71d224bd62f3785d96d46ad3ea3d73319bfbc2890caadae2dff72519673ca72323c3d99ba5c11d7c7acc6e14b8c5da0c4663475c2e5c3adef46f73bcdec043
    "hello".encode_sha512.encode_hex #=> 9b71d224bd62f3785d96d46ad3ea3d73319bfbc2890caadae2dff72519673ca72323c3d99ba5c11d7c7acc6e14b8c5da0c4663475c2e5c3adef46f73bcdec043


```

* * *

## [#](<#encode-base64>) encode_base64

Encode using Base64 algorithm.

* * *

## [#](<#encode-url>) encode_url

URL encode a string.
```ruby
 
    'Hello World'.encode_url # 'Hello%20World'


```

* * *

## [#](<#encode-urlsafe-base64>) encode_urlsafe_base64

Encode using URL-safe modification of Base64 algorithm.

* * *

## [#](<#encode-www-form>) encode_www_form

Join hash into URL-encoded string of parameters.
```ruby
 
    {"apple" => "red green", "2" => "3"}.encode_www_form #"apple=red+green&2=3"


```

* * *

## [#](<#ends-of-month>) ends_of_month

Returns a new date/time representing the end of the month.
```ruby
 
    "2017-08-18T00:00:00".to_time.end_of_month #2017-08-31 23:59:59 +0000


```

* * *

## [#](<#ends-with>) ends_with?

Returns true if string ends with a specific pattern. False otherwise.
```ruby
 
    "Hello!".ends_with?("!") #true


```

* * *

## [#](<#entries>) entries

Returns an array containing the items in enum.
```ruby
 
    (1..7).entries #=> [1, 2, 3, 4, 5, 6, 7]
    { 'a'=>1, 'b'=>2, 'c'=>3 }.entries   #=> [["a", 1], ["b", 2], ["c", 3]]


```

See [entries (opens new window)](<https://apidock.com/ruby/v2_5_5/Enumerable/entries>) method definition.

* * *

## [#](<#error>) error

Raise a job error with a user-defined error body.
```ruby
 
    error("Unable to find Account with ID: 123")


```

* * *

## [#](<#even>) even?

Returns true if integer is an even number.

See [even? (opens new window)](<https://apidock.com/ruby/Integer/even%3F>) method definition.

* * *

## [#](<#except>) except

Returns a hash that includes everything except given keys.
```ruby
 
    { name: "Jake", last_name: "Paul", age: "22" }.except(:name, :last_name) # { :age => "22" }


```

See [except (opens new window)](<https://apidock.com/rails/Hash/except>) method definition.

* * *

## [#](<#exclude>) exclude?

Returns true if field does not contain a value. Case sensitive.
```ruby
 
    "Partner account".exclude?("Partner") #false


```

See [exclude (opens new window)](<https://apidock.com/rails/String/exclude%3F>) method definition.

* * *

## [#](<#execution-context>) execution_context

RESTRICTED METHOD AVAILABILITY

This method is available only to connectors built within Embedded partner workspaces. It returns a hash containing the context of the recipe and job from which this action or trigger is invoked. If there is no applicable context, for example, the job ID when a request is sent in a trigger, the key's value is `null`.

The following table summarizes the lambdas: `execution_context` return values:

Key | recipe_id | job_id  
---|---|---  
execute | Yes | Yes  
methods (For each method called within execute) | Yes | Yes  
apply (For requests sent in the execute lambda) | Yes | Yes  
poll | Yes | No  
methods (For each method called within poll) | Yes | No  
apply (For requests sent in the poll lambda) | Yes | No  
object_definitions (For each fields method defined) | No | No  
pick_lists (For each pick_list method defined) | No | No  
methods (For each method called within pick_lists or object_definitions) | No | No  

You can reference the execution context using the `execution_context` method.
```ruby
 
    execution_context #=> { :recipe_id => "1234", :job_id => "j-ATh8ngzP-f69ak9" }
    execution_context[:recipe_id] #=> "1234"
    execution_context[:job_id] #=> "j-ATh8ngzP-f69ak9"


```

* * *

## [#](<#fetch>) fetch

Returns a value from the hash for the given key.

See [fetch (opens new window)](<https://apidock.com/ruby/Hash/fetch>) method definition.

* * *

## [#](<#find-all>) find_all

Returns an array containing all elements of a hash or array that satisfy the condition denoted in the block.
```ruby
 
    Foo = { :abc => 1, :bad => [1,2] }
    Foo.find_all { |i| i[0] == :abc } # [[:abc, 1]]


```

See [find_all (opens new window)](<https://apidock.com/ruby/Enumerable/find_all>) method definition.

* * *

## [#](<#find-index>) find_index

Compares each element in an array to a given block and returns the index for the first match.
```ruby
 
    (1..100).find_index { |i| i % 5 == 0 and i % 7 == 0 }  #=> 34


```

See [find_index (opens new window)](<https://apidock.com/ruby/v2_5_5/Enumerable/find_index>) method definition.

* * *

## [#](<#first>) first

Returns the first item in a list. Can also be used to return the first n items in a list.

See [first (opens new window)](<https://apidock.com/ruby/Array/first>) method definition.

* * *

## [#](<#flatten>) flatten

Flatten multi-dimensional array to simple array.
```ruby
 
    [[1, 2, 3],[4,5,6]].flatten #[1, 2, 3, 4, 5, 6]


```

See [flatten (opens new window)](<https://apidock.com/ruby/Array/flatten>) method definition.

* * *

## [#](<#flat-map>) flat_map

Returns a new array with the concatenated results of running block once for every element in enum.
```ruby
 
    [[1, 2], [3, 4]].flat_map { |e| e + [100] } #=> [1, 2, 100, 3, 4, 100]


```

See [flat_map (opens new window)](<https://apidock.com/ruby/v2_5_5/Enumerable/flat_map>) method definition.

* * *

## [#](<#follow-redirection>) follow_redirection

By default, we follow most 3XX redirect HTTP codes. In some cases, you may need to apply this to follow the redirect for any response code.
```ruby
 
        action_with_follow_redirection: {
          execute: lambda do |_connection, _input|
     get('https://run.mocky.io/v3/41abc094-6b10-41a9-8201-b15146258b12').follow_redirection.after_response do |code, body, headers|
       {
         code: code,
         body: body,
         headers: headers
       }
     end
          end
        }


```

* * *

## [#](<#format-json>) format_json

Convert request to JSON format and expect response body in JSON format.

* * *

## [#](<#format-map>) format_map

Creates a new array of strings by applying a format to each item in the input array.
```ruby
 
    [[{name: 'Jake', age: 23}].format_map('Name: %{name}, Age: %{age}') #['Name: Jake, Age: 23']
    [[22, 45], [33, 88]].format_map('Id: %s, Count: %s') #['Id: 22, Count: 45', 'Id: 33, Count: 88']
    ['Alex', 'Hao', 'Kai'].format_map('Name: %s') #['Name: Alex', 'Name: Hao', 'Name: Kai']


```

See [format_map](</formulas/array-list-formulas.html#formatmap>) method definition.

* * *

## [#](<#format-xml>) format_xml

Convert request to XML format and expect response body in XML format.

Takes three arguments:

  * root_element_name

  * Adds a root element tag to your outgoing XML payload.

  * namespaces

  * Adds additional tags to your payload for namespaces.

  * strip_response_namespaces

  * Strips namespaces from XML responses.

* * *

## [#](<#from-now>) from_now

Go forward in time. Returns timestamp of the moment that the formula was executed, with the specified time period added in Pacific Time (UTC-8/UTC-7).
```ruby
 
    4.months.from_now #2017-05-23T14:40:07.338328-07:00
    2.days.from_now #2017-01-05T14:40:07.338328-07:00
    30.minutes.from_now
    12.seconds.from_now


```

* * *

## [#](<#from-xml>) from_xml

Converts XML string to hash.
```ruby
 
    "<?xml version="1.0" encoding="UTF-8"?> <hash><foo type="integer"></foo></hash>".from_xml # { "hash": [ "foo": [ { "@type": "integer", "content!": "1" } ] ] }


```

* * *

## [#](<#grep>) grep

Searches through an enumerator for every element that satisfies your condition.

See [grep (opens new window)](<https://apidock.com/ruby/v2_5_5/Enumerable/grep>) method definition.

* * *

## [#](<#grep-v>) grep_v

Searches through an enumerator for every element that does not satisfy your condition.

See [grep_v (opens new window)](<https://apidock.com/ruby/v2_5_5/Enumerable/grep_v>) method definition.

* * *

## [#](<#group-by>) group_by

Group arrays into sets.

See [group_by (opens new window)](<http://apidock.com/rails/Enumerable/group_by>) method definition.

* * *

## [#](<#gsub>) gsub

Substitute a pattern with value. Case sensitive.
```ruby
 
    "Jean Marie".gsub(/J/, "M") #"Mean Marie"


```

See [gsub (opens new window)](<https://apidock.com/ruby/String/gsub>) method definition.

* * *

## [#](<#has-key>) has_key?

Returns true if the given key is present in hash.

See [has_key? (opens new window)](<https://apidock.com/ruby/GDBM/has_key%3F>) method definition.

* * *

## [#](<#headers>) headers

Add headers to a request.
```ruby
 
    .headers(Authorization: "Bearer HTB674HJK1")


```

* * *

## [#](<#hmac-md5>) hmac_md5

Creates HMAC_MD5 signature.
```ruby
 
    "username:password:nonce".hmac_md5("key")


```

* * *

## [#](<#hmac-sha1>) hmac_sha1

Creates HMAC_SHA1 signature.
```ruby
 
    "username:password:nonce".hmac_sha1("key")


```

* * *

## [#](<#hmac-sha256>) hmac_sha256

Creates HMAC_SHA256 signature.
```ruby
 
    "username:password:nonce".hmac_sha256("key")


```

* * *

## [#](<#hmac-sha512>) hmac_sha512

Creates HMAC_SHA512 signature.
```ruby
 
    "username:password:nonce".hmac_sha512("key")


```

* * *

## [#](<#ignore-redirection>) ignore_redirection

Allows you to stop a request from being redirected immediately. Commonly used in cases where your requests are redirected to a secondary site like AWS S3 to download a file. You will need to strip any authentication used in the apply: key using "current_url".
```ruby
 
        action_with_ignore_redirection: {
          execute: lambda do |_connection, _input|
     get('https://run.mocky.io/v3/41abc094-6b10-41a9-8201-b15146258b12').ignore_redirection.after_response do |code, body, headers|
       {
         code: code,
         body: body,
         headers: headers
       }
     end
          end
        },


```

* * *

## [#](<#ignored>) ignored

Ignore a comma-separate list of fields.
```ruby
 
    object_definition["user"].ignored("id", "created_at")


```

* * *

## [#](<#include>) include?

Returns true if field contains a value. False otherwise.

See [include? (opens new window)](<https://apidock.com/ruby/String/include%3F>) method definition.

* * *

## [#](<#inject>) inject

Combine elements in an array using an operation.

See [inject (opens new window)](<http://apidock.com/ruby/Enumerable/inject>) method definition.

* * *

## [#](<#insert>) insert

Insert elements into an array.

See [insert (opens new window)](<https://apidock.com/ruby/v2_5_5/Array/insert>) method definition.

* * *

## [#](<#in-time-zone>) in_time_zone

Converts the time to given time zone.
```ruby
 
    "2017-09-06T18:30:15.671720-05:00".to_time.in_time_zone("America/Los_Angeles") #"2017-09-06T16:30:15.671720-07:00"


```

* * *

## [#](<#is-a>) is_a?

Returns true if class is the class of obj, or if class is one of the superclasses of obj or modules included in obj.

Workato currently supports the following classes:

  * Array
  * Hash
  * Time
  * String
  * Integer
  * Float

See [is_a? (opens new window)](<https://apidock.com/ruby/Object/is_a%3F>) method definition.

* * *

## [#](<#is-true>) is_true?

Converts a value to boolean and returns true if value is truthy.

* * *

## [#](<#is-not-true>) is_not_true?

Converts a value to boolean and returns true if value is not truthy.

* * *

## [#](<#iso8601>) iso8601

Convert a date/date-time variable to ISO8601 format.

* * *

## [#](<#join>) join

Join array elements into a string.

See [join (opens new window)](<https://apidock.com/ruby/Array/join>) method definition.

* * *

## [#](<#jwt-decode>) jwt_decode

Decodes a JSON web token (JWT) using one of the following algorithms:

  * RS256
  * RS384
  * RS512
  * HS256
  * HS384
  * HS512
  * ES256
  * ES384
  * ES512

```ruby
 
    workato.jwt_decode( "eyJhbGciO...", "PEM key", \'RS256\') # => {"payload" => {"sub"=>"123", "name"=>"John", ...}, "header" => {"typ"=>"JWT", "alg"=>"RS256"}}
    workato.jwt_decode( "eyJhbGciO...", "PEM key", \'RS512\') # => {"payload" => {"sub"=>"123", "name"=>"John", ...}, "header" => {"typ"=>"JWT", "alg"=>"RS512"}}
    workato.jwt_decode( "eyJhbGciO...", "my$ecretK3y", \'HS256\') # => {"payload" => {"sub"=>"123", "name"=>"John", ...}, "header" => {"typ"=>"JWT", "alg"=>"HS256"}}


```

* * *

## [#](<#jwt-encode>) jwt_encode

Creates a JSON web token (JWT) using one of the following algorithms:

  * RS256
  * RS384
  * RS512
  * HS256
  * HS384
  * HS512
  * ES256
  * ES384
  * ES512

Adds other named parameters to the header, such as `kid` in the following example:
```ruby
 
    workato.jwt_encode({ name: "John Doe" }, "PEM key", 'RS256') # => "eyJhbGciO..."
    workato.jwt_encode({ name: "John Doe" }, "PEM key", 'RS512', kid: "24668") #=> "eyJ0eXAiO..."
    workato.jwt_encode({ name: "John Doe" }, "my$ecretK3y", 'HS256', kid: "24668") #=> "eyJ0eXAiO..."
    workato.jwt_encode({ name: "John Doe" }, "my$ecretK3y", 'HS256') #=> "eyJ0eXAiO..."
    workato.jwt_encode({ name: "John Doe" }, "ECDSA Key", 'ES256') #=> "eyJhbGciOiJ..."


```

* * *

## [#](<#last>) last

Returns the last item in a list. Can also be used to return the last n items in a list.

See [last (opens new window)](<https://apidock.com/ruby/Array/last>) method definition.

* * *

## [#](<#ljust>) ljust

Aligns strings to the left and pads with whitespace or specified pattern until string is the required length.
```ruby
 
    " test".ljust(10, "*") # " test*****"


```

See [ljust (opens new window)](<https://apidock.com/ruby/String/ljust>) method definition.

* * *

## [#](<#lookup>) lookup

Lookup a record from your lookup tables defined in Workato.
```ruby
 
    lookup('States list', 'State code': 'AZ')['State name'] #"Arizona"


```

See [lookup](</formulas/other-formulas.html#lookup>) method definition.

* * *

## [#](<#lstrip>) lstrip

Remove white space from the beginning of string.
```ruby
 
    "     Test     ".lstrip #"Test     "


```

See [lstrip (opens new window)](<https://apidock.com/ruby/String/lstrip>) method definition.

* * *

## [#](<#map>) map

Returns a new array after invoking block on each element.

* * *

## [#](<#md5-hexdigest>) md5_hexdigest

Creates message digest using the MD5 Message-Digest Algorithm.
```ruby
 
    "hello".md5_hexdigest #5d41402abc4b2a76b9719d911017c592


```

* * *

## [#](<#match>) match?

Returns true if a string contains a pattern. Case sensitive.
```ruby
 
    "Jean Marie".match?(/Marie/) #true


```

* * *

## [#](<#max-by>) max_by

Returns the object in enum that gives the maximum value from the given block.
```ruby
 
    %w(albatross dog horse).max_by { |x| x.length } # albatross


```

* * *

## [#](<#member>) member?

Alias of include?

See [member? (opens new window)](<https://apidock.com/ruby/v2_5_5/Enumerable/member%3F>) method definition.

* * *

## [#](<#merge>) merge

Returns a new hash containing merged contents.

See [merge (opens new window)](<https://ruby-doc.org/core-2.2.0/Hash.html#method-i-merge>) method definition.

* * *

## [#](<#minmax>) minmax

Returns a two element array which contains the minimum and the maximum value in the enumerable.
```ruby
 
    a = %w(albatross dog horse)
    a.minmax    #=> ["albatross", "horse"]
    a.minmax { |a, b| a.length <=> b.length }
    #=> ["dog", "albatross"]


```

See [minmax (opens new window)](<https://apidock.com/ruby/v2_5_5/Enumerable/minmax>) method definition.

* * *

## [#](<#minmax-by>) minmax_by

Returns a two element array containing the objects in enum that correspond to the minimum and maximum values respectively from the given block.
```ruby
 
    a = %w(albatross dog horse)
    a.minmax_by { |x| x.length }   #=> ["dog", "albatross"]


```

See [minmax_by (opens new window)](<https://apidock.com/ruby/v2_5_5/Enumerable/minmax_by>) method definition.

* * *

## [#](<#min-by>) min_by

Returns the object in enum that gives the minimum value from the given block
```ruby
 
    a = %w(albatross dog horse)
    a.min_by { |x| x.length }   #=> "dog"


```

See [min_by (opens new window)](<https://apidock.com/ruby/v2_5_5/Enumerable/min_by>) method definition.

* * *

## [#](<#net-lookup>) net.lookup

Lookups specified DNS records for a given host.
```ruby
 
    workato.net.lookup("www.google.com", "A") # => [{"address": "172.253.122.106"}, {"address":"172.253.122.103"}]


```

Takes two arguments:

  * name

  * The resource name such as the domain or host.

  * Record Type

  * Only supports "SRV" or "A" DNS record types

* * *

## [#](<#next>) next

Returns the next object in the enumerator, and move the internal position forward.

This is often used in config_fields where you can use `next` as a way to add a guard clause that checks inputs before the lambda function is executed.
```ruby
 
    object_definitions: {
      document: {
        fields: lambda do |connection, config_fields, object_definitions|
          next [] if config_fields.blank?
          get("https://www.webmerge.me/api/documents/#{config_fields["document_id"]}/fields").map {
     |field| field.slice("name")
          }
        end
      }
    }


```

See [next (opens new window)](<https://apidock.com/ruby/Enumerator/next>) method definition.

* * *

## [#](<#none>) none?

Passes each element of the collection to the given block. The method returns true if the block never returns true for all elements.
```ruby
 
    %w{ant bear cat}.none? { |word| word.length == 5 } #=> true


```

See [none? (opens new window)](<https://apidock.com/ruby/v2_5_5/Enumerable/none%3F>) method definition.

* * *

## [#](<#now>) now

Returns timestamp of the moment that the formula was executed in Pacific Time (UTC-8/UTC-7).
```ruby
 
    now #2017-01-23T14:04:53.365908-08:00
    now + 2.days #2017-01-25T14:04:53.365908-08:00


```

* * *

## [#](<#odd>) odd?

Returns true if integer is an odd number. See [odd? (opens new window)](<https://apidock.com/ruby/Integer/odd%3F>) method definition.

* * *

## [#](<#one>) one?

Passes each element of the collection to the given block. The method returns true if the block returns true exactly once.
```ruby
 
    [ nil, true, false ].one? #=> true


```

See [one? (opens new window)](<https://apidock.com/ruby/v2_5_5/Enumerable/one%3F>) method definition.

* * *

## [#](<#only>) only

White list a comma-separate of fields.
```ruby
 
    object_definition["user"].only("id", "name")


```

* * *

## [#](<#ordinalize>) ordinalize

Turns a number into an ordinal string used to denote the position in an ordered sequence such as first, second, third, fourth.
```ruby
 
    "1".ordinalize # "First"


```

* * *

## [#](<#pack>) pack

Packs contents of an array into a binary sequence.

See [pack (opens new window)](<https://apidock.com/ruby/Array/pack>) method definition.

* * *

## [#](<#parallel>) parallel

Accepts an array of requests and allows you to execute them in multiple threads.
```ruby
 
    batches = (0..200).map do |batch|
      post(url).headers(headers).request_body(payload)
    end
    results = parallel(batches, threads: 20)


```

See [Multi-threaded actions](</developing-connectors/sdk/guides/building-actions/multi-threaded-actions.html>) for more information.

* * *

## [#](<#parameterize>) parameterize

Replaces special characters in a string.
```ruby
 
    "öüâ".parameterize #"oua"


```

* * *

## [#](<#params>) params

Add parameter to a request.
```ruby
 
    .params(api_key: "HTB674HJK1")


```

* * *

## [#](<#parse-json>) parse_json

Works the same way as json.parse.

See [parse_json (opens new window)](<https://apidock.com/ruby/v1_9_3_392/JSON/parse>) method definition.

* * *

## [#](<#parse-yaml>) parse_yaml

Parse a YAML string. Supports true, false, nil, numbers, strings, arrays, hashes.
```ruby
 
    workato.parse_yaml("---\nfoo: bar") # => { "foo" => "bar" }


```

* * *

## [#](<#payload>) payload

Add payload to a request.
```ruby
 
    .payload(id: "345")


```

* * *

## [#](<#pbkdf2-hmac-sha1>) pbkdf2_hmac_sha1

Create keys of varying bit lengths using a password and a salt. Uses HMAC Sha1.
```ruby
 
    key128 = workato.pbkdf2_hmac_sha1("password", workato.random_bytes(8))
    key192 = workato.pbkdf2_hmac_sha1("password", workato.random_bytes(8), 1000, 24)
    key256 = workato.pbkdf2_hmac_sha1("password", workato.random_bytes(8), 1000, 32)


```

* * *

## [#](<#pluck>) pluck

Select one or more attributes from an array of objects.
```ruby
 
    [
      {"id": 1, "name": "David"},
      {"id": 2, "name": "Peter"}
    ].pluck("id")


```

Returns `[1, 2]`.

* * *

## [#](<#pluralize>) pluralize

Returns the plural form of the word in the string.

See [pluralize (opens new window)](<https://apidock.com/rails/String/pluralize>) method definition.

* * *

## [#](<#pop>) pop

Removes the last element from self and returns it, or nil if the array is empty.

If a number n is given, returns an array of the last n elements (or less) and removes it from array.
```ruby
 
    a = [ "a", "b", "c", "d" ]
    a.pop     #=> "d"
    a.pop(2)  #=> ["b", "c"]
    a  #=> ["a"]


```

See [pop (opens new window)](<https://apidock.com/ruby/Array/pop>) method definition.

* * *

## [#](<#presence>) presence

Returns the value if present. Otherwise returns nil.
```ruby
 
    nil.presence #nil
    "".presence #nil
    0.presence #0


```

See [presence (opens new window)](<https://apidock.com/rails/Object/presence>) method definition.

* * *

## [#](<#present>) present?

Returns true if the field has a value. False otherwise.
```ruby
 
    nil.present? #false
    "".present? #false
    0.present? #true


```

See [present? (opens new window)](<https://apidock.com/rails/Object/present%3F>) method definition.

* * *

## [#](<#puts>) puts

Ruby version of `console.log` or `stdout`. Not the same as the `put` method.

Any output using the `puts` method shows up in the console log when testing in the code editor. Use this to aid in your debugging.

* * *

## [#](<#rand>) rand

Random number between 0 and 1.

* * *

## [#](<#random-bytes>) random_bytes

Generates a specified number of random bytes.
```ruby
 
    workato.random_bytes(8)


```

* * *

## [#](<#reduce>) reduce

Combines all elements of enum by applying a binary operation, specified by a block or a symbol that names a method or operator.
```ruby
 
    (5..10).reduce { |sum, n| sum + n } # 45


```

See [reduce (opens new window)](<https://apidock.com/ruby/v2_5_5/Enumerable/reduce>) method definition.

* * *

## [#](<#reinvoke-after>) reinvoke_after

Used in multistep actions that work with asynchronous APIs. Calling this method causes the job to pause for a specific interval before reinvoking the original `execute` lambda it is called in. Accepts `seconds` to denote how long the job should pause for, and `continue` which allows the job to be reinvoked with additional context.
```ruby
 
    reinvoke_after(
      seconds: step_time, 
      continue: { 
        current_step: current_step + 1, 
        jobid: response['jobReference']['jobId'] 
      }
    )


```

See [Multistep actions](</developing-connectors/sdk/guides/building-actions/multistep-actions.html>) for more information.

* * *

## [#](<#reject>) reject

Selectively returns elements for which the block returns false. Similar but opposite of **select**.

See [reject (opens new window)](<http://apidock.com/ruby/v1_9_3_392/Array/reject>) method definition.

* * *

## [#](<#render-yaml>) render_yaml

Render an object into a YAML string.
```ruby
 
    workato.render_yaml({ "foo" => "bar" }) # => "---\nfoo: bar\n"


```

* * *

## [#](<#response-format-json>) response_format_json

Expect response in JSON format.

* * *

## [#](<#response-format-raw>) response_format_raw

Expect response in raw format. This can be chained after HTTP actions that expect binary data (such as PDFs and images) as responses.

* * *

## [#](<#response-format-xml>) response_format_xml

Expect response in XML format. Takes 1 argument.

  * strip_response_namespaces
  * Strips namespaces from XML responses.

* * *

## [#](<#request-format-json>) request_format_json

Convert request to JSON format.

* * *

## [#](<#request-format-multipart-form>) request_format_multipart_form

Convert request to multipart_form format.

* * *

## [#](<#request-format-raw>) request_format_raw

Convert request to raw format.

* * *

## [#](<#request-format-www-form-urlencoded>) request_format_www_form_urlencoded

Convert request to URL-encoded format.

* * *

## [#](<#request-format-xml>) request_format_xml

Convert request to XML format.

Takes two arguments:

  * root_element_name

  * Adds a root element tag to your outgoing XML payload.

  * namespaces

  * Adds additional tags to your payload for namespaces

## [#](<#required>) required

Make a comma-separate list of fields required.
```ruby
 
    object_definition["user"].required("id", "created_at")


```

* * *

## [#](<#reverse>) reverse

Reverse string or array.

* * *

## [#](<#reverse-each>) reverse_each

Builds a temporary array and traverses that array in reverse order.

See [reverse_each (opens new window)](<https://apidock.com/ruby/v2_5_5/Enumerable/reverse_each>) method definition.

* * *

## [#](<#rjust>) rjust

Aligns string to right and pads with whitespace or pattern until string is specified length.
```ruby
 
    "test".rjust(5) #" test"
    "test".rjust(10, "*!") #"*!*!* test"


```

See [rjust (opens new window)](<https://apidock.com/ruby/String/rjust>) method definition.

* * *

## [#](<#round>) round

Round the number by regular rounding rules.
```ruby
 
    11.99.round #12
    11.555.round(2) #11.56


```

See [round (opens new window)](<https://apidock.com/ruby/Float/round>) method definition.

* * *

## [#](<#rsa-sha256>) rsa_sha256

Creates a RS256 signature (SHA256 hash signed with an RSA key)
```ruby
 
    input['StringToSign'].rsa_sha256(rsa_private_key).base64


```

* * *

## [#](<#rsa-sha512>) rsa_sha512

Creates a RS512 signature (SHA512 hash signed with an RSA key).
```ruby
 
    input['StringToSign'].rsa_sha512(rsa_private_key).base64


```

* * *

## [#](<#rstrip>) rstrip

Remove white space from the end of string.
```ruby
 
    " Test ".rstrip #" Test"


```

See [rstrip (opens new window)](<https://apidock.com/ruby/String/rstrip>) method definition.

* * *

## [#](<#scan>) scan

Scans the string for a matching pattern.
```ruby
 
    "Thu, 01/23/2014".scan(/\d+/).join("-") #01-23-2014


```

See [scan (opens new window)](<https://apidock.com/ruby/String/scan>) method definition.

* * *

## [#](<#scrub>) scrub

If the string is invalid byte sequence then replace invalid bytes with given replacement character, else returns self.
```ruby
 
    "abc\u3042\x81".scrub("*") # "abc\u3042*"


```

See [scrub (opens new window)](<https://apidock.com/ruby/v2_5_5/String/scrub>) method definition.

* * *

## [#](<#select>) select

Selectively returns elements for which the block returns true.

See [select (opens new window)](<http://apidock.com/ruby/v1_9_3_392/Array/select>) method definition.

* * *

## [#](<#sha1>) SHA1

Encrypts a given string using the SHA1 encryption algorithm.
```ruby
 
    "abcdef".sha1.encode_base64 # "H4rBDyPFtbwRZ72oS4M+XAV6d9I="


```

See [SHA1 (opens new window)](<https://ruby-doc.org/stdlib-2.4.0/libdoc/digest/rdoc/Digest/SHA1.html>) method definition.

* * *

## [#](<#singularize>) singularize

The reverse of `pluralize`. Returns the singular form of a word in a string.
```ruby
 
    'posts'.singularize # => "post"


```

See [singularize (opens new window)](<https://apidock.com/rails/String/singularize>) method definition.

* * *

## [#](<#slice>) slice

Returns a substring of a given string, as defined by start indexes and length.
```ruby
 
    "Jean Marie\.slice(0,3) #"Jea"


```

See [slice (opens new window)](<https://apidock.com/ruby/String/slice>) method definition.

* * *

## [#](<#slice-after>) slice_after

Slices an array after a specific value.
```ruby
 
    ["a", "b", "c"].slice_after("b").to_a # [["a", "b"], ["c"]]


```

See [slice_after (opens new window)](<https://apidock.com/ruby/v2_5_5/Enumerable/slice_after>) method definition.

* * *

## [#](<#slice-before>) slice_before

Slices an array before a specific value.
```ruby
 
    ["a", "b", "c"].slice_before("b").to_a # [["a"], ["b", "c"]]


```

See [slice_before (opens new window)](<https://apidock.com/ruby/v2_5_5/Enumerable/slice_before>) method definition.

* * *

## [#](<#slice-when>) slice_when

Creates an enumerator for each chunked elements.
```ruby
 
    [1,2,4,9,10,11].slice_when { |i,j| i+1 != j}.to_a # [[1, 2], [4], [9, 10, 11]]


```

See [slice_when (opens new window)](<https://apidock.com/ruby/Enumerable/slice_when>) method definition.

* * *

## [#](<#smart-join>) smart_join

Join array to string. Removes empty and nil values. Trims the white space before joining.
```ruby
 
    [nil, " ", " Hello ", "   World "].smart_join(" ") #Hello World


```

See [smart_join](</formulas/array-list-formulas.html#smart-join>) method definition.

* * *

## [#](<#sort>) sort

Sort function returning new sorted array.

See [sort (opens new window)](<http://apidock.com/ruby/v1_9_3_392/Array/sort>) method definition.

* * *

## [#](<#sort-by>) sort_by

Sort function returning self.

See [sort_by (opens new window)](<https://apidock.com/ruby/Enumerable/sort_by>) method definition.

* * *

## [#](<#split>) split

Split string into an array by using defined pattern as delimiter.
```ruby
 
    "Split string".split() #["Split", "string"]
    "Split string".split("t") #["Spli", " s", "ring"]


```

See [split (opens new window)](<https://apidock.com/ruby/String/split>) method definition.

* * *

## [#](<#stream-out>) stream.out

Used in file stream producing actions that work with any of Workato's file streaming enabled connectors. Calling this method allows you to specify a `streaming` callback that is invoked when a downstream action downloads the file.
```ruby
 
    workato.stream.out("download_file", { file_id: file_id })


```

See [file streaming](</developing-connectors/sdk/guides/building-actions/streaming.html>) for more information.

* * *

## [#](<#stream-in>) stream.​in

Used in file stream consuming actions that work with any of Workato's file streaming enabled connectors. Calling this method allows you to specify a code block that can utilize a file stream to upload a file in chunks.

This method takes three arguments:

  1. the first positional argument being the file contents from a previous action
  2. `from` which is used to override the default offset of `0`. This will be used in implementing multi-step streaming
  3. `frame_size` which is used to override the size requested from a stream producer.

```ruby
 
    workato.stream.in(input["file"], from: previous_offset, frame_size: required_frame_size) do |chunk, starting_byte_range, ending_byte_range, eof, next_starting_byte_range| 
      put("/file/#{input['file_id']}").
        headers("Content-Range": "byte #{starting_byte_range}-#{ending_byte_range}/*").
        request_body(chunk).
        presence
    end


```

See [file streaming](</developing-connectors/sdk/guides/building-actions/streaming.html>) for more information.

* * *

## [#](<#strip>) strip

Strip white spaces from the beginning and the end of string.
```ruby
 
    "    This is an example   ".strip #"This is an example"


```

See [strip (opens new window)](<https://apidock.com/ruby/String/strip>) method definition.

* * *

## [#](<#strip-tags>) strip_tags

Strip html tags from the string.
```ruby
 
    "<html><body>Double bubble</body></html>".strip_tags #"Double bubble"


```

* * *

## [#](<#strftime>) strftime

Format date or time using %-placeholders.

* * *

## [#](<#sub>) sub

Substitute the first occurrence of a pattern with value.
```ruby
 
    "Mean Marie".sub(/M/, "J") #"Jean Marie"
    "Hello".sub(/[aeiou]/, "\*") #"H*llo"


```

* * *

## [#](<#suspend>) suspend

This method is used in [Wait for resume actions](</developing-connectors/sdk/guides/building-actions/wait-for-resume-actions.html>). These actions work with external systems that can send an API request when a long running process is complete. Calling this method suspends the job until Workato receives a corresponding request to its developer API, or until the specified suspension time expires.
```ruby
 
    suspend(
      continue: { 
        "state" => "suspended", 
        "url" => input['url']
      }, 
      expires_at: 10.minutes.from_now
    )


```

  * `continue`: This hash is passed to the `before_suspend`, `before_resume`, and `before_timeout_resume` lambdas.
  * `expires_at`: This is the time in PST that the job waits for a request to resume. After this time, the job continues with a `timeout` call. The maximum timeout is 60 days.

* * *

## [#](<#take>) take

Returns first N elements from an array.
```ruby
 
    [1, 2, 3, 4, 5, 0].take(3) #=> [1, 2, 3]


```

See [take (opens new window)](<https://apidock.com/ruby/v2_5_5/Enumerable/take>) method definition.

* * *

## [#](<#take-while>) take_while

Passes elements to the block until the block returns nil or false, then stops iterating and returns an array of all prior elements.
```ruby
 
    [1, 2, 3, 4, 5, 0].take_while { |i| i < 3 } #=> [1, 2]


```

See [take_while (opens new window)](<https://apidock.com/ruby/Array/take_while>) method definition.

* * *

## [#](<#tap>) tap

Yields x to the block, and then returns x.

The `tap` method is often used for transformation. For example, we can use the `tap` method to transform a webhook's payload. Consider the following example:
```ruby
 
    {
      "id" => {"value" => 1},
      "name" => {"value" => 2}
    }


```

If a webhook payload is delivered in this format, you can use `tap` to transform it into a more user friendly JSON.
```ruby
 
    webhook_notification: lambda do |input, payload|
      payload.tap do |output|
        output.each { |k, v| output[k] = v["value"] }
      end
    end


```

The final JSON will look as follows: `{"id"=>1, "name"=>2}`

See [tap (opens new window)](<https://apidock.com/ruby/Object/tap>) method definition.

* * *

## [#](<#tls-client-cert>) tls_client_cert

Allows you to dictate the TLS keys, TLS client, and intermediate certificates to be used in the request. Can be used by chaining it in a single request or used generally in the apply block.
```ruby
 
    get("https://www.exampleapi.com").
      tls_client_cert(
        certificate: connection['ssl_client_cert'],
        key: connection['ssl_client_key'],
        passphrase: connection['ssl_key_passphrase'],
        intermediates: connection['client_intermediate_certs'] # pass array if there are multiple intermediate certs
      )


```
```ruby

    apply: lambda do |connection|
      tls_client_cert(
        certificate: connection['ssl_client_cert'],
        key: connection['ssl_client_key'],
        passphrase: connection['ssl_key_passphrase'],
        intermediates: connection['client_intermediate_certs'] # pass array if there are multiple intermediate certs
      )
    end


```

* * *

## [#](<#tls-server-certs>) tls_server_certs

Allows you to dictate the TLS server certificates we should accept during the SSL handshake process. This is useful for self-signed or untrusted root CA certificates. Can be used by chaining it in a single request or used generally in the apply block.
```ruby
 
    get("https://www.exampleapi.com").
      tls_server_certs(
        certificates: [connection['server_ca_cert']], #additional intermediate server certificates can be given.
        strict: false # Set to true to only allow requests from the given server CA cert.
      )


```
```ruby

    apply: lambda do |connection|
      tls_server_certs(
        certificates: [connection['server_ca_cert']], #additional intermediate server certificates can be given.
        strict: false # Set to true to only allow requests from the given server CA cert.
      )
    end


```

* * *

## [#](<#to-currency>) to_currency

Convert to currency string.
```ruby
 
    1234567890.50.to_currency    # $1,234,567,890.50


```

* * *

## [#](<#to-currency-code>) to_currency_code

Convert alpha-2/3 country code or country name to ISO4217 currency code.
```ruby
 
    "India".to_currency_code #INR


```

* * *

## [#](<#to-currency-name>) to_currency_name

Convert alpha-2/3 country code or country name to ISO4217 currency name.
```ruby
 
    "India".to_currency_name #Rupees


```

* * *

## [#](<#to-currency-symbol>) to_currency_symbol

Convert alpha-2/3 country code or country name to ISO4217 currency symbol.
```ruby
 
    "India".to_currency_symbol # ₨


```

* * *

## [#](<#to-country-alpha2>) to_country_alpha2

Convert alpha-3 country code or country name to alpha2 country code.
```ruby
 
    "India".to_country_alpha2 #IN
    "IND".to_country_alpha2 #IN


```

* * *

## [#](<#to-country-alpha3>) to_country_alpha3

Convert alpha-2 country code or country name to alpha3 country code.
```ruby
 
    "Australia".to_country_alpha2 #AUS
    "AU".to_country_alpha2 #AUS


```

* * *

## [#](<#to-country-name>) to_country_name

Convert alpha-2/3 country code or country name to ISO3166 country name.
```ruby
 
    "GB".to_country_name #United Kingdom
    "GBR".to_country_name #United Kingdom


```

* * *

## [#](<#to-country-number>) to_country_number

Convert alpha-2/3 country code or country name to ISO3166 country numeric code.
```ruby
 
    "India".to_country_number #356


```

* * *

## [#](<#to-date>) to_date

Convert string or timestamp to date. Can be formatted.
```ruby
 
    "12/24/2014 10:30 PM".to_date(format: "MM/DD/YYYY")


```

* * *

## [#](<#to-f>) to_f

Convert to float. Numbers are rounded up or down according to regular rounding rules.
```ruby
 
    45.to_f #45.0


```

* * *

## [#](<#to-hex>) to_hex

Converts binary string to its hex representation.

* * *

## [#](<#to-i>) to_i

Convert to integer. Decimals are always rounded down.
```ruby
 
    45.67.to_i #45


```

* * *

## [#](<#to-json>) to_json

Converts hash or array into JSON string.
```ruby
 
    {"a" => "c d", "2" => "3"}.to_json #"{"a":"c d","2":"3"}"


```

* * *

## [#](<#to-phone>) to_phone

Convert string or number to a formatted phone number.
```ruby
 
    5551234.to_phone # 555-1234
    1235551234.to_phone(area_code: true) # (123) 555-1234
    1235551234.to_phone(delimiter: " ") # 123 555 1234
    1235551234.to_phone(country_code: 1) # +1-123-555-1234


```

* * *

## [#](<#to-param>) to_param

Returns a string representation for use as a URL query string.
```ruby
 
    {name: 'Jake', age: '22'}.to_param #name=Jake&age=22


```

* * *

## [#](<#to-s>) to_s

Convert to string.
```ruby
 
    45.67.to_s #"45.67"


```

* * *

## [#](<#to-state-code>) to_state_code

Convert state name to code.
```ruby
 
    "California".to_state_code #CA


```

* * *

## [#](<#to-state-name>) to_state_name

Convert state code to name.
```ruby
 
    "CA".to_state_name #"CALIFORNIA"


```

* * *

## [#](<#to-time>) to_time

Convert string or date to timestamp.
```ruby
 
    "2014-11-21".to_time #2014-11-21 00:00:00 +0000


```

* * *

## [#](<#to-xml>) to_xml

Converts hash or array into XML string.
```ruby
 
    {"name" => "Ken"}.to_xml(root: "user") # &#60;user&#62;&#60;name&#62;Ken&#60;/name&#62;&#60;/user&#62;


```

* * *

## [#](<#today>) today

Date today. Returns the date of the moment that the formula was executed, in Pacific time (UTC-8/UTC-7).
```ruby
 
    today #2016-07-13
    today + 2.days #2016-07-15


```

* * *

## [#](<#transliterate>) transliterate

Replaces non-ASCII characters with an ASCII approximation, or if none exists, a replacement character which defaults to '?'.
```ruby
 
    'Chloé'.transliterate #Chloe


```

* * *

## [#](<#upcase>) upcase

Convert string to upper case.
```ruby
 
    "Convert to UPCASE".upcase #"CONVERT TO UPCASE"


```

* * *

## [#](<#uniq>) uniq

Return unique items in an array.
```ruby
 
    [1.0, 1.5, 1.0].uniq #[1.0, 1.5]


```

* * *

## [#](<#unpack>) unpack

Decodes a string into an array.

See [unpack (opens new window)](<https://apidock.com/ruby/String/unpack>) method definition.

* * *

## [#](<#utc>) utc

Convert Time to UTC timezone.

See [utc (opens new window)](<http://ruby-doc.org/core-2.2.0/Time.html#method-c-utc>) method definition.

* * *

## [#](<#uuid>) uuid

Creates a UUID. Useful when sending strings that are unique in a request.
```ruby
 
    workato.uuid #c52d735a-aee4-4d44-ba1e-bcfa3734f553 => "eyJhbGciO..."


```

* * *

## [#](<#wday>) wday

Returns day of the week where 1 is Monday.

* * *

## [#](<#where>) where

Filter array by given condition.

* * *

## [#](<#while>) while

While loop statement.

See [ruby_loops (opens new window)](<https://www.tutorialspoint.com/ruby/ruby_loops.htm>) method definition.

* * *

## [#](<#wrap>) wrap

Wraps its argument in an array unless it is already an array

The wrap method is often used in the execute block of the while loop statement.
```ruby
 
    execute: lambda do |connection, input|
    {
        accounts: Array.wrap(get("/accounts", input)["records"])
      }
    end


```

This ensures that the `accounts` variable is always an array in spite of whatever return. At Workato, we often use this to guard against unexpected returns from the various APIs we work with.

See [wrap (opens new window)](<https://apidock.com/rails/Array/wrap/class>) method definition.

* * *

## [#](<#yday>) yday

Returns day of the year.
```ruby
 
    "2016-07-19 10:45:30".to_time.yday #201


```

* * *

## [#](<#yweek>) yweek

Returns week of the year.
```ruby
 
    "2016-07-19 10:45:30".to_time.yweek #29


```

* * *

## [#](<#zip>) zip

Used as a method called by arrays. Converts any arguments to arrays, then merges elements of self with corresponding elements from each argument.

See [zip (opens new window)](<https://apidock.com/ruby/Array/zip>) method definition.
