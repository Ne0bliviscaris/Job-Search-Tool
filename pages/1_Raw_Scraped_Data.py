import streamlit as st

import modules.data_collector as data_collector

st.title("All sites dataframe")
collected_frame = data_collector.all_sites_frame()

column_config = {
    "url": st.column_config.LinkColumn("URL"),
    "logo": st.column_config.ImageColumn("Logo", width=100),
}

st.data_editor(collected_frame, column_config=column_config)
if st.button("save records to file"):
    """Save dataframe to CSV when button is clicked"""
    data_collector.save_dataframe_to_csv(collected_frame, "modules/sites/records.csv")
