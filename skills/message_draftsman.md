# Referral Message Generation Skill

## Purpose

Generate **two personalized LinkedIn messages** for every selected contact:

1. **Referral Message** — for a person who is already a LinkedIn connection.
2. **Connection Note** — a short note sent with a LinkedIn connection request.

The goal is to make the recipient's decision as easy as possible.

The recipient should **not have to research the role, figure out the user's background, write an introduction, or ask for basic information**.

The message should provide:

* The exact role
* The job URL or job ID
* Exactly two specific reasons why the user fits
* Enough context to understand why the contact was selected
* A clear but low-pressure referral request

This skill only **drafts messages**.

It must never send messages, connection requests, emails, or referrals automatically.

---

# Core Principle

Follow this principle:

> **AI researches. AI prepares. Human verifies and sends.**

A referral uses another person's credibility.

Therefore, optimize for making the referral a **30-second decision**, not for making the user sound impressive.

The recipient should be able to understand:

1. Which exact role the user wants.
2. Why the user is a reasonable fit.
3. Why the user contacted them.
4. What the user is asking for.

Do not make the recipient do additional work to figure these things out.

---

# Inputs

The skill receives:

## 1. Job

* Company
* Job title
* Job description
* Job URL
* Job ID if available
* Relevant requirements
* Match score
* Matching reasons
* Potential gaps

The **exact job URL should be preferred over only mentioning the company or job title**.

If a job ID is available and useful, it may also be included.

Never invent a job URL or job ID.

---

## 2. User Profile

Read `USER.md`.

Relevant information may include:

* Years of experience
* Primary technologies
* Relevant projects
* Domain experience
* Significant achievements
* Location
* Other experience relevant to the specific role

Only use information that is actually present in `USER.md`.

Never invent experience, responsibilities, achievements, technologies, or results.

---

## 3. Contact

* Name
* Current title
* Company
* Team/department if available
* Technical background
* Profile URL
* Reason the contact was selected
* Referral potential
* Confidence

Do not claim the contact works on a specific team unless this is reasonably established.

---

# Message Types

Generate **both** message types for every contact.

---

# Message 1: Referral Message

This message is intended for someone who is **already a LinkedIn connection**.

## Objective

Make it possible for the recipient to decide whether to refer the user without needing additional research.

The message should contain:

1. Personal greeting
2. Exact role being targeted
3. Job URL or job ID
4. Why the user is contacting this person
5. Exactly **two specific reasons** why the user's background fits
6. Clear referral request
7. Low-pressure permission to decline
8. Resume mention

---

## Referral Message Length

Target approximately:

**60–100 words**

Do not force the message to be exactly a particular length.

Clarity and natural language are more important than hitting a word count.

---

# Job Reference Rule

Always provide the **exact role link** when a valid job URL is available.

Prefer:

> "I came across this Senior Ruby Engineer role: [URL]"

Instead of:

> "I saw that [Company] is hiring."

The recipient should not have to search the company's careers page.

If the job URL is unavailable but a job ID exists, use the job ID.

If neither is available, mention the exact job title and company without inventing a link.

---

# Exactly Two Fit Points

The referral message must contain **exactly two specific reasons** why the user fits the role.

Choose the two strongest and most relevant points from `USER.md` and the job description.

Good examples:

* 4+ years of Ruby on Rails experience
* Payment-system experience
* Building and operating Rails microservices
* PostgreSQL/Redis experience
* Relevant React experience
* Relevant Java/Spring Boot experience
* Experience building a service from scratch

Do not list five or six technologies.

Do not simply copy keywords from the job description.

The two points must represent **real evidence of fit**.

---

# Resume Rule

Assume the user can attach their resume when sending the message.

Prefer wording such as:

> "I've attached my resume for context."

or:

> "I've attached my resume if helpful."

Do not ask the recipient to request the resume if it can already be attached.

The goal is to eliminate unnecessary back-and-forth.

---

# Referral Request

Use a clear but low-pressure request.

Preferred style:

> "If you're comfortable referring me, I'd appreciate it. No problem at all if you'd rather not."

Other natural variations are allowed.

The message should make it easy for the recipient to say no.

Never use demanding language such as:

> "Please refer me."

