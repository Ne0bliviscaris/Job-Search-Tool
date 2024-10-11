import pandas as pd

from modules.data_processor import (
    build_dataframe,
    html_to_soup,
    process_records,
    set_filename,
)
from modules.websites import search_links


def all_sites_dataframe() -> pd.DataFrame:
    """
    Return a DataFrame containing all job records from all sites.
    """
    search_results = search_all_sites()
    all_records_frame = build_dataframe(search_results)
    cleaned_frame = all_records_frame.drop_duplicates()
    return cleaned_frame


def search_all_sites() -> list:
    """
    Search all websites in search_links
    """
    return [search_site(link) for link in search_links.keys()]


def search_site(link: str) -> list:
    """
    Get HTML block containing job search results from a file
    """
    file = set_filename(link)
    soup = html_to_soup(file)

    job_records = process_records(soup, search_links[link]) if soup is not None else []
    return job_records
