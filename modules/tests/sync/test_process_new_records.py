from datetime import datetime
from unittest.mock import patch

import pandas as pd
import pytest

from modules.settings import DATE_FORMAT
from modules.sync.sync import process_new_records
from modules.tests.sync.dummy_records import (
    get_dummy_db_records,
    get_dummy_empty_records,
    get_dummy_fully_overlapping_records,
    get_dummy_partially_overlapping_records,
    get_dummy_scraped_records,
)


@pytest.fixture
def empty_new_records():
    """Fixture for an empty DataFrame for new records."""
    return get_dummy_empty_records()


@pytest.fixture
def update_records():
    """Fixture for a DataFrame with new records."""
    return get_dummy_scraped_records()


@pytest.fixture
def empty_db():
    """Fixture for an empty DataFrame for current database."""
    return get_dummy_empty_records()


@pytest.fixture
def current_db():
    """Fixture for a DataFrame with current database records."""
    return get_dummy_db_records()


@pytest.fixture
def fully_overlapping_new_records():
    """Fixture for a DataFrame with overlapping new records."""
    return get_dummy_fully_overlapping_records()


@pytest.fixture
def partially_overlapping_new_records():
    """Fixture for a DataFrame with partially overlapping new records."""
    return get_dummy_partially_overlapping_records()


@patch("modules.sync.sync.save_records_to_db")
def test_empty_db_empty_update(mock_save_records_to_db, empty_db, empty_new_records):
    """Test process_new_records with empty DataFrames."""
    process_new_records(empty_db, empty_new_records)

    # Check if save_records_to_db was not called
    mock_save_records_to_db.assert_not_called()


@patch("modules.sync.sync.save_records_to_db")
def test_empty_db_with_new_records(mock_save_records_to_db, empty_db, update_records):
    """Test process_new_records with empty current_db and new_records containing two records."""
    process_new_records(empty_db, update_records)

    # Check if save_records_to_db was called once with the new records
    mock_save_records_to_db.assert_called_once()
    saved_df = mock_save_records_to_db.call_args[0][0]
    assert len(saved_df) == 5  # All 5 records should be saved
    assert all(saved_df["title"] == ["Job1", "Job2", "Job8", "Job9", "Job10"])
    assert all(saved_df["company_name"] == ["Company1", "Company2", "Company8", "Company9", "Company10"])
    assert "added_date" in saved_df.columns
    assert all(saved_df["added_date"] == pd.to_datetime(datetime.now().strftime(DATE_FORMAT)))


@patch("modules.sync.sync.save_records_to_db")
def test_with_current_db_and_new_records(mock_save_records_to_db, current_db, update_records):
    """Test process_new_records with current_db containing records and new_records containing two records."""
    process_new_records(current_db, update_records)

    # Check if save_records_to_db was called once with the new records
    mock_save_records_to_db.assert_called_once()
    saved_df = mock_save_records_to_db.call_args[0][0]
    assert len(saved_df) == 3, "Wrong number of records saved. Should be 3."
    assert all(saved_df["title"] == ["Job8", "Job9", "Job10"]), "Wrong titles saved. Should be Job8, Job9, Job10."
    assert all(saved_df["company_name"] == ["Company8", "Company9", "Company10"]), "Wrong company names saved."
    assert "added_date" in saved_df.columns, "added_date column should be present."
    assert all(saved_df["added_date"] == pd.to_datetime(datetime.now().strftime(DATE_FORMAT))), "Incorrect added_date."


@patch("modules.sync.sync.save_records_to_db")
def test_with_fully_overlapping_records(mock_save_records_to_db, current_db, fully_overlapping_new_records):
    """Test process_new_records with fully overlapping records."""
    process_new_records(current_db, fully_overlapping_new_records)

    # No records should be saved as all exist in database
    mock_save_records_to_db.assert_not_called()


@patch("modules.sync.sync.save_records_to_db")
def test_with_partially_overlapping_records(mock_save_records_to_db, current_db, partially_overlapping_new_records):
    """Test process_new_records with partially overlapping records."""
    process_new_records(current_db, partially_overlapping_new_records)

    # Only new records should be saved
    mock_save_records_to_db.assert_called_once()
    saved_df = mock_save_records_to_db.call_args[0][0]
    assert len(saved_df) == 2
    assert all(saved_df["title"] == ["Job8", "Job9"])
    assert all(saved_df["company_name"] == ["Company8", "Company9"])
    assert "added_date" in saved_df.columns
    assert all(saved_df["added_date"] == pd.to_datetime(datetime.now().strftime(DATE_FORMAT)))
