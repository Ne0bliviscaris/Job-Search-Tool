import streamlit as st

import modules.sync.sync as sync

st.set_page_config(layout="wide")

column_config = {
    "url": st.column_config.LinkColumn("URL"),
    "logo": st.column_config.ImageColumn("Logo", width=100),
    "id": st.column_config.TextColumn("ID", width=10),
}


st.title("Synchronisation module")
with st.expander("Plan: Create a synchronisation module"):
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


current_dataset = sync.show_synced_records()
if not current_dataset.empty:
    st.dataframe(current_dataset, column_config=column_config)
else:
    st.write("No synced records to display")


if st.button("Synchronize Records"):
    sync.sync_records()

archive = sync.show_archive()
if not archive.empty:
    with st.expander("Archive"):
        st.dataframe(archive, column_config=column_config)
else:
    st.write("No archived records to display")
