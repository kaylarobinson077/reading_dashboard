from xmlrpc.client import ResponseError
import requests
import os
import pandas as pd

from reading_dashboard.postgres import postgres_to_pandas, append_to_postgres

GOOGLE_BOOKS_URL = "https://www.googleapis.com/books/v1/"
GOOGLE_API_KEY = os.environ["GOOGLE_API_KEY"]


class GoogleBooks:
    def __init__(self):
        self.postgres = GoogleBooksPostgres()
        self.api = GoogleBooksApi()

    def get(self, books: list[dict]) -> pd.DataFrame:
        """
        Get book information from cached data if possible, and the Google Books API for
        new books not found in the cached dataset.

        If new books are queried, their info is appended to the data cache.

        Parameters
        ----------
        books : list[dict]
            List of books to query, where each book to query is a dict with keys for the
            title and author

        Returns
        -------
        book_info : pd.DataFrame
            Google Books information for the input books list
        """
        pass

    def _get_cached(self, books: list[dict]) -> (pd.DataFrame, list[dict]):
        """
        Pull cached book info for any books in the list that we've seen before.

        Parameters
        ----------
        books : list[dict]
            List of books to query, where each book to query is a dict with keys for the
            title and author

        Returns
        -------
        cached_book_info : pd.DataFrame
            Matching books from the input list that were found in the cached database
        books_not_found : list[dict]
            Books from the input list that were not found in the cached database
        """
        # get cached books
        df_cached = self.postgres.get_cached_books()

        # limit to requested books, matching on title
        cached_book_info = df_cached[
            df_cached["title"].isin([x["title"] for x in books])
        ]

        # check the books that weren't found in the cache
        books_not_found = [
            book for book in books if book["title"] not in cached_book_info["title"]
        ]

        return cached_book_info, books_not_found

    def _get_new(self, books: list[dict]) -> pd.DataFrame:
        """
        For new books not found in the cache, get their info from the Google Books API
        and add the book's information to the cached database.

        Parameters
        ----------
        books : list[dict]
            List of books to query, where each book to query is a dict with keys for the
            title and author

        Returns
        -------
        queried_book_info : pd.DataFrame
            Info for the books from the input list returned by the Google Books API
        """
        queried_book_info = self.api.query_multiple_books(books)
        append_to_postgres(queried_book_info, "google_books")
        return queried_book_info


class GoogleBooksPostgres:
    def get_cached_books() -> pd.DataFrame:
        return postgres_to_pandas("google_books")

    def cache_book(row):
        append_to_postgres(row, "google_books")


class GoogleBooksApi:
    def query_single_book(self, title: str, author: str) -> dict:
        query_root = f"{GOOGLE_BOOKS_URL}volumes?q="
        query = f"{query_root}intitle:{title}+inauthor:{author}&maxResults=1&key={GOOGLE_API_KEY}"
        try:
            response = requests.get(query)
            assert response.status_code == 200
            response_dict = response.json()
        except:
            if response.status_code == 429:
                raise RuntimeError("API said we exceeded hits for today :(")
            # TODO what is the specific type of error i should raise here?
            # TODO print more descriptive error message
            # TODO maybe give 'none' values for all attributes in this case, so that the
            # whole program doesn't break?
            raise ResponseError

        if not (response_dict.get("totalItems", 0) > 0):
            # raise Warning(f"Bad response for totalItems")
            print("totalItems too small")
            return {}

        if len(response_dict.get("items", [])) == 0:
            # raise Warning(f"Bad response, items empty")
            print("items is empty")
            return {}

        # assume that google searched well, and first match is the best match
        item = response_dict["items"][0]
        # volumeInfo contains the most interesting info that we care about
        item_info = item["volumeInfo"]

        return item_info

    def query_multiple_books(
        self,
        df_to_query: pd.DataFrame,
        title_col: str = "title",
        author_col: str = "author",
    ) -> pd.DataFrame:
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
        # df_googlebooks = pd.DataFrame()
        googlebooks_responses = []
        for idx, row in df_to_query.iterrows():
            # print(row[title_col])
            googlebook_info = self.query_single_book(row[title_col], row[author_col])
            googlebooks_responses += [googlebook_info]
            # add columns to df if any new fields
        #     new_cols = [x for x in googlebook_info.keys() if x not in list(df_googlebooks.columns)]
        #     if new_cols and list(df_googlebooks.columns):
        #         df_googlebooks = df_googlebooks.reindex(columns = list(df_googlebooks.columns) + new_cols)
        #     elif new_cols:
        #         df_googlebooks = df_googlebooks.reindex(columns = new_cols)

        #     df_googlebooks = df_googlebooks.append(googlebook_info, ignore_index=True)
        # print(df_googlebooks.head())
        # df_googlebooks
        df_googlebooks = pd.DataFrame.from_dict(googlebooks_responses).add_prefix(
            "googlebooks_"
        )
        return pd.concat([df_to_query, df_googlebooks], axis=1)
        # series_info.rename("googlebooks_{}".format, inplace=True).add_

    def __book_response_to_pandas(self, response_dict: dict) -> pd.Series:
        # TODO handle the case where response_dict doesn't return any matches
        # TODO move this validation to separate function?
        # check that the response matches our expectations
        # assert response_dict["kind"] == "books#volumes"
        if not (response_dict.get("totalItems", 0) > 0):
            # raise Warning(f"Bad response for totalItems")
            return pd.Series([], dtype=object)

        if len(response_dict.get("items", [])) == 0:
            # raise Warning(f"Bad response, items empty")
            return pd.Series([], dtype=object)

        # assume that google searched well, and first match is the best match
        item = response_dict["items"][0]
        # volumeInfo contains the most interesting info that we care about
        item_info = item["volumeInfo"]

        # TODO check that title / author are "close enough" match

        series_info = pd.Series(item_info)

        # prefix each index with `googlebooks` for uniqueness against other data sources
        # which contain the same information
        series_info.rename("googlebooks_{}".format, inplace=True)
        # print(series_info)
        return series_info


if __name__ == "__main__":
    df = pd.DataFrame(
        {
            "title": ["To Kill a Mockingbird", "Where the Red Fern Grows"],
            "author": ["Harper Lee", "Wilson Rawls"],
        }
    )
    df_ = GoogleBooksApi().query_multiple_books(df)
    print(df_.head())
