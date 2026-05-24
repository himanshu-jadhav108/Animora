# Contributing to Animora

Thank you for your interest in contributing to **Animora**! We welcome contributions to help make educational animation intuitive and accessible.

---

## 🛠️ Development Setup

Animora requires **Python 3.10+**. We recommend using a virtual environment.

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

Before submitting a Pull Request, make sure all quality checks pass locally:

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

All contributions must follow the architectural boundaries established in `docs/architecture/`:
1. **Separation of Concerns**: Layout algorithms belong in `animora.layout`, not inside component classes.
2. **First-Class Escape Hatch**: Every component must expose `.manim_object`.
3. **Type Safety**: All public functions and classes must be 100% type-annotated.
4. **Public API Exports**: Export public symbols explicitly in `__all__`.

---

## 📜 Code of Conduct

Please review and adhere to our [Code of Conduct](CODE_OF_CONDUCT.md) in all community interactions.
