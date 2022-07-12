test-getting-tweets-function:
	bash lambda-functions/getting-tweets-function/integration-tests/run.sh
	
test-processing-raw-function:
	bash lambda-functions/processing-raw-function/unit-tests/run_unit_tests.sh

test-utils:
	pytest -vv lambda-functions/utils

test-tweets-to-silver-function:
	pytest -vv lambda-functions/tweets-to-silver-function/unit-tests

test-users-to-silver-function:
	pytest -vv lambda-functions/users-to-silver-function/unit-tests

test-places-to-silver-function:
	pytest -vv lambda-functions/places-to-silver-function/unit-tests
	