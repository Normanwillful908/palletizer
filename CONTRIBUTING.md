# Contributing to Palletizer Full Stack

Thank you for your interest in contributing. Whether you are fixing a bug, adding a new connector or improving documentation, your help makes this project better for everyone.

## Getting Started

1. Fork the repository and clone your fork.
2. Install the project in development mode:

   ```bash
   pip install -e ".[dev]"
   ```

3. Create a feature branch:

   ```bash
   git checkout -b feature/your-feature-name
   ```

4. Make your changes and ensure the test suite passes:

   ```bash
   pytest -v
   ruff check .
   ```

5. Commit with a clear message and open a pull request.

## Code Style

We use [ruff](https://docs.astral.sh/ruff/) for linting and formatting. All code must pass `ruff check .` before merging. Key conventions:

- Use modern Python type annotations (`dict[str, Any]` instead of `Dict[str, Any]`).
- Use `str | None` instead of `Optional[str]`.
- Write docstrings in NumPy style.
- Keep functions focused and testable.

## Testing

Every new feature or bug fix should include tests. We use [pytest](https://docs.pytest.org/) with fixtures defined in `tests/conftest.py`. Run the full suite with:

```bash
pytest -v
```

## Reporting Issues

If you find a bug or have a feature request, please open an issue on GitHub. Include as much context as possible: your Python version, operating system, robot hardware (if relevant) and steps to reproduce the problem.

## Code of Conduct

This project follows the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md). By participating, you agree to uphold a respectful and inclusive environment.
