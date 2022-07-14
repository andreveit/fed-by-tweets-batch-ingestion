import os
import logging
import awswrangler as wr
from utils import FilesLister, build_file_name, get_database
from helper_functions import reorder_cols, setup_datatypes

LAYER = 'silver'
TABLE = 'tweets'

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
    
    # Subject Column
    df['subject'] = df.file_name.apply(lambda x: x.split('/')[0])
    
    # Drop duplicates
    df = df.drop_duplicates(subset=['id', 'subject'])
    
    # Reorder columns
    df = reorder_cols(df)

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
    logger.info(f'Table {LAYER}.{TABLE} saved successfully.')
    
    
    return {
        'statusCode': 200
    }
