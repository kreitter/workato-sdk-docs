# Workato SDK Documentation

> **Source**: https://docs.workato.com/en/developing-connectors/sdk/limits.html
> **Fetched**: 2026-01-18T02:50:16.781584

---

# [#](<#connector-sdk-limits>) Connector SDK limits

Description |  Limit   
---|---  
Maximum number of SDK/custom connectors in one workspace| 150  
Timeout for HTTP request inside SDK connectors in the Test code console| 40 seconds  
Timeout for HTTP request inside SDK connectors in a job at runtime| 3 minutes  
Timeout for compiling an SDK connector| 5 seconds  
SDK Timeout credentials refresh| 30 seconds  
Maximum number of swap outs in multi-step actions| 100  
Minimum swap interval in multi-step actions| 60 seconds  
Maximum number of job suspensions| 50  
[Maximum consecutive polling without any jobs produced](</developing-connectors/sdk/guides/trigger-limit.html#consecutive-polls-in-a-single-poll-cycle-without-jobs>)| 600  
[Maximum number of events in a single poll](</developing-connectors/sdk/guides/trigger-limit.html#number-of-events-per-poll>)| 1,000  
Maximum data allowed in custom connector code| 10 MB  
Compatible code formats| UTF-8 and JSON compatible  

FURTHER READING

  * Refer to the [SDK trigger polling limits](</developing-connectors/sdk/guides/trigger-limit.html>) documentation for more information on SDK polling trigger limits.
  * Refer to the [Platform limits](</limits.html>) documentation for more information about Workato limits.
