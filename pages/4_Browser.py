import os

import streamlit as st

from modules.dataframe_settings import column_conversions
from modules.sync.sync import SYNCED_FILE, save_csv, show_records

st.set_page_config(layout="wide")


def main_frame():
    """Main function to display the job offers browser as dataframe."""
    st.title("Active job offers")
    if os.path.exists(SYNCED_FILE):
        main_frame = show_records(SYNCED_FILE)
        if not main_frame.empty:
            edited_df = column_conversions(main_frame)
            if st.button("Save Changes"):
                save_csv(edited_df, SYNCED_FILE)
                st.success("Changes saved successfully!")


main_frame()
