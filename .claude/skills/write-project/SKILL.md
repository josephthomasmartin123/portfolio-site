---
name: write-project
description: Draft or refine the prose body of a project page on the portfolio site, in Joe's personal first-person voice. Reads two existing project pages first to mirror tone and structure, then turns rough notes, bullet points, photos, or a half-finished page into polished sections separated by <h2> headings. Use whenever the user wants to "write up" a project, flesh out a project page, polish a draft, or turn notes into the project body.
---

# write-project

Drafts the body of a project page in Joe's voice. The site is personal, not a portfolio selling document — preserve that.

## When to invoke

- "Write up the [X] project for me"
- "Turn these notes into the project page"
- "Flesh out the body of the [X] page"
- "Polish this draft"

## Process

### 1. Calibrate the voice — always do this first

Before writing a single word, read these two pages to anchor on Joe's actual voice:

1. `assets/projects/Nixie speakers/nixie-speakers.html` — polished hardware project, calm first-person register
2. `assets/projects/Multi agent eval arena/multi-agent-arena.html` — technical AI project, more analytical but still personal

Note specifically:
- Sentences flow as paragraphs, not bullet lists
- First-person ("I built", "I came across", "While researching") is normal
- Sections are short — usually 2-4 paragraphs each — separated by `<h2>` headings
- No marketing language. No "leveraging", no "robust", no "delighted to".
- Specifics (component names, numbers, references to other people's work) carry the page; vague claims do not
- Inspirations and references to others' work are credited by name in plain prose

### 2. Read the user's inputs

The user may give you any of:
- Rough bullet-point notes
- A half-written draft
- Photos and a one-liner
- Just a topic ("the headphone amp I built last weekend")

Ask follow-ups before drafting if any of these are unclear: what was the goal, what made it interesting, what did they actually build, what worked / didn't, who or what inspired it.

Don't fill gaps with invented detail — if you don't know a spec, leave a `<!-- TODO: confirm -->` marker rather than fabricating.

### 3. Structure

Mirror the existing pattern:

- One opening paragraph in `<p>` (the "why I built this" frame). No `<h2>` above it.
- 2-4 sections, each with a short `<h2>` and 1-3 `<p>` paragraphs underneath. Section titles should be descriptive and concrete ("The speakers", "The nixie clock amplifier", "What I learned"), not generic ("Background", "Conclusion").
- For technical AI projects, callouts and collapsible logs are available — see `assets/projects/red team sim/red-team-sim.html` and `multi-agent-arena.html` for the patterns. Use sparingly.

### 4. Output

Replace the `{{BODY}}` placeholder in the page (or update the existing `.project-body` section). Don't touch the dropdown, footer, or gallery unless asked.

For long writeups, build iteratively — write one section, get feedback, write the next. Don't dump 800 words at once unless explicitly asked.

## Style cheatsheet

- `var(--muted)` is fine for secondary text colour if needed
- Avoid: "leveraged", "robust", "seamless", "delighted", "passionate about", "cutting-edge", "best-in-class"
- Prefer: concrete nouns and verbs ("driver", "cabinet", "drove", "measured", "tuned to 40Hz")
- Em dashes are used in existing copy (`—`, written as the literal character or `&mdash;`)
- No emojis unless explicitly requested
- Small voice tells from existing pages: "with a few weeks free", "while researching X I came across Y", "the result is", "the design drew heavily from"
