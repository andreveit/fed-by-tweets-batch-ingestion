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
FUNCTION_NAME = 'Processing Raw Lambda Function'

S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME', 'twitter-project-data-lake-andre-testing')
S3_KEY_TABULAR_TWEETS = os.getenv('S3_KEY_TABULAR_TWEETS','bronze/batch/tabular/tweets/')
S3_KEY_TABULAR_PLACES = os.getenv('S3_KEY_TABULAR_PLACES','bronze/batch/tabular/places/')
S3_KEY_TABULAR_USERS = os.getenv('S3_KEY_TABULAR_USERS','bronze/batch/tabular/users/')


s3_folders = [
    S3_KEY_TABULAR_TWEETS,
    S3_KEY_TABULAR_PLACES,
    S3_KEY_TABULAR_USERS
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