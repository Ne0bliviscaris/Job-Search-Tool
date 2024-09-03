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


def process_records(soup, key):
    """
    Process HTML soup into JobRecord objects
    """
    PRINTS = False
    current_website = key.split("_")[0]
    search_records = detect_records(soup, containers.record(current_website))
    return [JobRecord(record, current_website) for record in search_records]


def build_dataframe(records):
    """
    Convert a list of JobRecord objects to a pandas DataFrame
    """
    PRINTS = False
    records_list = [record.record_to_dataframe() for record in records]
    df = pd.DataFrame(records_list)
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
