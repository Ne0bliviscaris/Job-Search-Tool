import streamlit as st

import modules.data_collector as data_collector
import modules.data_processor as data_processor
from modules.dataframe_settings import set_column_config


def new_records_frame():
    """Display new records."""
    new_records = data_collector.html_dataframe()
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
