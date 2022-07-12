import pandas as pd
from helper_functions import filter_last_update, setup_datatypes

BASE_PATH = 'lambda-functions/places-to-silver-function/unit-tests/data/'



def test_filter_last_update():
    expected = pd.read_parquet(BASE_PATH + 'filtered_places.snappy.parquet')
    
    df = pd.read_parquet(BASE_PATH + 'places_sample_data.snappy.parquet')
    actual = filter_last_update(df)

    pd.testing.assert_frame_equal(expected, actual)



def test_setup_datatypes():
    expected = pd.read_pickle(BASE_PATH + 'dtypes.pkl')

    df = pd.read_parquet(BASE_PATH + 'filtered_places.snappy.parquet')
    actual = setup_datatypes(df).dtypes

    pd.testing.assert_series_equal(expected,actual)