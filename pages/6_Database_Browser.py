import os

import streamlit as st

from modules.data_processor import load_records_from_db
from modules.database.database import update_edited_dataframe, update_record
from modules.dataframe_settings import column_conversions, convert_date_columns

st.set_page_config(layout="wide")


def save_changes_button(changed_dataframe):
    """Display the save changes button."""
    if st.button("Save Changes"):
        column_conversions(changed_dataframe)
        update_edited_dataframe(changed_dataframe, st.session_state)

        st.success("Changes saved successfully!")


def db_frame():
    """Main function to display the job offers browser as dataframe."""
    st.title("Job Offers Database Browser")
    raw_frame = load_records_from_db()
    if not raw_frame.empty:
        main_frame = column_conversions(raw_frame, key="editable_dataframe")
        # main_frame = st.data_editor(raw_frame, key="main_frame")
        save_changes_button(main_frame)
    else:
        st.warning("Database empty. Perform update to find records.")


db_frame()
st.session_state
