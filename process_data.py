import pandas as pd
import importlib
from pathlib import Path
from hamilton import driver
import streamlit as st

DATA_LOC = Path("data")

"""
Book-level features

Brainstorm of interesting features to add

From existing data
------------------
- num_pages
- days_to_finish
- time_read

From external sources
---------------------
- genre
- gender of author
- some measure of popularity
    - copies sold?
    - bestseller status?
- years since first published
- how many books the author has published
- average rating
"""

def load_book_data():
    book_data_loc = DATA_LOC / "leio_data.csv"
    book_data = pd.read_csv(book_data_loc)
    return book_data

def rename_cols(df):
    mapping = {
        "Title": "title",
        "Author": "author",
        "First Page": "first_page",
        "Next Page": "last_page",
        "Progress": "progress",
        "Started On": "started_on",
        "Last Read On": "last_read_on",
        "Archived On": "archived_on",
        "Time Read": "time_read",
        "Reading Sessions": "num_sessions",
        "Pages/Session": "pages_per_session",
        "Time/Session": "time_per_session",
        "Time/Page": "time_per_pages",
    }
    return df.rename(mapping,  axis="columns")

def get_initial_columns():

    book_data = load_book_data()
    book_data = rename_cols(book_data)
    initial_columns = book_data.to_dict("series")
    return initial_columns

@st.cache
def get_processed_data():

    # load and clean data
    initial_columns = get_initial_columns()
    print(initial_columns)

    module_name = "feature_functions"
    module = importlib.import_module(module_name)
    dr = driver.Driver(initial_columns, module)

    output_columns = [
        "title",
        "num_pages",
        "is_finished",
        "days_to_finish"
    ]

    feats = dr.execute(output_columns)
    return feats
