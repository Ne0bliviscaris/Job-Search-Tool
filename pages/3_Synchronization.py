import streamlit as st

from modules.dataframe_settings import set_column_config
from modules.sync.sync import sync_records

st.set_page_config(layout="wide")

column_config = set_column_config()


st.title("Synchronization module")
st.write("---")
if st.button("Synchronize Records"):
    archived_records, new_records = sync_records()
    new_count = len(new_records)
    archived_count = len(archived_records)
    st.success(f"Records synchronized successfully!\n{new_count} records added, \n{archived_count} records archived.")

    if not new_records.empty:
        st.title("New records:")
        with st.expander("New records"):
            st.dataframe(new_records, column_config=column_config)
    else:
        st.write("No new records to display")

    if not archived_records.empty:
        st.title("Archived records:")
        with st.expander("Archive"):
            st.dataframe(archived_records, column_config=column_config)
    else:
        st.write("No archived records to display")
