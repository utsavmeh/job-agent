# Job Discovery Skill

## Purpose

Find and extract relevant Ruby/Ruby on Rails job listings from a predefined set of job sources.

This skill is responsible **only for job discovery and extraction**.

Do not evaluate whether the job is a good match for the user, contact employees, generate referral messages, or apply for jobs. Those will be handled by separate skills.

---

## Target Sources

Only search these sources during the initial implementation:

1. Ruby on Remote
2. HireRubyDevs (https://hirerubydevs.com/)
3. jobs.rubyonrails.org
4. LinkedIn

Do not expand to other job boards unless explicitly instructed.

When possible, prefer searching the official/source website directly rather than relying on search-engine snippets.

---

## Objective

Find newly available or relevant Ruby/Ruby on Rails job listings and extract structured information from each listing.

For every job discovered, collect:

* Job title
* Company name
* Location
* Salary/compensation details
* Full job description
* Job URL
* Source website
* Date discovered
* Session id (`YYYY-MM-DD HH:MM` of the run start — identical for all jobs in one run)

If a field is unavailable, use `null` rather than guessing.

---

## Search Strategy

Use search queries and/or navigate the target websites.

Prioritize searches such as:

* Ruby on Rails
* Ruby
* Rails Developer
* Senior Ruby Developer
* Senior Ruby on Rails Developer
* Ruby Backend Engineer
* Rails Backend Engineer
* Ruby Full Stack Engineer

Do not restrict searches only to the exact phrase "Ruby on Rails". Relevant Ruby/Rails positions may use different titles.

---

## Extraction Rules

For each job:

1. Open the actual job listing whenever possible.
2. Extract the complete available job description.
3. Do not rely solely on search-result snippets.
4. Preserve the original meaning of the job description.
5. Do not invent missing information.
6. If salary is not provided, set salary to `null`.
7. If location is not provided, set location to `null`.
8. If the listing is inaccessible, mark it as `inaccessible` rather than fabricating information.

---

## Duplicate Detection

Avoid saving the same job multiple times.

Use the following priority for identifying duplicates:

1. Exact job URL
2. Source + company + job title
3. Company + job title + location

If the same job appears on multiple sources, retain the listing but mark the duplicate relationship where possible.

---

## Output Format

> **Session tracking (required):** every run is one session. At the start of
> the run resolve a session id once via `date "+%F %H:%M"` (Asia/Kolkata
> unless overridden, e.g. `2026-09-12 14:39`), reuse that exact value for
> every job in the run, store it in `jobs.session_id`, and include it in the
> output JSON below.

Return jobs in structured JSON:

```json
{
  "jobs": [
    {
      "title": "Senior Ruby on Rails Engineer",
      "company": "Example Company",
      "location": "Remote",
      "salary": "$120,000 - $150,000",
      "description": "Full job description...",
      "url": "https://example.com/job/123",
      "source": "Ruby on Remote",
      "discovered_at": "2026-09-12",
      "session_id": "2026-09-12 14:39"
    }
  ]
}
```

---

## Quality Requirements

Before returning a job, verify:

* The listing is actually a job opportunity.
* The company name is identifiable.
* The job title is identifiable.
* The URL points to the relevant listing whenever possible.
* The description belongs to that specific job.
* No information has been fabricated.

If information cannot be verified, clearly mark it as unavailable.

---

## Date Freshness Filter (Today / Yesterday Only)

Only return jobs posted **today or yesterday**, computed dynamically
at run time — never hardcode calendar dates.

* At the start of every run, resolve the run date as the current local
  date (`date +%F`, Asia/Kolkata unless the user overrides it).
  `today` = run date, `yesterday` = run date minus 1 day.
* Keep a job only when its posted/published date is today or yesterday:
  - Prefer the source's explicit published date (`Published X ago`,
    `postedDate`, LinkedIn `f_TPR=r86400`-style relative timestamps).
  - Normalize relative labels at runtime: "X hours ago" / "today" →
    today; "1 day ago" / "yesterday" → yesterday. Anything older
    ("2 days ago", "28 days ago", "about 2 months ago", etc.) is out.
  - If no published date is available, fall back to `discovered_at`
    (which must equal the run date) — but never invent a posted date.
* Drop anything older than yesterday before returning results.
* Store both `discovered_at` (run date) and `posted_at` (source date or
  `null`) in the output JSON so later runs can audit the filter.

---

## Important Restrictions

This skill must **not**:

* Apply for jobs.
* Submit applications.
* Send messages.
* Contact recruiters or employees.
* Generate referral requests.
* Automatically modify LinkedIn profiles.
* Automatically send LinkedIn messages.
* Expand beyond the four approved sources without permission.

The output of this skill will be consumed by later skills responsible for job evaluation and referral research.