> "Can you refer me ASAP?"

> "I really need a referral."

Do not use guilt, pressure, or emotional manipulation.

---

# Referral Message Structure

Prefer this general structure:

```text
Hi [Name],

I came across this [Exact Role] role at [Company]: [Job URL]

[Brief reason for contacting this person.]

I'm a [relevant experience] and I think I could be a fit because:
1. [Specific fit point]
2. [Specific fit point]

I've attached my resume for context. If you're comfortable referring me, I'd appreciate it. No problem at all if you'd rather not.

Thanks!
```

The exact wording should vary naturally depending on the contact.

Do not make every message follow the exact same sentence structure.

---

# Message 2: Connection Note

This message is intended for a person who is **not yet a LinkedIn connection**.

## Objective

The connection note has a different purpose from the referral message.

Its primary goal is:

**Get the connection accepted while establishing a legitimate reason for contacting the person.**

Do not attempt to fit the entire referral request into the connection note.

---

# Connection Note Character Limit

The connection note must be:

**300 characters or fewer.**

This is a hard limit.

Before returning the message, count the characters.

If the message exceeds 300 characters, rewrite it until it is within the limit.

Target approximately:

**220–280 characters**

when possible.

Do not sacrifice clarity just to use all 300 characters.

---

# Connection Note Content

Prefer including:

1. Person's name
2. Exact role
3. One strong reason for fit
4. Relevant reason for contacting this person
5. Short connection request

Example:

> Hi Rahul, I’m a Ruby on Rails developer with 4+ years of experience in payment systems and microservices. I came across the Senior Ruby Engineer role at [Company] and noticed your Rails/backend background. Would be great to connect.

The connection note does **not** need to contain:

* The full referral request
* All two fit points
* A long introduction
* The complete job description
* Excessive praise

If the job URL cannot fit naturally, prioritize the exact role and concise context.

If a short job URL is available, it may be included only if doing so keeps the note natural and under 300 characters.

---

# Connection Note Rules

The connection note must:

* Be ≤300 characters
* Sound human
* Clearly explain why the user wants to connect
* Reference the relevant role when possible
* Include genuine personalization
* Avoid sounding like mass outreach

Do not write:

> "Hi, I am looking for opportunities. Please connect."

Do not write:

> "Hi, I came across your amazing profile and would love to connect with you."

Do not write generic networking messages unrelated to the target job.

---

# Personalization

Every message must contain **at least one genuine connection** between:

* The contact
* The target job
* The user's experience

Examples:

* Contact is a Rails engineer and the job is a Rails role.
* Contact works in backend engineering and the job is a backend role.
* Contact appears to work in the relevant engineering organization.
* User's payment-system experience aligns with the target role.
* User and contact share Ruby/Rails/backend experience.

Personalization must be based on available evidence.

Never fabricate:

* A shared team
* A previous interaction
* A mutual connection
* A reporting relationship
* Knowledge of the contact's work that is not supported by available information

---

# Contact-Specific Personalization

## Engineering Manager

Focus on:

* Relevant engineering experience
* Role alignment
* Domain experience
* Ability to contribute to the relevant team

Example style:

> "I noticed you're working in engineering at [Company], so I wanted to reach out about this role..."

Do not claim they are the hiring manager unless that is established.

---

## Senior/Staff/Principal/Lead Rails Engineer

Focus on:

* Shared Ruby/Rails background
* Backend engineering
* Relevant systems
* Technical overlap

Example style:

> "I noticed your Ruby/backend background at [Company], so I thought I'd reach out about this role..."

---

## Technical Recruiter / Talent Acquisition

Focus on:

* Exact role
* Relevant experience
* Two strongest qualifications
* Clear interest in the role

Do not pretend to have a technical connection with the recruiter.

---

# Style

Messages should be:

* Concise
* Natural
* Professional
* Direct
* Respectful
* Personalized
* Easy to read
* Low-pressure

Write like a developer reaching out to another professional.

Do not write like a marketing email.

Do not optimize for sounding impressive.

Optimize for **clarity + credibility + low effort for the recipient**.

---

# Avoid

Do NOT use:

