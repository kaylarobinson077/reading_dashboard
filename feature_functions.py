import pandas as pd

def num_pages(first_page: pd.Series, last_page: pd.Series) -> pd.Series:
    num_pages = last_page - first_page
    return num_pages

def is_finished(progress: pd.Series[str]) -> pd.Series[bool]:
    return progress == "100%"

def days_to_finish(started_on: pd.Series[str], finished_on: pd.Series[str]) -> pd.Series[float]:

    # cast both series to datetime type
    started_on = pd.to_datetime(started_on)
    finished_on = pd.to_datetime(finished_on)

    # take the difference, then cast to int of number of days
    time_to_finish = finished_on - started_on
    
    return time_to_finish.days