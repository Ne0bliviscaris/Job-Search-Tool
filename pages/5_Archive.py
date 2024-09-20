import os

import streamlit as st

from modules.dataframe_settings import column_conversions
from modules.sync.sync import ARCHIVE_FILE, load_csv


def archive_frame():
    """Main function to display the job offers archive as dataframe."""
    st.set_page_config(layout="wide")

    st.title("Job archive browser")
    if os.path.exists(ARCHIVE_FILE):
        archive = load_csv(ARCHIVE_FILE)
        if not archive.empty:
            archive = column_conversions(archive, archive=True)


archive_frame()
