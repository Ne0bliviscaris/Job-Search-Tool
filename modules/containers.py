from modules.websites import JUSTJOINIT  # Same structure as RocketJobs
from modules.websites import (
    BULLDOGJOB,
    NOFLUFFJOBS,
    PRACUJPL,
    ROCKETJOBS,
    SOLIDJOBS,
    THEPROTOCOL,
    identify_website,
)


def search(search_link: str) -> str:
    """Returns search container for each website"""
    current_website = identify_website(search_link)
    if NOFLUFFJOBS in current_website:
        return '[class="list-container"]'
    elif THEPROTOCOL in current_website:
        return '[data-test="offersList"]'
    elif BULLDOGJOB in current_website:
        return '[id="__next"]'
    elif ROCKETJOBS in current_website or JUSTJOINIT in current_website:
        return '[data-test-id="virtuoso-item-list"]'
    elif SOLIDJOBS in current_website:
        return '[class="scrollable-content"]'
    elif PRACUJPL in current_website:
        return '[data-test="section-offers"]'
    else:
        return None


def detect_records(html, search_link) -> list[str]:
    """Returns record container content for each website"""
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

    elif SOLIDJOBS in search_link:
        record_container = "offer-list-item"
        return [job for job in html.find_all(record_container)]

    elif PRACUJPL in search_link:
        record_container = {"data-test": "default-offer"}
        return [job for job in html.find_all(attrs=record_container)]

    else:
        return None


def url(record, search_link) -> str:
    """Returns url container content for each website"""
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

    elif SOLIDJOBS in search_link:
        url_a = record.find("a", href=True)
        url = url_a.get("href")

    elif PRACUJPL in search_link:
        url_a = record.find("a", {"data-test": "link-offer"})
        url = url_a.get("href")

    if url:
        if url.startswith("http"):
            return url
        else:
            return search_link.rstrip("/") + "/" + url.lstrip("/")
    return None


def job_title(html, search_link) -> str:
    """Returns title container content for each website"""
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

    elif SOLIDJOBS in search_link:
        title = html.find("h2")
        return title.text.strip() if title else None

    elif PRACUJPL in search_link:
        title = html.find("h2", {"data-test": "offer-title"})
        return title.text.strip() if title else None

    else:
        return None


def tags(html, search_link: str) -> str:
    """Returns tags container content for each website as a string separated by ' | '"""
    if NOFLUFFJOBS in search_link:
        tags_container = {"data-cy": "category name on the job offer listing"}
        job_tags = [job.text for job in html.find_all(attrs=tags_container)]
        return " | ".join(job_tags) if job_tags else ""

    elif THEPROTOCOL in search_link:
        tags_container = {"data-test": "chip-expectedTechnology"}
        job_tags = [job.text for job in html.find_all(attrs=tags_container)]
        return " | ".join(job_tags) if job_tags else ""

    elif BULLDOGJOB in search_link:
        tags_container = {"class": lambda class_name: class_name and class_name.startswith("JobListItem_item__tags")}
        tags_block = html.find(attrs=tags_container)
        if tags_block:
            job_tags = [span.text for span in tags_block.find_all("span")]
            return " | ".join(job_tags) if job_tags else ""

    elif ROCKETJOBS in search_link or JUSTJOINIT in search_link:
        tag_container = lambda class_name: class_name and class_name.startswith("skill-tag")
        tags = html.find_all(class_=tag_container)
        return " | ".join(tag.text.strip() for tag in tags) if tags else ""

    elif SOLIDJOBS in search_link:
        tags_block = html.find_all("solidjobs-skill-display")
        job_tags = [tag.text.strip().replace("# ", "") for tag in tags_block]
        return " | ".join(job_tags) if job_tags else ""

    elif PRACUJPL in search_link:
        tags_block = html.find_all("span", {"data-test": "technologies-item"})
        job_tags = [tag.text.strip() for tag in tags_block]
        return " | ".join(job_tags) if job_tags else ""

    else:
        return None


def company(html, search_link: str) -> dict:
    """Returns company name container content for each website"""
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

    elif SOLIDJOBS in search_link:
        company = html.find("a", {"mattooltip": "Kliknij, aby zobaczy pozostałe oferty firmy."})
        return company.text.strip() if company else None

    elif PRACUJPL in search_link:
        company = html.find("h3", {"data-test": "text-company-name"})
        return company.text.strip() if company else None

    else:
        return None


def logo(html, search_link: str) -> dict:
    """Returns logo container content for each website"""
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

    elif SOLIDJOBS in search_link:
        logo = html.find("img")
        return logo.get("src") if logo else None

    elif PRACUJPL in search_link:
        logo = html.find("img", {"data-test": "image-responsive"})
        return logo.get("src") if logo else None

    else:
        return None


