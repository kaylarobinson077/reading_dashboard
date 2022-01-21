import streamlit as st
import pandas as pd
import numpy as np


from streamlit_helpers import draw_weeks_to_finish_histogram
from process_data import get_processed_data

st.title("Kayla's Reading Dashboard")

# load the data
data_load_state = st.text("Loading and processing data...")
data = get_processed_data()
data_load_state.text("Loading and processing data...done!")

# inspect the raw data
st.subheader("Raw data")
st.write(data)

# draw a histogram
st.subheader("Time to finish each book")

weeks_to_finish_histogram = draw_weeks_to_finish_histogram(data)
st.write(weeks_to_finish_histogram)
