# Security Policy

## Overview

The **Animora** team and maintainers take the security of this project seriously. We appreciate the efforts of security researchers, developers, and users who responsibly report potential vulnerabilities.

This document outlines how to report security issues, our response process, supported versions, and important security considerations when using Animora in your applications and pipelines.

---

## Supported Versions

Animora is currently in active early-stage development. Security patches and bug fixes are prioritized for the latest stable release published to PyPI.

| Version | Supported | Notes |
| :--- | :--- | :--- |
| **0.1.x** (Latest) | :white_check_mark: Yes | Actively maintained stable line. |
| **< 0.1.0** | :x: No | Pre-release / historical snapshots. |

*Users are strongly encouraged to upgrade to the latest released version of Animora to ensure they have the latest bug fixes and security improvements. As the project matures and reaches higher version milestones (1.0+), a formal long-term support (LTS) policy may be established.*

---

## Reporting a Vulnerability

If you believe you have found a security vulnerability in Animora, please **do NOT report it publicly** via GitHub Issues, public Pull Requests, public discussions, or social media until the maintainers have had an opportunity to review and coordinate remediation.

### Preferred Reporting Methods

1. **GitHub Private Vulnerability Reporting (Recommended)**:
   Navigate to the [Animora Security Advisories page](https://github.com/himanshu-jadhav108/Animora/security/advisories/new) and submit a private security advisory report.
2. **Direct Maintainer Contact**:
   If private vulnerability reporting is unavailable, contact the project maintainer via email:
   - **Contact**: `himanshujadhav40@gmail.com`
   - **Subject**: `[Animora Security] Potential vulnerability in <component/module>`

### Vulnerability Report Checklist

To help us investigate and triage the issue efficiently, please include as much of the following information as possible:

- [ ] **Description**: A clear summary of the vulnerability and its potential impact.
- [ ] **Affected Version**: The specific version of Animora where the issue was observed.
- [ ] **Reproduction Steps**: Step-by-step instructions to reproduce the issue.
- [ ] **Proof of Concept (PoC)**: Minimal code example or scene script demonstrating the issue (if applicable).
- [ ] **Expected vs. Actual Behavior**: What you expected to happen versus what actually happened.
- [ ] **Environment Details**: Operating system, Python version, Animora version, Manim version, and FFmpeg version.

> [!WARNING]
> **Data Privacy**: Please do **not** include sensitive credentials, API tokens, passwords, or personal data in your reports.

---

## Security Response Process

When a security report is submitted, we follow a simple, structured remediation workflow:

```text
  ┌────────────┐     ┌─────────────────┐     ┌───────────────┐     ┌──────────────────┐
  │ 1. Report  │ ──> │ 2. Acknowledge  │ ──> │ 3. Investigate│ ──> │ 4. Severity Risk │
  └────────────┘     └─────────────────┘     └───────────────┘     └──────────────────┘
                                                                             │
  ┌────────────┐     ┌─────────────────┐     ┌───────────────┐               │
  │ 7. Disclose│ <── │ 6. Release Fix  │ <── │ 5. Patch & Test │ <─────────────┘
  └────────────┘     └─────────────────┘     └───────────────┘
```

1. **Acknowledgement**: The maintainers will make reasonable efforts to acknowledge receipt of valid reports.
2. **Investigation**: We verify the vulnerability and reproduce it in a test environment.
3. **Severity Assessment**: We assess the potential impact, attack vector, and affected configurations.
4. **Fix Development & Testing**: A patch is created and tested privately to ensure it resolves the issue without introducing regressions.
5. **Release**: A patched version of Animora is built, tested, and published to PyPI.
6. **Coordinated Disclosure**: A security advisory is published via GitHub Security Advisories, crediting the reporter (if desired).

---

## Security Considerations for Animora

As a Python-based animation and rendering framework, developers and users should keep the following domain-specific security considerations in mind:

### 1. Processing Untrusted Input & Scripts
- Animora allows defining scenes and data visualizations using Python code. Executing untrusted Python scripts or loading untrusted scene configurations runs code with the full permissions of the executing user account.
- Always sanitize and validate external user-provided data (e.g., CSV, JSON, or mathematical expressions) before passing them into scene builders or chart components.

### 2. Filesystem & Media Output
- Rendering scenes and video export writes files (MP4, PNG, SVG, temporary caches) to disk.
- Avoid running rendering pipelines with elevated administrative/root privileges or writing outputs to untrusted shared directories.

### 3. External Tool Invocations (FFmpeg, Cairo, Pango)
- Underlying rendering backends (such as Manim) invoke system utilities like FFmpeg for video composition and encoding.
- Ensure that system binaries in your system `PATH` are authentic, verified binaries installed from reputable package managers or official distribution channels.
- Avoid passing unvalidated or untrusted user input directly into system process arguments.

### 4. Third-Party Dependencies
- Animora relies on upstream open-source libraries (`manim`, `numpy`, `networkx`, `click`, `rich`).
- Security vulnerabilities identified in upstream dependencies may affect downstream Animora deployments. Regularly update your environment's dependencies using `pip install --upgrade`.

---

## Responsible Disclosure Policy

We encourage security researchers to adhere to responsible disclosure principles:

- Make a good-faith effort to avoid privacy violations, data destruction, and service interruption during testing.
- Do not perform destructive attacks, denial-of-service (DoS) attacks against infrastructure, or social engineering against maintainers.
- Allow the project maintainers a reasonable opportunity to investigate and release a fix before disclosing details publicly.

---

## Security Acknowledgements

We appreciate and value the contributions of security researchers and community members who help protect Animora. With the reporter's permission, individuals who responsibly report confirmed security vulnerabilities will be recognized in release notes and security advisories.

---

## Security Disclaimer

Animora is open-source software distributed under the [MIT License](LICENSE). While we strive to maintain high security and code quality standards, the software is provided "as is", without warranty of any kind. Users and organizations are responsible for assessing their own security requirements, isolating execution environments, and maintaining updated dependencies.

---

## Relationship with Project Policies

Animora maintains clear and distinct documentation for each aspect of project governance:

| Document | Purpose |
| :--- | :--- |
| **[LICENSE](LICENSE)** | Source code usage, modification, and redistribution permissions (MIT License). |
| **[COPYRIGHT.md](COPYRIGHT.md)** | Copyright ownership (`Copyright © 2026 Himanshu Jadhav`) and project provenance. |
| **[TRADEMARKS.md](TRADEMARKS.md)** | Animora brand identity, project name usage, and fork naming guidelines. |
| **[CONTRIBUTING.md](CONTRIBUTING.md)** | Contribution workflow, coding standards, and intellectual property terms. |
| **[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)** | Attribution and licensing notices for upstream dependencies. |
| **[SECURITY.md](SECURITY.md)** | Vulnerability reporting, security response process, and security guidelines. |
