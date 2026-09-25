# Indian Tech Internships

[![CI](https://github.com/aditya-s45/placement-interns/actions/workflows/ci.yml/badge.svg)](https://github.com/aditya-s45/placement-interns/actions/workflows/ci.yml) ![Open roles](https://img.shields.io/badge/dynamic/json?label=open%20roles&query=open_total&url=https%3A%2F%2Faditya-s45.github.io%2Fplacement-interns%2Fapi%2Fstats.json&color=2f81f7) ![Updates](https://img.shields.io/badge/updates-every%20hour-3fb950) [![RSS](https://img.shields.io/badge/RSS-subscribe-e67e22)](https://aditya-s45.github.io/placement-interns/feed.xml)

A self-updating engine that tracks tech internships so you don't have to. Instead of refreshing a dozen career pages by hand, it reads company hiring feeds directly and keeps one live list, newest roles on top, refreshed automatically throughout the day.

**0 open roles · 22 new this week · 5,064 companies tracked · updated Sep 25, 2026 at 23:16 UTC**

**⭐Star this repo⭐** to save it and get updates when new roles are added.

**Live:** [dashboard](https://aditya-s45.github.io/placement-interns/) · [RSS feed](https://aditya-s45.github.io/placement-interns/feed.xml) (instant alerts in any RSS app) · [JSON API](https://aditya-s45.github.io/placement-interns/api/jobs.json)

**🔔 New roles in your inbox:** [subscribe by email](https://aditya-s45.github.io/placement-interns/#subscribe) - one email a day, only when new internships actually appeared, one-click unsubscribe. (Prefer RSS-to-email? [Feedrabbit works too](https://feedrabbit.com/subscriptions/new?url=https%3A%2F%2Fraw.githubusercontent.com%2Faditya-s45%2Fplacement-interns%2Fmain%2Fdocs%2Ffeed.xml).)
---

_No matching roles right now, the list fills as companies post. Star it and check back._

## What this is

This is an engine, not a hand-kept list. It polls company career feeds several times a day, finds the internships, removes duplicates, and rebuilds this page on its own. Every link comes straight from the source, so it's real and current, not a stale list someone forgot to update (speed matters).

## What makes this different

- **📅 [Drop Radar](#drop-radar)** - the only list that shows **what's coming**: each marquee company's typical opening window, then confirmed with the real drop date the moment the engine catches it live.
- **Real posted dates on every role** - pulled from each job portal itself, so newest-first actually means newest.
- **Skill tags + pay, extracted** - every posting's text is scanned for the stack it wants (Python, C++, PyTorch, ...) and the pay it states - searchable on the [dashboard](https://aditya-s45.github.io/placement-interns/), included in the CSV and API.
- **Alerts your way** - [email digests](https://aditya-s45.github.io/placement-interns/#subscribe), [RSS](https://aditya-s45.github.io/placement-interns/feed.xml), or Discord - plus a [live dashboard](https://aditya-s45.github.io/placement-interns/) with search and custom filters.
- **An engine, not a spreadsheet** - polled every hour across multiple ATS platforms with full source in this repo.

## Scope

- **Roles:** Software Engineering, Data Science & Machine Learning (and closely related technical internships)
- **Region:** India
- **Cycles:** Summer 2027 and Fall 2026

## About

I built this engine to automate tracking for top-tier tech internships across India and globally remote roles. Use it to spot roles early and apply before they fill up - being first genuinely helps.

## How to use

- Roles are grouped by cycle - **newest posting on top, oldest at the bottom.**
- The **Posted** column is the date the company published the role.
- **Flags:** 🆕 = spotted in the last 48 hours.
- Track your applications with [`data/internships.csv`](data/internships.csv) (opens in Excel / Google Sheets).
- Missing a company? Adding one takes a single line, see [CONTRIBUTING.md](CONTRIBUTING.md).

---

<a id="drop-radar"></a>

## 📅 Drop Radar — when companies usually post for Summer 2027

Stop refreshing career pages. Every date here is **real or verified** — no third-party list. 🎯 = the engine **saw the drop itself** from the company's own careers API; the rest are hand-checked typical opening windows for marquee names. ✅ = already live in the list above.

> **Heads up:** companies trend *earlier* every cycle, and "~Aug" is a month, not a day. Treat "expected" as when to **start watching**, and "rolling" companies as worth checking year-round.

| Company | Typical opening | Expected this cycle | Status |
|---|---|---|---|
| Citadel | ~Aug | ~Aug · any day now | ⏳ waiting |
| Citadel Securities | ~Aug | ~Aug · any day now | ⏳ waiting |
| Databricks | ~Aug | ~Aug · any day now | ⏳ waiting |
| DoorDash | ~Aug | ~Aug · any day now | ⏳ waiting |
| DRW | ~Aug | ~Aug · any day now | ⏳ waiting |
| Google | ~Aug | ~Aug · any day now | ⏳ waiting |
| Jane Street | ~Aug | ~Aug · any day now | ⏳ waiting |
| Meta | ~Aug | ~Aug · any day now | ⏳ waiting |
| Optiver | ~Aug | ~Aug · any day now | ⏳ waiting |
| Pinterest | ~Aug | ~Aug · any day now | ⏳ waiting |
| Salesforce | ~Aug | ~Aug · any day now | ⏳ waiting |
| SIG | ~Aug | ~Aug · any day now | ⏳ waiting |
| Snowflake | ~Aug | ~Aug · any day now | ⏳ waiting |
| Uber | ~Aug | ~Aug · any day now | ⏳ waiting |
| Adobe | ~Sep | ~Sep · any day now | ⏳ waiting |
| Airbnb | ~Sep | ~Sep · any day now | ⏳ waiting |
| Bloomberg | ~Sep | ~Sep · any day now | ⏳ waiting |
| Plaid | ~Sep | ~Sep · any day now | ⏳ waiting |
| Point72 | ~Sep | ~Sep · any day now | ⏳ waiting |
| Robinhood | ~Sep | ~Sep · any day now | ⏳ waiting |
| Roblox | ~Sep | ~Sep · any day now | ⏳ waiting |
| Stripe | ~Sep | ~Sep · any day now | ⏳ waiting |
| D.E. Shaw | ~Oct | ~Oct · in ~6d | ⏳ waiting |
| Coinbase | ~Dec | ~Dec | ⏳ waiting |
| Ramp | ~Dec | ~Dec | ⏳ waiting |
| Two Sigma | ~Dec | ~Dec | ⏳ waiting |
| Apple | rolling | year-round | ⏳ waiting |
| Datadog | rolling | year-round | ⏳ waiting |
| Jump Trading | rolling | year-round | ⏳ waiting |
| Microsoft | rolling | year-round | ⏳ waiting |

_77 companies on the [full radar](https://aditya-s45.github.io/placement-interns/#radar). **43** dated from our own live observations 🎯 (this grows every cycle). "~Aug" = hand-verified typical month, not a promise of the day; "rolling" = posts year-round; "waiting" = not seen in our tracked feeds yet, not a guarantee it isn't out somewhere else._

<details>
<summary><strong>Recently closed</strong> — 40 roles taken down in the last 14 days</summary>

| Company | Role | Cycle | Closed |
|---|---|---|---|
| Biogen | Co-op, Data Science | Summer 2027 | 2026-09-25 |
| Sprinklr | ML Intern | Summer 2027 | 2026-09-25 |
| American Express | Apprentice | Summer 2027 | 2026-09-25 |
| CWAN | Software Development Intern | Summer 2027 | 2026-09-25 |
| Jones Lang LaSalle (JLL) | Apprentice | Summer 2027 | 2026-09-25 |
| Citi | Services – Summer Analyst, India, 2027 | Summer 2027 | 2026-09-25 |
| Marvell | Intern, Software Engineer | Summer 2027 | 2026-09-25 |
| Intel | AI and Compiler Engineering Graduate Intern | Summer 2027 | 2026-09-25 |
| Corteva | Data Science Intern | Summer 2027 | 2026-09-24 |
| Marvell | AI Intern | Summer 2027 | 2026-09-24 |
| State Street | Apprentice | Summer 2027 | 2026-09-24 |
| Pearson | Apprentice, Financial Operations | Summer 2027 | 2026-09-24 |
| Pearson | Apprentice, Software Engineer | Summer 2027 | 2026-09-24 |
| Dun & Bradstreet | Apprentice (R-19888) | Summer 2027 | 2026-09-24 |
| Arista Networks | Junior AI-Assisted Automation Scripting Associate (Apprentice) | Summer 2027 | 2026-09-24 |
| IGS Energy | Software Engineer Intern | Summer 2027 | 2026-09-24 |
| Amgen | Grad Intern – Data Engineer – Technology, AI & Data (Summer 2027) | Summer 2027 | 2026-09-24 |
| Amgen | Undergrad Intern – Data Engineer – Technology, AI & Data (Summer 2027) | Summer 2027 | 2026-09-24 |
| GE Aerospace | Data Science Intern | Summer 2027 | 2026-09-23 |
| Wex | Backend Software Engineer Intern - C#, Cloud Security & AI (Undergraduate) | Summer 2027 | 2026-09-23 |
| Wex | Backend Software Engineer Intern - C#/Java & AI Workflows (Undergraduate) | Summer 2027 | 2026-09-23 |
| Wex | Backend Software Engineer Intern - Java & AI (Master’s) | Summer 2027 | 2026-09-23 |
| Wex | Fullstack Software Engineer Intern (Undergraduate) | Summer 2027 | 2026-09-23 |
| Wex | DevOps & Backend Software Engineer Intern (Undergraduate) | Summer 2027 | 2026-09-23 |
| Wex | Software Engineer Intern – AI & Cloud (Graduate/Master’s) | Summer 2027 | 2026-09-23 |
| Centria Autism | Clinical Apprentice - BCBA Fieldwork Program | Summer 2027 | 2026-09-23 |
| Hearst | Software Engineering Intern | Summer 2027 | 2026-09-23 |
| American Express | Apprentice | Summer 2027 | 2026-09-23 |
| CACI | Business/Systems Analyst Intern - Summer 2027 | Summer 2027 | 2026-09-23 |
| Centene | Cybersecurity Summer 2027 Intern (Undergraduate) | Summer 2027 | 2026-09-23 |
| Wex | Data & AI Intern (Graduate/Master’s) | Summer 2027 | 2026-09-23 |
| Wex | DevOps & AI Engineering Intern (Undergraduate) | Summer 2027 | 2026-09-23 |
| Ixigo | Full-Stack Intern - B2B | Summer 2027 | 2026-09-23 |
| First American | Software Engineering Intern - Remote | Summer 2027 | 2026-09-22 |
| Philips | Intern – Data Science and AI Engineering | Summer 2027 | 2026-09-22 |
| Amazon | Financial Analyst Intern, Ops FP&A | Summer 2027 | 2026-09-22 |
| Chemours | Data Visualization Analyst Summer Intern | Summer 2027 | 2026-09-21 |
| S&P Global | Apprentice | Summer 2027 | 2026-09-21 |
| Twilio | Software Engineer Intern (January 12th start, 23 weeks) | Summer 2027 | 2026-09-21 |
| Deutsche Bank | Apprentice Hiring for 2026- 2027 | Summer 2027 | 2026-09-21 |

</details>

---

## Hiring timeline

Internships posted per week, from each role's real published date - redrawn automatically on every run. When this line takes off, recruiting season is open:

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/trends-dark.svg">
  <img alt="Internships posted per week, drawn from real published dates" src="docs/trends-light.svg">
</picture>

## How it stays current

A small Python engine reads public company hiring feeds directly, keeps the roles that match the scope above, de-duplicates across sources, records each role's published date once (so it never shifts), and regenerates this page through GitHub Actions. It polls every company concurrently (async) with retry/backoff and per-host rate limits. The full source is in this repo.

_Engine (last run): 5,065 companies across 25 ATS platforms · 98% fetch success · completed in 265.1s._

## Platforms Scraped

The engine currently extracts live data from the following platforms:
- **Direct ATS (Applicant Tracking Systems):** Greenhouse, Lever, Ashby, SmartRecruiters, Workable
- **Aggregators:** Instahyre

## Contributing

Adding a company takes one line, see [CONTRIBUTING.md](CONTRIBUTING.md). Suggestions and pull requests are welcome.

## Note on dates

The **Posted** column shows when a role was published, with the newest at the top. I pull the posting date straight from each job portal, but a lot of them don't expose one publicly, so those rows show a dash (—) for now instead of a guessed date. The ones that do publish a date are dated. Know the real date for a dashed role? Open a PR and I'll merge it.

Roles can close at any time, so always confirm on the company's own site before applying.
