import os
import sys
from time import sleep

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
FUNCTION_NAME = 'Users to Silver Lambda Function'

S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME', 'twitter-project-data-lake-andre-testing')
S3_KEY_SILVER = os.getenv('S3_KEY_SILVER','silver/users.parquet/')

filer_checker = LoadedFilesChecker(S3_BUCKET_NAME, [S3_KEY_SILVER]).init()


# TESTING RESPONSE FROM LAMBDA
print(f'\n\nTesting {FUNCTION_NAME}\n\n')
tester = LocalLambdaTester().run_asserts()


# CHECKING PROCESSED FILES ON S3
sleep(2)
filer_checker.run_asserts()


print('\n\n','-'*40)
print(f'{FUNCTION_NAME} status: OK.')
print('-'*40, '\n\n')