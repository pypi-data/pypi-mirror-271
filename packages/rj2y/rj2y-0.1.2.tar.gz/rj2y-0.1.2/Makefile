
.PHONY: lint
lint:
	rye run ruff check

.PHONY: format
format:
	rye run ruff format

.PHONY: test
test:
	rye run pytest

.PHONY: clean
clean:
	rm -rf dist

.PHONY: build
build:
	${MAKE} clean
	rye build

publish-test:
	${MAKE} build
	rye publish --verbose --repository testpypi --repository-url https://test.pypi.org/legacy/


publish-prod:
	${MAKE} build
	rye publish
