import os
import subprocess


def main():
    import streamlit as st

    st.title("Job search automation tool")

    st.markdown(
        """
        #### Portfolio entry page.
        Project explanation
        #### Motivations behind the project
        Why this project, what it solves
        #### Challenges faced
        Difficulties faced during the project
        #### What I learned
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
