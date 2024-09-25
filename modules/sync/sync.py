import os
from datetime import datetime

import pandas as pd

from modules.dataframe_settings import ALL_COLUMNS

RAW_FILE = "modules/sites/records.csv"
SYNCED_FILE = "modules/sites/synced_records.csv"
ARCHIVE_FILE = "modules/sites/archived_records.csv"
COLUMNS_TO_COMPARE = ["title", "company_name", "website", "remote_status", "salary_text"]


def load_csv(file: str) -> pd.DataFrame:
    """Load CSV file, return empty DataFrame if file does not exist."""
    if os.path.exists(file):
        return pd.read_csv(file)
    return pd.DataFrame(columns=ALL_COLUMNS)


def save_csv(dataframe, file_path, mode="w", header=True):
    """Save DataFrame to CSV file."""
    dataframe.to_csv(file_path, mode=mode, header=header, index=False)


def set_columns(file: pd.DataFrame) -> set:
    """Set columns for the DataFrame."""
    columns_to_compare = file[COLUMNS_TO_COMPARE]
    rows_as_tuples = columns_to_compare.apply(tuple, axis=1)
    rows_to_compare = set(rows_as_tuples)
    return rows_to_compare


def filter_records(df, records) -> pd.DataFrame:
    """Returns only df records matching given records.
    Compares content of columns specified in COLUMNS_TO_COMPARE."""
    columns = df[COLUMNS_TO_COMPARE]
    df_rows = columns.apply(tuple, axis=1)
    is_in_records = df_rows.isin(records)
    return df[is_in_records]


def sync_records():
    """
    Main function to oversee the synchronisation process
    Extract records from raw, add additional information and return processed data into a new file
    """
    missing_records, new_records, current_file, update = changed_records()

    # Archive missing records
    cleaned_current_file = archive_records(current_file, missing_records)

    # If the record is new, add custom columns
    synced_file = process_new_records(cleaned_current_file, new_records, update)

    # Save the updated synced file
    save_csv(synced_file, SYNCED_FILE)

    # Return the archived and new records as DataFrames
    missing_records = filter_records(current_file, missing_records)
    new_records = filter_records(update, new_records)
    return missing_records, new_records


def process_new_records(cleaned_current_file: pd.DataFrame, new_records: set, update: pd.DataFrame) -> pd.DataFrame:
    """Process new records adding custom columns and timestamp."""
    new_records_df = filter_records(update, new_records)
    if not new_records_df.empty:
        new_records_df = add_timestamp(new_records_df, "added_date")
        merged_frame = pd.concat([cleaned_current_file, new_records_df], ignore_index=True)
        return merged_frame
    return cleaned_current_file


def archive_records(current_file: pd.DataFrame, missing_records: set) -> pd.DataFrame:
    """Archive missing records from synced file."""
    records_to_archive = filter_records(current_file, missing_records)

    if not records_to_archive.empty:
        records_to_archive = add_timestamp(records_to_archive, "archived_date")

        # Append records to the archive file, adding header if the file is empty
        is_empty_archive = not os.path.exists(ARCHIVE_FILE) or os.stat(ARCHIVE_FILE).st_size == 0
        save_csv(records_to_archive, ARCHIVE_FILE, mode="a", header=is_empty_archive)

        # Remove archived records from current_file
        current_file = remove_archived_records(current_file, missing_records)

    return current_file


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
    update = load_csv(RAW_FILE)
    current_file = load_csv(SYNCED_FILE)

    current_records = set_columns(current_file) if not current_file.empty else set()
    update_records = set_columns(update)

    missing_records = current_records - update_records
    new_records = update_records - current_records

    return missing_records, new_records, current_file, update


def add_timestamp(records_frame, column_name):
    """Add a timestamp to the records DataFrame."""
    timestamp = datetime.now().strftime("%d-%m-%Y")
    records_frame[column_name] = timestamp
    records_frame[column_name] = pd.to_datetime(records_frame[column_name])
    return records_frame
