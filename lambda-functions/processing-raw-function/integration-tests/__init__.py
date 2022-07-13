import os
import sys

print('word from __init__1')

def add_utils_to_path():
    while True:
        if os.getcwd().split('/')[-1] == 'fed-by-tweets-batch-ingestion':
            break
        os.chdir('..')
    sys.path.append(os.path.join(os.getcwd(), 'lambda-functions/utils/'))

add_utils_to_path()

print('word from __init__2')