
test-getweets:
	bash lambda-functions/getting-tweets-function/integration-tests/run.sh

test-procraw:
	bash lambda-functions/processing-raw-function/unit-tests/run.sh
	bash lambda-functions/processing-raw-function/integration-tests/run.sh

test-utils:
	pytest -vv lambda-functions/utils

test-tweetsts:
	pytest -vv lambda-functions/tweets-to-silver-function/unit-tests
	bash lambda-functions/tweets-to-silver-function/integration-tests/run.sh

test-usersts:
	pytest -vv lambda-functions/users-to-silver-function/unit-tests
	bash lambda-functions/users-to-silver-function/integration-tests/run.sh

test-placests:
	pytest -vv lambda-functions/places-to-silver-function/unit-tests
	bash lambda-functions/places-to-silver-function/integration-tests/run.sh

tests: test-utils test-getweets test-procraw test-tweetsts test-usersts test-placests