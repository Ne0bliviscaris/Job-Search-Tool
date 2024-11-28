import datetime
import os

import pandas as pd
from bs4 import BeautifulSoup
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session

from modules.containers import detect_records
from modules.database.database import JobOfferRecord, SessionLocal
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
    return os.path.join("modules/sites", f"{link}.html")


def save_dataframe_to_csv(dataframe: pd.DataFrame, file_path: str) -> None:
    """
    Save the given DataFrame to a CSV file.
    """
    dataframe.to_csv(file_path, index=False)


def load_records_from_db(archive=False) -> pd.DataFrame:
    """Load job records from the database."""
    db: Session = SessionLocal()
    try:
        if not archive:
            records = db.query(JobOfferRecord).where(JobOfferRecord.offer_status == "active").all()
        else:
            records = db.query(JobOfferRecord).filter(JobOfferRecord.offer_status == "archived").all()

        data = [
            {
                "id": record.id,
                "title": record.title,
                "logo": record.logo,
                "company_name": record.company_name,
                "location": record.location,
                "remote_status": record.remote_status,
                "min_salary": record.min_salary,
                "max_salary": record.max_salary,
                "salary_details": record.salary_details,
                "salary_text": record.salary_text,
                "tags": record.tags,
                "url": record.url,
                "website": record.website,
                "added_date": record.added_date,
                "notes": record.notes,
                "personal_rating": record.personal_rating,
                "application_status": record.application_status,
                "application_date": record.application_date,
                "feedback_received": record.feedback_received,
                "feedback_date": record.feedback_date,
                "archived_date": record.archived_date,
                "offer_status": record.offer_status,
                "users_id": record.users_id,
            }
            for record in records
        ]

        return pd.DataFrame(data)
    except OperationalError:
        empty_frame = pd.DataFrame()
        return empty_frame
    finally:
        db.close()


def update_record(record_id: str, updates: dict = None) -> None:
    """Update the status or fields of a record in the database."""
    db: Session = SessionLocal()
    try:
        record = db.query(JobOfferRecord).filter(JobOfferRecord.id == record_id).first()
        if record:
            if updates:
                for key, value in updates.items():
                    setattr(record, key, value)
            db.commit()
    finally:
        db.close()


def reactivate_all_offers():
    """Reactivate all archived offers."""
    db: Session = SessionLocal()
    try:
        records = db.query(JobOfferRecord).filter(JobOfferRecord.offer_status == "archived").all()
        for record in records:
            record.archived_date = None
            record.offer_status = "active"
        db.commit()

        print(f"Reactivated {len(records)} offers.")
    finally:
        db.close()


def db_drop_duplicates():
    """Remove duplicate records from the database."""
    db: Session = SessionLocal()
    try:
        records = db.query(JobOfferRecord).all()
        records_df = pd.DataFrame(records)
        COLUMNS_TO_COMPARE = ["title", "company_name", "website", "remote_status", "salary_text", "tags", "location"]
        records_df.drop_duplicates()
        db.commit()
    finally:
        db.close()
