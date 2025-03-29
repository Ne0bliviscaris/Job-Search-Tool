import os
import time

from modules.settings import SAVE_HTML
from modules.updater.data_processing.data_processor import set_filename_from_link
from modules.updater.error_handler import fancy_error_handler
from modules.updater.scraper.selenium_utils import scrape, setup_webdriver
from modules.updater.sites.SiteFactory import SiteFactory
from modules.websites import search_links


def update_all_sites():
    """Process all sites using webdriver and yield link names upon successful update."""
    with setup_webdriver() as web_driver:
        for link_name, search_link in search_links.items():
            if process_single_site(web_driver, search_link):
                yield link_name


@fancy_error_handler
def update_sites_with_progress_bar(st):
    """Display progress bar while updating sites."""
    progress_bar, status_box = handle_update_progress(st)
    progress = 0
    # Process each site using the core function that yields link_name
    for link_name in update_all_sites():
        progress += 1
        update_status(progress_bar, status_box, progress, link_name)
    st.success("All sites updated!")


def handle_update_progress(st) -> tuple:
    """Setup and return progress tracking elements."""
    progress_bar = st.empty()
    status_box = st.empty()
    return progress_bar, status_box


def process_single_site(web_driver, search_link: str) -> None:
    """Process single website update."""
    update_site(web_driver, search_link)
    return True


def update_site(webdriver, search_link) -> str:
    """Download HTML content from the search link and save it to a file."""
    job_site = SiteFactory.identify_website(search_link)
    search_block = scrape(webdriver, job_site)

    if SAVE_HTML:
        filename = os.path.join(set_filename_from_link(search_link))
        save_html_to_file(search_block, filename)

    return filename if SAVE_HTML else ""


def save_html_to_file(html_content: str, filename: str) -> None:
    """Save HTML content to a file."""
    with open(filename, "w", encoding="utf-8") as file:
        file.write(str(html_content))


def update_status(progress_bar, status_box, progress: int, link_name: str) -> None:
    """Update progress bar and status."""
    total = len(search_links)
    progress_bar.progress(progress / total)
    status_box.success(f"Downloaded: {link_name}")
    time.sleep(3)
    status_box.empty()
