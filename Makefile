
---

## 2) Makefile  
**File:** `Makefile`

```makefile
.PHONY: help venv install test clean

help:
	@echo "Available commands:"
	@echo "  make venv     - create virtual environment"
	@echo "  make install  - install dependencies"
	@echo "  make test     - run pytest"
	@echo "  make clean    - remove virtual environment and caches"

venv:
	python3 -m venv venv
	@echo "Virtual environment created."

install:
	./venv/bin/pip install -r requirements.txt

test:
	./venv/bin/pytest -q

clean:
	rm -rf venv
	rm -rf __pycache__ .pytest_cache
	find . -name "__pycache__" -type d -exec rm -rf {} +
