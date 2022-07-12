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
    df.id = df.id.astype('string')
    df.full_name = df.full_name.astype('string')
    df.country = df.country.astype('string')
    df.place_type = df.place_type.astype('string')
    df.import_date = pd.to_datetime(df.import_date)
    df.file_name = df.file_name.astype('string')
    return df