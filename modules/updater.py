import os

import containers as containers
import requests
from bs4 import BeautifulSoup
from data_collector import set_filename
from selenium_utils import get_container, setup_webdriver
from websites import identify_website, search_links


def fetch_html_requests(url: str) -> str:
    """
    Fetch HTML content from a URL using requests
    """
    response = requests.get(url)
    response.raise_for_status()
    return response.content


def fetch_html_selenium(url: str, search_container: str) -> str:
    """
    Fetch HTML content from a URL using Selenium
    """
    driver = setup_webdriver()
    with driver:
        driver.get(url)
        driver.implicitly_wait(5)
        search_block_html = get_container(driver, search_container)
    return search_block_html


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
    USE_SELENIUM = True
    if USE_SELENIUM:
        html_content = fetch_html_selenium(search_link, search_container)
    else:
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
    search_container = get_search_container(link)
    search_block = scrape(search_link, search_container)

    # Save HTML to file
    filename = os.path.join(set_filename(link))
    save_html_to_file(search_block, filename)

    return filename


def update_all_sites() -> None:
    """
    Download HTML content for all search links and save them to files.
    """
    for link, search_link in search_links.items():
        update_site(link, search_link)


if __name__ == "__main__":
    update_all_sites()
