import pandas as pd
import streamlit as st

from modules.data_processor import load_records_from_db
from modules.dataframe_settings import column_conversions

st.set_page_config(layout="wide")


"""Main function to display the job offers browser as dataframe."""
st.title("Job Offers Database Browser")
active = load_records_from_db()
archive = load_records_from_db(archive=True)
merged_frame = pd.concat([active, archive], ignore_index=True)
if not merged_frame.empty:
    merged_frame = column_conversions(merged_frame)
