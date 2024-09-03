import os

import containers as containers
import pandas as pd
import requests
from bs4 import BeautifulSoup
from JobRecord import JobRecord
from websites import search_links


def generate_filename(key):
    """
    Generate a readable filename based on the combined key
    """
    return f"{key}.html"


def get_search_block(search_link, search_container):
    """
    Get HTML block containing job search results
    """
    PRINTS = False
    response = requests.get(search_link)
    soup = BeautifulSoup(response.content, "html.parser")
    job_listing = soup.find(search_container)
    if PRINTS:
        print(f"[data_collector.py - get_search_block] Job listing: {job_listing}")
    return job_listing


def detect_records(search_results_block, record_container):
    """
    Split given HTML code block into records
    """
    PRINTS = False
    records = [job for job in search_results_block.find_all(id=record_container)]
    if PRINTS:
        print(f"[data_collector.py - detect_records] Records: {records}")
    return records


def search_all_sites():
    """
    Search all websites in search_links
    """
    PRINTS = False
    all_search_results = []
    for key, link in search_links.items():
        if PRINTS:
            print(f"[data_collector.py - search_all_sites] Searching site with key: {key}")
        search_result = search_site(key, link)
        all_search_results.append(search_result)
    return all_search_results


def html_to_soup(filename):
    """
    Convert HTML file to BeautifulSoup object
    """
    PRINTS = False
    if PRINTS:
        print(f"[data_collector.py - html_to_soup] Reading HTML from: {filename}")
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
            print(f"[data_collector.py - search_site] File not found: {filename}")
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


if __name__ == "__main__":
    # Search all websites
    all_search_results = search_all_sites()
    print(all_search_results[0][0])
