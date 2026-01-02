MYPY_CACHE ?= .mypy_cache

.PHONY: help
help:
	@echo "Available targets:"
	@echo "  run        - Start the Streamlit app"
	@echo "  test       - Run tests"
	@echo "  lint       - Run linter"
	@echo "  lint-fix   - Run linter with auto-fix"
	@echo "  format     - Format code"
	@echo "  typecheck  - Run type checker"
	@echo "  check      - Run all checks (lint, typecheck, test)"
	@echo "  clean      - Remove cache directories"

.PHONY: run
run:
	uv run streamlit run app.py

.PHONY: test
test:
	uv run pytest .

.PHONY: lint
lint:
	uv run ruff check .

.PHONY: lint-fix
lint-fix:
	uv run ruff check . --fix

.PHONY: format
format:
	uv run ruff format .

.PHONY: typecheck
typecheck:
	uv run mypy --config-file pyproject.toml --cache-dir $(MYPY_CACHE) .

.PHONY: check
check: lint typecheck test

.PHONY: clean
clean:
	rm -rf $(MYPY_CACHE) .pytest_cache .ruff_cache __pycache__ */__pycache__ */*/__pycache__
