from modules.settings import SAVE_HTML
from modules.updater.data_processing.site_files import set_filename_from_link
from modules.updater.sites.SiteFactory import SiteFactory
from modules.updater.webdriver import setup_webdriver
from modules.websites import search_links


def update_all_sites():
    """Process all sites using webdriver and yield link names upon successful update."""
    with setup_webdriver() as web_driver:
        for link_name, search_link in search_links.items():
            if update_site(web_driver, search_link):
                yield link_name


def update_site(webdriver, search_link) -> str:
    """Download HTML content from the search link and save it to a file."""
    job_site = SiteFactory.identify_website(search_link)
    search_block = job_site.scrape(webdriver)

    if SAVE_HTML:
        filename = set_filename_from_link(search_link, job_site.file_extension)
        job_site.save_file(filename, search_block)
    return search_block if search_block else True
