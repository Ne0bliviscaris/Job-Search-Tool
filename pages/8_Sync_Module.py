import pandas as pd
import streamlit as st

from modules.data_processor import db_drop_duplicates, reactivate_all_offers
from modules.dataframe_settings import column_conversions
from modules.sync.sync import show_recently_changed, sync_records
from modules.updater.updater import update_all_sites

st.set_page_config(layout="wide")

new_records = pd.DataFrame()
archived_records = pd.DataFrame()


def update_button():
    """Update all sites button."""
    if st.button("Update all sites"):
        with st.spinner("Updating..."):  # Display a spinner while updating
            update_all_sites()
            st.success("All sites updated successfully!")


def sync_button():
    """Synchronize database button."""
    if st.button("Perform database synchronization"):
        with st.spinner("Updating..."):  # Display a spinner while updating
            # Separate archived and new records as new functions - fetch records with added or archived date shorter than 1 day
            sync_records()
            st.success("All sites synced successfully!")


def show_active_offers():
    """Show active offers."""
    st.title("Recently added active offers:")
    ACTIVE = "active"
    active = show_recently_changed(ACTIVE)
    if active is not None and not active.empty:
        column_conversions(active)
    else:
        st.warning("No active records.")


def show_archived_offers():
    """Show archived offers."""
    st.title("Recently archived offers:")
    ARCHIVED = "archived"
    archived = show_recently_changed(ARCHIVED)
    if archived is not None and not archived.empty:
        column_conversions(archived, ARCHIVED)
    else:
        st.warning("No archived records.")


def resync_button():
    """Perform resynchronization of the database."""
    if st.button("Resynchronize all offers"):
        with st.spinner("Resynchronizing..."):
            reactivate_all_offers()
            st.warning("All offers desynchronized!")
            db_drop_duplicates()
            st.warning("Duplicates removed!")
            sync_records()
            st.success("All offers resynchronized!")


def reactivate_all_offers_button():
    """Perform desynchronization of the database."""
    if st.button("Reactivate all offers"):
        with st.spinner("Desynchronizing..."):
            reactivate_all_offers()
            st.warning("All offers reactivated!")


def main():
    update_button()
    sync_button()
    show_active_offers()
    show_archived_offers()
    resync_button()
    reactivate_all_offers_button()


main()
