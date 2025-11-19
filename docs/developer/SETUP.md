# Developer Setup

This guide describes how to configure a development environment for Project Cerebrus.

## Clone and Environment

1. Clone the repository:

   ```bash
   git clone <REPO_URL> cerebrus
   cd cerebrus
   ```

2. Create a virtual environment:

   ```bash
   py -3 -m venv .venv
   .venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Development Tools

Recommended tools:

- Python 3.11 (64-bit).
- Visual Studio Code, PyCharm, or equivalent.
- Git with a graphical diff tool (e.g. Beyond Compare, WinMerge).
- Optional:
  - `pre-commit` for automated formatting and linting.

## Running Tests

- To run all tests:

  ```bash
  pytest
  ```

- To run a subset:

  ```bash
  pytest tests/core/test_device_manager.py
  ```

## Static Checks

- Run `mypy` for type checking:

  ```bash
  mypy cerebrus
  ```

- Run `black` and `isort` to format code:

  ```bash
  black cerebrus tests
  isort cerebrus tests
  ```

Refer to `CODE_STANDARDS.md` for more details.
