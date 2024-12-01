import os
from datetime import datetime

import pandas as pd
from sqlalchemy import Boolean, Column, Date, Integer, String, create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

from modules.settings import DATE_FORMAT

DATABASE_URL = "sqlite:///modules/database/database.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class JobOfferRecord(Base):
    __tablename__ = "job_records"

    # Integer columns
    id = Column(Integer, primary_key=True, index=True)
    min_salary = Column(Integer, default=0)
    max_salary = Column(Integer, default=0)
    personal_rating = Column(Integer, default=0)
    users_id = Column(Integer, index=True, default=0)
    # String columns
    title = Column(String, index=True, default="")
    logo = Column(String, default="")
    company_name = Column(String, default="Unknown")
    location = Column(String, index=True, default=None)
    remote_status = Column(String, index=True, default="Unknown")
    salary_details = Column(String, default=None)
    salary_text = Column(String, default=None)
    tags = Column(String, index=True, default=None)
    url = Column(String, default=None)
    website = Column(String, index=True, default=None)
    notes = Column(String, default=None, nullable=True)
    application_status = Column(String, default="Not applied")
    offer_status = Column(String, default="active", index=True)
    # Date columns
    added_date = Column(Date, default=None, nullable=True)
    application_date = Column(Date, default=None, nullable=True)
    feedback_date = Column(Date, default=None, nullable=True)
    archived_date = Column(Date, default=None, nullable=True)
    # Other columns
    feedback_received = Column(Boolean, default=False, index=True)


def init_db():
    Base.metadata.create_all(bind=engine)


def save_records_to_db(dataframe: pd.DataFrame) -> None:
    """Save the given DataFrame to the database."""
    db: Session = SessionLocal()
    try:
        # Convert NaT to None for date columns
        date_columns = ["added_date", "application_date", "feedback_date", "archived_date"]
        for col in date_columns:
            if col in dataframe.columns:
                dataframe[col] = dataframe[col].apply(lambda x: None if pd.isna(x) else x)
                dataframe[col] = pd.to_datetime(dataframe[col], format=DATE_FORMAT, errors="coerce")

        # Prepare default values for non-date columns
        defaults = {
            "min_salary": 0,
            "max_salary": 0,
            "personal_rating": 0,
            "users_id": 0,
            "location": "",
            "salary_details": "",
            "salary_text": "",
            "tags": "",
            "url": "",
            "website": "",
            "notes": "",
            "application_status": "Not applied",
            "offer_status": "active",
        }

        # Fill missing values
        dataframe = dataframe.fillna(value=defaults)

        # Convert numeric columns to integers
        numeric_cols = ["min_salary", "max_salary", "personal_rating", "users_id"]
        for col in numeric_cols:
            if col in dataframe.columns:
                if col is not None:
                    dataframe[col] = pd.to_numeric(dataframe[col], errors="coerce").fillna(0).astype(int)

        for _, row in dataframe.iterrows():
            record = JobOfferRecord(
                # Integer columns
                min_salary=int(row.get("min_salary", 0)),
                max_salary=int(row.get("max_salary", 0)),
                personal_rating=int(row.get("personal_rating", 0)),
                users_id=int(row.get("users_id", 0)),
                # String columns
                title=str(row.get("title", "")),
                logo=str(row.get("logo", "")),
                company_name=str(row.get("company_name", "Unknown")),
                location=str(row.get("location", "")),
                remote_status=str(row.get("remote_status", "Unknown")),
                salary_details=str(row.get("salary_details", "")),
                salary_text=str(row.get("salary_text", "")),
                tags=str(row.get("tags", "")),
                url=str(row.get("url", "")),
                website=str(row.get("website", "")),
                notes=str(row.get("notes", "")),
                application_status=str(row.get("application_status", "Not applied")),
                offer_status=str(row.get("offer_status", "active")),
                # Date columns
                added_date=row.get("added_date"),
                application_date=row.get("application_date"),
                feedback_date=row.get("feedback_date"),
                archived_date=row.get("archived_date"),
                # Other columns
                feedback_received=bool(row.get("feedback_received", False)),
            )
            db.add(record)
        db.commit()
    finally:
        db.close()


def ensure_database_exists():
    if not os.path.exists(DATABASE_URL):
        init_db()


def insert_empty_record():
    """Insert an empty record to the database."""
    db: Session = SessionLocal()
    try:

        archived_date = datetime.strptime("26-11-2024", "%d-%m-%Y").date()
        record = JobOfferRecord(added_date=archived_date)
        db.add(record)
        db.commit()
    finally:
        db.close()


def update_record(record_id: int, updates: dict) -> None:
    """Update a single record in the database."""
    db: Session = SessionLocal()
    try:
        date_columns = ["added_date", "application_date", "feedback_date", "archived_date"]
        record = db.query(JobOfferRecord).filter(JobOfferRecord.id == record_id).first()
        if record:
            for key, value in updates.items():
                if key in date_columns:
                    value = datetime.strptime(value.split(" ")[0], DATE_FORMAT).date() if value else None
                setattr(record, key, value)
            db.commit()
    finally:
        db.close()


def update_edited_dataframe(changed_dataframe, st_session_state):
    """Update the edited records in the database."""

    edited_rows = st_session_state.get("editable_dataframe", {}).get("edited_rows", {})

    # Update each modified record in the database
    for row_id, updates in edited_rows.items():
        record_id = changed_dataframe.loc[int(row_id), "id"]
        update_record(int(record_id), updates)


def wipe_database():
    """Delete all records from the database."""
    db: Session = SessionLocal()
    try:
        db.query(JobOfferRecord).delete()
        db.commit()
    finally:
        db.close()
