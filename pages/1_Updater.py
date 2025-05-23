import streamlit as st

from modules.updater.updater import update_sites_with_progress_bar

st.title("Update all sites")
st.write("This script will update all sites by downloading the latest HTML content.")
st.write("Please wait until the process is finished.")

if st.button("Update All Sites"):
    """Update all sites data when button is clicked"""
    with st.spinner("Updating..."):  # Display a spinner while updating
        update_sites_with_progress_bar(st)
