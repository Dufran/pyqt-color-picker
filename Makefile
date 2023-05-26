SHELL := /bin/bash
.DEFAULT_GOAL := help
.PHONY: help

help:
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
	| sed -n 's/^\(.*\): \(.*\)##\(.*\)/\1##\3/p' \
	| column -t -s '##'


install: ## Install and update python dependencies
	@poetry install

lint: ## Check code with ruff linter
	@ruff . --fix

format: ## Format code with black
	@black .
run: ## Run code with python
	@python main.py

build: ## Build application 
	pyinstaller --windowed --onefile --noconfirm --add-data "assets:assets" \
	--icon="assets/icon.icns"  main.py