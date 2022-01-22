import pandas as pd
import os
import requests

GOOGLE_BOOKS_URL = "https://www.googleapis.com/books/v1/"
GOOGLE_API_KEY = os.environ["GOOGLE_API_KEY"]

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

def genre(title: pd.Series, author: pd.Series) -> list:
    
    genres = []

    for i in range(title.shape[0]):
        query_root = f"{GOOGLE_BOOKS_URL}volumes?q="
        query = f"{query_root}intitle:{title[i]}+inauthor:{author[i]}&key={GOOGLE_API_KEY}"
        response = requests.get(query)
        data = response.json()

        if "items" in data:
            first_match = data.get("items", None)[0]
        else:
            genres.append(None)
            continue

        if "volumeInfo" in first_match:
            categories = first_match["volumeInfo"].get("categories", None)
        else:
            genres.append(None)
            continue

        if categories is not None:
            genres.append(categories[0])
        else:
            genres.append(None)
        
