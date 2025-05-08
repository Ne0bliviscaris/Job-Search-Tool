import pandas as pd
from bs4 import BeautifulSoup

from modules.updater.data_processing.site_files import set_filename_from_link
from modules.updater.sites.JobSite import JobSite
from modules.updater.sites.SiteFactory import SiteFactory


def process_records(link: str):
    """Process HTML soup into JobRecord objects"""
    website: JobSite = SiteFactory.identify_website(link)
    file_name = set_filename_from_link(link, website.file_extension)
    records = website.records_list(html=file_name, link=link)
    return [SiteFactory.single_record(website=website, record=record) for record in records] if records else []


def build_dataframe(records):
    """Convert list of job records to pandas DataFrame"""
    records_matrix = [item.to_dict() for sublist in records for item in sublist]
    return pd.DataFrame(records_matrix)


def html_to_soup(filename: str) -> BeautifulSoup:
    """Convert HTML file to BeautifulSoup object"""
    with open(filename, "r", encoding="utf-8") as file:
        return BeautifulSoup(file, "html.parser")
