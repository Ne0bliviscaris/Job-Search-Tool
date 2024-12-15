# test_sync_records.py
from unittest.mock import patch

import pytest

from modules.sync.sync import find_record_changes, find_set_differences, sync_records
from modules.tests.sync.dummy_records import (
    get_dummy_db_records,
    get_dummy_empty_records,
    get_dummy_scraped_records,
)


@pytest.fixture
def db_records():
    """Get dummy database records."""
    return get_dummy_db_records()


@pytest.fixture
def scraped_records():
    """Get dummy scraped records."""
    return get_dummy_scraped_records()


@pytest.fixture
def empty_records():
    """Get empty records."""
    return get_dummy_empty_records()


def test_find_set_differences_empty_frames(empty_records, scraped_records):
    """Test finding differences with empty DataFrame."""

    # Compare empty records vs scraped records
    missing_set, new_set = find_set_differences(empty_records, scraped_records)
    assert len(missing_set) == 0
    assert len(new_set) == len(scraped_records)

    # Compare scraped records vs empty records
    missing_set, new_set = find_set_differences(scraped_records, empty_records)
    assert len(missing_set) == len(scraped_records)
    assert len(new_set) == 0


def test_find_record_changes_empty_db(empty_records, scraped_records):
    """Test find_record_changes with empty database."""
    missing_records, new_records = find_record_changes(scraped_records, empty_records)

    assert len(missing_records) == 0
    assert len(new_records) == len(scraped_records)


def test_find_record_changes_partial_overlap(db_records, scraped_records):
    """Test find_record_changes with partially overlapping records."""
    missing_records, new_records = find_record_changes(scraped_records, db_records)

    # First 2 records overlap, rest are new
    assert len(missing_records) == 5  # Records from db that aren't in scraped
    assert len(new_records) == 3  # Records 8,9,10 from scraped


def test_find_record_changes_identical_records(db_records):
    """Test find_record_changes with identical records."""
    missing_records, new_records = find_record_changes(db_records, db_records)

    assert len(missing_records) == 0
    assert len(new_records) == 0


def test_find_record_changes_no_overlap(db_records, scraped_records):
    """Test find_record_changes with completely different records."""
    # Filter scraped records to only include new ones (Job8, Job9, Job10)
    new_records_only = scraped_records[scraped_records["title"].isin(["Job8", "Job9", "Job10"])]

    missing_records, new_records = find_record_changes(new_records_only, db_records)

    assert len(missing_records) == len(db_records)
    assert len(new_records) == 3  # Jobs 8,9,10


@patch("modules.sync.sync.html_dataframe")
@patch("modules.sync.sync.load_records_from_db")
@patch("modules.sync.sync.save_records_to_db")
@patch("modules.sync.sync.update_record")
def test_sync_records_flow(mock_update, mock_save, mock_load_db, mock_html_df):
    """Test complete sync_records flow."""
    # Setup test data
    mock_html_df.return_value = get_dummy_scraped_records()  # Job1,2,8,9,10
    mock_load_db.return_value = get_dummy_db_records()  # Job1-7

    # Run sync
    sync_records()

    # Verify results
    mock_save.assert_called_once()  # Should save Job8,9,10
    assert mock_update.call_count == 5  # Should archive Job3-7

    # Verify saved records
    saved_df = mock_save.call_args[0][0]
    assert len(saved_df) == 3
    assert all(x in saved_df["title"].values for x in ["Job8", "Job9", "Job10"])

    # Verify archived records
    archived_titles = [call[1]["record_id"] for call in mock_update.call_args_list]
    assert len(archived_titles) == 5
    assert all(x in archived_titles for x in range(3, 8))  # IDs 3-7
