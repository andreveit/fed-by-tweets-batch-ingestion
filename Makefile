getting-tweets-function-tests:
	bash lambda-functions/getting-tweets/integration-tests/run.sh

processing-raw-function-tests:
	bash lambda-functions/processing-raw-function/unit-tests/run_unit_tests.sh

utils-tests:
	pytest -vv lambda-functions/utils

tweets-to-silver-function-tests:
	pytest -vv lambda-functions/tweets-to-silver-function/unit-tests

users-to-silver-function-tests:
	pytest -vv lambda-functions/users-to-silver-function/unit-tests