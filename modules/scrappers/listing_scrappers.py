import requests
from bs4 import BeautifulSoup


def get_search_block(search_link, search_container):
    """
    Get HTML block containing job search results
    """

    response = requests.get(search_link)
    soup = BeautifulSoup(response.content, "html.parser")
    job_listing = soup.find(search_container)
    # print(job_listing) # TEST PRINT
    return job_listing


def detect_records(search_results_block, record_container):
    """
    Split given HTML code block into records
    """
    records = [job for job in search_results_block.find_all(id=record_container)]
    return records

    # return records
