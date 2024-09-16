# Job-Search-Tool
Organizer for job searching across multiple sites. Fetch offers, measure recruitment progress, collect info about potential employer

Current dataframe state:

![Raw Scraped Screenshot](screenshots/raw_scraped.png)

# TODO:
## Data processing
#### Location fetching adjustments
- If site puts selected location on first place - use only the first location
- Else - fetch html with location block hovered to show extract list of all locations

#### Get proper search links
#### Raw data extraction improvements:
- Location extraction improvements - making sure that either a list or the proper location is extracted
#### Synchronization ETL module:
- Extract elements from raw CSV -> unify them across all sites
- Use tag and location dictionaries to unify variable elements
- Mark new offers as new
- Move finished offers to archive
- Gather additional data, like added time, removed time
- Browseable archive file
#### Records visualization:
- Prepare record template - fetch one record from CSV, fill specific fields
- Initially scrolled up, showing minimal info. Click, to show full record details

- Add additional editable fields: 
    - Mark as applied button - saves current time as time applied
    - Application status - not applied, applied, rejected
    - Feedback status - received or not received
    - Note field for feedback
    - Mark as interesting, prefferable 1-5 stars ranking

## Cloud related issues
#### Session and data access:
- Introduce session for admin user
- Columns not for public info available only for admin
- Saving data/files available only for admin
#### Move to docker container and host it remotely
- Run updater on a scheduler


# Ideas for the future:
- Scrape each interesting offer (3+ stars)
- Fetch and unify requirements, additional info etc
- Build RAG using my CV to analyze each offer in relation to my skills
- RAG generate unified template from scraped offers

# Changelog:
#### 16.09.2024
- Improvement in extracting job location. Added separate field for remote job status
- Properly extracting salary details (currency etc) 
- Fixed logo extraction from Nofluffjobs
- Storing job tags as a string
#### 14.09.2024
- Introduced Streamlit
#### 11.09.2024
- Integrated JustJoinIT.pl site
- Integrated Solid.jobs site
- Integrated it.pracuj.pl site
#### 10.09.2024
- Integrated Rocketjobs.pl site
- Integrated Bulldogjob.pl site
- Minor improvements to handling data extraction
#### 09.09.2024
- Massively reduced update time complexity by reusing one webdriver
#### 06.09.2024
- Moved data extraction to containers:
Instead of only pointing containers, functions now handle data extraction. This greatly improves scaleability for the project
- Big improvements to code clarity
- Solved *theprotocol* fetching inconsistencies by setting fixed chromedriver window size (not displayed anyway)
The point of failure was rendering site in mobile version by default
#### 05.09.2024
- Now salary extraction properly handles various notations
#### 04.09.2024
- Moved to *Selenium* scraping. This provides better results than requests.
- Introduced file handling. Now data is extracted from saved files, resulting in improved performance. Update function scrapes search links to their respective file.
- Search links are now stored in a dictionary with this structure: {website_tag1-tag2-tag3 : link} This enables using multiple links from same website.
#### 03.09.2024
- Temporarily dropped Streamlit and Selenium to work on basics.
#### 27.08.2024
- Moved to Streamlit
- Added function to turn records into dataframe
#### 26.08.2024
- Introduced JobRecord class to handle HTML records
