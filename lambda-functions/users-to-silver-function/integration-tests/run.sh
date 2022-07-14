#!/usr/bin/env bash

cd "$(dirname "$0")"

cd ../..

if [ "${LOCAL_IMAGE_NAME}" == "" ]; then 
    LOCAL_TAG=`date +"%Y-%m-%d-%H-%M"`
    export LOCAL_IMAGE_NAME="userstosilver:${LOCAL_TAG}"
    echo "LOCAL_IMAGE_NAME is not set, building a new image with tag ${LOCAL_IMAGE_NAME}"
    
    docker build -t ${LOCAL_IMAGE_NAME} -f ./dockerfile.usersilv-inttest .


else
    echo "No need to build image ${LOCAL_IMAGE_NAME}"
fi


docker run -d --rm -it --name userstosilver \
    -p 8080:8080 \
    -e AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID \
    -e AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY \
    -e AWS_DEFAULT_REGION="sa-east-1" \
    ${LOCAL_IMAGE_NAME}


sleep 5

echo ""
echo "Runnig tests..."
python3 ./users-to-silver-function/integration-tests/test_lambda.py

ERROR_CODE=$?

if [ ${ERROR_CODE} != 0 ]; then
    docker logs userstosilver
    docker kill userstosilver
    exit ${ERROR_CODE}
fi

docker kill userstosilver