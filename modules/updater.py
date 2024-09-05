import os

import containers as containers
from data_collector import set_filename
from selenium_utils import get_container, setup_webdriver
from websites import identify_website, search_links


def scrape(url: str, search_container: str) -> str:
    """
    Fetch HTML content from a URL using Selenium
    """
    driver = setup_webdriver()
    with driver:
        driver.get(url)
        driver.implicitly_wait(7)
        html_content = get_container(driver, search_container)
    return html_content


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
