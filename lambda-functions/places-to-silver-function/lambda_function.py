import os
import logging
import pandas as pd
import awswrangler as wr
from helper_functions import filter_last_update, setup_datatypes
from utils import FilesLister, get_database

LAYER = 'silver'
TABLE = 'places'

S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME', 'twitter-project-data-lake-andre-testing')
S3_KEY_BRONZE = os.getenv('S3_KEY_BRONZE',f'bronze/batch/tabular/{TABLE}/')
S3_KEY_SILVER = os.getenv('S3_KEY_SILVER',f'{LAYER}/')


database = get_database(S3_BUCKET_NAME, LAYER)

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
    df = filter_last_update(df)
    
    
    # Setup datatypes
    df = setup_datatypes(df)

    logger.info('Dataset processed successfully.')
    
    
    
    # SAVE DATA TO SILVER LAYER
    
    wr.s3.to_parquet(
            df=df,
            path='s3://'+S3_BUCKET_NAME+'/'+S3_KEY_SILVER+TABLE+'.parquet',
            dataset=True,
            mode="overwrite",
            database=database,
            table=TABLE
    )
    logger.info(f'Table silver.{TABLE} saved successfully.')
    
    
    return {
        'statusCode': 200
    }
