import streamlit as st

import modules.database.backup as backup


def backup_button():
    """Backup database button."""
    if st.button("Backup database"):
        with st.spinner("Backing up..."):  # Display a spinner while updating
            backup.backup_db()
            st.success("Database backed up successfully!")


def show_backups():
    """Show all database backups."""
    st.title("Restore backup:")
    backups_list = backup.fetch_all_backups()
    if backups_list:
        for backup_file in backups_list:
            col1, col2 = st.columns([2, 1])
            with col1:
                st.write(backup.get_date_from_filename(backup_file))
            with col2:
                if st.button("Restore", key=backup_file):
                    with st.spinner("Restoring..."):
                        backup.restore_backup(backup_file)

    else:
        st.warning("No backups found.")


st.title("Database Backup browser")
backup_button()
show_backups()
