from datetime import datetime
from unittest.mock import patch

import pandas as pd
import pytest

from modules.settings import DATE_FORMAT
from modules.tests.sync.dummy_records import (
    get_dummy_db_records,
    get_dummy_empty_records,
    get_dummy_scraped_records,
)
from modules.updater.data_processing.sync import process_new_records


@pytest.fixture
def empty_new_records():
    """Fixture for an empty DataFrame for new records."""
    return get_dummy_empty_records()


@pytest.fixture
def new_records():
    """Fixture for a DataFrame with new records."""
    return get_dummy_scraped_records()


@pytest.fixture
def current_db():
    """Fixture for a DataFrame with current database records."""
    return get_dummy_db_records()


@patch("modules.updater.data_processing.sync.save_records_to_db")
def test_empty_update(mock_save_records_to_db, empty_new_records):
    """Test process_new_records with empty DataFrames."""
    process_new_records(empty_new_records)

    # Check if save_records_to_db was not called
    mock_save_records_to_db.assert_not_called()


@patch("modules.updater.data_processing.sync.save_records_to_db")
def test_new_records(mock_save_records_to_db, new_records):
    """Test process_new_records with new_records containing two records."""
    process_new_records(new_records)

    # Check if save_records_to_db was called once with the new records
    mock_save_records_to_db.assert_called_once()
    saved_df = mock_save_records_to_db.call_args[0][0]
    assert len(saved_df) == 5  # All 5 records should be saved

    expected_titles = pd.Series(["Job1", "Job2", "Job8", "Job9", "Job10"])
    expected_companies = pd.Series(["Company1", "Company2", "Company8", "Company9", "Company10"])

    assert saved_df["title"].reset_index(drop=True).equals(expected_titles)
    assert saved_df["company_name"].reset_index(drop=True).equals(expected_companies)
    assert "added_date" in saved_df.columns

    today = pd.to_datetime(datetime.now().strftime(DATE_FORMAT))
    assert all(saved_df["added_date"].dt.strftime(DATE_FORMAT) == today.strftime(DATE_FORMAT))
