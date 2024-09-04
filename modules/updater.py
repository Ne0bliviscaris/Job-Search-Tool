import os

import containers as containers
import requests
from bs4 import BeautifulSoup
from data_collector import set_filename
from websites import identify_website, search_links


def fetch_html_requests(url: str) -> str:
    """
    Fetch HTML content from a URL
    """
    response = requests.get(url)
    response.raise_for_status()
    return response.content


def parse_with_beautifulsoup(html_content: str, search_container: dict) -> BeautifulSoup:
    """
    Parse HTML content using BeautifulSoup
    """
    soup = BeautifulSoup(html_content, "html.parser")
    return soup.find(search_container)


def scrape(search_link: str, search_container: dict) -> BeautifulSoup:
    """
    Get HTML block containing job search results
    """
    html_content = fetch_html_requests(search_link)
    job_listing = parse_with_beautifulsoup(html_content, search_container)
    return job_listing


def get_search_container(link: str) -> dict:
    """
    Get the search container based on the link.
    """
    current_website = identify_website(link)
    return containers.search(current_website)


def save_html_to_file(html_content: str, filename: str) -> None:
    """
    Save HTML content to a file.
    """
    with open(filename, "w", encoding="utf-8") as file:
        file.write(str(html_content))


def update_site(link: str, search_link: str) -> str:
    """
    Download HTML content from the search link and save it to a file.
    """
    PRINTS = False
    search_container = get_search_container(link)
    search_block = scrape(search_link, search_container)

    # Save HTML to file
    filename = os.path.join(set_filename(link))
    save_html_to_file(search_block, filename)

    if PRINTS:
        print(f"[updater.py - update_site] HTML content saved to: {filename}")
    return filename


def update_all_sites() -> None:
    """
    Download HTML content for all search links and save them to files.
    """
    PRINTS = False
    for link, search_link in search_links.items():
        if PRINTS:
            print(f"[updater.py - update_all_sites] Updating site with link: {search_link}")
        update_site(link, search_link)


if __name__ == "__main__":
    update_all_sites()
