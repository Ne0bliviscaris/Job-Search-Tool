import os

import pandas as pd
from data_processor import build_dataframe, html_to_soup, process_records
from websites import search_links


def set_filename(search_link):
    """
    Generate a readable filename based on the combined link
    """
    return os.path.join("modules/sites", f"{search_link}.html")


def search_all_sites():
    """
    Search all websites in search_links
    """
    all_search_results = []
    for link, search_link in search_links.items():
        search_result = search_site(link)
        all_search_results.append(search_result)
    return all_search_results


def search_site(search_link):
    """
    Get HTML block containing job search results from a file
    """
    filename = set_filename(search_link)
    soup = html_to_soup(filename)
    if soup is None:
        return []
    return process_records(soup, search_link)


def save_dataframe_to_csv(dataframe: pd.DataFrame, filename: str) -> None:
    """
    Save the given DataFrame to a CSV file.
    """
    dataframe.to_csv(filename, index=False)


if __name__ == "__main__":
    results = search_all_sites()
    # print(results)

    records_frame = build_dataframe(results)
    print(records_frame)
    # save_dataframe_to_csv(records_frame, "modules/sites/records.csv")
    # columns = records_frame[["Title", "Website", "Min salary", "Salary text"]]
    # print(columns)
