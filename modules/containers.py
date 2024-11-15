from modules.dicts import remote_work_dict
from modules.helper_functions import remove_remote_status
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
        block_name = lambda id_name: id_name and id_name.startswith("nfjPostingListItem")
        record_container = {"id": block_name}
        records = html.find_all(attrs=record_container)

    elif THEPROTOCOL in search_link:
        record_container = {"data-test": "list-item-offer"}
        records = html.find_all(attrs=record_container)

    elif BULLDOGJOB in search_link:
        block_name = lambda class_name: class_name and class_name.startswith("JobListItem_item")
        record_container = {"class": block_name}
        records = html.find_all("a", attrs=record_container)

    elif ROCKETJOBS in search_link or JUSTJOINIT in search_link:
        record_container = {"data-index": True}
        records = html.find_all(attrs=record_container)

    elif SOLIDJOBS in search_link:
        block_name = "sj-offer-list-item"  # <sj-offer-list-item> block
        records = html.find_all(block_name)

    elif PRACUJPL in search_link:
        record_container = {"data-test": "default-offer"}
        records = html.find_all(attrs=record_container)

    if records is not None:
        return [job for job in records]
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
        container = {"data-test": "link-offer"}
        url_a = record.find("a", container)
        url = url_a.get("href") if url_a else None

    if url:
        if url.startswith("http"):
            return url
        else:
            return search_link.rstrip("/") + "/" + url.lstrip("/")
    return None


def job_title(html, search_link) -> str:
    """Returns title container content for each website"""
    if NOFLUFFJOBS in search_link:
        container = {"data-cy": "title position on the job offer listing"}
        title = html.find(attrs=container)

    elif THEPROTOCOL in search_link:
        container = {"data-test": "text-jobTitle"}
        title = html.find(attrs=container)

    elif BULLDOGJOB in search_link:
        block_name = lambda class_name: class_name and class_name.startswith("JobListItem_item__title")
        container = {"class": block_name}
        title_block = html.find(attrs=container)
        title = title_block.h3

    elif ROCKETJOBS in search_link or JUSTJOINIT in search_link:
        title = html.h3

    elif SOLIDJOBS in search_link:
        title = html.h2

    elif PRACUJPL in search_link:
        container = {"data-test": "offer-title"}
        title = html.find("h2", container)

    return title.text.strip() if title else None


def tags(html, search_link: str) -> str:
    """Returns tags container content for each website as a string separated by ' | '"""
    if NOFLUFFJOBS in search_link:
        tags_container = {"data-cy": "category name on the job offer listing"}
        tags = html.find_all(attrs=tags_container)
        tags_list = [tag.text for tag in tags]

    elif THEPROTOCOL in search_link:
        tags_container = {"data-test": "chip-expectedTechnology"}
        tags = html.find_all(attrs=tags_container)
        tags_list = [tag.text for tag in tags]

    elif BULLDOGJOB in search_link:
        name = lambda class_name: class_name and class_name.startswith("JobListItem_item__tags")
        tags_container = {"class": name}

        tags_block = html.find(attrs=tags_container)
        if tags_block:
            tags_list = [span.text for span in tags_block.find_all("span")]

    elif ROCKETJOBS in search_link or JUSTJOINIT in search_link:
        name = lambda class_name: class_name and class_name.startswith("skill-tag")
        tags = html.find_all(class_=name)
        tags_list = [tag.text for tag in tags]

    elif SOLIDJOBS in search_link:
        tags_block = html.find_all("solidjobs-skill-display")
        if tags_block:
            tags_list = [tag.text.replace("#", "") for tag in tags_block]

    elif PRACUJPL in search_link:
        container = {"data-test": "technologies-item"}
        tags_block = html.find_all("span", container)
        tags_list = [tag.text.strip() for tag in tags_block]

    merged_tags = " | ".join(tags_list)
    return merged_tags if tags_list else None


