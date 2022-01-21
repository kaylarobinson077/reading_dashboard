import pandas as pd

def num_pages(first_page: pd.Series, last_page: pd.Series) -> pd.Series:
    num_pages = last_page - first_page
    return num_pages

def is_finished(progress: pd.Series) -> pd.Series:
    return progress == "100%"

def days_to_finish(started_on: pd.Series, last_read_on: pd.Series) -> pd.Series:

    # cast both series to datetime type
    started_on = pd.to_datetime(started_on)
    last_read_on = pd.to_datetime(last_read_on)

    # take the difference, then cast to int of number of days
    days_to_finish = last_read_on - started_on

    return days_to_finish.dt.days
