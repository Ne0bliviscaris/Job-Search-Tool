# FILE: test_archive_records.py
from datetime import datetime
from unittest.mock import patch

import pandas as pd
import pytest

from modules.settings import DATE_FORMAT
from modules.sync.sync import archive_records


@pytest.fixture
def empty_df():
    """Fixture for an empty DataFrame."""
    return pd.DataFrame()


@pytest.fixture
def single_record_df():
    """Fixture for a DataFrame with a single record."""
    return pd.DataFrame(
        {
            "id": [3],
            "title": ["Job3"],
            "company_name": ["Company3"],
            "website": ["www.company3.com"],
            "remote_status": ["Remote"],
            "salary_details": ["50k-60k"],
            "tags": ["tag1, tag2"],
            "location": ["Location3"],
            "min_salary": [50000],
            "max_salary": [60000],
            "personal_rating": [5],
            "users_id": [1],
            "added_date": [pd.to_datetime("2023-01-01")],
            "application_date": [None],
            "feedback_date": [None],
            "archived_date": [None],
            "feedback_received": [False],
            "application_status": ["Not applied"],
            "offer_status": ["active"],
        }
    )


@pytest.fixture
def multiple_records_df():
    """Fixture for a DataFrame with multiple records."""
    return pd.DataFrame(
        {
            "id": [3, 4],
            "title": ["Job3", "Job4"],
            "company_name": ["Company3", "Company4"],
            "website": ["www.company3.com", "www.company4.com"],
            "remote_status": ["Remote", "On-site"],
            "salary_details": ["50k-60k", "70k-80k"],
            "tags": ["tag1, tag2", "tag3, tag4"],
            "location": ["Location3", "Location4"],
            "min_salary": [50000, 70000],
            "max_salary": [60000, 80000],
            "personal_rating": [5, 4],
            "users_id": [1, 2],
            "added_date": [pd.to_datetime("2023-01-01"), pd.to_datetime("2023-01-02")],
            "application_date": [None, None],
            "feedback_date": [None, None],
            "archived_date": [None, None],
            "feedback_received": [False, False],
            "application_status": ["Not applied", "Applied"],
            "offer_status": ["active", "active"],
        }
    )


@pytest.fixture
def already_archived_df():
    """Fixture for a DataFrame with already archived records."""
    return pd.DataFrame(
        {
            "id": [1, 2],
            "title": ["Job1", "Job2"],
            "company_name": ["Company1", "Company2"],
            "website": ["www.company1.com", "www.company2.com"],
            "remote_status": ["Remote", "On-site"],
            "salary_details": ["50k-60k", "70k-80k"],
            "tags": ["tag1, tag2", "tag3, tag4"],
            "location": ["Location1", "Location2"],
            "min_salary": [50000, 70000],
            "max_salary": [60000, 80000],
            "personal_rating": [5, 4],
            "users_id": [1, 2],
            "added_date": [pd.to_datetime("2023-01-01"), pd.to_datetime("2023-01-02")],
            "application_date": [pd.to_datetime("2023-01-03"), pd.to_datetime("2023-01-04")],
            "feedback_date": [pd.to_datetime("2023-01-05"), pd.to_datetime("2023-01-06")],
            "archived_date": [pd.to_datetime("2023-01-07"), pd.to_datetime("2023-01-08")],
            "feedback_received": [True, False],
            "application_status": ["Applied", "Not applied"],
            "offer_status": ["archived", "archived"],
        }
    )


@pytest.fixture
def missing_columns_df():
    """Fixture for a DataFrame with missing columns."""
    return pd.DataFrame(
        {
            "title": ["Job1", "Job2"],
            "company_name": ["Company1", "Company2"],
        }
    )


@patch("modules.sync.sync.update_record")
def test_empty_df(mock_update_record, empty_df):
    """Test archive_records with an empty DataFrame."""
    archive_records(empty_df)
    mock_update_record.assert_not_called()


@patch("modules.sync.sync.update_record")
def test_single_record_df(mock_update_record, single_record_df):
    """Test archive_records with a single record."""
    archive_records(single_record_df)
    mock_update_record.assert_called_once()
    update_values = mock_update_record.call_args.kwargs["updates"]
    archived_date = pd.to_datetime(update_values["archived_date"]).strftime(DATE_FORMAT)
    assert archived_date == datetime.now().strftime(DATE_FORMAT)
    assert update_values["offer_status"] == "archived"


@patch("modules.sync.sync.update_record")
def test_multiple_records_df(mock_update_record, multiple_records_df):
    """Test archive_records with multiple records."""
    archive_records(multiple_records_df)

    assert mock_update_record.call_count == 2
    for call in mock_update_record.call_args_list:
        update_values = call.kwargs["updates"]
        archived_date = pd.to_datetime(update_values["archived_date"]).strftime(DATE_FORMAT)
        assert archived_date == datetime.now().strftime(DATE_FORMAT)
        assert update_values["offer_status"] == "archived"


@patch("modules.sync.sync.update_record")
def test_already_archived_df(mock_update_record, already_archived_df):
    """Test archive_records with already archived records."""
    archive_records(already_archived_df)
    assert mock_update_record.call_count == 2
    for call in mock_update_record.call_args_list:
        update_values = call.kwargs["updates"]
        archived_date = pd.to_datetime(update_values["archived_date"]).strftime(DATE_FORMAT)
        assert archived_date == datetime.now().strftime(DATE_FORMAT)
        assert update_values["offer_status"] == "archived"
