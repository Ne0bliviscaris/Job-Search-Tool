import pandas as pd
from bs4 import BeautifulSoup

from modules.containers import detect_records
from modules.JobRecord import JobRecord
from modules.websites import identify_website


def process_records(soup_object, link):
    """
    Process HTML soup into JobRecord objects
    """
    current_website = identify_website(link)
    records = detect_records(soup_object, current_website)
    return [JobRecord(record, current_website) for record in records]


def build_dataframe(records):
    """
    Convert a flattened list of JobRecord objects to a pandas DataFrame
    """
    records_list = [item for sublist in records for item in sublist]
    flattened_records = [record.prepare_dataframe() for record in records_list]
    return pd.DataFrame(flattened_records)


def html_to_soup(filename):
    """
    Convert HTML file to BeautifulSoup object
    """
    PRINTS = False
    if PRINTS:
        print(f"[data_processor.py - html_to_soup] Reading HTML from: {filename}")
    with open(filename, "r", encoding="utf-8") as file:
        return BeautifulSoup(file, "html.parser")
