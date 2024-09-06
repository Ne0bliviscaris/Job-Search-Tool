# Job-Search-Tool
Organizer for job searching across multiple sites. Fetch offers, measure recruitment progress, collect info about potential employer


# TODO:



**print class object instead of dataframe upon launching file**
**all JobRecord methods return none upon fail**

# - Move entire container handling to containers.py

# elif JUSTJOIN in search_link:
#        job_title = [job.text for job in self.html.find(attrs={"class": "css-3hs82j"})]
#        return job_title



- Multi website support
- Save to file function
- Sync with file
- Move out of date files to archive
- Add buttons to fetch records and save them to file

# Changelog:
27.08.2024
- Moved to Streamlit
- Added function to turn records into dataframe
26.08.2024
- Introduced JobRecord class to handle HTML records