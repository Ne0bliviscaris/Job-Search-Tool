import streamlit as st

from modules.database.backup import backup_db, fetch_all_backups, restore_backup


def backup_button():
    """Backup database button."""
    if st.button("Backup database"):
        with st.spinner("Backing up..."):  # Display a spinner while updating
            backup_db()
            st.success("Database backed up successfully!")


def show_backups():
    """Show all database backups."""
    st.title("Restore backup:")
    backups = fetch_all_backups()
    if backups:
        for backup in backups:
            col1, col2 = st.columns([2, 1])
            with col1:
                st.write(backup)  # display backup name
            with col2:
                if st.button("Restore", key=backup):
                    with st.spinner("Restoring..."):
                        restore_backup(backup)

    else:
        st.warning("No backups found.")


st.title("Database Backup browser")
backup_button()
show_backups()
