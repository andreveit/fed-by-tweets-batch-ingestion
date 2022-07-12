import logging
import pandas as pd
import awswrangler as wr
from utils import FilesLister, build_file_name
from helper_functions import reorder_cols, setup_datatypes

TABLE = 'tweets'
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