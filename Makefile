.PHONY: all
all: help

.PHONY: help
help:
	@echo '----'
	@echo 'build                   - build container'
	@echo 'run                     - run container'
	@echo 'compose                 - run compose'

.PHONY: build
build:
	docker build . --target builder -t prediction-app:latest

.PHONY: run
run:
	#! need env file to run
	docker run --env-file .env --rm -v ./input:/astrazeneca/input -v ./output:/astrazeneca/output prediction-app:latest

.PHONY: compose
compose:
	docker compose -f docker-compose.yml up --build

