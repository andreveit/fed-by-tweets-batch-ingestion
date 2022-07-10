import boto3

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