---
name: sync-claude-md
description: Refresh the auto-generated sections of CLAUDE.md from real filesystem state — the "Existing projects" table and the canonical dropdown snippet. Keeps CLAUDE.md from going stale as projects are added or renamed. Use whenever the user says "sync claude.md", "update claude.md", "claude.md is out of date", or after any new-project run.
---

# sync-claude-md

Regenerates the parts of `CLAUDE.md` that describe the current site state, so future agent sessions read accurate context. The rest of `CLAUDE.md` (style notes, path conventions, etc.) is hand-maintained — leave it alone.

## When to invoke

- "Sync CLAUDE.md"
- "Update CLAUDE.md with the new project"
- After every `new-project` run
- When `audit-site` reports CLAUDE.md drift

## Process

### 1. Discover current projects

Look at the dropdown in `index.html` — that's the canonical source of which projects are live and what order they're in:

```bash
awk '/dropdown-menu/,/<\/ul>/' index.html | grep -oE '<li><a href="[^"]+">[^<]+</a></li>'
```

For each entry, capture: display name, path, folder name (decoded).

### 2. Regenerate the "Existing projects" table

Replace the markdown table under `### Existing projects` in `CLAUDE.md`. Format:

```markdown
| Project | Folder | Page |
|---|---|---|
| Display Name | `assets/projects/<Folder>/` | `<page>.html` |
```

One row per project, in the order they appear in the dropdown. Group with the dropdown divider — the AI projects sit below the divider in the dropdown but in the table they can be in the same flat list (the order conveys grouping).

### 3. Regenerate the dropdown HTML snippet

Replace the `<ul class="dropdown-menu">` block under the `## Nav` section of CLAUDE.md with the actual current dropdown from `index.html` (no `../../../` prefix — the snippet in CLAUDE.md is the root-page version). Preserve the `dropdown-divider` location.

### 4. Don't touch anything else

Specifically preserve:
- Stack section
- File structure section
- Path conventions section (especially the warning about `../../`)
- Style notes
- The KnotPulse/FitnessInsights notes (they describe Tailwind-export quirks)
- The Red team sim / multi-agent arena CSS class notes

If you're not sure whether a section is hand-maintained or auto-syncable, leave it alone.

### 5. Diff before writing

Show the user a diff of CLAUDE.md changes before saving, especially if rows are being removed (could indicate a project was deleted vs the script just not finding it). Confirm before overwriting.

## Markers (optional, future-proofing)

If you want this to be foolproof, add HTML comment markers around the auto-synced sections in CLAUDE.md:

```markdown
<!-- AUTO-SYNC: project-table -->
| Project | Folder | Page |
...
<!-- /AUTO-SYNC -->
```

Then this skill only ever touches content between markers. Suggest this to the user the first time the skill runs if markers aren't already present.
