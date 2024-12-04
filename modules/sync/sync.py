from datetime import datetime, timedelta

import pandas as pd
from sqlalchemy.orm import Session

from modules.data_collector import html_dataframe
from modules.database.database import (
    JobOfferRecord,
    SessionLocal,
    ensure_database_exists,
    load_records_from_db,
    save_records_to_db,
    update_record,
)
from modules.debug.sync import DEBUG_SYNC, find_differences
from modules.settings import DATE_FORMAT

ensure_database_exists()
COLUMNS_TO_COMPARE = [
    "title",
    "company_name",
    "website",
    "remote_status",
    "salary_details",
    "tags",
    "location",
]


def sync_records():
    """
    Main function to oversee the synchronisation process
    Extract records from raw, add additional information and return processed data into a new file
    """
    update = html_dataframe()
    db = load_records_from_db(all_records=DEBUG_SYNC)
    missing_records, new_records = find_changed_records(update, db)
    if not DEBUG_SYNC:
        archive_records(missing_records)
        process_new_records(db, new_records)


def prepare_comparison(frame: pd.DataFrame):
    """Set columns for the DataFrame."""
    columns_to_compare = frame[COLUMNS_TO_COMPARE]
    rows_as_tuples = columns_to_compare.apply(tuple, axis=1)
    rows_to_compare = set(rows_as_tuples)
    return rows_to_compare


def filter_matching_df(db_records, tested_records) -> pd.DataFrame:
    """Returns only df records matching given records.
    Compares content of columns specified in COLUMNS_TO_COMPARE."""
    if not db_records.empty:
        columns = db_records[COLUMNS_TO_COMPARE]
        df_rows = columns.apply(tuple, axis=1)
        matching_records = df_rows.isin(tested_records)
        return db_records[matching_records]
    else:
        return pd.DataFrame()


def process_new_records(current_db: pd.DataFrame, new_records: pd.DataFrame) -> None:
    """Process new records adding custom columns and timestamp."""
    if not new_records.empty:
        if current_db.empty:
            new_records = add_date_to_column(new_records, column="added_date")
            save_records_to_db(new_records)
        else:
            # Ensure new records are not already in the current database
            new_set = prepare_comparison(new_records)
            current_set = prepare_comparison(current_db)
            unique_new_set = new_set - current_set
            unique_new_df = new_records[new_records.apply(tuple, axis=1).isin(unique_new_set)]

            if not unique_new_df.empty:
                unique_new_df = add_date_to_column(unique_new_df, column="added_date")
                save_records_to_db(unique_new_df)


def archive_records(missing_df: set) -> pd.DataFrame:
    """Archive missing records from synced file."""
    if not missing_df.empty:
        missing_df = add_date_to_column(missing_df, column="archived_date")

        for _, row in missing_df.iterrows():
            update_values = {
                "archived_date": str(row["archived_date"]),
                "offer_status": "archived",
            }
            update_record(record_id=row["id"], updates=update_values)


def find_changed_records(update, current_db):
    """Load files and return missing and new records."""

    current_set = prepare_comparison(current_db) if not current_db.empty else set()
    update_set = prepare_comparison(update) if not update.empty else set()

    missing_set = current_set - update_set
    new_set = update_set - current_set

    missing_df = filter_matching_df(current_db, missing_set)
    new_df = filter_matching_df(update, new_set)

    if DEBUG_SYNC:
        find_differences(current_db, update)
    return missing_df, new_df


def add_date_to_column(frame, column):
    """Add a timestamp to the records DataFrame."""
    date_time = datetime.now().strftime(DATE_FORMAT)
    date = date_time.split(" ")[0]

    frame[column] = date
    frame[column] = pd.to_datetime(frame[column], format=DATE_FORMAT)
    return frame


def show_recently_changed(record_type) -> pd.DataFrame:
    """Load job records from the database where added_date is less than 1 day old.
    Inputs: "active" or "archived"."""
    db: Session = SessionLocal()
    RECENT_DAYS_THRESHOLD = 1
    try:
        three_days_ago = datetime.now() - timedelta(days=RECENT_DAYS_THRESHOLD)

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
