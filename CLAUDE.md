# Portfolio Site — Claude Code Guide

## Stack
Plain HTML/CSS/vanilla JS. No frameworks, no build tools, no npm.

## File structure
```
portfolio-site/
├── index.html          # Homepage (shows all projects)
├── projects.html       # Projects listing
├── about.html          # About + CV (merged)
├── style.css           # Single stylesheet — all styles live here
├── lightbox.js         # Lightbox for project page images
└── assets/
    ├── Joseph Martin CV March 2026.pdf
    └── projects/
        └── <Project Name>/   # One folder per project
            ├── <page>.html   # Project detail page
            └── <images>
```

## Path conventions — CRITICAL

Project pages are three levels deep from root (`assets/projects/<name>/`). Always use `../../../` to reach root-level files:

```html
<link rel="stylesheet" href="../../../style.css" />
<script src="../../../lightbox.js"></script>
<a href="../../../index.html">Joseph Martin</a>
<a href="../../../projects.html">Projects</a>
```

Using `../../` is a **common bug** — it resolves to `assets/style.css` which doesn't exist. VS Code Live Server returns index.html for 404s, which browsers reject as a stylesheet (wrong MIME type), making pages render as raw text.

## Nav

Every page shares the same nav. Active page uses `aria-current="page"`. CV is embedded at the bottom of about.html — there is no separate CV nav link.

```html
<nav>
  <div class="container">
    <a class="nav-brand" href="index.html">Joseph Martin</a>
    <ul class="nav-links">
      <li class="nav-dropdown">
        <a href="projects.html">Projects</a>
        <ul class="dropdown-menu">
          <li><a href="assets/projects/Nixie%20speakers/nixie-speakers.html">Nixie Tube Speakers</a></li>
          <li><a href="assets/projects/Speaker%20project%202/3d-speakers.html">3D-Printed Speakers</a></li>
          <li><a href="assets/projects/Fitnessinsights/fitness_portfolio.html">Fitness Insights</a></li>
          <li><a href="assets/projects/knotpulse/index.html">KnotPulse</a></li>
          <li><a href="assets/projects/TechConnect/Sitedemo.html">TechConnect</a></li>
          <li class="dropdown-divider"></li>
          <li><a href="assets/projects/Multi%20agent%20eval%20arena/multi-agent-arena.html">Multi Agent Arena</a></li>
          <li><a href="assets/projects/red%20team%20sim/red-team-sim.html">LLM Red-Teaming</a></li>
        </ul>
      </li>
      <li><a href="about.html">About</a></li>
    </ul>
  </div>
</nav>
```

Active page uses `aria-current="page"` on the relevant link. The brand name links home — no separate "Home" nav item.

For project pages (three levels deep), prefix all hrefs with `../../../`. When adding a new project, update the dropdown list on **all** pages.

For project pages (three levels deep), all hrefs need `../../../` prefix.

## Footer

```html
<footer>
  <div class="container">
    &copy; <span id="yr"></span> Joseph Martin &mdash;
    <a href="https://www.linkedin.com/in/joseph-martin1/" target="_blank" rel="noopener">LinkedIn</a>
  </div>
</footer>
<script>document.getElementById("yr").textContent = new Date().getFullYear();</script>
```

## Images

- HEIC images must be converted to JPEG before use:
  `sips -s format jpeg "$f" --out "${f%.HEIC}.jpg"`
- Use URL-encoded paths in HTML: spaces → `%20`
- Gallery images: use `<img class="gallery-img" ...>` (lightbox picks these up via lightbox.js)

## Project pages

### Existing projects
| Project | Folder | Page |
|---|---|---|
| Nixie Tube Speakers | `assets/projects/Nixie speakers/` | `nixie-speakers.html` |
| 3D-Printed Speakers | `assets/projects/Speaker project 2/` | `3d-speakers.html` |
| Multi Agent Arena | `assets/projects/Multi agent eval arena/` | `multi-agent-arena.html` |
| Red Team Sim | `assets/projects/red team sim/` | `red-team-sim.html` |
| KnotPulse | `assets/projects/knotpulse/` | `index.html` |
| FitnessInsights | `assets/projects/Fitnessinsights/` | `fitness_portfolio.html` |
| TechConnect | `assets/projects/TechConnect/` | `Sitedemo.html` |

### KnotPulse & FitnessInsights
These were exported from AI tools (Tailwind-based). They have a portfolio nav added inline at the top using pure inline styles — do **not** load style.css on them as it conflicts with Tailwind.

### Red team sim & multi-agent arena
Use `style.css` for styling. Key CSS classes:
- `.project-body` — main content wrapper
- `.project-body h3` — section headers
- `.project-callout` — highlighted callout boxes
- `.sp-omegacore` / `.sp-agent4` / `.sp-nexusprime` / `.sp-apexsingularity` — speaker colours for dialogue logs
- `.private-label` — red badge for private channel messages
- `<details>`/`<summary>` — collapsible sections for logs/appendix

## Style notes

- Keep tone personal — this is a personal site, not a portfolio selling document
- Don't add corporate/salesy language
- Preserve the owner's voice when editing text
- `var(--muted)` for secondary text colour
- No emojis unless explicitly requested
