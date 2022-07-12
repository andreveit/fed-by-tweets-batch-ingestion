import pandas as pd

def filter_last_update(df_):
    df = df_.copy()
    del df_
    df = df.sort_values('import_date', ascending = False)
    df['latest'] = df.groupby('id').cumcount()
    df = df[df.latest == 0].drop(columns=['latest'])
    return df


def setup_datatypes(df_):
    df = df_.copy()
    del df_
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
    return df