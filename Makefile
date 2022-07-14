
test-getting-tweets-function:
	bash lambda-functions/getting-tweets-function/integration-tests/run.sh

test-processing-raw-function:
	bash lambda-functions/processing-raw-function/unit-tests/run.sh
	bash lambda-functions/processing-raw-function/integration-tests/run.sh

test-utils:
	pytest -vv lambda-functions/utils

test-tweets-to-silver-function:
	pytest -vv lambda-functions/tweets-to-silver-function/unit-tests
	bash lambda-functions/tweets-to-silver-function/integration-tests/run.sh

test-users-to-silver-function:
	pytest -vv lambda-functions/users-to-silver-function/unit-tests

test-places-to-silver-function:
	pytest -vv lambda-functions/places-to-silver-function/unit-tests

tests:
	test-utils
	test-getting-tweets-function 
	test-processing-raw-function