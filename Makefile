.PHONY: help install install-dev test lint format clean build upload

help:  ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:  ## Install the package
	pip install -e .

install-dev:  ## Install development dependencies
	pip install -e ".[dev]"

test:  ## Run tests
	pytest tests/ -v

lint:  ## Run linting
	flake8 src/
	mypy src/

format:  ## Format code
	black src/ tests/
	isort src/ tests/

clean:  ## Clean build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

clean-all:  ## Deep clean all artifacts and cache files
	python scripts/clean_project.py

build:  ## Build the package
	python -m build

upload-test:  ## Upload to Test PyPI
	python -m twine upload --repository testpypi dist/*

upload:  ## Upload to PyPI (requires API token)
	python -m twine upload dist/*

check-dist:  ## Check distribution files
	twine check dist/*

publish:  ## Full publish workflow (clean, build, check, upload)
	$(MAKE) clean
	$(MAKE) build
	$(MAKE) check-dist
	@echo "Ready to upload. Run 'make upload-test' first, then 'make upload'"

dev-setup:  ## Set up development environment
	python -m venv .venv
	.venv/bin/pip install --upgrade pip
	.venv/bin/pip install -e ".[dev]"
	@echo "Development environment set up. Activate with: source .venv/bin/activate"

demo:  ## Run a demo with sample PDF
	@echo "Creating a sample PDF for demo..."
	@python -c "import fitz; doc = fitz.open(); page = doc.new_page(); page.insert_text((50, 50), 'Sample PDF for testing PDF Zipper'); doc.save('sample.pdf'); doc.close(); print('Sample PDF created: sample.pdf')"
	@echo "Running PDF info command..."
	pdf-zipper info sample.pdf
	@echo "Demo complete!"

check:  ## Run all checks (lint, test)
	$(MAKE) lint
	$(MAKE) test

build-exe:  ## Build standalone executable
	python scripts/build_executable.py

build-cli:  ## Build CLI-only executable
	pyinstaller --onefile --name pdf-zipper-cli scripts/main_cli_only.py

build-gui:  ## Build GUI executable with enhanced Textual support
	python scripts/build_gui_executable.py

build-full:  ## Build full executable (may fail due to GUI dependencies)
	pyinstaller --onefile --name pdf-zipper-full scripts/main.py

install-build:  ## Install build dependencies
	pip install -e ".[build]"

clean-exe:  ## Clean executable build artifacts
	rm -rf build/ dist/ release/ hooks/
	find . -name "*.spec" -delete

test-exe:  ## Test built executables
	@echo "Testing CLI executable..."
	@if [ -f "release/pdf-zipper-cli-macos-arm64" ]; then \
		./release/pdf-zipper-cli-macos-arm64 --version; \
	elif [ -f "dist/pdf-zipper-cli" ]; then \
		./dist/pdf-zipper-cli --version; \
	else \
		echo "No CLI executable found. Run 'make build-exe' first."; \
	fi
