import asyncio

from modules.settings import SAVE_HTML
from modules.updater.data_processing.site_files import set_filename_from_link
from modules.updater.sites.SiteFactory import SiteFactory
from modules.websites import search_links


async def update_site(search_link):
    """Run scraper in executor for async update."""
    job_site = SiteFactory.identify_website(search_link)
    loop = asyncio.get_event_loop()
    search_block = await loop.run_in_executor(None, job_site.scrape)
    if SAVE_HTML:
        filename = set_filename_from_link(search_link, job_site.file_extension)
        job_site.save_file(filename, search_block)
    return search_block if search_block else True


async def update_all_sites():
    """Run all site updates concurrently and yield link names."""
    tasks = [update_site(search_link) for link_name, search_link in search_links.items()]
    await asyncio.gather(*tasks)
    for i, link_name in enumerate(search_links.keys()):
        yield link_name
