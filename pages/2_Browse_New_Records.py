import streamlit as st

from modules.dataframe_settings import set_column_config
from modules.updater.data_processing.update_processor import update_html_dataframe


def new_records_frame():
    """Display new records."""
    new_records = update_html_dataframe()
    if not new_records.empty:
        # Potential tweak: dataframe_settings.column_conversions(new_records)
        column_config = set_column_config()
        st.data_editor(new_records, column_config=column_config)
    else:
        st.warning("No new records.")


# Set page configuration
st.set_page_config(layout="wide")

st.title("All sites dataframe")

new_records_frame()
