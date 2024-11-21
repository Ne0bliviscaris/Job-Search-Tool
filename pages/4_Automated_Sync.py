import pandas as pd
import streamlit as st

from modules.auto_sync import auto_sync, show_archived_records, show_new_records

st.set_page_config(layout="wide")

new_records = pd.DataFrame()
archived_records = pd.DataFrame()
synced_status = False

if st.button("Perform automatic synchronization"):
    with st.spinner("Updating..."):  # Display a spinner while updating
        archived_records, new_records = auto_sync()
        st.success("All sites synced successfully!")
        synced_status = True

if synced_status:
    show_new_records(new_records)
    show_archived_records(archived_records)
