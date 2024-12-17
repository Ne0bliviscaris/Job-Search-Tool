import os
import time

from modules.updater.data_processing.data_processor import set_filename
from modules.updater.scraper.selenium_utils import scrape, setup_webdriver
from modules.websites import search_links


def update_all_sites(st) -> None:
    """Download HTML content for all search links."""
    try:
        with setup_webdriver() as web_driver:
            progress_bar, status_box = handle_update_progress(st)
            progress = 0

            for link_name, search_link in search_links.items():
                if process_single_site(web_driver, link_name, search_link):
                    progress += 1
                    update_status(progress_bar, status_box, progress, link_name)

            st.success("All sites updated!")
    except Exception as e:
        st.error("Make sure you have properly configured Webdriver (see modules/settings.py)")


def handle_update_progress(st) -> tuple:
    """Setup and return progress tracking elements."""
    progress_bar = st.empty()
    status_box = st.empty()
    return progress_bar, status_box


def process_single_site(web_driver, link_name: str, search_link: str) -> None:
    """Process single website update."""
    try:
        update_site(web_driver, link_name, search_link)
        return True
    except Exception as e:
        print(f"Error updating {link_name}: {e}")
        return False


def update_site(webdriver, link: str, search_link: str) -> str:
    """
    Download HTML content from the search link and save it to a file.
    """
    search_block = scrape(webdriver, search_link)

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


def update_status(progress_bar, status_box, progress: int, link_name: str) -> None:
    """Update progress bar and status."""
    total = len(search_links)
    progress_bar.progress(progress / total)
    status_box.success(f"Downloaded: {link_name}")
    time.sleep(3)
    status_box.empty()
