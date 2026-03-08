.PHONY: install dev test lint format clean docker run

install:
	pip install -e .

dev:
	pip install -e ".[dev]"

test:
	pytest -v

lint:
	ruff check .

format:
	ruff check --fix .

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf build dist .pytest_cache .coverage htmlcov .ruff_cache

docker:
	docker build -t palletizer .

run:
	python -m palletizer_full.run