def company(html, search_link: str) -> str:
    """Returns company name container content for each website"""
    if NOFLUFFJOBS in search_link:
        name = lambda x: x and x.startswith("company-name")
        company_container = {"class": name}
        company = html.find(attrs=company_container)

    elif THEPROTOCOL in search_link:
        company_container = {"data-test": "text-employerName"}
        company = html.find(attrs=company_container)

    elif BULLDOGJOB in search_link:
        # Company container is first div after job title
        name = lambda class_name: class_name and class_name.startswith("JobListItem_item__title")
        title_company_container = {"class": name}
        title_company_block = html.find(attrs=title_company_container)
        # Find the <h3> tag with offer title and get the <div> sibling
        title_container = title_company_block.h3
        company = title_container.find_next_sibling("div")

    elif ROCKETJOBS in search_link or JUSTJOINIT in search_link:
        company_icon = {"data-testid": "ApartmentRoundedIcon"}
        svg_icon = html.find("svg", company_icon)
        if svg_icon:
            parent_name = lambda class_name: class_name and class_name.startswith("MuiBox-root")
            parent_div = svg_icon.find_parent("div", class_=parent_name)
            company = parent_div.span

    elif SOLIDJOBS in search_link:
        company = html.find("a", {"mattooltip": "Kliknij, aby zobaczy pozostałe oferty firmy."})

    elif PRACUJPL in search_link:
        company = html.find("h3", {"data-test": "text-company-name"})

    return company.text if company else None


def logo(html, search_link: str) -> str:
    """Returns logo container content for each website"""
    if NOFLUFFJOBS in search_link:
        logo_container = {"alt": "Company logo"}
        if logo_container:
            logo = html.find(attrs=logo_container)

    elif THEPROTOCOL in search_link:
        logo_container = {"data-test": "icon-companyLogo"}
        if logo_container:
            logo = html.find(attrs=logo_container)

    elif BULLDOGJOB in search_link:
        logo_container = {"class": lambda class_name: class_name and class_name.startswith("JobListItem_item__logo")}
        if logo_container:
            logo = html.find(attrs=logo_container).img

    elif ROCKETJOBS in search_link or JUSTJOINIT in search_link:
        logo = html.img

    elif SOLIDJOBS in search_link:
        logo = html.find("img")

    elif PRACUJPL in search_link:
        logo = html.find("img", {"data-test": "image-responsive"})

    if logo:
        logo_src = logo.get("src")
    return logo_src if logo_src else None


def location(html, search_link: str) -> str:
    """Returns location container content for each website"""
    location = None
    if NOFLUFFJOBS in search_link:
        location_container = {"data-cy": "location on the job offer listing"}
        location_block = html.find(attrs=location_container).span
        try:
            location = location_block.text.strip()
        except:
            print("Error fetching data from record: NOFLUFFJOBS -> Location")

    elif THEPROTOCOL in search_link:
        try:
            location_container = {"data-test": "text-workplaces"}
            location_block = html.find(attrs=location_container)
            if location_block:
                location = location_block.text
        except:
            print("Error fetching data from record: THEPROTOCOL -> Location")

    elif BULLDOGJOB in search_link:
        name = lambda class_name: class_name and class_name.startswith("JobListItem_item__details")
        details_block = html.find(attrs={"class": name})
        try:
            location_block = details_block.div.div
            if location_block:
                spans = location_block.find_all("span")
                location_texts = [span.text.strip() for span in spans]
                location = " | ".join(location_texts)
        except:
            print("Error fetching data from record: BULLDOGJOB -> Location")

    elif ROCKETJOBS in search_link or JUSTJOINIT in search_link:
        # <span> within parent folder of location icon
        try:
            company_icon = {"data-testid": "PlaceOutlinedIcon"}
            svg_icon = html.find("svg", company_icon)
            if svg_icon:
                parent_block_class = lambda class_name: class_name and class_name.startswith("MuiBox-root")
                parent_div = svg_icon.find_parent("div", class_=parent_block_class)
                if parent_div:
                    location_raw = parent_div.span
                    if location_raw:
                        location = location_raw.text
        except:
            website = "JUSTJOINIT" if JUSTJOINIT in search_link else "ROCKETJOBS"
            print(f"Error fetching data from record: {website} -> Location")

    elif SOLIDJOBS in search_link:
        try:
            location_container = html.find("div", class_="flex-row")
            if location_container:
                location_span = location_container.find_all("span")[1]
                if location_span:
                    location = (
                        location_span.text.replace("100% zdalnie ", "").replace("(", "").replace(")", "").strip()
                    )
        except:
            print("Error fetching data from record: SOLIDJOBS -> Location")

    elif PRACUJPL in search_link:
        try:
            loc = html.find("h4", {"data-test": "text-region"})
            if loc and loc.strong:
                location = loc.strong.text
        except:
            print("Error fetching data from record: PRACUJPL -> Location")

    location = remove_remote_status(location)

    return location


