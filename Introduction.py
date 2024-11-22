import os
import subprocess

import streamlit as st

st.set_page_config(layout="wide")


def main():
    st.title("Job search scraper multitool")
    st.markdown(
        """
        #### Job searching is inconvenient.
        Not only are there multiple websites, but it's also hard to keep track of all the job offers you have applied to.
        

        I have built this tool to spare myself the pain of browsing through 7 major polish job boards every day.
        
        ---        
        #### The idea is simple:
        For each job board, I have pasted a link with applied filters that I want to check every day.

        - The **update** module scrapes the search results and stores them as HTML files.
        - The **data collector** module extracts offers from HTML files and stores them in a database.
        - Then comes the **synchronization** module, which tracks new offers and archives outdated ones.
        - This leaves the **offers browser** and **archive**, which are self-explanatory.
        ---
        #### Functionality:
        - Scrape job offers from 7 websites: No Fluff Jobs, Bulldog Job, The:Protocol, Rocket Jobs, Just Join IT, Solid Jobs, Pracuj.pl
        - Extract and unify data into a single database
        - Track application and feedback status, add notes and personal ratings
        - Serve it all in a convenient way
        """
    )


if __name__ == "__main__":
    if not os.environ.get("RUNNING"):
        # Mark streamlit as running
        os.environ["RUNNING"] = "1"
        # Get file path
        file_path = os.path.abspath(__file__)
        # Run streamlit in a new process
        subprocess.run(f"streamlit run {file_path}")
    else:
        main()
