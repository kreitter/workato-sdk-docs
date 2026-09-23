# Workato SDK Documentation

> **Source**: https://docs.workato.com/en/developing-connectors/sdk/limits.html
> **Fetched**: 2026-09-23T02:17:31.337145

---

[](<https://www.workato.com/>)/[docs](</en>)

  * [Product Updates](<https://www.workato.com/product-hub/changelog/?utm_source=docs.workato.com>)
  * [Status Page](<https://status.workato.com?utm_source=docs.workato.com>)
  * [Workato Academy](<https://academy.workato.com/?utm_source=docs.workato.com>)

  * [ English](</en/developing-connectors/sdk/limits>)
  * [ 日本語](</ja/developing-connectors/sdk/limits>)

[Get a trial](<https://www.workato.com/request_demo?utm_content=docs_nav_cta>)

[Connector SDK](</en/developing-connectors/sdk>)

Are you an LLM? You can read better optimized documentation at /en/developing-connectors/sdk/limits.md for this page in Markdown format

# Connector SDK quotas [​](<#connector-sdk-limits>)

Copy page

The Connector SDK is subject to the following quotas.

DEFAULT QUOTAS

The quotas on this page are defaults based on Workato best practices and are configured to enable optimal platform performance. Customers on Enterprise plans or above can contact their Customer Success Representative to request an extension of these quotas for their specific use cases.

Description| Quota  
---|---  
Maximum number of SDK/custom connectors in one workspace| 150  
Timeout for HTTP request inside SDK connectors in the Test code console| 40 seconds  
Timeout for HTTP request inside SDK connectors in a job at runtime| 3 minutes  
Timeout for compiling an SDK connector| 5 seconds  
SDK Timeout credentials refresh| 30 seconds  
Maximum number of swap outs in multi-step actions| 100  
Minimum swap interval in multi-step actions| 60 seconds  
Maximum number of job suspensions| 50  
[Maximum consecutive polling without any jobs produced](</en/developing-connectors/sdk/guides/trigger-limit.html#consecutive-polls-in-a-single-poll-cycle-without-jobs>)| 600  
[Maximum number of events in a single poll](</en/developing-connectors/sdk/guides/trigger-limit.html#number-of-events-per-poll>)| 1,000  
Maximum data allowed in custom connector code| 10 MB  
Compatible code formats| UTF-8 and JSON compatible  

FURTHER READING

  * Refer to the [SDK trigger polling quotas](</en/developing-connectors/sdk/guides/trigger-limit>) documentation for more information on SDK polling trigger quotas.
  * Refer to the [Platform quotas](</en/limits>) documentation for more information about Workato quotas.

**Last updated:**

Ask AI
