import os

import streamlit as st

from modules.database.database import load_records_from_db, update_edited_dataframe
from modules.dataframe_settings import column_conversions
from modules.settings import DEBUG_MODE

st.set_page_config(layout="wide")


def save_changes_button(changed_dataframe):
    """Display the save changes button."""
    if st.button("Save Changes"):
        update_edited_dataframe(changed_dataframe, st.session_state)
        st.success("Changes saved successfully!")


def db_frame():
    """Main function to display the job offers browser as dataframe."""
    st.title("Job Offers Database Browser")
    raw_frame = load_records_from_db()
    if not raw_frame.empty:
        main_frame = column_conversions(raw_frame, key="editable_dataframe")
        save_changes_button(main_frame)
    else:
        st.warning("Database empty. Perform update to find records.")


db_frame()
if DEBUG_MODE:
    if "editable_dataframe" in st.session_state:
        st.session_state["editable_dataframe"]["edited_rows"]
