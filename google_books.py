from this import d
from xmlrpc.client import ResponseError
import requests
import os
import pandas as pd

GOOGLE_BOOKS_URL = "https://www.googleapis.com/books/v1/"
GOOGLE_API_KEY = os.environ["GOOGLE_API_KEY"]

class google_books:
    def __init__(self):
        pass

    def query_single_book(self, title: str, author: str) -> dict:
        query_root = f"{GOOGLE_BOOKS_URL}volumes?q="
        query = f"{query_root}intitle:{title}+inauthor:{author}&key={GOOGLE_API_KEY}"
        try:
            response = requests.get(query)
            response_dict = response.json()
        except:
            # TODO what is the specific type of error i should raise here?
            # TODO print more descriptive error message
            # TODO maybe give 'none' values for all attributes in this case, so that the
            # whole program doesn't break?
            raise ResponseError
            
        return self.__book_response_to_pandas(response_dict)

    def query_multiple_books(self, df_to_query: pd.DataFrame, title_col: str="title", author_col: str="author") -> pd.DataFrame:
        """
        Inputs
        ------
        df_to_query: pd.DataFrame
            Dataframe dictating the titles to be queried. Expected to contain a column with
            book titles, and a column with book authors. Extra columns are ignored.
        title_col: str
            Name of the column in df_input containing book titles.
        author_col: str
            Name of the column in df_input containing book authors.

        Returns
        -------
        df_plus_googlebooks: pd.DataFrame
            Copy of the input Dataframe `df_to_query`, with additional columns containing
            information returned from Google Books queries.
        """
        # TODO make author optional?

        assert title_col in df_to_query.columns
        assert author_col in df_to_query.columns

        # df_plus_googlebooks = df_to_query.copy()
        df_googlebooks = pd.DataFrame()

        for idx, row in df_to_query.iterrows():
            googlebook_info = self.query_single_book(row[title_col], row[author_col])
            df_googlebooks = df_googlebooks.append(googlebook_info, ignore_index=True)
        return pd.concat([df_to_query, df_googlebooks], axis=1)

    def __book_response_to_pandas(self, response_dict: dict) -> pd.Series:
        # TODO handle the case where response_dict doesn't return any matches
        # TODO move this validation to separate function?
        # check that the response matches our expectations
        assert response_dict["kind"] == "books#volumes"
        if response_dict.get("totalItems", 0) > 0:
            return pd.Series()

        if len(response_dict.get("items", []) == 0:
            return pd.Series()

        # assume that google searched well, and first match is the best match
        item = response_dict["items"][0]
        # volumeInfo contains the most interesting info that we care about
        item_info = item["volumeInfo"]

        # TODO check that title / author are "close enough" match

        series_info = pd.Series(item_info)

        # prefix each index with `googlebooks` for uniqueness against other data sources
        # which contain the same information
        series_info.rename("googlebooks_{}".format, inplace=True)
        return series_info

if __name__=="__main__":
    df = pd.DataFrame({"title": ["To Kill a Mockingbird", "Where the Red Fern Grows"], "author": ["Harper Lee", "Wilson Rawls"]})
    df_ = google_books().query_multiple_books(df)
    print(df_.head())