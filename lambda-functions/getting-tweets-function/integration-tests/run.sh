#!/usr/bin/env bash

cd "$(dirname "$0")"

if [ "${LOCAL_IMAGE_NAME}" == "" ]; then 
    LOCAL_TAG=`date +"%Y-%m-%d-%H-%M"`
    export LOCAL_IMAGE_NAME="getting-tweets:${LOCAL_TAG}"
    echo "LOCAL_IMAGE_NAME is not set, building a new image with tag ${LOCAL_IMAGE_NAME}"
    docker build -t ${LOCAL_IMAGE_NAME} ..
else
    echo "no need to build image ${LOCAL_IMAGE_NAME}"
fi

docker run -d --rm --name gettingtweets \
    -p 8080:8080 \
    -e S3_BUCKET_NAME="twitter-project-data-lake-andre-testing" \
    -e S3_LANDING_LAYER="bronze" \
    -e S3_ACESS_KEY=$AWS_ACCESS_KEY_ID \
    -e S3_SECRET_KEY=$AWS_SECRET_ACCESS_KEY \
    -e BEARER_TOKEN=$BEARER_TOKEN \
    ${LOCAL_IMAGE_NAME}


ERROR_CODE=$?
if [ ${ERROR_CODE} != 0 ]; then
    exit ${ERROR_CODE}
fi



sleep 5

echo ""
echo "Runnig tests..."
python3 test_lambda.py

ERROR_CODE=$?

if [ ${ERROR_CODE} != 0 ]; then
    docker logs gettingtweets
    docker kill gettingtweets
    exit ${ERROR_CODE}
fi

docker kill gettingtweets