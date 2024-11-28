import os

import streamlit as st

from modules.data_processor import load_records_from_db
from modules.database.database import update_records_in_db
from modules.dataframe_settings import column_conversions

st.set_page_config(layout="wide")


def db_frame():
    """Main function to display the job offers browser as dataframe."""
    st.title("Job Offers Database Browser")
    raw_frame = load_records_from_db(archive=True)
    if not raw_frame.empty:
        archive_frame = column_conversions(raw_frame, "Archive")
        if st.button("Save Changes"):
            update_records_in_db(archive_frame)
            st.success("Changes saved successfully!")

    else:
        st.warning("No records found.")


db_frame()
