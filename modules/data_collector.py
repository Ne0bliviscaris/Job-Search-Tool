import os

import requests
from bs4 import BeautifulSoup
from data_processor import html_to_soup, process_records
from websites import search_links


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


def generate_filename(key, directory=None):
    """
    Generate a readable filename based on the combined key
    """
    filename = f"{key}.html"
    if directory:
        return os.path.join(directory, filename)
    return filename


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


def search_site(key, search_link):
    """
    Get HTML block containing job search results from a file
    """
    PRINTS = False
    filename = generate_filename(key, "modules/sites")
    soup = html_to_soup(filename)
    if soup is None:
        if PRINTS:
            print(f"[data_collector.py - search_site] File not found: {filename}")
        return []
    return process_records(soup, key)


if __name__ == "__main__":
    results = search_all_sites()[0][0]
    print(results)
