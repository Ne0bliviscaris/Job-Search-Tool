import containers as containers
import pandas as pd
from bs4 import BeautifulSoup
from JobRecord import JobRecord


def detect_records(search_results_block, record_container):
    """
    Split given HTML code block into records
    """
    PRINTS = False
    records = [job for job in search_results_block.find_all(id=record_container)]
    if PRINTS:
        print(f"[data_processor.py - detect_records] Records: {records}")
    return records


def process_records(soup, link):
    """
    Process HTML soup into JobRecord objects
    """
    current_website = link.split("_")[0]
    search_records = detect_records(soup, containers.record(current_website))
    return [JobRecord(record, current_website) for record in search_records]


def build_dataframe(records):
    """
    Convert a flattened list of JobRecord objects to a pandas DataFrame
    """
    records_list = [item for sublist in records for item in sublist]
    flattened_records = [record.record_to_dataframe() for record in records_list]
    df = pd.DataFrame(flattened_records)
    return df


def html_to_soup(filename):
    """
    Convert HTML file to BeautifulSoup object
    """
    PRINTS = False
    if PRINTS:
        print(f"[data_processor.py - html_to_soup] Reading HTML from: {filename}")
    with open(filename, "r", encoding="utf-8") as file:
        return BeautifulSoup(file, "html.parser")
