# Referral Message Generation Skill

## Purpose

Generate a short, personalized referral request based on:

* The target job description
* The user's professional profile (`USER.md`)
* The contact's current role
* The contact's technical background
* Relevant overlap between the job, user, and contact

The message should sound like something a real developer would naturally send to another professional.

This skill only **drafts messages**.

It must never send messages, connection requests, emails, or referrals automatically.

---

# Inputs

The skill receives:

### 1. Job

* Company
* Job title
* Job description
* Job URL
* Relevant requirements

### 2. User Profile

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

Never invent experience.

### 3. Contact

* Name
* Current title
* Company
* Team/department if available
* Technical background
* Profile URL
* Reason the contact was selected

---

# Personalization

The message should use **at least one genuine connection** between the contact, job, and user.

Examples:

* Contact is a Rails engineer and the job is a Rails role.
* Contact works on backend engineering and the job is a backend role.
* Contact appears to be part of the relevant engineering organization.
* User's payment/microservices experience aligns with the company's role.
* User and contact share a relevant technical area.

Do not fabricate a relationship or claim that the contact works on a specific team unless that information is reasonably established.

---

# Style

Messages should be:

* Concise
* Natural
* Professional
* Direct
* Respectful
* Personalised
* Easy to read

Target approximately **60–100 words**.

Avoid unnecessary introductions or long explanations.

The message should make the referral request clear.

---

# Avoid

Do NOT use:

* Excessive flattery
* "I'm a huge fan of your work"
* "I've been following your amazing journey"
* Generic corporate language
* Long descriptions of the user's career
* Excessive technical jargon
* Fake familiarity
* Overly formal language
* Obviously AI-generated phrasing
* Claims that cannot be verified

Do not mention every technology in the user's profile.

Only mention the **2–3 most relevant points**.

---

# Referral Request

The request should be clear but low-pressure.

Preferred language:

> "Would you be open to referring me?"

or

> "If you feel my background could be a fit, would you be open to referring me?"

Avoid demanding language such as:

> "Please refer me."

---

# Message Structure

Prefer this structure:

```text
Greeting

Why I'm contacting you / how I found the role

Relevant connection between my background and the role

Why I'm contacting this particular person

Clear referral request

Optional offer to share resume

Short closing
```

Keep the structure flexible so messages don't all sound identical.

---

# Example

For a Senior Ruby on Rails position:

> Hi [Name], I came across [Company]'s [Role] opening and noticed your backend/Rails background there. I'm a Ruby on Rails developer with 4+ years of experience, including payment systems and Rails microservices. The role looks closely aligned with my experience. If you feel my background could be a fit, would you be open to referring me? Happy to share my resume. Thanks!

---

# Contact-Specific Personalization

The message should change depending on the contact.

### Engineering Manager

Focus on:

* Relevant experience
* Role alignment
* Technical/domain experience

Example style:

> I noticed you're working in engineering at [Company]...

### Senior/Staff Rails Engineer

Focus on:

* Shared technical background
* Ruby/Rails
* Backend engineering
* Relevant systems

Example style:

> I noticed your background in Ruby/backend engineering at [Company]...

### Technical Recruiter

Focus on:

* Role
* Experience level
* Strongest relevant qualifications

Avoid pretending to have a technical connection with the recruiter.

---

# Personalization Quality Check

Before producing the message, verify:

1. Is the company correct?
2. Is the job title correct?
3. Is the contact's name correct?
4. Is the contact's role correctly represented?
5. Are all claims about the user supported by `USER.md`?
6. Does the message contain a genuine reason for contacting this person?
7. Is the referral request explicit?
8. Does the message sound natural?

If important information is unavailable, use a simpler message rather than guessing.

---

# Output

Return:

```json id="u7e3pc"
{
  "contact": "Jane Doe",
  "message": "Hi Jane, I came across Example Corp's Senior Ruby Engineer opening and noticed your backend engineering background there. I'm a Ruby on Rails developer with 4+ years of experience, including payment systems and Rails microservices. The role looks closely aligned with my experience. If you feel my background could be a fit, would you be open to referring me? Happy to share my resume. Thanks!",
  "personalization_points": [
    "Contact has backend engineering background",
    "User has relevant Rails and payment-system experience",
    "Target role is a strong technical match"
  ]
}
```

---

## Important Rule

**Never optimize for sounding impressive. Optimize for sounding like a real person who has a legitimate reason to contact this specific employee.**

The final message must always be reviewed and manually sent by the user.

---

# Database Output

Record **ALL drafted messages** in `jobs.db`, table `contacts`.

* Write the draft into the existing `contacts.generated_message` column
  for the matching (job_id, profile_url) row — do not create a new table.
* The job's match strength is already in `jobs.score`; read it via the
  `job_id` join when reporting, never duplicate it per message.
* After drafting, set `contacts.referral_status = "message_drafted"`.

