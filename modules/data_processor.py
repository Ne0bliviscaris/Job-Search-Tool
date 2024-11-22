import datetime
import os

import pandas as pd
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session

from modules.containers import detect_records
from modules.JobRecord import JobRecord
from modules.websites import identify_website

from .database.database import JobOfferRecord, SessionLocal, init_db


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
    return os.path.join("modules/sites", f"{link}.html")


def save_dataframe_to_csv(dataframe: pd.DataFrame, file_path: str) -> None:
    """
    Save the given DataFrame to a CSV file.
    """
    dataframe.to_csv(file_path, index=False)


def save_records_to_db(dataframe: pd.DataFrame) -> None:
    """Save the given DataFrame to the database."""
    init_db()
    db: Session = SessionLocal()
    try:
        for _, row in dataframe.iterrows():
            record = JobOfferRecord(
                title=row.get("title", ""),
                logo=row.get("logo", ""),
                company_name=row.get("company_name", "Unknown"),
                location=row.get("location", None),
                remote_status=row.get("remote_status", "Unknown"),
                min_salary=row.get("min_salary", None),
                max_salary=row.get("max_salary", None),
                salary_details=row.get("salary_details", None),
                salary_text=row.get("salary_text", None),
                tags=row.get("tags", None),
                url=row.get("url", ""),
                website=row.get("website", ""),
                added_date=row.get("added_date", None),
                notes=row.get("notes", None),
                personal_rating=row.get("personal_rating", 0),
                application_status=row.get("application_status", "Not applied"),
                application_date=row.get("application_date", None),
                feedback_received=row.get("feedback_received", False),
                feedback_date=row.get("feedback_date", None),
                archived_date=row.get("archived_date", None),
                offer_status="active",
                users_id=row.get("users_id", 0),
            )
            db.add(record)
        db.commit()
    finally:
        db.close()


def update_record_status(url: str, new_status: str) -> None:
    """Update the status of a record in the database."""
    db: Session = SessionLocal()
    try:
        record = db.query(JobOfferRecord).filter(JobOfferRecord.url == url).first()
        if record:
            record.offer_status = new_status
            if new_status == "archived":
                record.archived_date = datetime.now().date()
            db.commit()
    finally:
        db.close()
