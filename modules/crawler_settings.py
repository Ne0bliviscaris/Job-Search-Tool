# NoFluffJobs
    job_name = job.find(attrs={"data-cy": "title position on the job offer listing"}).text
    job_tags = [tag.text for tag in job.find_all(attrs={"data-cy": "category name on the job offer listing"})]
    salary_elements = job.find(attrs={"data-cy": "salary ranges on the job offer listing"})
    job_location = [loc.text.strip() for loc in job.find_all(attrs={"data-cy": "location on the job offer listing"})]
    job_url = "https://nofluffjobs.com" + job["href"]
    company_name = job.find("h4").text.strip()