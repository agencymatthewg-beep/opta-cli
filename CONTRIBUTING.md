# Contributing to Opta CLI

Thank you for your interest in contributing to Opta CLI! We welcome contributions in the form of bug reports, feature requests, and pull requests.

---

## 🐛 Bug Reports and Feature Requests

Please submit bug reports and feature requests as [GitHub issues](https://github.com/optamize/opta-cli/issues).

When reporting bugs, include:
- Your operating system and Python version
- Steps to reproduce the issue
- Expected vs actual behavior
- Any relevant error messages or logs

---

## 🔧 Development Setup

### 1. Clone the Repository

```bash
git clone https://github.com/optamize/opta-cli.git
cd opta-cli
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

### 3. Activate the Virtual Environment

**macOS/Linux:**
```bash
source venv/bin/activate
```

**Windows:**
```bash
venv\Scripts\activate
```

### 4. Install in Editable Mode

```bash
pip install -e .
```

### 5. Install Development Dependencies

```bash
pip install -r requirements/requirements-dev.txt
```

### 6. Install Pre-commit Hooks (Optional)

```bash
pre-commit install
```

This will automatically format code and run checks before each commit.

---

## 🎨 Code Style

Opta CLI follows the existing **Aider code style**:

### Style Guidelines
- **PEP 8** with a maximum line length of **100 characters**
- **No type hints** — Aider's original style
- **isort** for import sorting
- **Black** for code formatting

### Running Formatters

Pre-commit hooks will run automatically if installed. You can also run them manually:

```bash
pre-commit run --all-files
```

---

## 🧪 Testing

### Running Tests

Run the entire test suite:
```bash
pytest
```

Run specific test files:
```bash
pytest tests/basic/test_coder.py
```

Run a specific test:
```bash
pytest tests/basic/test_coder.py::TestCoder::test_specific_case
```

### Writing Tests

- Place tests in the `tests/` directory
- Follow the naming convention: `test_*.py`
- Match the existing test structure and patterns
- Aim for high code coverage on new features

---

## 📝 Pull Request Process

### Before Submitting

1. **Small changes** — Feel free to submit directly
2. **Large changes** — Open an issue first to discuss the approach
3. **Run tests** — Ensure all tests pass locally
4. **Update docs** — Add or update documentation for new features
5. **Follow style** — Pre-commit hooks help with this

### PR Guidelines

- Write a clear description of what the PR does
- Reference any related issues (`Fixes #123`)
- Keep PRs focused on a single feature or fix
- Add tests for new functionality
- Update the CHANGELOG.md if applicable

### Review Process

- Maintainers will review your PR
- Address any feedback or requested changes
- Once approved, your PR will be merged

---

## 🔄 Managing Dependencies

When adding new dependencies:

1. Add to the appropriate `.in` file:
   - `requirements.in` — Main dependencies
   - `requirements-dev.in` — Development dependencies

2. Recompile requirements:
   ```bash
   pip install pip-tools
   ./scripts/pip-compile.sh
   ```

3. Commit both the `.in` and `.txt` files

---

## 📚 Documentation

### Building Documentation Locally

The documentation is built with Jekyll:

1. Install Ruby and Bundler
2. Navigate to `aider/website`
3. Install dependencies:
   ```bash
   bundle install
   ```
4. Build or serve:
   ```bash
   bundle exec jekyll build
   bundle exec jekyll serve
   ```

### Documentation Guidelines

- Keep examples practical and concise
- Use consistent formatting
- Test all code examples
- Link to related documentation

---

## 🐳 Docker

Build the Docker image:

```bash
docker build -t opta-cli -f docker/Dockerfile .
```

---

## 🏗️ Project Structure

```
opta-cli/
├── aider/              # Main source code
│   ├── coders/         # Core editing logic
│   ├── models/         # LLM provider integrations
│   ├── website/        # Documentation site
│   └── ...
├── tests/              # Test suite
│   ├── basic/          # Basic unit tests
│   └── ...
├── requirements/       # Dependency specifications
├── scripts/            # Utility scripts
└── benchmark/          # Benchmarking tools
```

---

## 🎯 Areas for Contribution

### High Priority
- **MCP server integrations** — Add new MCP servers
- **LLM provider support** — Add new model providers
- **Terminal themes** — Design new themes
- **Documentation** — Improve guides and examples
- **Bug fixes** — Fix reported issues

### Medium Priority
- **Test coverage** — Improve test coverage
- **Performance** — Optimize slow operations
- **Refactoring** — Clean up technical debt

### Exploratory
- **IDE integrations** — VS Code, JetBrains plugins
- **Agent patterns** — New multi-agent workflows
- **UI improvements** — Better terminal UX

---

## 🤔 Questions?

- Open a [GitHub Discussion](https://github.com/optamize/opta-cli/discussions)
- Ask in the issue tracker
- Contact the maintainers

---

## 📜 Licensing

By contributing to Opta CLI, you agree that your contributions will be licensed under the Apache 2.0 License.

Review the [Individual Contributor License Agreement](https://aider.chat/docs/legal/contributor-agreement.html) from the original Aider project for reference.

---

## 🙏 Thank You

Every contribution, no matter how small, helps make Opta CLI better. We appreciate your time and effort!

---

<p align="center">
  <strong>Happy coding! 🚀</strong>
</p>
