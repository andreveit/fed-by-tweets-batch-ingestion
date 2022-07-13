import utils
from utils import FilesLister
import json
import os

def load_json(filename):
    print(os.getcwd())
    with open('lambda-functions/utils/tests/data/' + filename, 'r') as file:
        return json.load(file)

def file_lister():
    return FilesLister('twitter-project-data-lake-andre')


def test_build_file_name():
    S3_BUCKET_NAME = 'some-bucket'
    S3_KEY_RAW = 'bronze/batch/tabular/tweets/'

    actual = utils.build_file_name(S3_BUCKET_NAME, S3_KEY_RAW)
    expected = 's3://some-bucket/bronze/batch/tabular/tweets/tweets.parquet'
    assert expected == actual
    


def test_remove_pref_suf():
    actual = utils.remove_pref_suf('/thats/a/test/')
    expected = 'thats/a/test'
    assert actual == expected



def test_select_keys():
    s3_key = 'bronze/batch/raw'
    objects = load_json('s3_objects.json')
    keys_list = [ i['Key'] for i in objects['Contents'] ]
    actual = file_lister()._select_keys(keys_list,s3_key)
    expected = load_json('test_select_keys.json')
    assert expected == actual

