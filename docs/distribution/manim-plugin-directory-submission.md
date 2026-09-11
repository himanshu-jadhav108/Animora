# Manim Community Plugin Directory Submission Handoff

This document provides the complete, verified submission package for listing **Animora** on the official [Manim Community Plugin Directory](https://plugins.manim.community/).

---

## 1. Background & Discovery Mechanism

The Manim Community plugin website is hosted at [https://plugins.manim.community/](https://plugins.manim.community/) and maintained via the GitHub repository [ManimCommunity/plugins-site](https://github.com/ManimCommunity/plugins-site).

### Discovery Logic:
1. **Automated Scanning:** A scheduled GitHub Action runs daily to index packages on PyPI that match the regular expression `<(.*)>manim-(?P<name>.*)<(.*)>`.
2. **Explicit Directory Inclusion (`extras`):** Packages that do not use the `manim-` naming prefix (such as `chanim`, `statanim`, `llmanim`, and `qual-manim`) are listed in `scripts/default.json` under the `"extras"` array.
3. **Runtime Plugin Detection:** Animora registers the official plugin entry point in `pyproject.toml`:
   ```toml
   [project.entry-points."manim.plugins"]
   animora = "animora"
   ```
   This enables Manim's CLI to detect Animora natively via `manim plugins -l`:
   ```text
   Manim Community v0.21.0
   Plugins:
    • animora
   ```

---

## 2. Submission Steps (Human Maintainer Action)

Because submitting a Pull Request to `ManimCommunity/plugins-site` requires GitHub user authentication, follow these simple steps:

### Step 1: Fork and Clone `ManimCommunity/plugins-site`
```bash
git clone https://github.com/<your-username>/plugins-site.git
cd plugins-site
git checkout -b add-animora
```

### Step 2: Edit `scripts/default.json`
Append `"animora"` to the `"extras"` array in `scripts/default.json`:

```diff
     "extras": [
         "chanim",
         "statanim",
         "llmanim",
-        "qual-manim"
+        "qual-manim",
+        "animora"
     ],
```

### Step 3: Commit and Push
```bash
git add scripts/default.json
git commit -m "Add animora to plugin directory"
git push origin add-animora
```

### Step 4: Open Pull Request
Open a PR to `ManimCommunity/plugins-site:main` using the pre-drafted metadata below.

---

## 3. Pull Request Template

**Title:** `Add animora to plugin directory`

**Description:**
```markdown
### Description
Add `animora` to the Manim Community plugin directory extras list.

### Package Details
- **Package Name:** animora
- **PyPI URL:** https://pypi.org/project/animora/
- **GitHub Repository:** https://github.com/himanshu-jadhav108/Animora
- **Documentation:** https://himanshu-jadhav108.github.io/Animora/
- **Description:** High-level, declarative animation framework built on top of Manim for educational, technical, and algorithmic visualization.
- **Entry Point:** Registered under `[project.entry-points."manim.plugins"]` (`animora = "animora"`), verified with `manim plugins -l`.
```
