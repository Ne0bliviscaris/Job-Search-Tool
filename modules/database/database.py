import os

import pandas as pd
from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    Date,
    Integer,
    String,
    create_engine,
    text,
)
from sqlalchemy.orm import Session, declarative_base, sessionmaker

DATABASE_URL = "sqlite:///modules/database/database.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class JobOfferRecord(Base):
    __tablename__ = "job_records"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, default="")
    logo = Column(String, default="")
    company_name = Column(String, default="Unknown")
    location = Column(String, index=True, default=None)
    remote_status = Column(String, index=True, default="Unknown")
    min_salary = Column(Integer, default=0)
    max_salary = Column(Integer, default=0)
    salary_details = Column(String, default=None)
    salary_text = Column(String, default=None)
    tags = Column(String, index=True, default=None)
    url = Column(String, default=None)
    website = Column(String, index=True, default=None)
    added_date = Column(Date, default=None, nullable=True)
    notes = Column(String, default=None)
    personal_rating = Column(Integer, default=0)
    application_status = Column(String, default="Not applied")
    application_date = Column(Date, default=None, nullable=True)
    feedback_received = Column(Boolean, default=False, index=True)
    feedback_date = Column(Date, default=None, nullable=True)
    archived_date = Column(Date, default=None, nullable=True)
    offer_status = Column(String, default="active", index=True)
    users_id = Column(Integer, index=True, default=0)


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
                # dataframe[col] = pd.to_datetime(dataframe[col], errors="coerce")
                # dataframe[col] = dataframe[col].where(dataframe[col].notna(), None)

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
                dataframe[col] = pd.to_numeric(dataframe[col], errors="coerce").fillna(0).astype(int)

        for _, row in dataframe.iterrows():
            record = JobOfferRecord(
                title=str(row.get("title", "")),
                logo=str(row.get("logo", "")),
                company_name=str(row.get("company_name", "Unknown")),
                location=str(row.get("location", "")),
                remote_status=str(row.get("remote_status", "Unknown")),
                min_salary=float(row.get("min_salary", 0)),
                max_salary=int(row.get("max_salary", 0)),
                salary_details=str(row.get("salary_details", "")),
                salary_text=str(row.get("salary_text", "")),
                tags=str(row.get("tags", "")),
                url=str(row.get("url", "")),
                website=str(row.get("website", "")),
                added_date=row.get("added_date"),
                notes=str(row.get("notes", "")),
                personal_rating=int(row.get("personal_rating", 0)),
                application_status=str(row.get("application_status", "Not applied")),
                application_date=row.get("application_date"),
                feedback_received=bool(row.get("feedback_received", False)),
                feedback_date=row.get("feedback_date"),
                archived_date=row.get("archived_date"),
                offer_status=str(row.get("offer_status", "active")),
                users_id=int(row.get("users_id", 0)),
            )
            db.add(record)
        db.commit()
    finally:
        db.close()


def update_records_in_db(dataframe: pd.DataFrame) -> None:
    """Update existing records in database."""
    db: Session = SessionLocal()
    try:
        # # Convert dates
        # date_columns = ["added_date", "application_date", "feedback_date", "archived_date"]
        # for col in date_columns:
        #     if col in dataframe.columns:
        #         dataframe[col] = pd.to_datetime(dataframe[col], errors="coerce")
        #         dataframe[col] = dataframe[col].where(~dataframe[col].isna(), None)

        # # Process numeric columns
        # numeric_cols = ["min_salary", "max_salary", "personal_rating", "users_id"]
        # for col in numeric_cols:
        #     if col in dataframe.columns:
        #         dataframe[col] = dataframe[col].fillna(None)
        #         dataframe[col] = dataframe[col].astype(float).round().astype(int)

        # Update records
        for row in dataframe.itertuples():

            record_id = row.id
            if record_id:
                # query = (
                #     db.query(JobOfferRecord)
                #     .filter(JobOfferRecord.id == record_id)
                #     .update(
                #         {
                #             "title": str(row.title),
                #             "logo": str(row.logo),
                #             "company_name": str(row.company_name),
                #             "location": str(row.location),
                #             "remote_status": str(row.remote_status),
                #             "min_salary": int(row.min_salary),
                #             "max_salary": int(row.max_salary),
                #             "salary_details": str(row.salary_details),
                #             "salary_text": str(row.salary_text),
                #             "tags": str(row.tags),
                #             "url": str(row.url),
                #             "website": str(row.website),
                #             "added_date": row.added_date,
                #             "notes": str(row.notes),
                #             "personal_rating": int(row.personal_rating),
                #             "application_status": str(row.application_status),
                #             "application_date": row.application_date,
                #             "feedback_received": bool(row.feedback_received),
                #             "feedback_date": row.feedback_date,
                #             "archived_date": row.archived_date,
                #             "offer_status": str(row.offer_status),
                #             "users_id": int(row.users_id),
                #         }
                #     )
                # )
                # print(query)
                query = text(
                    """UPDATE job_records SET 
                                title=:title, 
                                logo=:logo, 
                                company_name=:company_name, 
                                location=:location, 
                                remote_status=:remote_status, 
                                min_salary=:min_salary, 
                                max_salary=:max_salary, 
                                salary_details=:salary_details, 
                                salary_text=:salary_text, 
                                tags=:tags, 
                                url=:url, 
                                website=:website, 
                                added_date=:added_date, 
                                notes=:notes, 
                                personal_rating=:personal_rating, 
                                application_status=:application_status, 
                                application_date=:application_date, 
                                feedback_received=:feedback_received, 
                                feedback_date=:feedback_date, 
                                archived_date=:archived_date, 
                                offer_status=:offer_status, 
                                users_id=:users_id 
                                WHERE id=:id"""
                )
                params = {
                    "title": str(row.title),
                    "logo": str(row.logo),
                    "company_name": str(row.company_name),
                    "location": str(row.location),
                    "remote_status": str(row.remote_status),
                    "min_salary": int(row.min_salary) if not pd.isnull(row.min_salary) else None,
                    "max_salary": int(row.max_salary) if not pd.isnull(row.max_salary) else None,
                    "salary_details": str(row.salary_details),
                    "salary_text": str(row.salary_text),
                    "tags": str(row.tags),
                    "url": str(row.url),
                    "website": str(row.website),
                    "notes": str(row.notes),
                    "personal_rating": int(row.personal_rating),
                    "added_date": row.added_date if not pd.isnull(row.added_date) else None,
                    "application_status": str(row.application_status),
                    "application_date": (row.application_date if not pd.isnull(row.application_date) else None),
                    "feedback_received": bool(row.feedback_received),
                    "feedback_date": row.feedback_date if not pd.isnull(row.feedback_date) else None,
                    "archived_date": row.archived_date if not pd.isnull(row.archived_date) else None,
                    "offer_status": str(row.offer_status),
                    "users_id": int(row.users_id),
                    "id": row.id,
                }
            db.execute(query, params)
        db.commit()
    finally:
        db.close()


def ensure_database_exists():
    if not os.path.exists(DATABASE_URL):
        init_db()


from datetime import datetime


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
