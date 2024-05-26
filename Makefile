MYPY_CACHE ?= .mypy_cache

.PHONY: mypy
mypy:
	mypy --config-file pyproject.toml --cache-dir $(MYPY_CACHE) .

.PHONY: test
test:
	pytest .

.PHONY: ruff
ruff:
	ruff check .

.PHONY: ruff-fix
ruff-fix:
	ruff check . --fix
