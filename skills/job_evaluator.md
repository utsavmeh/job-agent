# Job Evaluation & Scoring Skill

## Purpose

Evaluate discovered Ruby/Ruby on Rails jobs against the user's professional profile and preferences.

This skill receives structured job listings from the `job_discovery` skill and determines:

* Whether the job should be rejected
* How closely the job matches the user's profile
* A score from 1–100
* Why the job is a good or poor match
* Potential skill gaps
* Whether the job should be recorded (rejected jobs are not saved; every recorded job proceeds to contact research)

This skill must **not** apply for jobs or contact anyone.

---

## Rejection Criteria

Immediately reject a job if any of the following clearly apply:

### 1. Junior / Internship

Reject:

* Internships
* Entry-level roles clearly intended for beginners
* Junior Developer roles
* Roles requiring significantly less experience than the user's 4+ years

### 2. Non-Ruby Roles

Reject roles where Ruby/Rails is not a meaningful part of the position.

Examples:

* Java-only
* Python-only
* PHP-only
* .NET-only
* Frontend-only roles

A role may still be considered if Ruby/Rails is one of the meaningful technologies in the position.

### 3. Clearly Unsuitable Compensation

If compensation is explicitly provided and is clearly below the user's target of ₹25 LPA, significantly deprioritize or reject the role.

Do **not** reject a job solely because compensation information is unavailable.

---

# Scoring

Score every non-rejected job from **1–100**.

The score should reflect how valuable the opportunity is for the user.

Start with a base score of **0** and apply the following criteria.

---

## 1. Seniority & Ruby/Rails Alignment — Maximum +30

Award up to 30 points:

* +30: Senior Ruby/Rails role with strong Rails requirements
* +25: Ruby/Rails role with senior-level responsibilities
* +20: Mid-level Ruby/Rails role with strong technical alignment
* +10: Ruby role where Rails is secondary
* +0: Ruby/Rails is only incidental

Senior Rails positions should receive the strongest score.

---

## 2. Technical Stack Overlap — Maximum +20

Evaluate overlap between the job requirements and the user's experience.

Relevant technologies include:

* PostgreSQL
* Redis
* Microservices
* React
* REST APIs
* Payment systems
* Backend engineering
* Java/Spring Boot
* AWS/cloud technologies

Award points based on meaningful overlap rather than simply counting keywords.

Example:

```text
Strong overlap:
+20

Good overlap:
+15

Moderate overlap:
+10

Limited overlap:
+5

No meaningful overlap:
+0
```

Do not award points simply because a technology appears once in the job description.

---

## 3. Location Alignment — Maximum +20

Evaluate whether the location matches the user's preferences.

* +20: Remote
* +20: India NCR / Delhi NCR
* +15: Remote within India or location-flexible India role
* +10: Other Indian location with reasonable alignment
* +5: International role with potentially relevant remote/contract arrangement
* +0: Clearly incompatible location/work arrangement

Do not assume that an international role is remote unless the job description explicitly indicates it.

---

## 4. Compensation — Maximum +15

The user's target compensation is approximately **₹25 LPA or higher**.

Award:

* +15: Explicitly ≥ ₹25 LPA or clearly equivalent
* +10: Compensation appears close to the target
* +5: Compensation is unknown
* +0: Clearly below the target

For international salaries, convert only when a reliable conversion can reasonably be made. Otherwise, preserve the original currency and explain the uncertainty.

---

## 5. Skill Gaps / Misalignment — Maximum -30

Deduct points for significant gaps.

Examples:

* Major required technology with no relevant experience
* Required experience substantially above the user's experience
* Role is heavily focused on technologies outside the user's background
* Seniority expectations significantly exceed the user's profile

Use:

* -10: Minor gap
* -20: Significant gap
* -30: Major gap / strong misalignment

Total deduction across all gaps is capped at **-30**. Count one
underlying gap once even when several signals point at it (e.g.
"15+ years" in both requirements and nice-to-have is a single
seniority gap, not two). Match short tech tokens on word boundaries
(`ror` must not match "error", `java` must not match "JavaScript").

Do not penalize the user simply because they do not have every technology listed in the job description.

---

# Score Normalization

After applying all scoring criteria:

```text
If score > 100 → score = 100
If score < 1   → score = 1
```

---

# Recommendations

Use the final score to classify the job:

### 90–100

`HIGH PRIORITY`

Excellent match. Highest priority for outreach after contacts are found.

### 75–89

`GOOD MATCH`

Worth pursuing. Still research referral contacts like every other recorded job.

### 60–74

`POSSIBLE MATCH`

Potentially useful, but should be reviewed carefully. Still research referral contacts.

### 1–59

`LOW PRIORITY`

