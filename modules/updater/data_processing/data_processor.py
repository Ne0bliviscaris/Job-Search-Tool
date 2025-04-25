import os

import pandas as pd
from bs4 import BeautifulSoup

from modules.updater.sites.JobSite import JobSite
from modules.updater.sites.SiteFactory import SiteFactory
from modules.websites import search_links


def process_records(search_block: BeautifulSoup, link: str):
    """Process HTML soup into JobRecord objects"""
    website: JobSite = SiteFactory.identify_website(link)
    records = website.records_list(html=search_block)
    return [SiteFactory.single_record(website=website, record=record) for record in records]


def build_dataframe(records):
    """Convert list of job records to pandas DataFrame"""
    records_matrix = [item.to_dict() for sublist in records for item in sublist]
    return pd.DataFrame(records_matrix)


def html_to_soup(filename: str) -> BeautifulSoup:
    """Convert HTML file to BeautifulSoup object"""
    with open(filename, "r", encoding="utf-8") as file:
        return BeautifulSoup(file, "html.parser")


def set_filename(link: str) -> str:
    """Generate a readable filename based on the combined link"""
    return os.path.join("modules\\updater\\sites\\HTML\\", f"{link}.html")


def set_filename_from_link(link: str) -> str:
    """Generate filename based on link key in search_links dict"""
    link_name = next((key for key, value in search_links.items() if value == link), link)
    return os.path.join("modules\\updater\\sites\\HTML", f"{link_name}.html")
