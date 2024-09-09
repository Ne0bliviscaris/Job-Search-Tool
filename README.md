# Job-Search-Tool
Organizer for job searching across multiple sites. Fetch offers, measure recruitment progress, collect info about potential employer


# TODO:
- Multi website support
- Save to file function
- Sync with file
- Move out of date files to archive
- Add buttons to fetch records and save them to file

# Changelog:
<details>
# 09.09.2024
Massively reduced update time complexity by reusing one webdriver
# 06.09.2024
- Moved data extraction to containers:
Instead of only pointing containers, functions now handle data extraction. This greatly improves scaleability for the project
- Big improvements to code clarity
- Solved *theprotocol* fetching inconsistencies by setting fixed chromedriver window size (not displayed anyway)
The point of failure was rendering site in mobile version by default
# 05.09.2024
- Now salary extraction properly handles various notations
# 04.09.2024
- Moved to *Selenium* scraping. This provides better results than requests.
- Introduced file handling. Now data is extracted from saved files, resulting in improved performance. Update function scrapes search links to their respective file.
- Search links are now stored in a dictionary with this structure: {website_tag1-tag2-tag3 : link} This enables using multiple links from same website.
# 03.09.2024
- Temporarily dropped Streamlit and Selenium to work on basics.
# 27.08.2024
- Moved to Streamlit
- Added function to turn records into dataframe
26.08.2024
- Introduced JobRecord class to handle HTML records
</details>