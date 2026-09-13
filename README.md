# job-agent

Automated Ruby on Rails job search pipeline: discover fresh postings, score them
against your profile, find referral contacts, and draft outreach — on a schedule.

## How it works

```
discover (4 boards) → today/yesterday filter → score 1–100 → dedupe → jobs.db
                                                              → contacts → referral drafts
```

1. **Scour** (`skills/job_scourer.md`) — pulls listings from jobs.rubyonrails.org,
   HireRubyDevs, LinkedIn (Ruby on Remote is Cloudflare-blocked headless).
   Only keeps jobs posted today or yesterday, computed from the run date.
2. **Evaluate** (`skills/job_evaluator.md`) — scores each job 1–100 on seniority +
   Rails alignment, stack overlap, location, compensation, minus capped skill gaps.
   75+ = GOOD MATCH, 90+ = HIGH PRIORITY. Everything is recorded, not just winners.
3. **Contacts** (`skills/contact_finder.md`) — 2–3 referral prospects per qualified
   job, ranked: hiring manager → senior/staff engineer → Rails engineer → recruiter.
   Never contacts anyone; you verify and send manually.
4. **Drafts** (`skills/message_draftsman.md`) — short personalized referral request
   per contact (60–100 words, low-pressure ask, resume offer).

## Automated runs

`run_pipeline.py` does steps 1–2 headlessly (detail-page enrichment, capped
scoring, `INSERT OR IGNORE` dedup) and prints a summary. A cron job runs it every
6 hours and posts the summary to Telegram. Contact research stays manual.

## Data

`jobs.db` (SQLite):

- `jobs` — url, source, company, title, location, salary, description, **score**,
  recommendation, matching reasons/gaps, posted/discovered dates, research status,
  embedded `contacts_json` / `messages_json`, and **`session_id`**
  (`YYYY-MM-DD HH:MM` of the run — identical for all jobs in one run).
  Unique indexes on normalized URL and company+title+location block duplicates.
- `contacts` — job link, name, title, profile URL, priority, tech background,
  referral reason, generated message, status.

## Usage

```bash
python3 run_pipeline.py        # one run, prints summary
sqlite3 jobs.db "SELECT company, title, score FROM jobs WHERE score >= 75;"
```

## Dashboard

`index.html` is a local viewer for `jobs.db` (loads it in-browser via
sql.js — nothing is uploaded). Serve the folder with the bundled server,
then open it:

```bash
python3 server.py            # then http://localhost:8000/ (file:// won't work)
python3 server.py 8080       # custom port
```

`server.py` serves the folder statically and also provides the write API:
`DELETE /api/jobs/<id>` (removes the job plus its `contacts` rows) and
`PATCH /api/jobs/<id>` with `{"applied": true|false}` (flips the `applied`
flag on the job). The 🗑 Delete icon and the ✓ Mark applied button ask for
confirmation first, then call the API and reload the DB.

> Plain `python3 -m http.server` still works for read-only viewing, but
> Delete / Mark applied need `python3 server.py` — the dashboard will tell
> you if the API is unreachable.

Stats, search, **Session filter** (one entry per agent run, newest first),
source/status/applied filters, sorting, per-job referral contacts, dark/light mode.
**Auto ↻** re-reads the DB every 30s while the agent runs; **↻ Refresh** pulls
manually. Every run must stamp `session_id` (`date "+%F %H:%M"`, same value
for all jobs in the run) — enforced by `skills/job_scourer.md`.

## Manual run (full flow, step by step)

The automated runner covers discovery + scoring only. For the complete flow
including contacts and drafts, work through the skills in order:

1. **Discover** — open each board and collect fresh postings (title, company,
   location, salary, full description from the detail page, URL, source):
   jobs.rubyonrails.org, https://hirerubydevs.com/ (try the India lander),
   LinkedIn past-24h search. Drop anything not posted today/yesterday
   (run-relative dates, never hardcoded). Save as `jobs_raw.json`.
2. **Evaluate** — score every job 1–100 per `skills/job_evaluator.md`
   (seniority/Rails fit, stack overlap, location, comp, gaps capped at -30).
   Save all results as `jobs_evaluated.json`; insert every row into `jobs`
    with `INSERT OR IGNORE` (unique indexes reject dupes). Stamp every row with
    the run's `session_id` (`date "+%F %H:%M"`). 75+ gets
   `referral_research_status = "pending"`, below 75 `"not_qualified"`.
   Once all rows are in the DB, delete `jobs_raw.json` — it's transient
   scratch, and both it and `jobs.db` are gitignored so they never pile
   up in the repo.
3. **Contacts** — for each 75+ job, find up to 3 people per
   `skills/contact_finder.md` (manager → senior/staff → Rails eng → recruiter).
   Verify current employment from public profiles; never invent URLs.
   Insert into `contacts` linked via `job_id`, status `"pending"`.
4. **Drafts** — write one 60–100 word message per contact per
   `skills/message_draftsman.md`, store in `contacts.generated_message`,
   set status `"message_drafted"`. Review, then send manually —
   nothing here ever messages anyone on its own.
5. **Verify** — `SELECT count(*) FROM jobs;` and
   `SELECT c.name, j.score FROM contacts c JOIN jobs j ON c.job_id = j.id;`
   to confirm everything landed.

## Setup (scheduler)

1. Copy the runner where the scheduler expects it:
   `cp run_pipeline.py ~/.hermes/scripts/job_pipeline.py`
   (re-copy after every edit — the schedule runs the copy).
2. Create an every-6h job delivering to your Telegram chat.
