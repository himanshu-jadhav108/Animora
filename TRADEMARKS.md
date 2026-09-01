# Animora Brand & Project Identity Guidelines

## Purpose & Scope

**Animora is the name used to identify the official Animora project.**

This policy describes permitted and discouraged uses of the project's name and branding. It does not itself create or establish trademark rights.

The primary objective of this guideline is to ensure that the open-source community can freely build on, fork, extend, and redistribute Animora, while protecting users from confusion regarding which distribution is the authentic, official Animora project.

---

## The Open Source Model: Code vs. Brand

Animora strictly decouples the source code license from the project's brand identity:

```text
                ANIMORA PROJECT
                       │
          ┌────────────┴────────────┐
          │                         │
      SOURCE CODE                 BRAND
          │                         │
     MIT License              Project Policy
          │                         │
          ▼                         ▼
   • Anyone can use          • Identifies official
   • Anyone can fork           project & releases
   • Anyone can modify       • Avoids confusing or
   • Anyone can sell           misleading representations
```

- **Source Code (MIT License)**: The underlying source code is licensed under the permissive [MIT License](LICENSE). You are completely free to inspect, copy, modify, merge, publish, distribute, sublicense, and sell copies of the software according to its terms.
- **Project Name & Visual Branding**: The MIT License applies to the source code. It does **not** grant permission to use the "Animora" name, logo, or associated branding in a manner that implies official endorsement, sponsorship, maintenance, certification, or affiliation with the official Animora project.

---

## Fork and Derivative Work Guidelines

We actively encourage developers to fork Animora, experiment with new rendering algorithms, and create specialized packages. To keep things clear for users, downstream distributions should follow these practical naming guidelines:

### Permitted / Recommended Uses
You may reference the Animora name truthfully to describe compatibility, provenance, or technical basis:
- **"Based on Animora"** (e.g., *MatrixAnim — An educational graphics toolkit based on Animora*)
- **"A fork of Animora"** (e.g., *BioAnim — A specialized bioinformatics visualization engine forked from Animora*)
- **"Compatible with Animora"** (e.g., *Animora-GL Plugin — Hardware-accelerated shaders compatible with Animora*)
- **"Extension for Animora"** (e.g., *GraphViewer — An interactive visual debugger for Animora*)

### Discouraged / Potentially Misleading Uses
You should not name or brand third-party forks, services, or commercial products in a way that could mislead users into thinking the fork is the official project or officially maintained by the Animora team:
- **"Animora Official"** — when maintained by an independent third party without official affiliation.
- **"Official Animora Pro"** — when no official relationship or partnership exists.
- **"Animora, maintained by XYZ"** — when XYZ is not the authentic maintainer of the official project.
- Using the official Animora logo as the primary icon or logo for an independent fork or product.

*(Note: These examples are illustrative guidelines intended to foster community clarity and prevent user confusion, not formal legal determinations.)*

---

## Logo and Visual Assets

Original media assets (such as diagrams in `docs/assets/media/` and official logo concepts) represent the visual identity of the official project. 

- You may display the official logo to link to or truthfully reference the official Animora project.
- If you distribute a significantly modified fork of Animora, we recommend creating a distinct logo and visual theme for your fork to maintain clarity for your users.

---

## Future Trademark Preparation

Animora was created and is maintained by **Himanshu Jadhav**. As the project evolves, the maintainers may pursue formal trademark registration for "Animora" and associated marks in relevant jurisdictions.

- **Current Status**: "Animora" is used as the project and brand name of this open-source software.
- **Registration Statement**: This repository does not claim that "Animora" is a registered trademark unless formal registration is officially completed and documented. No fake trademark symbols or unverified registration claims are made.
- **Future Growth**: If formal trademark registration occurs in the future, this document will be updated with verified registration details.

---

## Questions & Clarifications

If you have questions about whether a planned use of the Animora name or logo is consistent with these guidelines, please open a discussion or reach out to the project maintainer via the [GitHub repository](https://github.com/himanshu-jadhav108/Animora).
