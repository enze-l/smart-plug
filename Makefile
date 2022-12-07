development-dependencies:
	@pipenv sync --dev

lint: development-dependencies
	@pipenv run flake8

fix-lint: development-dependencies
	@pipenv run black .

unit-test: development-dependencies
	@pipenv run python3 -m unittest

silent-unit-test: development-dependencies
	@pipenv run python3 -m unittest

test: lint unit-test
