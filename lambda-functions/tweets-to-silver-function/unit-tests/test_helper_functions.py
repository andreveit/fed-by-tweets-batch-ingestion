import pandas as pd
from helper_functions import reorder_cols, setup_datatypes

BASE_PATH = 'lambda-functions/tweets-to-silver-function/unit-tests/data/'

def get_inputdata(filename):
    return pd.read_parquet(BASE_PATH + filename)


def test_reorder_cols():
    expected = [
        'id',
        'created_at',
        'author_id',
        'text',
        'place_id',
        'subject',
        'import_date',
        'file_name'
    ]
    
    df = get_inputdata('input_sample.snappy.parquet')
    actual = reorder_cols(df).columns.tolist()

    assert expected == actual



def test_setup_datatypes():
    expected = pd.read_pickle(BASE_PATH + 'dtypes.pck')
    print(expected)

    df = get_inputdata('input_right_order_sample.snappy.parquet')
    actual = setup_datatypes(df).dtypes

    pd.testing.assert_series_equal(expected, actual)