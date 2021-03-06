import os
import sys

def add_utils_to_path():
    while True:
        if os.getcwd().split('/')[-1] == 'fed-by-tweets-batch-ingestion':
            break
        os.chdir('..')
    sys.path.append(os.path.join(os.getcwd(), 'lambda-functions/utils/'))

add_utils_to_path()
from utils import LoadedFilesChecker, LocalLambdaTester



# SETUP TEST

#**S3 acess keys should be on env
FUNCTION_NAME = 'Getting Tweets Lambda Function'
S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME', 'twitter-project-data-lake-andre-testing')


s3_folders = [
    'bronze/batch/raw/lula/',
    'bronze/batch/raw/bolsonaro/',
]
filer_checker = LoadedFilesChecker(S3_BUCKET_NAME, s3_folders).init()



# TESTING RESPONSE FROM LAMBDA
print(f'\n\nTesting {FUNCTION_NAME}\n\n')
tester = LocalLambdaTester().run_asserts()


# CHECKING PROCESSED FILES ON S3
filer_checker.run_asserts()


print('\n\n','-'*40)
print(f'{FUNCTION_NAME} status: OK.')
print('-'*40, '\n\n')



# import requests
# import json

# url = 'http://localhost:8080/2015-03-31/functions/function/invocations'

# expected_response = {
#         'statusCode': 200
#     }

# event = {
#     'foo':'bar'
# }

# print('Triggering getting-tweets lambda function...')
# actual_response = requests.post(url, json=event).json()

# print(json.dumps(actual_response, indent=2))

# assert expected_response == actual_response, 'Received unexpected response.'
# print('Getting Tweets Lambda function status: OK.')