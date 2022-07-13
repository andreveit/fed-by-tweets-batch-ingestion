import logging
import os
import awswrangler as wr
from processing import Processor
from utils import build_file_name, get_database

PROCESSING_INTERVAL = os.getenv('PROCESSING_INTERVAL',4)

S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME', 'twitter-project-data-lake-andre-testing')
S3_KEY_RAW = os.getenv('S3_KEY_RAW', 'bronze/batch/raw/')
S3_KEY_TABULAR_TWEETS = os.getenv('S3_KEY_TABULAR_TWEETS','bronze/batch/tabular/tweets/')
S3_KEY_TABULAR_PLACES = os.getenv('S3_KEY_TABULAR_PLACES','bronze/batch/tabular/places/')
S3_KEY_TABULAR_USERS = os.getenv('S3_KEY_TABULAR_USERS','bronze/batch/tabular/users/')

LAYER = 'bronze'
database = get_database(S3_BUCKET_NAME, LAYER)





def lambda_handler(event, context):
    tweets, places, users = Processor(S3_BUCKET_NAME, S3_KEY_RAW, PROCESSING_INTERVAL).get_dataframes()
    
    # Write on S3
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    
    wr.s3.to_parquet(
            df=tweets,
            path=build_file_name(S3_BUCKET_NAME, S3_KEY_TABULAR_TWEETS),
            dataset=True,
            mode="append",
            database=database,
            table="tweets"
    )
    logger.info(f'Table {database}.tweets saved successfully.')
    
    
    wr.s3.to_parquet(
            df=places,
            path=build_file_name(S3_BUCKET_NAME, S3_KEY_TABULAR_PLACES),
            dataset=True,
            mode="append",
            database=database,
            table="places"
    )
    logger.info(f'Table {database}.places saved successfully.')
    
    
    wr.s3.to_parquet(
            df=users,
            path=build_file_name(S3_BUCKET_NAME, S3_KEY_TABULAR_USERS),
            dataset=True,
            mode="append",
            database=database,
            table="users"
    )
    logger.info(f'Table {database}.users saved successfully.')
    
    
    reponse = {
        'statusCode': 200
    }
    return reponse

    
