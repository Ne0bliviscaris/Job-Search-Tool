import os
import subprocess

import streamlit as st

pages = [
    st.Page("nav\\scraped_data.py", title="Scraped data", default=True),
    st.Page("nav\\updater.py", title="Updater"),
]

pg = st.navigation(pages)
pg.run()


# Launch streamlit and check if it's not already running
if __name__ == "__main__" and not os.environ.get("RUNNING_IN_STREAMLIT"):
    # Mark streamlit as running
    os.environ["RUNNING_IN_STREAMLIT"] = "1"
    # Get file path
    file_path = os.path.abspath(__file__)
    # Run streamlit
    subprocess.run(["streamlit", "run", file_path], check=True)
