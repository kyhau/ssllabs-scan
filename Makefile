# ssllabs-scan Makefile - Unit Testing Focus
# Provides targets for running unit tests locally

.PHONY: help test test-coverage clean clean-all install-test-deps yamllint build check-poetry setup-venv update-deps lock install-deps

# Default target
help: ## Show this help message
	@echo "Available targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

# Variables
POETRY := poetry
PYTHON := $(POETRY) run python
PYTEST := $(POETRY) run pytest
BUILD := $(POETRY) build
PACKAGE := ssllabsscan

# Check if poetry is available, install if not
check-poetry:
	@which poetry > /dev/null || (echo "Installing Poetry..." && pip install --user poetry && echo "Poetry installed successfully!")

# Configure Poetry to use project-local venv (run once)
setup-venv: check-poetry ## Configure Poetry to use .venv in project directory
	@echo "Configuring Poetry for project-local virtualenv..."
	$(POETRY) config virtualenvs.in-project true
	@echo "Poetry will now create .venv/ in the project directory"
	@echo "This isolates dependencies from your global Python environment"

# Installation targets
install-test-deps: check-poetry ## Install test dependencies
	@echo "Installing test dependencies..."
	$(POETRY) install --with dev
	@echo "Dependencies installed."

install-deps: check-poetry ## Install project dependencies
	@echo "Installing project dependencies..."
	$(POETRY) install
	@echo "Dependencies installed."

# Build targets
build: check-poetry ## Build the package
	@echo "Building package..."
	$(BUILD)
	@echo "Package built successfully."

# Testing targets
test: install-test-deps ## Run unit tests without coverage
	@echo "Running unit tests..."
	$(PYTEST) $(PACKAGE)/tests/ -v --junit-xml junit.xml

test-coverage: install-test-deps ## Run unit tests with coverage reporting
	@echo "Running unit tests with coverage..."
	$(PYTEST) $(PACKAGE)/tests/ -v --cov=$(PACKAGE) --cov-report=xml:coverage.xml --cov-report=term-missing --junit-xml junit.xml

# Linting targets
yamllint: check-poetry ## Run yamllint on GitHub workflow files
	@echo "Running yamllint on GitHub workflows..."
	$(POETRY) run yamllint -c .github/linters/.yaml-lint.yml .github/

# Dependency management
update-deps: check-poetry ## Update dependencies to latest compatible versions
	@echo "Updating dependencies..."
	$(POETRY) update
	@echo "Dependencies updated in poetry.lock"

lock: check-poetry ## Regenerate poetry.lock from pyproject.toml
	@echo "Regenerating lock file..."
	$(POETRY) lock
	@echo "Lock file regenerated"

# Cleanup targets
clean: ## Clean test artifacts, build artifacts and temporary files
	rm -rf .coverage*
	rm -rf coverage.xml
	rm -rf junit.xml
	rm -rf htmlcov/
	rm -rf build/
	rm -rf dist/
	rm -rf eggs/
	rm -rf .eggs/
	rm -rf *.egg-info/
	rm -rf *.egg
	rm -rf .pytest_cache/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.py[cod]" -delete

clean-all: ## Clean everything including virtual environment
	$(MAKE) clean
	rm -rf .venv/

# Default target when no target is specified
.DEFAULT_GOAL := help

