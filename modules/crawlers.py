import pandas as pd

import modules.containers as containers
from modules.JobRecord import JobRecord
from modules.scrappers.listing_scrappers import detect_records, get_search_block
from modules.websites import identify_website, search_links


def search_all_sites():
    """
    Search all websites in search_links
    """
    all_search_results = []
    for site in search_links:
        search_result = search_site(site)
        all_search_results.append(search_result)
    return all_search_results


# This function will manage the search for each website
def search_site(search_link):
    """
    Get HTML block containing job search results
    """
    current_website = identify_website(search_link)
    search_container = containers.search(current_website)
    record_container = containers.record(current_website)

    search_block = get_search_block(search_link, search_container)
    search_records = detect_records(search_block, record_container)

    # Process HTML code into JobRecord objects
    extracted_record = [JobRecord(record, current_website) for record in search_records]
    return extracted_record


def build_dataframe(records):
    """
    Convert a list of JobRecord objects to a pandas DataFrame
    """
    records_list = [record.record_to_dataframe() for record in records]
    df = pd.DataFrame(records_list)
    return df


def main():
    """
    Main function
    """
    search_results = search_all_sites()
    all_records = [record for site in search_results for record in site]
    df = build_dataframe(all_records)
    return df
