import pandas as pd
import os


def num_pages(first_page: pd.Series, last_page: pd.Series) -> pd.Series:
    num_pages = last_page - first_page
    return num_pages

def is_finished(progress: pd.Series) -> pd.Series:
    return progress == "100%"

def time_to_finish(started_on: pd.Series, last_read_on: pd.Series) -> pd.Series:

    # cast both series to datetime type
    started_on = pd.to_datetime(started_on)
    last_read_on = pd.to_datetime(last_read_on)

    return last_read_on - started_on

def time_read(time_read: pd.Series) -> pd.Series:
    return pd.to_datetime(time_read)


        
