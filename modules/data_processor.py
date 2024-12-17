import os

import pandas as pd
from bs4 import BeautifulSoup

from modules.containers import detect_records
from modules.JobRecord import JobRecord
from modules.websites import identify_website


def process_records(soup_object: BeautifulSoup, link: str) -> list[JobRecord]:
    """
    Process HTML soup into JobRecord objects
    """
    current_website = identify_website(link)
    records = detect_records(soup_object, current_website)
    return [JobRecord(record, current_website) for record in records]


def build_dataframe(records):
    """Convert a matrix[link][number] of JobRecords to a pandas DataFrame"""
    records_matrix = [item for sublist in records for item in sublist]
    flattened_records = [record.prepare_dataframe() for record in records_matrix]
    return pd.DataFrame(flattened_records)


def html_to_soup(filename: str) -> BeautifulSoup:
    """
    Convert HTML file to BeautifulSoup object
    """
    with open(filename, "r", encoding="utf-8") as file:
        return BeautifulSoup(file, "html.parser")


def set_filename(link: str) -> str:
    """
    Generate a readable filename based on the combined link
    """
    return os.path.join("modules/updater/sites", f"{link}.html")


def save_dataframe_to_csv(dataframe: pd.DataFrame, file_path: str) -> None:
    """
    Save the given DataFrame to a CSV file.
    """
    dataframe.to_csv(file_path, index=False)
