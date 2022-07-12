import logging
import pandas as pd
import awswrangler as wr
from utils import FilesLister, build_file_name

TABLE = 'tweets'
S3_BUCKET_NAME = 'twitter-project-data-lake-andre'
S3_KEY_BRONZE = f'bronze/batch/tabular/{TABLE}/'
S3_KEY_SILVER = 'silver/'


logger = logging.getLogger()
logger.setLevel(logging.INFO)




def reorder_cols(df):
    cols_order = ['id'
        ,'created_at'
        ,'author_id'
        ,'text'
        ,'place_id'
        ,'subject'
        ,'import_date'
        ,'file_name'
    ]
    
    return df[cols_order]
    
def setup_datatypes(df):
    df.id = df.id.astype('int64')
    df.created_at = pd.to_datetime(df.created_at)
    df.author_id = df.author_id.astype('int64')
    df.text = df.text.astype('string')
    df.place_id = df.place_id.astype('string')
    df.subject = df.subject.astype('string')
    df.import_date = pd.to_datetime(df.import_date)
    df.file_name = df.file_name.astype('string')
    return df


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
