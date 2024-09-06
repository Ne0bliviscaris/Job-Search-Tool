import os

import containers as containers
from data_collector import set_filename
from selenium_utils import scrape
from websites import search_links


def update_site(link: str, search_link: str) -> str:
    """
    Download HTML content from the search link and save it to a file.
    """
    search_block = scrape(search_link)

    # Save HTML to file
    filename = os.path.join(set_filename(link))
    save_html_to_file(search_block, filename)

    return filename


def save_html_to_file(html_content: str, filename: str) -> None:
    """
    Save HTML content to a file.
    """
    with open(filename, "w", encoding="utf-8") as file:
        file.write(str(html_content))


def update_all_sites() -> None:
    """
    Download HTML content for all search links and save them to files.
    """
    for link, search_link in search_links.items():
        update_site(link, search_link)


if __name__ == "__main__":
    update_all_sites()
