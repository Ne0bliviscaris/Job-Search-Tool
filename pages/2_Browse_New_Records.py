import streamlit as st

import modules.data_collector as data_collector
import modules.data_processor as data_processor
from modules.dataframe_settings import set_column_config

# Set page configuration
st.set_page_config(layout="wide")

st.title("All sites dataframe")
collected_frame = data_collector.all_sites_dataframe()


column_config = set_column_config()
st.data_editor(collected_frame, column_config=column_config)

if st.button("export to CSV"):
    data_processor.save_dataframe_to_csv(collected_frame, "modules/sites/records.csv")
    st.success("Saved!")
