import streamlit as st

from modules.data_collector import all_sites_dataframe, save_dataframe_to_csv
from modules.dataframe_settings import set_column_config
from modules.sync.sync import sync_records
from modules.updater.updater import update_all_sites

column_config = set_column_config()


def auto_sync():
    """Perform automatic synchronization of job offers."""
    update_all_sites()
    search_records = all_sites_dataframe()
    records_file = "modules/sites/records.csv"
    save_dataframe_to_csv(search_records, records_file)
    archived_records, new_records = sync_records()
    return archived_records, new_records


def show_new_records(new_records):
    """Display new records."""
    if not new_records.empty:
        st.title("New records:")
        st.dataframe(new_records, column_config=column_config)
    else:
        st.write("No new records to display")


def show_archived_records(archived_records):
    """Display archived records."""
    if not archived_records.empty:
        st.title("Archived records:")
        st.dataframe(archived_records, column_config=column_config)
    else:
        st.write("No archived records to display")
