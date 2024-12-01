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

        # Convert numeric columns to integers
        numeric_cols = ["min_salary", "max_salary", "personal_rating", "users_id"]
        for col in numeric_cols:
            if col in dataframe.columns:
                if col is not None:
                    dataframe[col] = pd.to_numeric(dataframe[col], errors="coerce").fillna(0).astype(int)

        for row in dataframe.itertuples():
            record = JobOfferRecord(
                # Integer columns
                min_salary=row.min_salary,
                max_salary=row.max_salary,
                personal_rating=row.personal_rating if hasattr(row, "personal_rating") else 0,
                users_id=row.users_id if hasattr(row, "users_id") else 0,
                # String columns
                title=row.title,
                logo=row.logo,
                company_name=row.company_name,
                location=row.location,
                remote_status=row.remote_status,
                salary_details=row.salary_details,
                salary_text=row.salary_text,
                tags=row.tags,
                url=row.url,
                website=row.website,
                notes=row.notes if hasattr(row, "notes") else None,
                application_status=row.application_status if hasattr(row, "application_status") else "Not applied",
                offer_status=row.offer_status if hasattr(row, "offer_status") else "active",
                # Date columns
                added_date=row.added_date if hasattr(row, "added_date") else None,
                application_date=row.application_date if hasattr(row, "application_date") else None,
                feedback_date=row.feedback_date if hasattr(row, "feedback_date") else None,
                archived_date=row.archived_date if hasattr(row, "archived_date") else None,
                # Other columns
                feedback_received=row.feedback_received if hasattr(row, "feedback_received") else False,
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
