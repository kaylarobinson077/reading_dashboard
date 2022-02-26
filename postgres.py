# import the relevant sql library
from sqlalchemy import create_engine
import pandas as pd

DATABASE_URL = "postgresql://xxx"


def postgres_to_pandas(table_name: str):
    engine = create_engine(DATABASE_URL, echo=False)
    return pd.read_sql_table(table_name, con=engine)


def append_to_postgres(row: pd.Series, table_name: str):
    engine = create_engine(DATABASE_URL, echo=False)
    row.to_sql(table_name, engine, if_exists="append")
