import logging
import awswrangler as wr
from processing import Processor
from utils import build_file_name

INTERVAL = 4 # Processing interval

S3_BUCKET_NAME = 'twitter-project-data-lake-andre'
S3_KEY_RAW = 'bronze/batch/raw/'
S3_KEY_TABULAR_TWEETS = 'bronze/batch/tabular/tweets/'
S3_KEY_TABULAR_PLACES = 'bronze/batch/tabular/places/'
S3_KEY_TABULAR_USERS = 'bronze/batch/tabular/users/'


def lambda_handler(event, context):
    tweets, places, users = Processor(S3_BUCKET_NAME, S3_KEY_RAW, INTERVAL).get_dataframes()
    
    # Write on S3
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    
    wr.s3.to_parquet(
            df=tweets,
            path=build_file_name(S3_BUCKET_NAME, S3_KEY_TABULAR_TWEETS),
            dataset=True,
            mode="append",
            database="bronze",
            table="tweets"
    )
    logger.info('Table bronze.tweets saved successfully.')
    
    
    wr.s3.to_parquet(
            df=places,
            path=build_file_name(S3_BUCKET_NAME, S3_KEY_TABULAR_PLACES),
            dataset=True,
            mode="append",
            database="bronze",
            table="places"
    )
    logger.info('Table bronze.places saved successfully.')
    
    
    wr.s3.to_parquet(
            df=users,
            path=build_file_name(S3_BUCKET_NAME, S3_KEY_TABULAR_USERS),
            dataset=True,
            mode="append",
            database="bronze",
            table="users"
    )
    logger.info('Table bronze.users saved successfully.')
    
    
    reponse = {
        'statusCode': 200
    }
    return reponse

    