* Excessive flattery
* "I'm a huge fan of your work"
* "I've been following your amazing journey"
* Generic corporate language
* Long career summaries
* Excessive technical jargon
* Fake familiarity
* Overly formal language
* Obviously AI-generated phrasing
* Unverified claims
* Emotional pressure
* Guilt
* Repeated requests
* Long lists of technologies
* Generic "Are there any opportunities?" messages

Do not mention every technology in `USER.md`.

Select only the strongest evidence relevant to the specific job.

---

# Two-Point Fit Selection

Before drafting the referral message:

1. Compare the job requirements with `USER.md`.
2. Identify the strongest areas of genuine overlap.
3. Select exactly **two**.
4. Prefer concrete experience over generic skills.

For example:

Instead of:

> "I have experience with Ruby, Rails, PostgreSQL, Redis, React, APIs and microservices."

Prefer:

> "I have 4+ years of Ruby on Rails experience and have worked on payment systems and Rails microservices."

The second version is easier to understand and more credible.

---

# No Recipient Work Rule

The recipient should not have to:

* Search for the job
* Find the job posting
* Ask what role the user wants
* Ask for the user's resume
* Figure out why the user is qualified
* Write the user's introduction
* Ask which team the role belongs to
* Research the user's background

Provide the relevant information upfront.

---

# Low-Pressure Rule

The message should preserve the relationship even if the person declines.

Use language that gives the recipient an easy way to say no.

Preferred:

> "If you're comfortable referring me, I'd appreciate it. No problem at all if you'd rather not."

Do not repeatedly follow up aggressively.

A respectful decline should not be treated as rejection of the relationship.

---

# Personalization Quality Check

Before producing the messages, verify:

1. Is the company correct?
2. Is the exact job title correct?
3. Is the contact's name correct?
4. Is the contact's current role correctly represented?
5. Are all claims about the user supported by `USER.md`?
6. Is there a genuine reason for contacting this person?
7. Does the referral message contain the exact job URL or job ID when available?
8. Does the referral message contain exactly two specific fit points?
9. Is the resume mentioned?
10. Is the referral request explicit but low-pressure?
11. Does the connection note have a legitimate reason for connecting?
12. Is the connection note ≤300 characters?
13. Do both messages sound natural?
14. Are there any fabricated claims?
15. Does the message avoid unnecessary flattery and corporate language?

If important information is unavailable, simplify the message rather than guessing.

---

# Output

Return:

```json
{
  "contact": "Jane Doe",

  "referral_message": "Hi Jane, I came across this Senior Ruby Engineer role at Example Corp: [JOB_URL]. I noticed your backend/Rails background there, so I wanted to reach out. I have 4+ years of Ruby on Rails experience and have worked on payment systems and Rails microservices. I've attached my resume for context. If you're comfortable referring me, I'd appreciate it. No problem at all if you'd rather not. Thanks!",

  "connection_note": "Hi Jane, I’m a Ruby on Rails developer with 4+ years of experience in payment systems and microservices. I came across the Senior Ruby Engineer role at Example Corp and noticed your Rails/backend background. Would be great to connect.",

  "connection_note_character_count": 257,

  "personalization_points": [
    "Contact has relevant Rails/backend background",
    "User has 4+ years of Ruby on Rails experience",
    "User has payment-system and microservices experience"
  ]
}
```

The `connection_note_character_count` must reflect the actual character count of the generated connection note.

---

# Database Output

Record **ALL drafted messages** in `jobs.db`, table `contacts`.

Write both generated messages into the existing contact row:

* `contacts.generated_message` → referral message
* Add/update the connection-note field **only if an existing connection-note column already exists**

Do **not** create a new table.

If the database currently has no column for the connection note, do not silently alter the schema.

Instead, report that the database schema needs a migration/additional column, for example:

```text
connection_note
```

The job's match strength is already in `jobs.score`; read it via the `job_id` join when reporting.

Do not duplicate the job score inside each message.

After drafting, set:

```text
contacts.referral_status = "message_drafted"
```

---

# Important Rule

**Never optimize for sounding impressive. Optimize for making the recipient's decision easy.**

The recipient should be able to understand the exact role, see two credible reasons for the user's fit, access the job, see the resume, and decide whether to refer — without doing additional work.

The final messages must always be reviewed and manually sent by the user.
