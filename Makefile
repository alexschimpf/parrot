GREEN  := $(shell tput -Txterm setaf 2)
YELLOW := $(shell tput -Txterm setaf 3)
WHITE  := $(shell tput -Txterm setaf 7)
RESET  := $(shell tput -Txterm sgr0)

# help
TARGET_MAX_CHAR_NUM=20
help:
	@echo ''
	@echo 'Usage:'
	@echo '  ${YELLOW}make${RESET} ${GREEN}<target>${RESET}'
	@echo ''
	@echo 'Targets:'
	@awk '/^[a-zA-Z\-\_0-9]+:/ { \
		helpMessage = match(lastLine, /^# (.*)/); \
		if (helpMessage) { \
			helpCommand = substr($$1, 0, index($$1, ":")-1); \
			helpMessage = substr(lastLine, RSTART + 2, RLENGTH); \
			printf "  ${YELLOW}%-$(TARGET_MAX_CHAR_NUM)s${RESET} ${GREEN}%s${RESET}\n", helpCommand, helpMessage; \
		} \
	} \
	{ lastLine = $$0 }' $(MAKEFILE_LIST)

# run all tests with coverage
run-tests:
	MOCKS_BASE_PATH=./.boot PYTHONPATH=. pytest --cov=app --cov-fail-under=80 --no-cov-on-fail tests/

# run unit tests
run-unit-tests:
	MOCKS_BASE_PATH=./.boot PYTHONPATH=. pytest tests/unit/*

# run api tests
run-api-tests:
	MOCKS_BASE_PATH=./.boot PYTHONPATH=. pytest tests/api/*

# run app docker container
run-docker:
	docker build -t parrot . && docker run -p 8000:80 parrot

# type check python
type-check:
	mypy .

# lint
lint:
	flake8 app tests

# install dev dependencies
install-dev:
	pip install -r requirements.dev.txt

# install pre-commit
install-pre-commit:
	pre-commit install --hook-type pre-commit --hook-type commit-msg
