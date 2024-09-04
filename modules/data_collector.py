import os

from data_processor import build_dataframe, html_to_soup, process_records
from websites import search_links


def set_filename(link):
    """
    Generate a readable filename based on the combined link
    """
    return os.path.join("modules/sites", f"{link}.html")


def search_all_sites():
    """
    Search all websites in search_links
    """
    PRINTS = False
    all_search_results = []
    for link, search_link in search_links.items():
        if PRINTS:
            print(f"[data_collector.py - search_all_sites] Searching site with link: {link}")
        search_result = search_site(link)
        all_search_results.append(search_result)
    return all_search_results


def search_site(link):
    """
    Get HTML block containing job search results from a file
    """
    PRINTS = False
    filename = set_filename(link)
    soup = html_to_soup(filename)
    if soup is None:
        if PRINTS:
            print(f"[data_collector.py - search_site] File not found: {filename}")
        return []
    return process_records(soup, link)


if __name__ == "__main__":
    results = search_all_sites()  # [1][0]
    # print(results)

    records_frame = build_dataframe(results)
    # print(records_frame)

    columns = records_frame[["Title", "Company name"]]
    print(columns)
