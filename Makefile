MYPY_CACHE ?= .mypy_cache

.PHONY: run
run:
	streamlit run app.py

.PHONY: test
test:
	pytest .

.PHONY: mypy
mypy:
	mypy --config-file pyproject.toml --cache-dir $(MYPY_CACHE) .

.PHONY: ruff
ruff:
	ruff check .

.PHONY: ruff-fix
ruff-fix:
	ruff check . --fix
