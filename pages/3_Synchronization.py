import streamlit as st

from modules.dataframe_settings import set_column_config
from modules.sync.sync import ARCHIVE_FILE, SYNCED_FILE, load_csv, sync_records

st.set_page_config(layout="wide")

column_config = set_column_config()


st.title("Synchronization module")
with st.expander("Plan: Create a synchronization module"):
    st.markdown(
        """
            - Extract data from records.csv and process them into a new file
            """
    )
with st.expander("Idea"):
    st.markdown(
        """
            - Sync function that will oversee the process:
                - Create a class that will handle the data processing
                - Function to move closed offers to the archive and add the date of closure
            """
    )
with st.expander("Class object to handle the data processing"):
    st.markdown(
        """
            - Unify simillar job tags, split them into categories easy to use in filters
            - Enrich the data with additional information
                - Date of creation
                - Single press [applied] button to add current date
                - Application date
                - Feedback received
                - Notes
                - Add personal rating (1-5 stars)

                - **Add application button (idea)**
                - **Scrape the job offer content (idea)**
            - Return the processed data as a dataframe with editable fields:
                - Application date
                - Feedback received
                - Notes
                - Personal rating
            """
    )

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