Low priority for outreach, but still record the job and still research referral contacts.

---

# Matching Reasons

For every job scoring **75 or higher**, provide concise reasons explaining the score.

Example:

```text
Matching reasons:
- Senior Ruby on Rails position
- Strong Rails backend requirements
- PostgreSQL and Redis overlap
- Microservices experience is relevant
- Remote position
- Compensation meets target
```

---

# Potential Gaps

Identify meaningful gaps separately.

Example:

```text
Potential gaps:
- Requires Kubernetes production experience
- AWS experience is preferred
- Role expects 6+ years of experience
```

Do not describe missing technologies as gaps unless they are actually important to the role.

---

# Database Output

Record **ALL evaluated jobs** in `jobs.db`, not just qualified ones.

Use the existing `jobs.score` INTEGER column — do not create a new score field.
`jobs.score` already exists in the schema; always write the 1–100 score there.

Store at minimum:

```text
job_url
source
company
title
location
salary
description
score
recommendation
matching_reasons
potential_gaps
evaluated_at
referral_research_status
```

Set:

```text
referral_research_status = "pending"
```

for **every newly recorded job**, regardless of score. Do not use
`not_qualified` to skip contact research. Score and `recommendation`
rank the jobs; contact research still runs for all of them.

## Deduplication (No Duplicate Jobs, Ever)

Never insert a duplicate job. Before every insert, normalize and check:

1. Normalize the URL: lowercase, strip query string, fragment, and
   trailing slash (e.g. `https://x.com/jobs/1?utm=a` → `https://x.com/jobs/1`).
2. Normalize text keys: trim + lowercase company, title, location.
3. Skip the insert when ANY of these matches an existing row:
   - normalized `job_url`
   - `source` + normalized company + normalized title
   - normalized company + normalized title + normalized location
4. Write with `INSERT OR IGNORE` (or a pre-check SELECT) so reruns and
   overlapping sources can never create a second row. The DB also
   enforces this via unique indexes — treat an index conflict as
   "already recorded", never as an error to work around.
5. If the same job appears on multiple sources, keep the first row and
   ignore the later copy (optionally note the second URL in the kept
   row's notes, never as a new row).

---

# Example Output

```json id="h6m3sx"
{
  "job_url": "https://example.com/jobs/123",
  "company": "Example Corp",
  "title": "Senior Ruby on Rails Engineer",
  "score": 92,
  "recommendation": "HIGH PRIORITY",
  "matching_reasons": [
    "Senior Ruby on Rails role",
    "Strong PostgreSQL and Redis overlap",
    "Microservices experience is relevant",
    "Remote position",
    "Compensation meets the ₹28 LPA target"
  ],
  "potential_gaps": [
    "Kubernetes experience is preferred"
  ],
  "referral_research_status": "pending"
}
```

---

## Search Limits & Stopping Conditions

Each execution of this skill is a **single bounded discovery run**.

The agent must stop searching when **any one** of the following conditions is reached:

* 20 unique job listings have been collected, OR
* 10 search queries have been executed for a source, OR
* 2 pages have been checked for a search query, OR
* 10 minutes have elapsed since the discovery run started, OR
* No new jobs are being discovered from the current source.

Do not continue searching simply because more jobs might exist.

Once a stopping condition is reached:

1. Stop all further searches.
2. Deduplicate the collected jobs.
3. Return the jobs discovered during this run.
4. Clearly report which stopping condition was reached.

### Default Target

Aim to collect **10–20 unique job listings per run**.

Quality is more important than reaching 20.

If 7 good jobs are found after searching the allowed sources, return those 7 rather than continuing indefinitely to find more.

### Source Limits

Process the approved sources in order:

1. Ruby on Remote
2. Hiring Ruby Devs
3. jobs.rubyonrails.org
4. LinkedIn

Do not spend unlimited time on a single source.

For each source:

* Maximum 10 searches
* Maximum 2 pages per search
* Stop early if no new relevant jobs are found

### Never Do This

The agent must never:

* Continuously scroll/search indefinitely
* Re-run the same search repeatedly
* Search for more jobs after reaching the target
* Keep searching because the result count is below 20
* Wait indefinitely for a website
* Automatically start another discovery run after finishing

A new search should happen only when the user explicitly starts another run or an external scheduler triggers a new run.


## Important Rules

* Never fabricate salary information.
* Never assume remote eligibility.
* Never treat every keyword match as meaningful experience.
* Missing information is **not automatically a negative**.
* Distinguish between a true skill gap and a technology that is merely listed as "nice to have."
* The score is a prioritization tool, not a hiring prediction.
* Every recorded job proceeds to referral contact research. Do not skip
  contact research based on score.
