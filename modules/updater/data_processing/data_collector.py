import pandas as pd
import streamlit as st

from modules.updater.data_processing.site_files import set_filename_from_link
from modules.updater.sites.JobSite import JobSite
from modules.updater.sites.SiteFactory import SiteFactory
from modules.websites import search_links


def build_dataframe(records):
    """Convert list of job records to pandas DataFrame"""
    records_matrix = [item.to_dict() for sublist in records for item in sublist]
    return pd.DataFrame(records_matrix)


def html_dataframe() -> pd.DataFrame:
    """Return a DataFrame containing all job records from all sites."""
    search_results = search_all_sites()
    all_records_frame = build_dataframe(search_results)
    cleaned_frame = all_records_frame.drop_duplicates()
    return cleaned_frame


def search_all_sites() -> list:
    """Search all websites in search_links"""
    return [search_site(link) for link in search_links.values()]


def search_site(link: str) -> list:
    """Get HTML block containing job search results from a file"""
    try:
        job_records = process_records(link)
    except FileNotFoundError:
        print(f"Run updater to process link: {link}.")
        job_records = []

        if "st" in globals():
            st.toast(f"**Run updater to process link:**\n{link}", icon="⚠️")
    return job_records


def process_records(link: str):
    """Process HTML soup into JobRecord objects"""
    website: JobSite = SiteFactory.identify_website(link)

    file_name = set_filename_from_link(link, website.file_extension)
    file_content = website.load_file(file_name)

    records = website.records_list(data=file_content)
    return [SiteFactory.single_record(website=website, record=record) for record in records] if records else []
