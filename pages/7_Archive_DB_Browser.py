import os

import streamlit as st

import modules.data_processor as data_processor
from modules.data_processor import load_records_from_db, save_records_to_db
from modules.dataframe_settings import column_conversions

st.set_page_config(layout="wide")


def db_frame():
    """Main function to display the job offers browser as dataframe."""
    st.title("Job Offers Database Browser")
    raw_frame = load_records_from_db(archive=True)
    if not raw_frame.empty:
        main_frame = column_conversions(raw_frame, "Archive")
        if st.button("Save Changes"):
            save_records_to_db(main_frame)
            st.success("Changes saved successfully!")

        if st.button("Save modifications"):
            data_processor.save_records_to_db(raw_frame)
            st.success("Saved to database!")
    else:
        st.warning("No records found.")


db_frame()
