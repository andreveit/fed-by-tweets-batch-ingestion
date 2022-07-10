import os
from datetime import datetime, timedelta

import boto3
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.sensors.python import PythonSensor
from ingestion.apis import RecentAPI
from ingestion.ingestors import BatchIngestor
from ingestion.writers import FileWriter, S3Writer


S3_LOCATION = 'test/RecentAPI'





# SENSOR Helper Function Definition
def retrieve_objects():
    s3_client = boto3.client('s3',
                            aws_access_key_id = os.environ.get("S3_ACESS_KEY"),
                            aws_secret_access_key = os.environ.get("S3_SECRET_KEY"))
    r = s3_client.list_objects(Bucket = os.environ.get("S3_BUCKET_NAME"))
    return r

def select_keys(keys_list, pattern):
    selected_keys = []
    for key in keys_list:
        match_counter = 0
        for pat in pattern.split('/'):
            if pat in key.split('/'):
                match_counter += 1
                
        if match_counter >= len(pattern.split('/')):
            selected_keys.append(key)

    return selected_keys


def check_file():

    pattern = os.environ.get("S3_LANDING_LAYER") + '/' + S3_LOCATION

    r = retrieve_objects()
    keys_list = [ i['Key'] for i in r['Contents'] ]

    selected_keys = select_keys(keys_list, pattern)

    keys_ix = [ix for ix,key in enumerate(keys_list) if key in selected_keys  ]
    last_modifieds = [r['Contents'][i]['LastModified'] for i in keys_ix]

    for time in last_modifieds:
        if (datetime.utcnow().date() == time.date()):
            return True
        else:
            return False





# PULL_DATA Helper Function Definition
def pull_data_func():
    
    query_params = {
                    'query': 'from: elonmusk',
                    'user.fields':'id,location,name,public_metrics,created_at',
                    'tweet.fields': 'author_id',
                    'max_results':'10'
                    }
    
    BatchIngestor(query_params,
                1,
                RecentAPI,
                S3_LOCATION,
                S3Writer).ingest()







# DAG Definition
default_args = default_args={
        'depends_on_past': False,
        'email': ['andre.veit@gmail.com'],
        'email_on_failure': True,
        'email_on_retry': False,
        'retries': 3,
        'retry_delay': timedelta(minutes=15),

    }

with DAG('igestion_data_dag',
        default_args=default_args,
        description='Pull tweets from RecentAPI and process throug DataLake all the way to Silver layer.',
        schedule_interval=timedelta(days=1),
        start_date=datetime(2022, 4, 1),
        catchup=False,
        tags=['ingestion']
        ) as dag:



    pull_data = PythonOperator(
        task_id = 'pull_data',
        python_callable  = pull_data_func

    )

 
    check_s3_file = PythonSensor(
        task_id='check_s3_file',
        poke_interval=300,
        timeout=1000,
        mode="reschedule",
        python_callable=check_file
)
    
    
pull_data >> check_s3_file
