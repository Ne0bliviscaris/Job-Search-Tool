import os

import streamlit as st

from modules.data_processor import load_records_from_db, save_records_to_db
from modules.dataframe_settings import column_conversions

st.set_page_config(layout="wide")


def db_frame():
    """Main function to display the job offers browser as dataframe."""
    st.title("Job Offers Database Browser")
    raw_frame = load_records_from_db()
    if not raw_frame.empty:
        main_frame = column_conversions(raw_frame)
        if st.button("Save Changes"):
            save_records_to_db(main_frame)
            st.success("Changes saved successfully!")


db_frame()
