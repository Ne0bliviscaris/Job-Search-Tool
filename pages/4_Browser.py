import os

import streamlit as st

from modules.dataframe_settings import column_conversions
from modules.sync.sync import SYNCED_FILE, load_csv, save_csv

st.set_page_config(layout="wide")


def main_frame():
    """Main function to display the job offers browser as dataframe."""
    st.title("Active job offers")
    if os.path.exists(SYNCED_FILE):
        raw_frame = load_csv(SYNCED_FILE)
        if not raw_frame.empty:
            main_frame = column_conversions(raw_frame)
            if st.button("Save Changes"):
                save_csv(main_frame, SYNCED_FILE)
                st.success("Changes saved successfully!")


main_frame()
