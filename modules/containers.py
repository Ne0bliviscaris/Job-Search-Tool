from websites import JUSTJOINIT  # Same structure as RocketJobs
from websites import BULLDOGJOB, NOFLUFFJOBS, ROCKETJOBS, THEPROTOCOL, identify_website


def search(search_link: str) -> str:
    """
    Returns search container for each website
    """
    current_website = identify_website(search_link)
    if NOFLUFFJOBS in current_website:
        return "nfj-postings-list"
    elif THEPROTOCOL in current_website:
        return '[data-test="offersList"]'
    elif BULLDOGJOB in current_website:
        return '[id="__next"]'
    elif ROCKETJOBS in current_website or JUSTJOINIT in current_website:
        return '[data-test-id="virtuoso-item-list"]'
    else:
        raise ValueError(f"Unknown website: {current_website}")


def detect_records(html, search_link) -> list[str]:
    """
    Returns record container content for each website
    """
    if NOFLUFFJOBS in search_link:
        record_container = {"id": lambda id_name: id_name and id_name.startswith("nfjPostingListItem")}
        return [job for job in html.find_all(attrs=record_container)]

    elif THEPROTOCOL in search_link:
        record_container = {"data-test": "list-item-offer"}
        return [job for job in html.find_all(attrs=record_container)]

    elif BULLDOGJOB in search_link:
        record_container = {
            "class": lambda class_name: (
                class_name
                and class_name.startswith("JobListItem_item")
                and all(
                    excluded not in class_name for excluded in ["logo", "title", "details", "salary", "tags", "save"]
                )
            )
        }
        return [job for job in html.find_all(attrs=record_container)]

    elif ROCKETJOBS in search_link or JUSTJOINIT in search_link:
        record_container = {"data-index": True}
        return [job for job in html.find_all(attrs=record_container)]
    else:
        raise ValueError(f"Unknown website: {search_link}")


def url(record, search_link) -> str:
    """
    Returns url container content for each website
    """
    if NOFLUFFJOBS in search_link:
        # url = record.get("a", href=True)
        url = record.get("href")

    elif THEPROTOCOL in search_link:
        url = record.get("href")

    elif BULLDOGJOB in search_link:
        url = record.get("href")

    elif ROCKETJOBS in search_link or JUSTJOINIT in search_link:
        url_a = record.find("a", href=True)
        url = url_a.get("href")

    if url:
        if url.startswith("http"):
            return url
        else:
            return search_link.rstrip("/") + "/" + url.lstrip("/")
    return None


def job_title(html, search_link) -> str:
    """
    Returns title container content for each website
    """
    if NOFLUFFJOBS in search_link:
        title_container = {"data-cy": "title position on the job offer listing"}
        title = html.find(attrs=title_container)
        return title.text if title else None

    elif THEPROTOCOL in search_link:
        title_container = {"data-test": "text-jobTitle"}
        title = html.find(attrs=title_container)
        return title.text if title else None

    elif BULLDOGJOB in search_link:
        title_container = {"class": lambda class_name: class_name and class_name.startswith("JobListItem_item__title")}
        title_block = html.find(attrs=title_container)
        if title_block:
            title = title_block.find("h3")
            return title.text if title else None
    elif ROCKETJOBS in search_link or JUSTJOINIT in search_link:
        title = html.h3
        return title.text if title else None

    else:
        raise ValueError(f"Unknown website: {search_link}")


def tags(html, search_link: str) -> list[str]:
    """
    Returns tags container content for each website
    """
    if NOFLUFFJOBS in search_link:
        tags_container = {"data-cy": "category name on the job offer listing"}
        job_tags = [job.text for job in html.find_all(attrs=tags_container)]
        return job_tags if job_tags else None

    elif THEPROTOCOL in search_link:
        tags_container = {"data-test": "chip-expectedTechnology"}
        job_tags = [job.text for job in html.find_all(attrs=tags_container)]
        return job_tags if job_tags else None

    elif BULLDOGJOB in search_link:
        tags_container = {"class": lambda class_name: class_name and class_name.startswith("JobListItem_item__tags")}
        tags_block = html.find(attrs=tags_container)
        if tags_block:
            job_tags = [span.text for span in tags_block.find_all("span")]
            return job_tags if job_tags else []

    elif ROCKETJOBS in search_link or JUSTJOINIT in search_link:
        tag_container = lambda class_name: class_name and class_name.startswith("skill-tag")
        tags = html.find_all(class_=tag_container)
        return [tag.text.strip() for tag in tags] if tags else []

    else:
        raise ValueError(f"Unknown website: {search_link}")