def remote_status(html, search_link: str) -> str:
    """Returns location container content for each website"""

    if NOFLUFFJOBS in search_link:
        location_container = {"data-cy": "location on the job offer listing"}
        location = html.find(attrs=location_container)
        if location:
            status = location.text

    elif THEPROTOCOL in search_link:
        remote_container = {"data-test": "text-workModes"}
        remote_status = html.find(attrs=remote_container).text
        if remote_status:
            status = remote_status.lower()

    elif BULLDOGJOB in search_link:
        remote_container = lambda class_name: class_name and class_name.startswith("JobListItem_item__details")
        details_block = html.find(attrs={"class": remote_container})
        if details_block:
            first_block = details_block.div
            if first_block:
                status = first_block.text

    elif ROCKETJOBS in search_link or JUSTJOINIT in search_link:
        # <span> within parent folder of remote status icon
        location_icon = {"style": "display: block;"}
        location = html.find("div", location_icon)
        if location:
            parent_div = location.find_parent("div")
            if parent_div:
                status = parent_div.text.lower()

    elif SOLIDJOBS in search_link:
        location = html.find_all("span", {"mattooltip": True})
        remote_status = location[-1]
        status = remote_status.text.strip()

    elif PRACUJPL in search_link:
        additional_info_containers = lambda tag: tag.has_attr("data-test") and tag["data-test"].startswith(
            "offer-additional-info"
        )
        additional_info = html.find_all(additional_info_containers)
        status = additional_info[-1].text

    if status:
        status = status.lower()
        for key, keywords in remote_work_dict.items():
            if any(keyword in status for keyword in keywords):
                return key

    else:
        return "No status"


def salary(html, search_link: str) -> dict:
    """Returns salary container content for each website"""
    salary = None
    if NOFLUFFJOBS in search_link:
        salary_container = {"data-cy": "salary ranges on the job offer listing"}
        salary = html.find(attrs=salary_container)

    elif THEPROTOCOL in search_link:
        salary_container = {"data-test": "text-salary"}
        salary = html.find(attrs=salary_container)

    elif BULLDOGJOB in search_link:
        salary_container = lambda class_name: class_name and class_name.startswith("JobListItem_item__salary")
        container = html.find(attrs={"class": salary_container})
        if container:
            salary = container.text

    elif ROCKETJOBS in search_link or JUSTJOINIT in search_link:
        # All containers on site are MuiBox-root. Need to find the right one
        MuiBox_block = lambda class_name: class_name and class_name.startswith("MuiBox-root")
        # Salary is contained in the same parent div as the h3 tag with job title
        h3_container = html.h3
        if h3_container:
            parent_div = h3_container.find_parent("div", class_=MuiBox_block)
            # Salary is in <span> inside the parent div of <h3>
            if parent_div:
                salary_elements = parent_div.find_all("span")
                if salary_elements:
                    elements = [pay.text.strip() for pay in salary_elements]
                    if elements:
                        salary = " - ".join(elements)

    elif SOLIDJOBS in search_link:
        salary_container = html.find("sj-salary-display")
        if salary_container:
            salary = salary_container.text.strip()

    elif PRACUJPL in search_link:
        salary_container = html.find("span", {"data-test": "offer-salary"})
        if salary_container:
            salary = salary_container.text.strip()

    return salary if salary else None
