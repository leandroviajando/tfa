SHELL := /bin/bash
MAKEFLAGS += --silent

.PHONY: help
# make help: @ List available tasks on this project
help:
	grep -h -E '[a-zA-Z0-9\.\-]+:.*?@ .*$$' $(MAKEFILE_LIST) | tr -d '#' | awk 'BEGIN {FS = ":.*?@ "}; {printf "\033[36m%-40s\033[0m %s\n", $$1, $$2}'

.PHONY: clean
# make clean: @ Remove cache, checkpoints, coverage, etc.
clean:
	find . -type f -name *.DS_Store -ls -delete
	find . | grep -E '(__pycache__|\.pyc|\.pyo)' | xargs rm -rf
	find . | grep -E .mypy_cache | xargs rm -rf
	find . | grep -E .pytest_cache | xargs rm -rf
	find . | grep -E .ipynb_checkpoints | xargs rm -rf
	find . | grep -E .trash | xargs rm -rf
	rm -f .coverage

.PHONY: build
# make build: @ Build db, app and web
build:
	docker system prune -f
	docker compose up --build -d

.PHONY: run
# make run: @ Run db, app and web
run:
	docker compose up -d

.PHONY: stop
# make stop: @ Stop db, app and web
stop:
	docker-compose down

.PHONY: test
# make test: @ Run tests
test: | run
	docker compose exec app pytest tests
	docker compose exec web yarn jest
