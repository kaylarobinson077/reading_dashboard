import streamlit as st
import pandas as pd


# sample invocation:
# streamlit run app.py

from streamlit_helpers import draw_num_pages_histogram
from process_data import get_processed_data

st.title("Kayla's Reading Dashboard")

# load the data
data = get_processed_data()
print(data.columns)
# draw a histogram
st.subheader("Number of pages in each book")

num_pages_hist = draw_num_pages_histogram(data)
st.write(num_pages_hist)
