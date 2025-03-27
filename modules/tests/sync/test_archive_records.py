# FILE: test_archive_records.py
from datetime import datetime
from unittest.mock import patch

import pandas as pd
import pytest

from modules.settings import DATE_FORMAT
from modules.tests.sync.dummy_records import (
    get_dummy_already_archived_records,
    get_dummy_db_records,
    get_dummy_empty_records,
)
from modules.updater.data_processing.sync import archive_records


@pytest.fixture
def empty_df():
    """Fixture for an empty DataFrame."""
    return get_dummy_empty_records()


@pytest.fixture
def single_record_df():
    """Fixture for a DataFrame with a single active record."""
    db_records = get_dummy_db_records()
    return db_records[db_records["id"] == 3].copy()


@pytest.fixture
def multiple_records_df():
    """Fixture for a DataFrame with multiple active records."""
    db_records = get_dummy_db_records()
    records_3_and_4 = db_records[db_records["id"].isin([3, 4])].copy()
    return records_3_and_4


@pytest.fixture
def already_archived_df():
    """Fixture for a DataFrame with already archived records."""
    return get_dummy_already_archived_records()


@patch("modules.sync.sync.update_record")
def test_empty_df(mock_update_record, empty_df):
    """Test archive_records with an empty DataFrame."""
    archive_records(empty_df)
    mock_update_record.assert_not_called()


@patch("modules.sync.sync.update_record")
def test_single_record_df(mock_update_record, single_record_df):
    """Attempt to archive single active record from db."""
    archive_records(single_record_df)
    mock_update_record.assert_called_once()
    update_values = mock_update_record.call_args.kwargs["updates"]
    archived_date = pd.to_datetime(update_values["archived_date"]).strftime(DATE_FORMAT)
    assert archived_date == datetime.now().strftime(DATE_FORMAT), "archived_date is incorrect"
    assert update_values["offer_status"] == "archived", "offer_status not set to archived"


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
    assert mock_update_record.call_count == 4

    for call in mock_update_record.call_args_list:
        update_values = call.kwargs["updates"]
        archived_date = pd.to_datetime(update_values["archived_date"]).strftime(DATE_FORMAT)
        assert archived_date == datetime.now().strftime(DATE_FORMAT)
        assert update_values["offer_status"] == "archived"
