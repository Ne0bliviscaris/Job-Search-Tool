import os
import subprocess

import streamlit as st

st.title("Job search automation tool")


st.markdown(
    """

            #### Portfolio entry page.
            Project explaination
            #### Motivations behind the project
            Why this project, what it solves
            #### Challenges faced
            Difficulties faced during the project
            #### What I learned

            """
)

# Launch streamlit and check if it's not already running
if __name__ == "__main__" and not os.environ.get("RUNNING"):
    # Mark streamlit as running
    os.environ["RUNNING"] = "1"
    # Get file path
    file_path = os.path.abspath(__file__)
    # Run streamlit
    subprocess.run(f"streamlit run {file_path}")
