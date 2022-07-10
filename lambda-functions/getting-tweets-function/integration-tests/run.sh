#!/usr/bin/env bash

cd "$(dirname "$0")"

if [ "${LOCAL_IMAGE_NAME}" == "" ]; then 
    LOCAL_TAG=`date +"%Y-%m-%d-%H-%M"`
    export LOCAL_IMAGE_NAME="getting-tweets:${LOCAL_TAG}"
    echo "LOCAL_IMAGE_NAME is not set, building a new image with tag ${LOCAL_IMAGE_NAME}"
    sudo docker build -t ${LOCAL_IMAGE_NAME} ..
else
    echo "no need to build image ${LOCAL_IMAGE_NAME}"
fi

sudo docker run -d --rm --name gettingtweets \
    -p 8080:8080 \
    -e S3_BUCKET_NAME="twitter-project-misc" \
    -e S3_LANDING_LAYER="tests" \
    ${LOCAL_IMAGE_NAME}



sleep 5

echo "Runnig tests..."
python3 test_lambda.py

ERROR_CODE=$?

if [ ${ERROR_CODE} != 0 ]; then
    docker logs gettingtweets
    docker kill gettingtweets
    exit ${ERROR_CODE}
fi

docker kill gettingtweets