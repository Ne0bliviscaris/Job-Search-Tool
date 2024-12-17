import os
import time

from modules.data_processor import set_filename
from modules.selenium_utils import scrape, setup_webdriver
from modules.websites import search_links


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


def update_all_sites() -> None:
    """
    Download HTML content for all search links and save them to files.
    """

    with setup_webdriver() as web_driver:
        for link_name, search_link in search_links.items():
            update_site(web_driver, link_name, search_link)
            print(f"Downloaded {link_name}")
        print("All links downloaded")


def streamlit_update_all(st) -> None:
    """
    Download HTML content for all search links and save them to files.
    """
    try:
        with setup_webdriver() as web_driver:
            progress_bar = st.empty()
            status_box = st.empty()
            current_status = 0

            for link_name, search_link in search_links.items():
                update_site(web_driver, link_name, search_link)
                status_box.success(f"Downloaded: {link_name}")
                current_status += 1
                progress_bar.progress(current_status / len(search_links))
                time.sleep(3)
                status_box.empty()
            st.success("All sites updated!")
    except Exception as e:
        st.error("Make sure you have properly configured Webdriver (see modules/settings.py)")
