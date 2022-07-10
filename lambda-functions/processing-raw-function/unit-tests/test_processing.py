from jinja2 import pass_context
import pytest
import json
import pandas as pd
import numpy as np
from processing import Parser, Processor
from datetime import datetime


class ParserMock(Parser):
    def _load_file(self):
        with open('tests/data/sample_tweet_file.json', 'r') as file:
            self.file = json.load(file)

def standardize(df):
    df = df.fillna(value=np.nan)
    for col in df.columns.tolist():
        df[col] = df[col].astype(str)
    return df.drop(columns = ['import_date'])


@pytest.fixture
def parser_mock():
    return ParserMock('my-bucket', 'bronze/batch/raw/')

@pytest.fixture
def processor_mock():
    return Processor('my-bucket', 'bronze/batch/raw/', )


def test_parse_tweets(parser_mock):
    expected = standardize(pd.read_csv('tests/data/expected_parse_tweets.csv'))
    actual = standardize(parser_mock._parse_tweets())

    pd.testing.assert_frame_equal(expected, actual)


def test_parse_places(parser_mock):
    expected = standardize(pd.read_csv('tests/data/expected_parse_places.csv'))
    actual = standardize(parser_mock._parse_places())

    pd.testing.assert_frame_equal(expected, actual)

def test_parse_users(parser_mock):
    expected = standardize(pd.read_csv('tests/data/expected_parse_users.csv'))
    actual = standardize(parser_mock._parse_users())

    pd.testing.assert_frame_equal(expected, actual)


def test_get_file_date():
    actual = Processor.get_file_date('2022-06-19-22_30.json')
    expected = datetime(2022,6,19,22,30)
    assert actual == expected

def test_select_files():
    pass

def test_get_dataframes():
    pass