def company(html, search_link: str) -> dict:
    """
    Returns company name container content for each website
    """
    if NOFLUFFJOBS in search_link:
        company_container = {
            "class": "tw-text-gray-60 company-name tw-w-[50%] desktop:tw-w-auto tw-mb-0 !tw-text-xs !desktop:tw-text-sm tw-font-semibold desktop:tw-font-normal"
        }
        company = html.find(attrs=company_container)
        return company.text if company else None

    elif THEPROTOCOL in search_link:
        company_container = {"data-test": "text-employerName"}
        company = html.find(attrs=company_container)
        return company.text if company else None

    elif BULLDOGJOB in search_link:
        title_container = {"class": lambda class_name: class_name and class_name.startswith("JobListItem_item__title")}
        title_block = html.find(attrs=title_container)
        if title_block:
            # Find the <h3> tag and then get the next <div> sibling
            h3_tag = title_block.find("h3")
            if h3_tag:
                company_div = h3_tag.find_next_sibling("div")
                if company_div:
                    return company_div.text.strip()

    elif ROCKETJOBS in search_link or JUSTJOINIT in search_link:
        MuiBox_block = lambda class_name: class_name and class_name.startswith("MuiBox-root")
        svg_icon = html.find("svg", {"data-testid": "ApartmentRoundedIcon"})
        if svg_icon:
            parent_div = svg_icon.find_parent("div", class_=MuiBox_block)
            if parent_div:
                company_name = parent_div.span
                return company_name.text.strip() if company_name else None

    else:
        raise ValueError(f"Unknown website: {search_link}")


def logo(html, search_link: str) -> dict:
    """
    Returns logo container content for each website
    """
    if NOFLUFFJOBS in search_link:
        logo_container = {"alt": "Company logo"}
        logo = html.find(attrs=logo_container)
        return logo.get("src") if logo else None

    elif THEPROTOCOL in search_link:
        logo_container = {"data-test": "icon-companyLogo"}
        logo = html.find(attrs=logo_container)
        return logo.get("src") if logo else None

    elif BULLDOGJOB in search_link:
        logo_container = {"class": lambda class_name: class_name and class_name.startswith("JobListItem_item__logo")}
        logo = html.find(attrs=logo_container)
        return logo.find("img").get("src") if logo else None

    elif ROCKETJOBS in search_link or JUSTJOINIT in search_link:
        logo = html.img
        return logo.get("src") if logo else None

    else:
        raise ValueError(f"Unknown website: {search_link}")


def location(html, search_link: str) -> dict:
    """
    Returns location container content for each website
    """
    if NOFLUFFJOBS in search_link:
        location_container = {"data-cy": "location on the job offer listing"}
        job_location_elements = html.find_all(attrs=location_container)
        job_location = [job.text.strip() for job in job_location_elements]
        return job_location[0] if job_location else None
    elif THEPROTOCOL in search_link:
        location_container = {"data-test": "text-workModes"}
        job_location_elements = html.find_all(attrs=location_container)
        job_location = [job.text.strip() for job in job_location_elements]
        return job_location if job_location else None
    elif BULLDOGJOB in search_link:
        location_container = {
            "class": lambda class_name: class_name and class_name.startswith("JobListItem_item__details")
        }
        details_block = html.find(attrs=location_container)
        if details_block:
            hidden_block = details_block.find("div", class_="hidden")
            if hidden_block:
                job_location = [span.text.strip() for span in hidden_block.find("span")]
                return job_location if job_location else None
    elif ROCKETJOBS in search_link:
        MuiBox_block = html.find_all("div", class_="MuiBox-root")
        location_elements = MuiBox_block[11].find_all("span")
        if location_elements:
            locations = [loc.text.strip() for loc in location_elements]
            return " | ".join(locations)
        return None
    # Here JustJoinIT differs from RocketJobs by one index
    elif JUSTJOINIT in search_link:
        MuiBox_block = html.find_all("div", class_="MuiBox-root")
        location_elements = MuiBox_block[11].find_all("span")
        if location_elements:
            locations = [loc.text.strip() for loc in location_elements[1:]]
            return " | ".join(locations)
        return None
    else:
        raise ValueError(f"Unknown website: {search_link}")


def salary(html, search_link: str) -> dict:
    """
    Returns salary container content for each website
    """
    if NOFLUFFJOBS in search_link:
        salary_container = {"data-cy": "salary ranges on the job offer listing"}
        return html.find(attrs=salary_container)

    elif THEPROTOCOL in search_link:
        salary_container = {"data-test": "text-salary"}
        return html.find(attrs=salary_container)

    elif BULLDOGJOB in search_link:
        salary_container = {
            "class": lambda class_name: class_name and class_name.startswith("JobListItem_item__salary")
        }
        salary_elements = html.find(attrs=salary_container)
        return salary_elements if salary_elements else ""

    elif ROCKETJOBS in search_link or JUSTJOINIT in search_link:
        # All containers on site are MuiBox-root. Need to find the right one
        MuiBox_block = lambda class_name: class_name and class_name.startswith("MuiBox-root")

        # Salary is contained in the same parent div as the h3 tag with job title
        h3_container = html.h3
        if h3_container:
            parent_div = h3_container.find_parent("div", class_=MuiBox_block)
            # Salary is hidden in MuiBox-root inside another MuiBox-root inside the parent div with h3
            if parent_div:
                salary_div = parent_div.find("div", class_=MuiBox_block).find("div", class_=MuiBox_block)
                if salary_div:
                    salary_elements = salary_div.find_all("span")
                    if salary_elements:
                        salary = [pay.text.strip() for pay in salary_elements]
                        return " - ".join(salary)
        return ""
    else:
        raise ValueError(f"Unknown website: {search_link}")
