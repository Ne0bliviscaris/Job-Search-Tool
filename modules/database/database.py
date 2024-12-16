import os

import pandas as pd
from sqlalchemy import Boolean, Column, DateTime, Integer, String, create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session, declarative_base, sessionmaker

from modules.dicts import DATE_COLUMNS

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
    added_date = Column(DateTime, default=None, nullable=True)
    application_date = Column(DateTime, default=None, nullable=True)
    feedback_date = Column(DateTime, default=None, nullable=True)
    archived_date = Column(DateTime, default=None, nullable=True)
    # Other columns
    feedback_received = Column(Boolean, default=False, index=True)


def init_db():
    Base.metadata.create_all(bind=engine)


def save_records_to_db(dataframe: pd.DataFrame) -> None:
    """Save the given DataFrame to the database."""
    db: Session = SessionLocal()
    try:
        # Convert NaT to None and strings to Timestamp for date columns
        for col in DATE_COLUMNS:
            if col in dataframe.columns:
                dataframe[col] = dataframe[col].apply(lambda x: None if pd.isna(x) else pd.Timestamp(x))
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


def update_edited_dataframe(changed_dataframe, st_session_state):
    """Update the edited records in the database."""

    edited_rows = st_session_state.get("editable_dataframe", {}).get("edited_rows", {})

    # Update each modified record in the database
    for row_id, updates in edited_rows.items():
        record_id = changed_dataframe.loc[int(row_id), "id"]
        update_record(int(record_id), updates)


def update_record(record_id: int, updated_fields: dict) -> None:
    """Update a single record in the database."""
    db: Session = SessionLocal()
    try:
        record = db.query(JobOfferRecord).filter(JobOfferRecord.id == record_id).first()
        if record:
            for key, value in updated_fields.items():
                if key in DATE_COLUMNS and value:
                    value = pd.Timestamp(value)
                setattr(record, key, value)
            db.commit()
    finally:
        db.close()


def wipe_database():
    """Delete all records from the database."""
    db: Session = SessionLocal()
    try:
        db.query(JobOfferRecord).delete()
        db.commit()
    finally:
        db.close()


def load_records_from_db(archive=False, all_records=False) -> pd.DataFrame:
    """Load job records from the database."""
    db: Session = SessionLocal()
    try:
        if not all_records:
            if not archive:
                records = db.query(JobOfferRecord).where(JobOfferRecord.offer_status == "active").all()
            else:
                records = db.query(JobOfferRecord).filter(JobOfferRecord.offer_status == "archived").all()
        else:
            records = db.query(JobOfferRecord).all()
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

        db_frame = pd.DataFrame(data)
        db_frame = convert_dates_to_timestamps(db_frame)
        return db_frame

    except OperationalError:
        empty_frame = pd.DataFrame()
        return empty_frame
    finally:
        db.close()


def convert_dates_to_timestamps(frame: pd.DataFrame) -> pd.DataFrame:
    """Convert date columns to Timestamp objects."""
    for col in DATE_COLUMNS:
        if col in frame.columns:
            frame[col] = pd.to_datetime(frame[col])
    return frame


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
