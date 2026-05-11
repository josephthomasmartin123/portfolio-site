---
name: new-project
description: Scaffold a new project on the portfolio site. Creates the assets/projects/<Name>/ folder, generates a project page from the standard template with correct ../../../ paths, optionally converts HEIC photos to JPEG, copies images into a subfolder, adds a card to projects.html and index.html, and updates the Projects dropdown on every page that has one. Use whenever the user says "new project", "scaffold a project", "add a project to the site", or similar.
---

# new-project

Scaffolds a new project on Joe's portfolio site so it shows up in the nav, on the projects grid, and as a dedicated detail page — all wired up correctly the first time.

## When to invoke

- "I want to add a new project — it's called X"
- "Scaffold a project for [X]"
- "Make me a new project page for the speakers I just built"

## Inputs to collect

If the user gives only a name, ask for the rest before writing files. In Claude Code, ask conversationally; in Cowork, use AskUserQuestion.

1. **Display name** — appears in dropdown / card title / page H1
2. **Folder slug** — defaults to display name with spaces preserved (the site uses `%20`-encoded paths, so spaces are fine and match existing convention). Confirm before creating.
3. **Page filename** — kebab-case version of the name (e.g. `vacuum-tube-amp.html`). Existing projects mix conventions; pick what fits.
4. **Category tag** — one of `hardware`, `data`, `concept`, `ai` (matches the filter buttons on `projects.html`)
5. **Card position** — does it sit above or below the dropdown's `dropdown-divider`? Convention: physical/data/concept above, AI projects below.
6. **One-line description** — for the card and the page lede.
7. **Cover image** — pick one from the project's photos, or leave a `card-image-placeholder` for now.
8. **Project meta chips** — 2-4 short `<strong>Label</strong> Value` pairs for `.project-meta` (e.g. Type / Drivers / Inspiration). Optional.

## Steps

### 1. Create folder + handle photos

```bash
mkdir -p "assets/projects/<Folder Name>/images"
# For HEIC photos, in the source folder:
for f in *.HEIC; do sips -s format jpeg "$f" --out "${f%.HEIC}.jpg"; done
# Then move JPEGs into assets/projects/<Folder Name>/images/
```

### 2. Generate the project page

Start from `templates/project-page.html` (sibling of this SKILL.md). Replace placeholders:

- `{{TITLE}}` — display name (use `&amp;` for ampersands)
- `{{LEDE}}` — one-line description
- `{{META_ROWS}}` — `<span><strong>Label</strong> Value</span>` rows, or remove the entire `.project-meta` div if none
- `{{BODY}}` — start with one `<p>` lede paragraph; sections fleshed out later (or via the `write-project` skill)
- `{{GALLERY}}` — `<figure><img class="gallery-img" src="images/<file>" alt="..." loading="lazy" /></figure>` per image, or remove the gallery block if none
- `{{DROPDOWN_ITEMS}}` — **do not hardcode**. Read the current dropdown from `index.html` (lines under `<ul class="dropdown-menu">`), prepend `../../../` to each href, append the new entry in the right position, paste into the template.

Save to `assets/projects/<Folder Name>/<page>.html`.

CRITICAL: every `href` and `src` for root-level files must use `../../../` (three levels up). `../../` is the common bug — it silently breaks because Live Server returns index.html for 404s with a stylesheet MIME mismatch.

### 3. Add card to projects.html and index.html

Insert into `.projects-grid`:

```html
<article class="card" id="<slug>" data-tag="<category>">
  <img class="card-image" src="assets/projects/<Encoded%20Folder>/images/<cover>.jpg" alt="..." />
  <!-- or, if no cover: <div class="card-image-placeholder">Interactive concept</div> -->
  <div class="card-body">
    <span class="card-tag">Hardware|Data|Concept|AI &amp; Simulation</span>
    <h2 class="card-title">{{Display Name}}</h2>
    <p class="card-desc">{{One-liner}}</p>
    <a class="card-link" href="assets/projects/<Encoded%20Folder>/<page>.html">View project &rarr;</a>
  </div>
</article>
```

Position it sensibly — group hardware together, AI together. Mirror the surrounding article structure exactly.

### 4. Update the Projects dropdown — on every page

The dropdown lives in:

- `index.html`
- `projects.html`
- `about.html`
- Every `assets/projects/*/<page>.html` that uses `style.css`

For root-level pages, add `<li><a href="assets/projects/<Encoded%20Folder>/<page>.html">Display Name</a></li>` in the right position relative to `dropdown-divider`. For project pages (three levels deep), prefix with `../../../`. Use `%20` for spaces.

The KnotPulse and FitnessInsights pages have inline-styled nav (Tailwind exports — they don't load `style.css`). Skip them for the dropdown if they don't have one, or update inline if they do — check first.

### 5. Run the audit + sync skills

After scaffolding, invoke `audit-site` to verify path correctness and dropdown consistency. Then invoke `sync-claude-md` so the project table in CLAUDE.md stays accurate.

## Style reminders

Read CLAUDE.md's "Style notes" before drafting any prose. Personal first-person register, no corporate/salesy language. Match the tone of `assets/projects/Nixie speakers/nixie-speakers.html` ("With a few weeks free after finishing university, I built this project from scratch...").
