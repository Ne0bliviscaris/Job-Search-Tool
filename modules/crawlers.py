import os

import containers as containers
import pandas as pd
from bs4 import BeautifulSoup
from JobRecord import JobRecord
from scrapers.listing_scrapers import detect_records, get_search_block
from websites import identify_website, search_links


def generate_filename(current_website, tag):
    """
    Generate a readable filename based on the website and tag
    """
    sanitized_tag = tag.replace(" ", "_")
    return f"{current_website}_{sanitized_tag}.html"


def search_all_sites():
    """
    Search all websites in search_links
    """
    PRINTS = False
    all_search_results = []
    for website, links in search_links.items():
        for tag, link in links.items():
            if PRINTS:
                print(f"[crawlers.py - search_all_sites] Searching site: {website} with tag: {tag}")
            search_result = search_site(link, tag)
            all_search_results.append(search_result)
    return all_search_results


def html_to_soup(filename):
    """
    Convert HTML file to BeautifulSoup object
    """
    PRINTS = True
    if PRINTS:
        print(f"[crawlers.py - html_to_soup] Reading HTML from: {filename}")
    with open(filename, "r", encoding="utf-8") as file:
        return BeautifulSoup(file, "html.parser")


def search_site(search_link, tag):
    """
    Get HTML block containing job search results from a file
    """
    PRINTS = True
    current_website = identify_website(search_link)
    filename = os.path.join("modules/sites", generate_filename(current_website, tag))

    if not os.path.exists(filename):
        if PRINTS:
            print(f"[crawlers.py - search_site] File not found: {filename}")
        return []

    soup = html_to_soup(filename)
    search_records = detect_records(soup, containers.record(current_website))

    # Process HTML code into JobRecord objects
    extracted_record = [JobRecord(record, current_website) for record in search_records]
    return extracted_record


def build_dataframe(records):
    """
    Convert a list of JobRecord objects to a pandas DataFrame
    """
    PRINTS = True
    records_list = [record.record_to_dataframe() for record in records]
    df = pd.DataFrame(records_list)
    return df


def update_site(search_link, tag):
    """
    Download HTML content from the search link and save it to a file.
    """
    PRINTS = True
    current_website = identify_website(search_link)
    search_container = containers.search(current_website)

    search_block = get_search_block(search_link, search_container)

    # Ensure the directory exists
    directory = "modules/sites/"
    os.makedirs(directory, exist_ok=True)

    # Save HTML to file
    filename = os.path.join(directory, generate_filename(current_website, tag))
    with open(filename, "w", encoding="utf-8") as file:
        file.write(str(search_block))

    if PRINTS:
        print(f"[crawlers.py - update_site] HTML content saved to: {filename}")
    return filename


if __name__ == "__main__":
    # # Download HTML content from the first search link
    # first_website = next(iter(search_links))
    # first_tag = next(iter(search_links[first_website]))
    # search_link = search_links[first_website][first_tag]  # Use the first search link as an example
    # downloaded_file = update_site(search_link, first_tag)
    # print(f"HTML content saved to: {downloaded_file}")

    # Search all websites
    all_search_results = search_all_sites()
    print(all_search_results[0][0])
