import streamlit as st

st.title("Synchronisation module")

st.markdown(
    """
            #### Plan: Create a synchronisation module
            - Extract data from records.csv and process them into a new file

            #### Idea:
            - Sync function that will oversee the process:
                - Create a class that will handle the data processing
                - Function to move closed offers to the archive and add the date of closure

                



            #### Class features:
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
                



            
            #### Create archive
            """
)
