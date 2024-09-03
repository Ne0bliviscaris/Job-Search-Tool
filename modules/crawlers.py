import os

import containers as containers
import pandas as pd
from JobRecord import JobRecord
from scrapers.listing_scrapers import detect_records, get_search_block
from websites import (
    JUSTJOIN,
    NOFLUFFJOBS,
    ROCKETJOBS,
    THEPROTOCOL,
    identify_website,
    search_links,
)


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


def update_site(search_link):
    """
    Download HTML content from the search link and save it to a file.
    """
    current_website = identify_website(search_link)
    search_container = containers.search(current_website)

    search_block = get_search_block(search_link, search_container)

    # Ensure the directory exists
    directory = f"modules/sites/"
    os.makedirs(directory, exist_ok=True)

    # Save HTML to file
    filename = os.path.join(directory, f"{current_website}.html")
    with open(filename, "w", encoding="utf-8") as file:
        file.write(str(search_block))

    return filename


if __name__ == "__main__":
    # # Download HTML content from the first search link
    # search_link = search_links[0]  # Use the first search link as an example
    # downloaded_file = update_site(search_link)
    # print(f"HTML content saved to: {downloaded_file}")

    # Search all websites
    all_search_results = search_all_sites()
    print(all_search_results)
