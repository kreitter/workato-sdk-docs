# Workato SDK Documentation

> **Source**: https://docs.workato.com/en/developing-connectors/sdk/guides/trigger-limit.html
> **Fetched**: 2026-01-18T02:50:14.480627

---

# [#](<#sdk-trigger-limit>) SDK trigger limits

Workato enforces specific limits on SDK triggers to optimize performance and ensure system stability. We apply limits to the following trigger processing functions:

Description |  Limit   
---|---  
[Maximum consecutive polling without any jobs produced](</developing-connectors/sdk/guides/trigger-limit.html#consecutive-polls-in-a-single-poll-cycle-without-jobs>)| 600  
[Maximum number of events in a single poll](</developing-connectors/sdk/guides/trigger-limit.html#number-of-events-per-poll>)| 1,000  

## [#](<#consecutive-polls-in-a-single-poll-cycle-without-jobs>) Consecutive polls in a single poll cycle without jobs

Without a limit, triggers can poll consecutively to retrieve valid results. The `can_poll_more` boolean attribute in the SDK trigger poll response controls this behavior. Workato enforces a limit on consecutive polls in a single poll cycle when no jobs are produced.

### [#](<#throttling-mechanism>) Throttling mechanism

Workato throttles a trigger if it polls consecutively without producing any jobs. Throttling minimizes unnecessary polling and ensures system stability. Triggers are limited to 600 consecutive polls in a single poll cycle without jobs before Workato pauses polling for 5 minutes. This threshold gradually decreases over time to 50 consecutive polls.

Workato pauses polling for 5 minutes when your trigger exceeds this limit. Polling resumes after the pause automatically and the counter continues from where it left off. Workato pauses polling again for another 5 minutes if the next poll also produces no jobs. The counter resets to zero if a poll produces jobs.

This pattern repeats until the poll cycle ends when `can_poll_more` equals false. Triggers can only poll once every 5 minutes without producing jobs after reaching the limit.

### [#](<#notification-mechanism>) Throttling notification

Workato sends email notifications automatically when a recipe is throttled. These notifications provide relevant details and keep you informed about throttled recipes.

#### [#](<#recipients>) Throttling notification recipients

Workato sends the following notifications about throttled recipes to specific recipients based on their role:

  * **Workspace admins:** notifications are sent directly to the admin of the workspace where the recipe runs.
  * **Embedded partners:** notifications are sent to the Embedded partner’s workspace email. Embedded customers do not receive these notifications.

#### [#](<#notification-details>) Throttling notification details

Workato provides notifications at two key points to keep you informed about throttled recipes. Workato sends an email that contains details about the throttling event when a recipe is throttled for the first time. This ensures you are immediately aware of any issues affecting your recipes.

Additionally, at the end of each month, Workato sends a summary email that lists all recipes throttled during that month. This email provides a comprehensive overview of throttled recipes and serves as a reminder.

## [#](<#number-of-events-per-poll>) Number of events in a single poll

Without a limit, a single poll can fetch an unbounded number of records, which can result in excessive platform load. Workato limits the number of events generated from a single poll to 1,000 in SDK connector triggers.

### [#](<#what-counts-as-a-poll-and-an-event>) What counts as a poll and an event?

A poll is one request made by the trigger to check for new data from the external system. It is a single invocation of the poll block in your SDK trigger.

An event is one record in the events array returned in the response from the poll. Workato converts each event into a job. Typically, one event creates one job.

### [#](<#use-pagination-in-your-trigger>) Use pagination in your trigger

If your external API returns more than 1,000 records, you must implement pagination in your poll logic to divide the results across multiple polls.

This is typically done by:

  * Setting an appropriate page size. For example, `request_page_size = 100`
  * Tracking an offset, timestamp, or token with the `next_poll` key
  * Setting `can_poll_more: true` to poll again immediately instead of waiting the default 5-minute interval

For example:
```ruby
 
    poll: lambda do |connection, input, closure, _eis, _eos|
      updated_since = (closure || input['since']).to_time.utc.iso8601
      request_page_size = 100

      response = get("/records/endpoint").params(
        updated_since: updated_since,
        page_size: request_page_size
      )

      next_updated_since = response['data'].last['updated_at'] unless response['data'].blank?

      {
        events: response['data'],                         # Array of jobs
        next_poll: next_updated_since,                   # Pass cursor for next poll
        can_poll_more: response['total_records'] >= request_page_size # Trigger next poll immediately
      }
    end


```

If there are 10,000 records, this configuration fetches them across 100 polls. Each poll returns up to 100 records, which generate 100 events and 100 jobs. This approach meets the 1,000-event-per-poll limit.

### [#](<#limiting-mechanism>) Limiting mechanism

Workato stops a recipe if the trigger fetches an excessive number of events in a single poll. This prevents system overload and ensures stability. Starting June 9th, 2025, triggers are limited to `1000` events in a single poll. The recipe is stopped if your trigger exceeds this limit.

### [#](<#stopped-recipe-notification>) Stopped recipe notification

Workato sends email notifications automatically when a recipe is stopped. These notifications provide relevant details and keep you informed about affected recipes.

#### [#](<#notification-recipients>) Notification recipients

Workato sends the following notifications about stopped recipes to specific recipients based on their role:

  * **Workspace admins:** notifications are sent directly to the admin of the workspace where the recipe runs.
  * **Embedded partners:** notifications are sent to the Embedded partner’s workspace email. Embedded customers do not receive these notifications.

#### [#](<#notification-details-2>) Notification details

Workato provides notifications at two key points to keep you informed about stopped recipes due to the limit.

Workato sends an email that contains information about the recipe when a recipe is stopped for the first time. This ensures you are immediately aware of issues affecting your recipe.

Additionally, Workato sends a monthly summary email listing all affected recipes. This summary gives a complete view of impacted recipes and serves as a reminder.

### [#](<#frequently-asked-questions>) Frequently asked questions

#### [#](<#does-the-limit-apply-to-total-events-over-time>) Does the limit apply to total events over time?

No. The limit applies to each individual poll, not the total number of events processed across time.

#### [#](<#what-if-my-trigger-needs-to-process-100-000-events>) What if my trigger needs to process 100,000 events?

You can process them across multiple polls. For example, use 100 polls with 1,000 events each.
