import pandas as pd
import importlib
from pathlib import Path
from hamilton import driver
from google_books import google_books


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

def load_leio_data():
    book_data_loc = DATA_LOC / "leio_data.csv"
    leio_data = pd.read_csv(book_data_loc)
    return rename_leio_cols(leio_data)

def append_googlebooks_data(df):
    gb = google_books()
    return gb.query_multiple_books(df)


def rename_leio_cols(df):
    mapping = {
        "Title": "title",
        "Author": "author",
        "First Page": "first_page",
        "Last Page": "last_page",
        "Next Page": "next_page",
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

    leio_data = load_leio_data()
    leio_googlebooks = append_googlebooks_data(leio_data)
    initial_columns = leio_googlebooks.to_dict("series")
    return initial_columns

def drop_bad_rows(df):

    # negative number of pages
    if "num_pages" in df.columns:
        df.drop(df[df["num_pages"]<0].index, inplace=True)

    return df

def get_processed_data():

    # load and clean data
    initial_columns = get_initial_columns()

    module_name = "feat_eng_functions"
    module = importlib.import_module(module_name)
    dr = driver.Driver(initial_columns, module)

    output_columns = [
        "title",
        "num_pages",
        "is_finished",
        "time_to_finish",
        "time_read",
        "genre"
    ]

    feats = dr.execute(output_columns)
    feats = drop_bad_rows(feats)

    print(feats["genre"].unique)

    return feats

if __name__=="__main__":
    get_processed_data()