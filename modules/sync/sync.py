from datetime import datetime, timedelta

import pandas as pd
from sqlalchemy import update
from sqlalchemy.orm import Session

from modules.data_collector import all_sites_dataframe
from modules.data_processor import load_records_from_db
from modules.database.database import (
    JobOfferRecord,
    SessionLocal,
    ensure_database_exists,
    save_records_to_db,
)
from modules.settings import DATE_FORMAT

ensure_database_exists()
COLUMNS_TO_COMPARE = ["title", "company_name", "website", "remote_status", "salary_text", "tags", "location"]


def prepare_comparison(frame: pd.DataFrame) -> set:
    """Set columns for the DataFrame."""
    columns_to_compare = frame[COLUMNS_TO_COMPARE]
    rows_as_tuples = columns_to_compare.apply(tuple, axis=1)
    rows_to_compare = set(rows_as_tuples)
    return rows_to_compare


def filter_records(db_records, tested_records) -> pd.DataFrame:
    """Returns only df records matching given records.
    Compares content of columns specified in COLUMNS_TO_COMPARE."""
    if not db_records.empty:
        columns = db_records[COLUMNS_TO_COMPARE]
        df_rows = columns.apply(tuple, axis=1)
        matching_records = df_rows.isin(tested_records)
        return db_records[matching_records]
    else:
        return pd.DataFrame()


def sync_records():
    """
    Main function to oversee the synchronisation process
    Extract records from raw, add additional information and return processed data into a new file
    """

    missing_records, new_records, current_db, update = changed_records()

    # Archive missing records
    cleaned_dataframe = archive_records(current_db, missing_records)

    # If the record is new, add custom columns
    synced_dataframe = process_new_records(cleaned_dataframe, new_records, update)

    # Save the updated synced file
    if new_records:
        save_records_to_db(synced_dataframe)


def process_new_records(cleaned_current_file, new_records, update_frame: pd.DataFrame) -> pd.DataFrame:
    """Process new records adding custom columns and timestamp."""
    new_records_df = filter_records(update_frame, new_records)
    if not new_records_df.empty:
        new_records_df = add_date_to_column(new_records_df, column="added_date")
        merged_new_frame = pd.concat([cleaned_current_file, new_records_df], ignore_index=True)
        return merged_new_frame
    return cleaned_current_file


def archive_records(db_records, missing_records: set) -> pd.DataFrame:
    """Archive missing records from synced file."""
    records_to_archive = filter_records(db_records, missing_records)

    if not records_to_archive.empty:
        records_to_archive = add_date_to_column(records_to_archive, column="archived_date")

        db: Session = SessionLocal()
        try:
            # Prepare the update statement
            for _, row in records_to_archive.iterrows():
                update_values = {
                    "archived_date": row["archived_date"],
                    "offer_status": "archived",
                }
                update_status = update(JobOfferRecord).where(JobOfferRecord.id == row["id"]).values(update_values)
                db.execute(update_status)
            db.commit()
        finally:
            db.close()


def remove_archived_records(df: pd.DataFrame, records_to_remove: set) -> pd.DataFrame:
    """Remove records from DataFrame based on compared columns content."""
    columns = df[COLUMNS_TO_COMPARE]
    rows_as_tuples = columns.apply(tuple, axis=1)

    # Filter out rows that are in records_to_remove
    not_in_records_to_remove = ~rows_as_tuples.isin(records_to_remove)
    cleaned_df = df[not_in_records_to_remove]
    return cleaned_df


def changed_records() -> tuple:
    """Load files and return missing and new records."""
    update = all_sites_dataframe()
    current_db = load_records_from_db()

    current_records = prepare_comparison(current_db) if not current_db.empty else set()
    update_records = prepare_comparison(update) if not update.empty else set()

    missing_records = current_records - update_records
    new_records = update_records - current_records

    return missing_records, new_records, current_db, update


def add_date_to_column(frame, column):
    """Add a timestamp to the records DataFrame."""
    frame[column] = datetime.now().strftime(DATE_FORMAT)
    frame[column] = pd.to_datetime(frame[column], format=DATE_FORMAT)
    return frame


def show_recently_changed(record_type) -> pd.DataFrame:
    """Load job records from the database where added_date is less than 1 day old.
    Inputs: "active" or "archived"."""
    db: Session = SessionLocal()
    try:
        three_days_ago = datetime.now() - timedelta(days=3)

        if record_type == "active":
            records = (
                db.query(JobOfferRecord)
                .filter(JobOfferRecord.added_date >= three_days_ago)
                .where(JobOfferRecord.offer_status == "active")
                .all()
            )
        elif record_type == "archived":
            records = (
                db.query(JobOfferRecord)
                .filter(JobOfferRecord.archived_date >= three_days_ago)
                .where(JobOfferRecord.offer_status == "archived")
                .all()
            )

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
                "notes": record.notes if hasattr(record, "notes") else "",
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
    finally:
        db.close()
