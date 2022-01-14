import pandas as pd
import importlib
from pathlib import Path
from hamilton import driver

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
    return df.rename(mapping)

def main():

    # load and clean data
    book_data = load_book_data()
    book_data = rename_cols(book_data)

    module_name = "feature_functions"
    module = importlib.import_module(module_name)
    dr = driver.Driver(book_data, module)

    output_columns = [
        "num_pages",
        "is_finished",
        "days_to_finish"
    ]

    feats = dr.execute(output_columns)
    prinnt(df)

if __name__ == "__main__":
    main()