import streamlit as st

from modules.data_processor import reactivate_all_offers
from modules.database.database import wipe_database
from modules.dataframe_settings import column_conversions
from modules.settings import DEBUG_MODE
from modules.sync.sync import show_recently_changed, sync_records
from modules.updater.updater import update_all_sites

st.set_page_config(layout="wide")


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
            sync_records()
            st.success("All sites synced successfully!")


def show_active_offers():
    """Show active offers."""
    st.title("Recently added active offers:")
    active = show_recently_changed("active")
    if active is not None and not active.empty:
        column_conversions(active)
    else:
        st.warning("No active records.")


def show_archived_offers():
    """Show archived offers."""
    st.title("Recently archived offers:")
    archived = show_recently_changed("archived")
    if archived is not None and not archived.empty:
        column_conversions(archived, "archived")
    else:
        st.warning("No archived records.")


def reactivate_all_offers_button():
    """Perform desynchronization of the database."""
    if st.button("Reactivate all offers"):
        with st.spinner("Desynchronizing..."):
            reactivate_all_offers()
            st.warning("All offers reactivated!")


def wipe_button():
    """Wipe database button."""
    if st.button("Wipe database"):
        with st.spinner("Wiping..."):
            wipe_database()
            st.warning("Database wiped!")


def main():
    # Buttons in horizontal layout using columns
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        sync_button()
    if DEBUG_MODE:
        with col2:
            reactivate_all_offers_button()
        with col3:
            wipe_button()
    with col4:
        update_button()

    show_active_offers()
    show_archived_offers()


main()
