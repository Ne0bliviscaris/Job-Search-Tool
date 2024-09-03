import os

import containers as containers
import requests
from bs4 import BeautifulSoup
from data_collector import set_filename
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


def get_search_container(link):
    """
    Get the search container based on the link.
    """
    current_website = link.split("_")[0]
    return containers.search(current_website)


def save_html_to_file(html_content, filename):
    """
    Save HTML content to a file.
    """
    with open(filename, "w", encoding="utf-8") as file:
        file.write(str(html_content))


def update_site(link, search_link):
    """
    Download HTML content from the search link and save it to a file.
    """
    PRINTS = False
    search_container = get_search_container(link)
    search_block = get_search_block(search_link, search_container)

    # Save HTML to file
    filename = os.path.join(set_filename(link))
    save_html_to_file(search_block, filename)

    if PRINTS:
        print(f"[update_site.py - update_site] HTML content saved to: {filename}")
    return filename


def update_all_sites():
    """
    Download HTML content for all search links and save them to files.
    """
    PRINTS = False
    for link, search_link in search_links.items():
        if PRINTS:
            print(f"[update_site.py - update_all_sites] Updating site with link: {link}")
        update_site(link, search_link)


if __name__ == "__main__":
    update_all_sites()
