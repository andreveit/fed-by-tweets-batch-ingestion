import pandas as pd


def reorder_cols(df_):
    df = df_.copy()
    del df_
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
    

def setup_datatypes(df_):
    df = df_.copy()
    del df_
    df.id = df.id.astype('int64')
    df.created_at = pd.to_datetime(df.created_at)
    df.author_id = df.author_id.astype('int64')
    df.text = df.text.astype('string')
    df.place_id = df.place_id.astype('string')
    df.subject = df.subject.astype('string')
    df.import_date = pd.to_datetime(df.import_date)
    df.file_name = df.file_name.astype('string')
    return df