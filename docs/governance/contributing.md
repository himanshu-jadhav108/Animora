# Contributing to Animora

Thank you for your interest in contributing to **Animora**! We welcome contributions to help make educational, mathematical, and algorithmic visualization intuitive and accessible.

---

## 📜 Contribution Licensing & Intellectual Property

To ensure that Animora remains open, accessible, and legally sound for everyone, all contributions are subject to the following principles:

1. **Retained Ownership**: You retain applicable intellectual property rights and copyright in your original contributions.
2. **Grant of Rights**: By submitting a pull request, patch, or documentation to the Animora repository, you grant the project maintainers and users the permissions necessary to distribute, modify, and license your contribution under the project's MIT License.
3. **Originality & Authority**: You confirm that you created the contribution yourself or have the legal right to submit it under the terms of the MIT License.
4. **No Proprietary Code**: Please do not submit proprietary, confidential, or trade secret code or assets without explicit written authorization from the respective rights holder.
5. **Third-Party Code & Assets**: If your contribution includes or relies on third-party code, fonts, icons, or data:
   - The third-party material must use a compatible permissive open-source license (such as MIT, BSD-2/3-Clause, or Apache 2.0).
   - You must clearly identify the provenance, author, and license in the pull request description.
6. **Brand & Asset Clarity**: Do not introduce third-party trademarks, logos, or commercial assets that would create ambiguity regarding project identity or ownership.

---

## 🛠️ Development Setup

Animora requires **Python 3.10+**. We recommend using a virtual environment:

### 1. Clone the repository
```bash
git clone https://github.com/himanshu-jadhav108/Animora.git
cd Animora
```

### 2. Create and activate a virtual environment
```bash
python -m venv .venv

# On Linux/macOS:
source .venv/bin/activate

# On Windows:
.venv\Scripts\activate
```

### 3. Install in editable mode with development dependencies
```bash
pip install -e ".[dev]"
```

---

## 🧪 Quality Checks & Validation

Before submitting a Pull Request, please ensure all quality checks pass locally:

### Run Linter and Formatter
```bash
ruff check .
ruff format --check .
```
To auto-fix linting and formatting issues:
```bash
ruff check --fix .
ruff format .
```

### Run Type Checking
```bash
mypy src/ tests/
```

### Run Tests
```bash
pytest
```

### Build Documentation
```bash
mkdocs build
```

---

## 📐 Architecture Guidelines

All contributions must follow the architectural boundaries established in the Architecture section:
1. **Separation of Concerns**: Layout algorithms belong in `animora.layout`, not inside component classes.
2. **First-Class Escape Hatch**: Every component must expose `.manim_object` to allow native Manim customization.
3. **Type Safety**: All public functions and classes must be 100% type-annotated with strict mypy validation.
4. **Public API Exports**: Export public symbols explicitly in `__all__` across all module and package entrypoints.
5. **Zero Unjustified Dependencies**: Do not introduce new hard runtime dependencies without architectural discussion and justification.
