import os

import containers as containers
import pandas as pd
from bs4 import BeautifulSoup
from JobRecord import JobRecord
from scrapers.listing_scrapers import detect_records, get_search_block
from websites import identify_website, search_links


def generate_filename(key):
    """
    Generate a readable filename based on the combined key
    """
    return f"{key}.html"


def search_all_sites():
    """
    Search all websites in search_links
    """
    PRINTS = False
    all_search_results = []
    for key, link in search_links.items():
        if PRINTS:
            print(f"[crawlers.py - search_all_sites] Searching site with key: {key}")
        search_result = search_site(key, link)
        all_search_results.append(search_result)
    return all_search_results


def html_to_soup(filename):
    """
    Convert HTML file to BeautifulSoup object
    """
    PRINTS = False
    if PRINTS:
        print(f"[crawlers.py - html_to_soup] Reading HTML from: {filename}")
    with open(filename, "r", encoding="utf-8") as file:
        return BeautifulSoup(file, "html.parser")


def process_records(soup, key):
    """
    Process HTML soup into JobRecord objects
    """
    PRINTS = False
    current_website = key.split("_")[0]
    search_records = detect_records(soup, containers.record(current_website))
    return [JobRecord(record, current_website) for record in search_records]


def search_site(key, search_link):
    """
    Get HTML block containing job search results from a file
    """
    PRINTS = False
    filename = os.path.join("modules/sites", generate_filename(key))
    soup = html_to_soup(filename)
    if soup is None:
        if PRINTS:
            print(f"[crawlers.py - search_site] File not found: {filename}")
        return []
    return process_records(soup, key)


def build_dataframe(records):
    """
    Convert a list of JobRecord objects to a pandas DataFrame
    """
    PRINTS = False
    records_list = [record.record_to_dataframe() for record in records]
    df = pd.DataFrame(records_list)
    return df


def update_site(key, search_link):
    """
    Download HTML content from the search link and save it to a file.
    """
    PRINTS = False
    current_website = key.split("_")[0]
    search_container = containers.search(current_website)

    search_block = get_search_block(search_link, search_container)

    # Ensure the directory exists
    directory = "modules/sites/"
    os.makedirs(directory, exist_ok=True)

    # Save HTML to file
    filename = os.path.join(directory, generate_filename(key))
    with open(filename, "w", encoding="utf-8") as file:
        file.write(str(search_block))

    if PRINTS:
        print(f"[crawlers.py - update_site] HTML content saved to: {filename}")
    return filename


def update_all_sites():
    """
    Download HTML content for all search links and save them to files.
    """
    PRINTS = False
    for key, search_link in search_links.items():
        if PRINTS:
            print(f"[crawlers.py - update_all_sites] Updating site with key: {key}")
        update_site(key, search_link)


if __name__ == "__main__":
    # Update all websites
    # update_all_sites()

    # Search all websites
    all_search_results = search_all_sites()
    print(all_search_results[0][0])
