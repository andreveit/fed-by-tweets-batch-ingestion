from secrets import get_secrets
import os
from ingestion.apis import RecentAPI
from ingestion.ingestors import BatchIngestor
from ingestion.writers import S3Writer


get_secrets()
print('S3_ACESS_KEY = ',os.getenv('S3_ACESS_KEY'))
print('S3_SECRET_KEY = ',os.getenv('S3_SECRET_KEY'))

def lambda_handler(event, context):
    
    query_params = {
                'query': 'lula OR "Luiz Inacio" OR "Luíz Inácio" - is:retweet',
                'user.fields':'name,username,public_metrics,location,verified',
                'tweet.fields': 'created_at,geo',
                'place.fields':'full_name,name,place_type,country,geo',
                'expansions':'author_id,geo.place_id',
                'max_results':'100'
    }
    
    
    BatchIngestor(query_params,
                    6,
                    RecentAPI,
                    'batch/raw/lula',
                    S3Writer
                ).ingest()
    
    


    query_params = {
                'query': 'bolsonaro OR "Jair Bolsonaro" - is:retweet',
                'user.fields':'name,username,public_metrics,location,verified',
                'tweet.fields': 'created_at,geo',
                'place.fields':'full_name,name,place_type,country,geo',
                'expansions':'author_id,geo.place_id',
                'max_results':'100'
    }
    
    
    BatchIngestor(query_params,
                    6,
                    RecentAPI,
                    'batch/raw/bolsonaro',
                    S3Writer
                ).ingest()



    reponse = {
        'statusCode': 200
    }
    return reponse
