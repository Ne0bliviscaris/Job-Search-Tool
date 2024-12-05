from datetime import datetime
from unittest.mock import patch

import pandas as pd
import pytest

from modules.settings import DATE_FORMAT
from modules.sync.sync import process_new_records


# Test data
@pytest.fixture
def empty_new_records():
    """Fixture for an empty DataFrame for new records."""
    return pd.DataFrame()


@pytest.fixture
def new_records():
    """Fixture for a DataFrame with new records."""
    return pd.DataFrame(
        {
            "title": ["Job1", "Job2"],
            "company_name": ["Company1", "Company2"],
            "website": ["www.company1.com", "www.company2.com"],
            "remote_status": ["Remote", "On-site"],
            "salary_details": ["50k-60k", "70k-80k"],
            "tags": ["tag1, tag2", "tag3, tag4"],
            "location": ["Location1", "Location2"],
        }
    )


@pytest.fixture
def empty_db():
    """Fixture for an empty DataFrame for current database."""
    return pd.DataFrame()


@pytest.fixture
def current_db():
    """Fixture for a DataFrame with current database records."""
    return pd.DataFrame(
        {
            "title": ["Job3", "Job4"],
            "company_name": ["Company3", "Company4"],
            "website": ["www.company3.com", "www.company4.com"],
            "remote_status": ["Remote", "On-site"],
            "salary_details": ["90k-100k", "110k-120k"],
            "tags": ["tag5, tag6", "tag7, tag8"],
            "location": ["Location3", "Location4"],
            "min_salary": [90000, 110000],
            "max_salary": [100000, 120000],
            "personal_rating": [5, 4],
            "users_id": [1, 2],
            "added_date": [pd.to_datetime("2023-01-01"), pd.to_datetime("2023-01-02")],
            "application_date": [pd.to_datetime("2023-01-03"), pd.to_datetime("2023-01-04")],
            "feedback_date": [pd.to_datetime("2023-01-05"), pd.to_datetime("2023-01-06")],
            "archived_date": [pd.to_datetime("2023-01-07"), pd.to_datetime("2023-01-08")],
            "feedback_received": [True, False],
            "application_status": ["Applied", "Not applied"],
            "offer_status": ["active", "archived"],
        }
    )


@pytest.fixture
def overlapping_new_records():
    """Fixture for a DataFrame with overlapping new records."""
    return pd.DataFrame(
        {
            "title": ["Job1", "Job3"],
            "company_name": ["Company1", "Company3"],
            "website": ["www.company1.com", "www.company3.com"],
            "remote_status": ["Remote", "Remote"],
            "salary_details": ["50k-60k", "90k-100k"],
            "tags": ["tag1, tag2", "tag5, tag6"],
            "location": ["Location1", "Location3"],
        }
    )


@patch("modules.sync.sync.save_records_to_db")
def test_empty_db_empty_update(mock_save_records_to_db, empty_db, empty_new_records):
    """Test process_new_records with empty DataFrames."""
    process_new_records(empty_db, empty_new_records)

    # Check if save_records_to_db was not called
    mock_save_records_to_db.assert_not_called()


@patch("modules.sync.sync.save_records_to_db")
def test_empty_db_with_new_records(mock_save_records_to_db, empty_db, new_records):
    """Test process_new_records with empty current_db and new_records containing two records."""
    process_new_records(empty_db, new_records)

    # Check if save_records_to_db was called once with the new records
    mock_save_records_to_db.assert_called_once()
    saved_df = mock_save_records_to_db.call_args[0][0]
    assert len(saved_df) == 2
    assert all(saved_df["title"] == ["Job1", "Job2"])
    assert all(saved_df["company_name"] == ["Company1", "Company2"])
    assert "added_date" in saved_df.columns
    assert all(saved_df["added_date"] == pd.to_datetime(datetime.now().strftime(DATE_FORMAT)))


@patch("modules.sync.sync.save_records_to_db")
def test_with_current_db_and_new_records(mock_save_records_to_db, current_db, new_records):
    """Test process_new_records with current_db containing records and new_records containing two records."""
    process_new_records(current_db, new_records)

    # Check if save_records_to_db was called once with the new records
    mock_save_records_to_db.assert_called_once()
    saved_df = mock_save_records_to_db.call_args[0][0]
    assert len(saved_df) == 2
    assert all(saved_df["title"] == ["Job1", "Job2"])
    assert all(saved_df["company_name"] == ["Company1", "Company2"])
    assert "added_date" in saved_df.columns
    assert all(saved_df["added_date"] == pd.to_datetime(datetime.now().strftime(DATE_FORMAT)))


@patch("modules.sync.sync.save_records_to_db")
def test_with_overlapping_records(mock_save_records_to_db, current_db, overlapping_new_records):
    """Test process_new_records with overlapping records between current_db and new_records."""
    process_new_records(current_db, overlapping_new_records)

    # Check if save_records_to_db was called once with the new records
    mock_save_records_to_db.assert_called_once()
    saved_df = mock_save_records_to_db.call_args[0][0]
    assert len(saved_df) == 1  # Only one new unique record should be saved
    assert saved_df["title"].iloc[0] == "Job1"
    assert saved_df["company_name"].iloc[0] == "Company1"
    assert "added_date" in saved_df.columns
    assert saved_df["added_date"].iloc[0] == pd.to_datetime(datetime.now().strftime(DATE_FORMAT))
