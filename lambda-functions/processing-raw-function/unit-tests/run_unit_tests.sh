#!/usr/bin/env bash

cd "$(dirname "$0")"
cd ../..

docker build -t processing-raw-unit-test-img \
            -f ./dockerfile.raw-unittest .

echo "Starting container..."
docker run -it --rm \
     --name processing-raw-unit-test \
     processing-raw-unit-test-img

sleep 1


ERROR_CODE=$?

if [ ${ERROR_CODE} != 0 ]; then
    docker logs processing-raw-unit-test
    docker kill processing-raw-unit-test
    exit ${ERROR_CODE}
fi


if [ ${ERROR_CODE} = 0 ]; then
    echo "Test Processing Raw: OK"
fi