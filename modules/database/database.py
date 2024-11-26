import os

import pandas as pd
from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    Date,
    Float,
    Integer,
    MetaData,
    String,
    create_engine,
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
    min_salary = Column(Float, default=None)
    max_salary = Column(Float, default=None)
    salary_details = Column(String, default=None)
    salary_text = Column(String, default=None)
    tags = Column(String, index=True, default=None)
    url = Column(String, default=None)
    website = Column(String, index=True, default=None)
    added_date = Column(Date, default=None)
    notes = Column(String, default=None)
    personal_rating = Column(Integer, CheckConstraint("personal_rating >= 0 AND personal_rating <= 5"), default=0)
    application_status = Column(String, default="Not applied")
    application_date = Column(Date, default=None)
    feedback_received = Column(Boolean, default=False, index=True)
    feedback_date = Column(Date, default=None)
    archived_date = Column(Date, default=None)
    offer_status = Column(String, default="active", index=True)
    users_id = Column(Integer, index=True, default=0)


def init_db():
    Base.metadata.create_all(bind=engine)


def save_records_to_db(dataframe: pd.DataFrame) -> None:
    """Save the given DataFrame to the database."""
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


def ensure_database_exists():
    if not os.path.exists(DATABASE_URL):
        init_db()
