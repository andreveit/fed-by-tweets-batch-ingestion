import logging
import pandas as pd
import awswrangler as wr
from utils import FilesLister, build_file_name

TABLE = 'users'
S3_BUCKET_NAME = 'twitter-project-data-lake-andre'
S3_KEY_BRONZE = f'bronze/batch/tabular/{TABLE}/'
S3_KEY_SILVER = 'silver/'



logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    
    # LOAD DATA

    files = FilesLister(S3_BUCKET_NAME).list(S3_KEY_BRONZE)
    files = ['s3://'+S3_BUCKET_NAME+'/'+i for i in files]
    df = wr.s3.read_parquet(files)
    logger.info('Loaded files successfully.')

    
    
    # APPLY TRANSFORMATIONS
    
    # Filter latest update
    df = df.sort_values('import_date', ascending = False)
    df['latest'] = df.groupby('id').cumcount()
    df = df[df.latest == 0].drop(columns=['latest'])
    
    
    # Setup datatypes
    df.id = df.id.astype('int64')
    df.username = df.username.astype('string')
    df.name = df.name.astype('string')
    df.location = df.location.astype('string')
    df.followers_count = df.followers_count.astype('int32')
    df.following_count = df.following_count.astype('int32')
    df.listed_count = df.listed_count.astype('int32')
    df.tweet_count = df.tweet_count.astype('int32')
    df.verified = df.verified.astype(bool)
    df.import_date = pd.to_datetime(df.import_date)
    df.file_name = df.file_name.astype('string')

    logger.info('Dataset processed successfully.')
    
    
    
    # SAVE DATA TO SILVER LAYER
    
    wr.s3.to_parquet(
            df=df,
            path=build_file_name(S3_BUCKET_NAME, S3_KEY_SILVER + TABLE),
            dataset=True,
            mode="overwrite",
            database="silver",
            table=TABLE
    )
    logger.info(f'Table silver.{TABLE} saved successfully.')
    
    
    return {
        'statusCode': 200
    }
