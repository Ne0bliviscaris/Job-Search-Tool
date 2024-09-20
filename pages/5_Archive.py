import os

import streamlit as st

from modules.dataframe_settings import column_conversions, handle_missing_columns
from modules.sync.sync import ARCHIVE_FILE, show_records


def archive_frame():
    """Main function to display the job offers archive as dataframe."""
    st.set_page_config(layout="wide")

    st.title("Job archive browser")
    if os.path.exists(ARCHIVE_FILE):
        archive = show_records(ARCHIVE_FILE)
        if not archive.empty:
            archive = handle_missing_columns(archive)
            archive = column_conversions(archive, archive=True)


archive_frame()
