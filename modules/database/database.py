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
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///modules/database/database.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class JobOfferRecord(Base):
    __tablename__ = "job_records"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    logo = Column(String)
    company_name = Column(String)
    location = Column(String, index=True)
    remote_status = Column(String, index=True)
    min_salary = Column(Float)
    max_salary = Column(Float)
    salary_details = Column(String)
    salary_text = Column(String)
    tags = Column(String, index=True)
    url = Column(String)
    website = Column(String, index=True)
    added_date = Column(Date)
    notes = Column(String)
    personal_rating = Column(Integer, CheckConstraint("personal_rating >= 0 AND personal_rating <= 5"), default=0)
    application_status = Column(String, default="Not applied")
    application_date = Column(Date)
    feedback_received = Column(Boolean, default=False, index=True)
    feedback_date = Column(Date)
    archived_date = Column(Date)
    offer_status = Column(String, default="active", index=True)
    users_id = Column(Integer, index=True, default=0)


def init_db():
    Base.metadata.create_all(bind=engine)
