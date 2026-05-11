---
name: audit-site
description: Audit the portfolio site for consistency drift. Checks ../../../ path correctness on every project page, dropdown completeness across pages, broken image refs, leftover HEIC files that should be JPEG, and nav/footer drift. Reports a punch list. Use whenever the user says "audit the site", "check for broken stuff", "is everything consistent", or after running new-project.
---

# audit-site

Runs a consistency sweep over the portfolio site and reports what's drifted.

## When to invoke

- "Audit the site"
- "Anything broken?"
- "Check the project pages are consistent"
- After any `new-project` run (called automatically as the last step)
- Before pushing to live

## Checks to run

Run these from the repo root. Report findings as a punch list — `[OK]` / `[WARN]` / `[BROKEN]` — at the end. Don't fix anything without confirmation; the audit is read-only by default.

### 1. ../../../ path correctness on project pages

Every file under `assets/projects/*/` that references `style.css`, `lightbox.js`, `index.html`, `projects.html`, or `about.html` must use `../../../`. Anything else is broken.

```bash
grep -RE 'href="\.\./(style|index|projects|about)|src="\.\./(style|lightbox)' assets/projects/ || echo "OK: no shallow ../ paths in project pages"
grep -RE 'href="\.\./\.\./(style|index|projects|about)|src="\.\./\.\./(style|lightbox)' assets/projects/ && echo "BROKEN: ../../ paths found — should be ../../../" || echo "OK: no ../../ paths"
```

Exception: KnotPulse and FitnessInsights are Tailwind-based and do not load `style.css` (they have inline-styled nav). Skip them for the stylesheet check.

### 2. Dropdown consistency across pages

The Projects dropdown must match across `index.html`, `projects.html`, `about.html`, and every project page that loads `style.css`.

```bash
# Extract the dropdown <li><a> entries from each page and diff
for f in index.html projects.html about.html assets/projects/*/*.html; do
  echo "=== $f ==="
  awk '/dropdown-menu/,/<\/ul>/' "$f" | grep -oE '<a [^>]*>[^<]*</a>' | sort
done
```

Pages whose extracted dropdown entries don't match index.html's should be flagged. Note: KnotPulse and FitnessInsights may not have a dropdown — check separately.

### 3. Broken image refs

```bash
# For each <img src="..."> in HTML files, verify the file exists relative to the HTML file's location
python3 - << 'PY'
import os, re, sys
root = "."
broken = []
for dirpath, _, files in os.walk(root):
    if ".git" in dirpath or ".claude" in dirpath:
        continue
    for f in files:
        if not f.endswith(".html"):
            continue
        path = os.path.join(dirpath, f)
        with open(path, errors="ignore") as fh:
            html = fh.read()
        for m in re.finditer(r'<img[^>]+src="([^"]+)"', html):
            src = m.group(1)
            if src.startswith(("http://", "https://", "data:")):
                continue
            # URL-decode %20 etc
            from urllib.parse import unquote
            decoded = unquote(src)
            target = os.path.normpath(os.path.join(dirpath, decoded))
            if not os.path.exists(target):
                broken.append((path, src))
print(f"Broken image refs: {len(broken)}")
for p, s in broken[:50]:
    print(f"  {p}: {s}")
PY
```

### 4. HEIC files that should be JPEG

```bash
find assets/ -iname "*.HEIC" -o -iname "*.heic" 2>/dev/null
```

Report any found — they should be converted with `sips -s format jpeg` per CLAUDE.md.

### 5. Footer and copyright year script

Every page should have the `&copy; <span id="yr"></span>` + LinkedIn footer and the inline script setting the year. Flag any missing.

```bash
for f in $(find . -name "*.html" -not -path "./.claude/*"); do
  grep -q 'id="yr"' "$f" || echo "WARN: $f missing footer year span"
done
```

### 6. Project page lightbox script

Every project page that loads `style.css` should also load `../../../lightbox.js`. Flag any that don't.

```bash
for f in assets/projects/*/*.html; do
  if grep -q '../../../style.css' "$f"; then
    grep -q 'lightbox.js' "$f" || echo "WARN: $f loads style.css but not lightbox.js"
  fi
done
```

### 7. CLAUDE.md drift

Compare the project list in `CLAUDE.md`'s "Existing projects" table against actual folders under `assets/projects/`. Flag missing or stale entries. (If drift found, suggest running `sync-claude-md`.)

## Output format

Report as a punch list:

```
SITE AUDIT — <date>

Path correctness:    [OK]
Dropdown consistency: [WARN] about.html missing AIxBio Hackathon entry
Image refs:          [BROKEN] assets/projects/X/page.html: missing.jpg
HEIC files:          [WARN] 2 .HEIC files found
Footer:              [OK]
Lightbox:            [OK]
CLAUDE.md drift:     [WARN] 2 projects missing from table — run sync-claude-md
```

Then list each WARN/BROKEN with the file path so it's actionable. Don't fix anything in audit mode — the user runs the fix as a separate step.
