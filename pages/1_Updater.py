import streamlit as st

from modules.updater.updater import update_all_sites

st.title("Update all sites")
st.write("This script will update all sites by downloading the latest HTML content.")
st.write("Please wait until the process is finished.")
if st.button("Update All Sites"):
    """Update all sites data when button is clicked"""
    update_all_sites()
    st.success("All sites updated successfully!")
