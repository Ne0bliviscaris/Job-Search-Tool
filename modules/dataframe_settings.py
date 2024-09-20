import pandas as pd
import streamlit as st

MAIN_FRAME_COLUMNS = [
    "title",
    "logo",
    "company_name",
    "location",
    "remote_status",
    "min_salary",
    "max_salary",
    "salary_details",
    "tags",
    "added_date",
    "url",
    "application_date",
    "feedback_received",
    "notes",
    "personal_rating",
]
ARCHIVE_COLUMNS = [
    "title",
    "logo",
    "company_name",
    "location",
    "remote_status",
    "min_salary",
    "max_salary",
    "salary_details",
    "tags",
    "added_date",
    "url",
    "application_date",
    "feedback_received",
    "notes",
    "personal_rating",
    "archived_date",
]


def set_column_config():
    """Return column configuration for the data editor."""
    return {
        "url": st.column_config.LinkColumn("URL"),
        "logo": st.column_config.ImageColumn("Logo", width=100),
        "application_date": st.column_config.DateColumn("Application date", format="DD-MM-YYYY"),
        "added_date": st.column_config.DateColumn("Application date", format="DD-MM-YYYY"),
        "feedback_received": st.column_config.CheckboxColumn("Feedback received"),
        "notes": st.column_config.TextColumn("Notes"),
    }


def column_conversions(frame, archive=False):
    """Return column conversions for the data editor."""
    if archive is False:
        columns = MAIN_FRAME_COLUMNS
    else:
        columns = ARCHIVE_COLUMNS

    frame["added_date"] = pd.to_datetime(frame["added_date"], errors="coerce")
    if "archived_date" in frame.columns:
        frame["archived_date"] = pd.to_datetime(frame["archived_date"], errors="coerce")
    if "application_date" in frame.columns:
        frame["application_date"] = pd.to_datetime(frame["application_date"], errors="coerce")
    edited_df = st.data_editor(frame[columns], disabled=archive, column_config=set_column_config())
    return edited_df


def handle_missing_columns(frame):
    """Handle missing columns in the dataframe."""
    if not frame.empty:
        for col in ["application_date", "feedback_received", "notes", "personal_rating"]:
            if col not in frame.columns:
                frame[col] = None  # lub odpowiednia wartość domyślna
        return frame