def location(html, search_link: str) -> dict:
    """Returns location container content for each website"""
    if NOFLUFFJOBS in search_link:
        location_container = {"data-cy": "location on the job offer listing"}
        location = html.find(attrs=location_container)
        return location.text if location else None

    elif THEPROTOCOL in search_link:
        location_container = {"data-test": "text-workplaces"}
        job_location_elements = html.find_all(attrs=location_container)
        location = [job.text for job in job_location_elements if job.text]

        # Separate field for remote status
        remote_keywords = ["remote", "zdalna"]
        hybrid_keywords = ["hybrid", "hybrydowa", "remote hybrid"]
        stationary_keywords = ["stationary", "stacjonarna", "full office"]
        location = [
            loc
            for loc in location
            if not any(keyword in loc.lower() for keyword in remote_keywords + hybrid_keywords + stationary_keywords)
        ]

        return " | ".join(location) if location else None

    elif BULLDOGJOB in search_link:
        location_container = {
            "class": lambda class_name: class_name and class_name.startswith("JobListItem_item__details")
        }
        details_block = html.find(attrs=location_container)
        if details_block:
            hidden_block = details_block.find("div", class_="hidden")
            if hidden_block:
                job_location = [span.text.strip() for span in hidden_block.find_all("span") if span.text.strip()]
                # Remove "remote" from the location - separate field for remote status
                job_location = [loc for loc in job_location if "remote" not in loc.lower()]
                formatted_location = " | ".join(job_location).replace(",", " | ")
                return formatted_location if formatted_location else None

    elif ROCKETJOBS in search_link:
        MuiBox_block = html.find_all("div", class_="MuiBox-root")
        location_elements = MuiBox_block[11].find_all("span")
        if location_elements:
            locations = [loc.text for loc in location_elements]
            return locations[0]
        return None

    # Here JustJoinIT differs from RocketJobs by one index
    elif JUSTJOINIT in search_link:
        MuiBox_block = html.find_all("div", class_="MuiBox-root")
        location_elements = MuiBox_block[11].find_all("span")
        locations = [loc.text for loc in location_elements[1:]]
        return locations[0]

    elif SOLIDJOBS in search_link:
        """
        Returns location container content for SOLIDJOBS website
        """
        location_container = html.find("div", class_="flex-row")
        if location_container:
            location_elements = location_container.find_all("i", {"aria-hidden": "true"})
            if len(location_elements) > 1:
                location = location_elements[1].parent
                formatted_location = location.text.replace("100% zdalnie", "").replace("(", "").replace(")", "")
                return formatted_location.strip()
        return None

    elif PRACUJPL in search_link:
        loc = html.find("h4", {"data-test": "text-region"})
        if loc and loc.strong:
            location = loc.strong.text.replace("Cała Polska (praca zdalna)", "").strip()
            return location
        return None

    else:
        return None


def remote_status(html, search_link: str) -> str:
    """Returns location container content for each website"""
    if NOFLUFFJOBS in search_link:
        location_container = {"data-cy": "location on the job offer listing"}
        locations = html.find_all(attrs=location_container)
        status = [loc.text.strip() for loc in locations]
        if "remote" in status:
            return "Remote"
        elif "hybrid" in status:
            return "Hybrid"
        else:
            return "Stationary"

    elif THEPROTOCOL in search_link:
        remote_container = {"data-test": "text-workModes"}
        job_location_elements = html.find_all(attrs=remote_container)
        job_location = [job.text.strip().lower() for job in job_location_elements]

        remote_keywords = ["remote", "zdalna"]
        hybrid_keywords = ["hybrid", "hybrydowa", "remote hybrid"]

        for location in job_location:
            if any(keyword in location for keyword in remote_keywords):
                return "Remote"
            elif any(keyword in location for keyword in hybrid_keywords):
                return "Hybrid"
            else:
                return "Stationary"
    elif BULLDOGJOB in search_link:
        remote_container = {
            "class": lambda class_name: class_name and class_name.startswith("JobListItem_item__details")
        }
        details_block = html.find(attrs=remote_container)
        if details_block:
            hidden_block = details_block.find("div", class_="hidden")
            if hidden_block:
                job_location = [span.text.strip().lower() for span in hidden_block.find_all("span")]
                if "remote" in job_location:
                    return "Remote"
                else:
                    return "Stationary"

    elif ROCKETJOBS in search_link:
        MuiBox_block = html.find_all("div", class_="MuiBox-root")
        location = MuiBox_block[11].find_all("span")
        if "Praca zdalna" in location[-1].text:
            return "Remote"
        else:
            return "Stationary"

    # Here JustJoinIT differs from RocketJobs by one index
    elif JUSTJOINIT in search_link:
        MuiBox_block = html.find_all("div", class_="MuiBox-root")
        location = MuiBox_block[11].find_all("span")
        if "remote" in location[-1].text:
            return "Remote"
        elif "hybryd" in location[-1].text:
            return "Hybrid"
        else:
            return "Stationary"

    elif SOLIDJOBS in search_link:
        """
        Returns location container content for SOLIDJOBS website
        """
        location = html.find_all("a", {"mattooltip": True})
        remote_status = location[-1]
        if "zdalna" in remote_status.text:
            return "Remote"
        elif "hybrydowa" in remote_status.text:
            return "Hybrid"
        else:
            return "Stationary"

    elif PRACUJPL in search_link:
        additional_info_containers = lambda tag: tag.has_attr("data-test") and tag["data-test"].startswith(
            "offer-additional-info"
        )
        additional_info = html.find_all(additional_info_containers)
        status = additional_info[-1].text
        if "zdalna" in status:
            return "Remote"
        elif "hybrydowa" in status:
            return "Hybrid"
        else:
            return "Stationary"

    else:
        return None


def salary(html, search_link: str) -> dict:
    """Returns salary container content for each website"""
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

    elif SOLIDJOBS in search_link:
        salary = html.find("span", class_="badge-salary")
        return salary.text.strip() if salary else None

    elif PRACUJPL in search_link:
        salary = html.find("span", {"data-test": "offer-salary"})
        return salary.text.strip() if salary else None

    else:
        return None
