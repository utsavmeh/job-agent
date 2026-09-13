# Contact Identification & Ranking Skill

## Purpose

Identify the **2–3 most relevant people** at a company who could realistically help with a referral for a specific job.

This skill receives **every recorded job** from the evaluation stage, not only high-scoring ones.

It must prioritize **relevance and referral potential**, not the number of contacts found.

Do not skip a job because of `score`, `recommendation`, or a former `not_qualified` status. Research contacts for each job.

It must not contact, message, connect with, or send requests to anyone.

---

## Target

Find up to **3 high-quality contacts per company/job**.

Prefer fewer high-quality contacts over filling all three slots with weak candidates.

If only one or two genuinely relevant people can be identified, return only those people.

Still attempt research for every job. Do not leave a job unresearched because the score is below 75. If no public, non-invented people can be found after a real search, record that the job was researched and move on — never invent contacts to fill the quota.

---

# Priority Ranking

Rank potential contacts using the following hierarchy.

### Priority 1 — Hiring / Engineering Manager

Highest priority.

Look for:

* Hiring Manager
* Engineering Manager
* Engineering Director
* Team Lead
* Manager responsible for the relevant engineering team

Prefer people who appear connected to the specific role or team.

---

### Priority 2 — Senior / Staff / Principal Engineers

Look for engineers who are:

* Senior Software Engineer
* Staff Engineer
* Principal Engineer
* Lead Engineer

Prefer people working in the same technical area as the job.

For example, for a Ruby on Rails position, prioritize engineers with Ruby/Rails/backend experience.

---

### Priority 3 — Ruby/Rails Engineers

Look for:

* Ruby Developer
* Ruby on Rails Developer
* Rails Engineer
* Backend Engineer using Ruby
* Software Engineer with clear Ruby/Rails experience

Prefer engineers who appear to work on the same or a closely related team.

---

### Priority 4 — Technical Recruiters

Look for:

* Technical Recruiter
* Engineering Recruiter
* Talent Acquisition Partner
* Technical Talent Partner

Prefer recruiters associated with:

* Engineering hiring
* The relevant department
* The target location
* The specific job, when identifiable

---

### Priority 5 — Other Relevant Employees

Consider other employees only when they have a reasonable likelihood of helping with a referral.

Examples:

* Engineers in the same organization
* Technical leads
* Former/current team members
* Employees with strong technical overlap

Do not select random employees simply because they work at the company.

---

# Relevance Evaluation

Each candidate should be evaluated based on:

1. **Role relevance**
2. **Technical relevance**
3. **Team/department relevance**
4. **Connection to the target job**
5. **Potential ability to provide a referral**

Technical similarity should be particularly important for engineering positions.

For example:

```text
Target:
Senior Ruby on Rails Engineer

Contact A:
Engineering Manager — Backend Platform
Relevance: Very High

Contact B:
Staff Ruby Engineer
Relevance: Very High

Contact C:
Technical Recruiter — Engineering
Relevance: High

Contact D:
Senior Frontend Engineer
Relevance: Low
```

Prefer A/B/C over D.

---

# Information to Collect

For every selected contact, collect:

* Full name
* Current company
* Current title
* Profile URL
* Team/department if available
* Technical background
* Relevant technologies
* Relationship to the target role, if identifiable
* Referral potential
* Reason for selecting the person
* Confidence level

Example:

```json id="8c5g2n"
{
  "name": "Jane Doe",
  "company": "Example Corp",
  "title": "Senior Software Engineer",
  "profile_url": "https://...",
  "department": "Backend Engineering",
  "technical_background": [
    "Ruby",
    "Ruby on Rails",
    "PostgreSQL",
    "Microservices"
  ],
  "priority": 2,
  "referral_potential": "high",
  "reason": "Senior Rails engineer working in the same backend area as the target role.",
  "confidence": "high"
}
```

---

# Ranking

Rank contacts from strongest to weakest.

Example:

```text
1. Engineering Manager — Backend
   Priority: 1
   Referral potential: High

2. Staff Ruby Engineer
   Priority: 2
   Referral potential: High

3. Engineering Recruiter
   Priority: 4
   Referral potential: Medium/High
```

Do not automatically rank someone higher solely because they have a higher job title.

A Staff Ruby Engineer may be a better contact for a Rails role than an Engineering Director who works in an unrelated area.

---

# Verification Rules

Use publicly available information where possible.

Prefer information that confirms:

* The person currently works at the company.
* Their current role.
* Their technical background.
* Their relevance to the target job.

Do not assume that an old profile or outdated search result represents their current employment.

If current employment cannot be confidently established:

```text
confidence = "low"
```

and avoid selecting that person unless there are no better alternatives.

---

# LinkedIn

LinkedIn can be used as a source for identifying people and their profile URLs.

However:

* Do not automatically send connection requests.
* Do not automatically send messages.
* Do not modify profiles.
* Do not pretend to be the user.
* Do not bypass authentication, CAPTCHAs, or access restrictions.
* If profile information cannot be accessed reliably, use other publicly available sources where possible.

The final verification is always performed manually by the user.

---

# Output

Return up to 3 contacts per job.

```json id="b7n4qx"
{
  "job": {
    "company": "Example Corp",
    "title": "Senior Ruby on Rails Engineer"
  },
  "contacts": [
    {
      "name": "Jane Doe",
      "title": "Engineering Manager",
      "profile_url": "https://...",
      "priority": 1,
      "referral_potential": "high",
      "reason": "Likely responsible for the backend engineering team hiring for this role.",
      "confidence": "high"
    },
    {
      "name": "John Smith",
      "title": "Staff Software Engineer",
      "profile_url": "https://...",
      "priority": 2,
      "referral_potential": "high",
      "reason": "Works on Ruby/Rails backend systems at the company.",
      "confidence": "high"
    }
  ]
}
```

---

## Important Rules

* Maximum **3 contacts per job**.
* Research every recorded job. Score does not gate this skill.
* Quality over quantity.
* Never invent profile URLs or employment information.
* Never assume someone can provide a referral.
* Do not select people solely because they have a prestigious title.
* Prefer contacts with direct technical/team relevance.
* Never contact anyone automatically.
* The user must manually verify the person before sending a message.

---

# Database Output

Record **ALL contacts** in `jobs.db`, table `contacts`. Create contact rows for every job where people were found.

* Link each contact via `contacts.job_id` → `jobs.id`.
* The job's match strength lives in the existing `jobs.score` column —
  do NOT add a score column to `contacts`; join on `job_id` to read it.
* Store at minimum: `job_id, name, current_title, company, profile_url,
  priority_rank, technical_background (JSON), referral_potential_reason,
  referral_status`.
* Set `referral_status = "pending"` for newly found contacts.
* After researching a job, set `jobs.referral_research_status = "completed"`
  even if zero contacts could be found without inventing people.

