import streamlit as st

from modules.updater.updater import update_all_sites
from modules.websites import search_links


def update_sites_with_progress_bar():
    """Display progress bar while updating sites."""
    progress_bar, status_box = handle_update_progress()
    progress = 0
    # Process each site using the core function that yields link_name
    for link_name in update_all_sites():
        progress += 1
        update_status(progress_bar, status_box, progress, link_name)
    st.success("All sites updated!")


def handle_update_progress() -> tuple:
    """Setup and return progress tracking elements."""
    progress_bar = st.empty()
    status_box = st.empty()
    return progress_bar, status_box


def update_status(progress_bar, status_box, progress: int, link_name: str) -> None:
    """Update progress bar and status."""
    total = len(search_links)
    progress_bar.progress(progress / total)
    status_box.success(f"Downloaded: {link_name}")
    status_box.empty()


st.title("Update all sites")
st.write("This script will update all sites by downloading the latest HTML content.")
st.write("Please wait until the process is finished.")

if st.button("Update All Sites"):
    with st.spinner("Updating..."):  # Display a spinner while updating
        update_sites_with_progress_bar()
