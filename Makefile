.PHONY: help setup-init setup-venv install install-dev install-test install-all lock update-deps test test-with-coverage lint-python lint-yaml format-python pre-commit build clean clean-all check-poetry

.DEFAULT_GOAL := help

# Help
help: ## Show this help message
	@echo "Available targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

# Variables
POETRY := poetry
PYTHON := $(POETRY) run python
PYTEST := $(POETRY) run pytest
BUILD := $(POETRY) build
PACKAGE_NAME := ssllabsscan
TEST_PATH := tests/

# Utilities (internal use only)
check-poetry:
	@which poetry > /dev/null || (echo "Installing Poetry..." && pip install --user poetry && echo "Poetry installed successfully!")

# Setup
setup-init: setup-venv lock install-all ## Complete first-time setup (configure venv, lock, install all deps)
	@echo "✓ Setup complete! Run 'make help' to see available commands."

setup-venv: check-poetry ## Configure Poetry to use .venv in project directory
	@$(POETRY) config virtualenvs.in-project true

# Installation
install: check-poetry ## Install main dependencies only
	@$(POETRY) install

install-dev: check-poetry ## Install main + dev dependencies
	@$(POETRY) install --with dev

install-test: check-poetry ## Install main + test dependencies
	@$(POETRY) install --with test

install-all: check-poetry ## Install all dependencies (main + dev + test)
	@$(POETRY) install --with dev --with test

# Dependency management
lock: check-poetry ## Regenerate poetry.lock from pyproject.toml
	@$(POETRY) lock

update-deps: check-poetry ## Update dependencies to latest compatible versions
	@$(POETRY) update

# Testing
test: install-test ## Run unit tests without coverage
	@$(PYTEST) $(TEST_PATH) -v --junit-xml junit.xml

test-with-coverage: install-test ## Run unit tests with coverage reporting
	@$(PYTEST) $(TEST_PATH) -v --cov=$(PACKAGE_NAME) --cov-report=xml:coverage.xml --cov-report=term-missing --junit-xml junit.xml

# Code quality
lint-python: install-dev ## Lint Python code with flake8
	@$(POETRY) run flake8 --max-line-length=100 $(PACKAGE_NAME)/ $(TEST_PATH)

lint-yaml: install-dev ## Lint YAML files with yamllint
	@$(POETRY) run yamllint -c .github/linters/.yaml-lint.yml .github/

format-python: install-dev ## Format Python code with black
	@$(POETRY) run black --line-length=100 $(PACKAGE_NAME)/ $(TEST_PATH)

# Pre-commit checks
pre-commit: format-python lint-python lint-yaml test-with-coverage ## Run all quality checks before committing
	@echo "✓ All pre-commit checks passed!"

# Build
build: check-poetry ## Build the package
	@$(BUILD)

# Cleanup
clean: ## Clean test artifacts, build artifacts and temporary files
	@echo "Cleaning up artifacts..."
	@rm -rf .coverage* coverage.xml htmlcov/
	@rm -rf junit.xml
	@rm -rf build/ dist/ *.egg-info/
	@rm -rf .pytest_cache/
	@find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.py[cod]" -delete 2>/dev/null || true
	@echo "✓ Cleanup complete"

clean-all: clean ## Clean everything including virtual environment
	@echo "Removing virtual environment..."
	@rm -rf .venv/
	@echo "✓ Full cleanup complete"
