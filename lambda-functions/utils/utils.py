'''

This module contains utility functions to interact with AWS resorses and testing functions.


'''


import json
import requests
import boto3

PROD_BUCKET='twitter-project-data-lake-andre'



def build_file_name(bucket, s3_key):
    return 's3://' + bucket + '/' + s3_key + s3_key.split('/')[-2] +".parquet"


def remove_pref_suf(x):
    return '/'.join([i for i in x.split('/') if i != ""])


class FilesLister:
    '''
    List files in a given s3 key.
    '''
    
    def __init__(self, S3_BUCKET_NAME: str):
        self.S3_BUCKET_NAME = S3_BUCKET_NAME


    def _retrieve_objects(self):
        '''
        Get all objects from S3.
        '''
        s3_client = boto3.client('s3'
                            # ,aws_access_key_id = os.environ.get("S3_ACESS_KEY")
                            # ,aws_secret_access_key = os.environ.get("S3_SECRET_KEY")
                            )

        r = s3_client.list_objects(Bucket = self.S3_BUCKET_NAME)
        return r
    

    def _select_keys(self, keys_list, s3_key):
        '''
        Get objects that are inside th s3_key.
        '''
        selected_keys = []
        for key in keys_list:
            match_counter = 0
            for pat in s3_key.split('/'):
                if pat in key.split('/'):
                    match_counter += 1
                    
            if match_counter >= len(s3_key.split('/')):
                selected_keys.append(key)
    
        return selected_keys
    
    

    def list(self, s3_key: str):
        s3_key = remove_pref_suf(s3_key)
        objects = self._retrieve_objects()
        keys_list = [ i['Key'] for i in objects['Contents'] ]

        return self._select_keys(keys_list,s3_key)




class LoadedFilesChecker:
    '''
    Check if processed files were properly saved in S3.
    '''

    def __init__(self, bucket: str, s3_folders: list) -> None:
        self.bucket = bucket
        self.s3_folders = s3_folders
        self.client = boto3.client('s3')
        self.files_lister = FilesLister(bucket)


    def init(self):
        '''
        Memorize pre-existent files in s3 folders.
        '''
        self.memory = {}

        for folder in self.s3_folders:
            folder_objects = self.files_lister.list(folder)
            self.memory[folder] = folder_objects
         
        return self


    def run_asserts(self) -> None:
        self._assert_files()


    def cleanup(self) -> None:
        '''
        Delete all files from s3 folder.
        '''
        for folder in self.s3_folders:
            folder_objects = self.files_lister.list(folder)
            new_objects = [i for i in folder_objects if i not in self.memory[folder]]
            self.client.delete_objects(
                        Bucket=self.bucket,
                        Delete={'Objects': [{'Key': key} for key in new_objects]}
            )


    def _assert_files(self) -> None:
        '''
        Check if new files were loaded.
        '''
        for folder in self.s3_folders:
            folder_objects = self.files_lister.list(folder)
            new_objects = [i for i in folder_objects if i not in self.memory[folder]]
            print('\n',new_objects,'\n')
            assert len(new_objects) > 0, f'Processed files were not found.\nbucket: {self.bucket} - path: {folder}.'




class LocalLambdaTester:
    '''
    Triggers lambda functions on localhost and validates its response.
    '''

    URL = 'http://localhost:8080/2015-03-31/functions/function/invocations'

    def __init__(self, expected_response = None, event = None) -> None:
        expected_response_ = {
                'statusCode': 200
        }
        event_ = {
                'foo':'bar'
        }

        self.expected_response = expected_response or expected_response_
        self.event = event or event_


    def run_asserts(self):
        print('Triggering Lambda Function...')
        actual_response = requests.post(self.URL, json=self.event).json()
        print('\n\n',json.dumps(actual_response, indent=2))

        assert self.expected_response == actual_response, '[ERROR] Received unexpected response from Lambda.'



def get_database(bucket, layer):
    '''
    Return the proper DATABASE NAME according to the especified bucket.
    '''
    if 'testing' in bucket:
        return 'testing_' + layer

    elif 'staging' in bucket:
        return'staging_' + layer

    elif bucket == PROD_BUCKET:
        return layer

    else:
        raise ValueError(f"It's not possible to infer the DATABASE NAME through the bucker name {bucket}")