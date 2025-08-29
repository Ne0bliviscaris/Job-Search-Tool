import pandas as pd
import streamlit as st

from modules.updater.data_processing.site_files import set_filename_from_link
from modules.updater.sites.JobSite import JobSite
from modules.updater.sites.SiteFactory import SiteFactory
from modules.websites import search_links


def update_html_dataframe() -> pd.DataFrame:
    """Return a DataFrame containing all update records from all links."""
    job_records = process_all_links()
    all_records_frame = build_dataframe(job_records)
    return all_records_frame.drop_duplicates()


def process_all_links():
    """Yields JobSite instances containing separated job offers.
    Raises FileNotFoundError if update file is not found."""
    for link in search_links.values():
        try:
            yield process_website(link)
        except FileNotFoundError:
            print(f"Update file not found. Run updater to process link: {link}.")
            if "st" in globals():
                st.toast(f"**Update file not found. Run updater to process link:**\n{link}", icon="⚠️")
            continue


def process_website(link: str):
    """Process job records from a given link. Returns a list of JobSite instances containing separated job offers."""
    website: JobSite = SiteFactory.identify_website(link)

    file_name = set_filename_from_link(link, website.file_extension)
    file_content = website.load_file(file_name)
    records = website.records_list(data=file_content)
    print(f"Processing: {file_name}. Found {len(records)} records.")
    return create_offer_instances(website.__class__, records)


def create_offer_instances(site_class, records):
    """Create JobSite instances from job records"""
    return [site_class(html=record) for record in records] if records else []


def build_dataframe(records):
    """Convert list of job records to pandas DataFrame"""
    records_matrix = [item.to_dict() for sublist in records for item in sublist]
    return pd.DataFrame(records_matrix)
