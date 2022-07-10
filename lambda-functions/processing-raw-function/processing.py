import logging
import json
from datetime import datetime, timedelta
import string
import pandas as pd
import boto3
from utils import FilesLister, remove_pref_suf 

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class Parser:
    '''
    Parses Recent API response.
    '''
    
    def __init__(self, bucket: string, s3_key: string):
        self.bucket = bucket
        self.s3_key = s3_key
        self.file_name = '/'.join(self.s3_key.split('/')[-2:])
        self._load_file()


    def _load_file(self):
        s3_client = boto3.client('s3')
        self.file = s3_client.get_object(Bucket = self.bucket, Key = self.s3_key)['Body'].read()
        self.file =  json.loads(self.file)


    def _parse_tweets(self):
        tweets_dict = {
            'id' : [],
            'created_at' : [],
            'author_id' : [],
            'text' : [],
            'place_id' : []
        }

        for pag in self.file['data']:
            for tweet_num in pag['data']:
                for k in list(tweets_dict.keys()):
                    try:
                        if k == 'place_id':
                            field = tweet_num['geo'][k]
                        else:
                            field = tweet_num[k]
                                
                        tweets_dict[k].append(field)
                        
                    except:
                        tweets_dict[k].append(None)


        df_tweets = pd.DataFrame(tweets_dict)
        df_tweets['import_date'] = datetime.now()
        df_tweets['file_name'] = self.file_name

        return df_tweets




    def _parse_places(self):
        places_dict = {
            'id' : [],
            'full_name' : [],
            'country' : [],
            'place_type' : []
        }

        for pag in self.file['data']:
            try:
                for place_num in pag['includes']['places']:
                    for k in list(places_dict.keys()):
                        try:
                            places_dict[k].append(place_num[k])
                        except:
                            places_dict[k].append(None)
            except:
                pass

        df_places = pd.DataFrame(places_dict)
        df_places['import_date'] = datetime.now()
        df_places['file_name'] = self.file_name

        return df_places




    def _parse_users(self):
        users_dict = {
            'id' : [],
            'username' : [],
            'name' : [],
            'location' : [],
            'followers_count' : [],
            'following_count' : [],
            'listed_count' : [],
            'tweet_count' : [],
            'verified' : [],
        }

        public_metrics = ['followers_count', 'following_count', 'listed_count', 'tweet_count']

        for pag in self.file['data']:
            try:
                for user_num in pag['includes']['users']:
                    for k in list(users_dict.keys()):
                        try:
                            if k in public_metrics:
                                field = user_num['public_metrics'][k]
                            else:
                                field = user_num[k]
                                    
                            users_dict[k].append(field)
                            
                        except:
                            users_dict[k].append(None)
            except:
                pass

        df_users = pd.DataFrame(users_dict)
        df_users['import_date'] = datetime.now()
        df_users['file_name'] = self.file_name

        return df_users


    def get_dataframes(self):
        '''
        Returns parsed DFs: df_tweets, df_places, df_users.
        '''
        return [self._parse_tweets(), self._parse_places(), self._parse_users()]







class Processor:
    def __init__(self, bucket, s3_key, interval):
        self.interval = interval
        self.bucket = remove_pref_suf(bucket)
        self.s3_key = remove_pref_suf(s3_key)
        

    @staticmethod
    def get_file_date(file):
        '''
        Retrurns datetime object based on the file name.
        '''

        file = file.split('/')[-1]
        date = file.split('.')[0].split('-')[:3]
        date = [int(i) for i in date]

        time = file.split('.')[0].split('-')[-1].split('_')
        time = [int(i) for i in time]

        return datetime(date[0], date[1], date[2], time[0], time[1])




    def _select_files(self):
        '''
        Select files to be processed based on the ingestion time and interval definition.
        '''
        files = FilesLister(self.bucket).list(self.s3_key)

        selected_files = []
        for file in files:
            file_time = Processor.get_file_date(file)

            # Check processing condition
            dead_line = datetime.now() - timedelta(hours=self.interval)
            logger.debug(f'Check processing condition file_time: {file_time}  -  dead_line: {dead_line}  -  assert: {file_time > dead_line}' )
            if file_time > dead_line:
                selected_files.append(file)
                logging.info(f'File added to processing list:  {file_time}  -  ingested on: {file_time}' )

        return selected_files




    def get_dataframes(self):
        dfs_list_collection = [[],[],[]]
        
        if self._select_files() == []:
            logger.info('No files to be processed. Check out the processing interval set.')
            return [], [], []
        
        for file in self._select_files():
            for dfs_list, df in zip(dfs_list_collection, Parser(self.bucket, file).get_dataframes()):           
                dfs_list.append(df)

        tweets = pd.concat(dfs_list_collection[0])
        places = pd.concat(dfs_list_collection[1])
        users = pd.concat(dfs_list_collection[2])
        
        logger.info(f'Data Processed successfully!\n tweets shape: {tweets.shape}   -   places shape: {places.shape}   -   users shape: {users.shape}')

        return tweets, places, users
