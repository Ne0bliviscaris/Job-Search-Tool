from modules.helper_functions import process_remote_status, remove_remote_status
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
    records = None

    if NOFLUFFJOBS in search_link:
        try:
            block_name = lambda id_name: id_name and id_name.startswith("nfjPostingListItem")
            record_container = {"id": block_name}
            records = html.find_all(attrs=record_container)
        except:
            print("Error detecting records: NOFLUFFJOBS")

    elif THEPROTOCOL in search_link:
        try:
            record_container = {"data-test": "list-item-offer"}
            records = html.find_all(attrs=record_container)
        except:
            print("Error detecting records: THEPROTOCOL")

    elif BULLDOGJOB in search_link:
        try:
            block_name = lambda class_name: class_name and class_name.startswith("JobListItem_item")
            record_container = {"class": block_name}
            records = html.find_all("a", attrs=record_container)
        except:
            print("Error detecting records: BULLDOGJOB")

    elif ROCKETJOBS in search_link or JUSTJOINIT in search_link:
        try:
            record_container = {"data-index": True}
            records = html.find_all(attrs=record_container)
        except:
            website = "JUSTJOINIT" if JUSTJOINIT in search_link else "ROCKETJOBS"
            print(f"Error detecting records: {website}")

    elif SOLIDJOBS in search_link:
        try:
            block_name = "sj-offer-list-item"  # <sj-offer-list-item> block
            records = html.find_all(block_name)
        except:
            print("Error detecting records: SOLIDJOBS")

    elif PRACUJPL in search_link:
        try:
            record_container = {"data-test": "default-offer"}
            records = html.find_all(attrs=record_container)
        except:
            print("Error detecting records: PRACUJPL")

    if records is not None:
        return [job for job in records]
    else:
        return None


def url(record, search_link) -> str:
    """Returns url container content for each website"""
    url = None
    if NOFLUFFJOBS in search_link:
        try:
            url = record.get("href")
        except:
            print("Error fetching data from record: NOFLUFFJOBS -> URL")

    elif THEPROTOCOL in search_link:
        try:
            url = record.get("href")
        except:
            print("Error fetching data from record: THEPROTOCOL -> URL")

    elif BULLDOGJOB in search_link:
        try:
            url = record.get("href")
        except:
            print("Error fetching data from record: BULLDOGJOB -> URL")

    elif ROCKETJOBS in search_link or JUSTJOINIT in search_link:
        try:
            url_a = record.find("a", href=True)
            url = url_a.get("href")
        except:
            website = "JUSTJOINIT" if JUSTJOINIT in search_link else "ROCKETJOBS"
            print(f"Error fetching data from record: {website} -> URL")

    elif SOLIDJOBS in search_link:
        try:
            url_a = record.find("a", href=True)
            url = url_a.get("href")
        except:
            print("Error fetching data from record: SOLIDJOBS -> URL")

    elif PRACUJPL in search_link:
        try:
            container = {"data-test": "link-offer"}
            url_a = record.find("a", container)
            url = url_a.get("href") if url_a else None
        except:
            print("Error fetching data from record: PRACUJPL -> URL")

    if url:
        if url.startswith("http"):
            return url
        else:
            return search_link.rstrip("/") + "/" + url.lstrip("/")
    return None


def job_title(html, search_link) -> str:
    """Returns title container content for each website"""
    title = None

    if NOFLUFFJOBS in search_link:
        try:
            container = {"data-cy": "title position on the job offer listing"}
            title = html.find(attrs=container)
        except:
            print("Error fetching data from record: NOFLUFFJOBS -> Title")

    elif THEPROTOCOL in search_link:
        try:
            container = {"data-test": "text-jobTitle"}
            title = html.find(attrs=container)
        except:
            print("Error fetching data from record: THEPROTOCOL -> Title")

    elif BULLDOGJOB in search_link:
        try:
            block_name = lambda class_name: class_name and class_name.startswith("JobListItem_item__title")
            container = {"class": block_name}
            title_block = html.find(attrs=container)
            title = title_block.h3
        except:
            print("Error fetching data from record: BULLDOGJOB -> Title")

    elif ROCKETJOBS in search_link or JUSTJOINIT in search_link:
        try:
            title = html.h3
        except:
            website = "JUSTJOINIT" if JUSTJOINIT in search_link else "ROCKETJOBS"
            print(f"Error fetching data from record: {website} -> Title")

    elif SOLIDJOBS in search_link:
        try:
            title = html.h2
        except:
            print("Error fetching data from record: SOLIDJOBS -> Title")

    elif PRACUJPL in search_link:
        try:
            container = {"data-test": "offer-title"}
            title = html.find("h2", container)
        except:
            print("Error fetching data from record: PRACUJPL -> Title")

    return title.text.strip() if title else None


def tags(html, search_link: str) -> str:
    """Returns tags container content for each website as a string separated by ' | '"""
    tags_list = []

    if NOFLUFFJOBS in search_link:
        try:
            tags_container = {"data-cy": "category name on the job offer listing"}
            tags = html.find_all(attrs=tags_container)
            tags_list = [tag.text for tag in tags]
        except:
            print("Error fetching data from record: NOFLUFFJOBS -> Tags")

    elif THEPROTOCOL in search_link:
        try:
            tags_container = {"data-test": "chip-expectedTechnology"}
            tags = html.find_all(attrs=tags_container)
            tags_list = [tag.text for tag in tags]
        except:
            print("Error fetching data from record: THEPROTOCOL -> Tags")

    elif BULLDOGJOB in search_link:
        try:
            name = lambda class_name: class_name and class_name.startswith("JobListItem_item__tags")
            tags_container = {"class": name}
            tags_block = html.find(attrs=tags_container)
            if tags_block:
                tags_list = [span.text for span in tags_block.find_all("span")]
        except:
            print("Error fetching data from record: BULLDOGJOB -> Tags")

    elif ROCKETJOBS in search_link or JUSTJOINIT in search_link:
        try:
            name = lambda class_name: class_name and class_name.startswith("skill-tag")
            tags = html.find_all(class_=name)
            tags_list = [tag.text for tag in tags]
        except:
            website = "JUSTJOINIT" if JUSTJOINIT in search_link else "ROCKETJOBS"
            print(f"Error fetching data from record: {website} -> Tags")

    elif SOLIDJOBS in search_link:
        try:
            tags_block = html.find_all("solidjobs-skill-display")
            if tags_block:
                tags_list = [tag.text.replace("#", "") for tag in tags_block]
        except:
            print("Error fetching data from record: SOLIDJOBS -> Tags")

    elif PRACUJPL in search_link:
        try:
            container = {"data-test": "technologies-item"}
            tags_block = html.find_all("span", container)
            tags_list = [tag.text.strip() for tag in tags_block]
        except:
            print("Error fetching data from record: PRACUJPL -> Tags")

    merged_tags = " | ".join(tags_list) if tags_list else None
    return merged_tags


def company(html, search_link: str) -> str:
    """Returns company name container content for each website"""
    company = None

    if NOFLUFFJOBS in search_link:
        try:
            name = lambda x: x and x.startswith("company-name")
            company_container = {"class": name}
            company = html.find(attrs=company_container)
        except:
            print("Error fetching data from record: NOFLUFFJOBS -> Company")

    elif THEPROTOCOL in search_link:
        try:
            company_container = {"data-test": "text-employerName"}
            company = html.find(attrs=company_container)
        except:
            print("Error fetching data from record: THEPROTOCOL -> Company")

    elif BULLDOGJOB in search_link:
        try:
            # Company container is first div after job title
            name = lambda class_name: class_name and class_name.startswith("JobListItem_item__title")
            title_company_container = {"class": name}
            title_company_block = html.find(attrs=title_company_container)
            # Find the <h3> tag with offer title and get the <div> sibling
            title_container = title_company_block.h3
            company = title_container.find_next_sibling("div")
        except:
            print("Error fetching data from record: BULLDOGJOB -> Company")

    elif ROCKETJOBS in search_link or JUSTJOINIT in search_link:
        try:
            company_icon = {"data-testid": "ApartmentRoundedIcon"}
            svg_icon = html.find("svg", company_icon)
            if svg_icon:
                parent_name = lambda class_name: class_name and class_name.startswith("MuiBox-root")
                parent_div = svg_icon.find_parent("div", class_=parent_name)
                company = parent_div.span
        except:
            website = "JUSTJOINIT" if JUSTJOINIT in search_link else "ROCKETJOBS"
            print(f"Error fetching data from record: {website} -> Company")

    elif SOLIDJOBS in search_link:
        try:
            company = html.find("a", {"mattooltip": "Kliknij, aby zobaczy pozostałe oferty firmy."})
        except:
            print("Error fetching data from record: SOLIDJOBS -> Company")

    elif PRACUJPL in search_link:
        try:
            company = html.find("h3", {"data-test": "text-company-name"})
        except:
            print("Error fetching data from record: PRACUJPL -> Company")

    return company.text if company else None


def logo(html, search_link: str) -> str:
    """Returns logo container content for each website"""
    logo = None
    logo_src = None
    if NOFLUFFJOBS in search_link:
        try:
            logo_container = {"alt": "Company logo"}
            if logo_container:
                logo = html.find(attrs=logo_container)
        except:
            print("Error fetching data from record: NOFLUFFJOBS -> Logo")

    elif THEPROTOCOL in search_link:
        try:
            logo_container = {"data-test": "icon-companyLogo"}
            if logo_container:
                logo = html.find(attrs=logo_container)
        except:
            print("Error fetching data from record: THEPROTOCOL -> Logo")

    elif BULLDOGJOB in search_link:
        try:
            logo_container = {
                "class": lambda class_name: class_name and class_name.startswith("JobListItem_item__logo")
            }
            if logo_container:
                logo = html.find(attrs=logo_container).img
        except:
            print("Error fetching data from record: BULLDOGJOB -> Logo")

    elif ROCKETJOBS in search_link or JUSTJOINIT in search_link:
        try:
            logo = html.img
        except:
            website = "JUSTJOINIT" if JUSTJOINIT in search_link else "ROCKETJOBS"
            print(f"Error fetching data from record: {website} -> Logo")

    elif SOLIDJOBS in search_link:
        try:
            logo = html.find("img")
        except:
            print("Error fetching data from record: SOLIDJOBS -> Logo")

    elif PRACUJPL in search_link:
        try:
            logo = html.find("img", {"data-test": "image-responsive"})
        except:
            print("Error fetching data from record: PRACUJPL -> Logo")

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
    status = None
    if NOFLUFFJOBS in search_link:
        try:
            location_container = {"data-cy": "location on the job offer listing"}
            location = html.find(attrs=location_container)
            if location:
                status = location.text
        except:
            print("Error fetching data from record: NOFLUFFJOBS -> Remote status")

    elif THEPROTOCOL in search_link:
        try:
            remote_container = {"data-test": "text-workModes"}
            remote_status = html.find(attrs=remote_container)
            if remote_status:
                status = remote_status.text.lower()
        except:
            print("Error fetching data from record: THEPROTOCOL -> Remote status")

    elif BULLDOGJOB in search_link:
        try:
            container_name = "JobListItem_item__details"
            remote_container = lambda class_name: class_name and class_name.startswith(container_name)
            details_block = html.find(attrs={"class": remote_container})
            if details_block:
                first_block = details_block.div
                if first_block:
                    status = first_block.text
        except:
            print("Error fetching data from record: BULLDOGJOB -> Remote status")

    elif ROCKETJOBS in search_link or JUSTJOINIT in search_link:
        # <span> within parent folder of remote status icon
        try:
            location_icon = {"style": "display: block;"}
            location = html.find("div", location_icon)
            if location:
                parent_div = location.find_parent("div")
                if parent_div:
                    status = parent_div.text.lower()
        except:
            website = "JUSTJOINIT" if JUSTJOINIT in search_link else "ROCKETJOBS"
            print(f"Error fetching data from record: {website} -> Remote status")

    elif SOLIDJOBS in search_link:
        try:
            location = html.find_all("span", {"mattooltip": True})
            remote_status = location[-1]
            status = remote_status.text.strip()
        except:
            print("Error fetching data from record: SOLIDJOBS -> Remote status")

    elif PRACUJPL in search_link:
        try:
            tag_name = "offer-additional-info"
            additional_info_containers = lambda tag: tag.has_attr("data-test") and tag["data-test"].startswith(
                tag_name
            )
            additional_info = html.find_all(additional_info_containers)
            status = additional_info[-1].text
        except:
            print("Error fetching data from record: PRACUJPL -> Remote status")

    return process_remote_status(status)


def salary(html, search_link: str) -> dict:
    """Returns salary container content for each website"""
    salary = None
    if NOFLUFFJOBS in search_link:
        try:
            salary_container = {"data-cy": "salary ranges on the job offer listing"}
            salary = html.find(attrs=salary_container)
        except:
            print("Error fetching data from record: NOFLUFFJOBS -> Salary")

    elif THEPROTOCOL in search_link:
        try:
            salary_container = {"data-test": "text-salary"}
            salary = html.find(attrs=salary_container)
        except:
            print("Error fetching data from record: THEPROTOCOL -> Salary")

    elif BULLDOGJOB in search_link:
        try:
            container_name = "JobListItem_item__salary"
            salary_container = lambda class_name: class_name and class_name.startswith(container_name)
            container = html.find(attrs={"class": salary_container})
            if container:
                salary = container.text
        except:
            print("Error fetching data from record: BULLDOGJOB -> Salary")

    elif ROCKETJOBS in search_link or JUSTJOINIT in search_link:
        try:
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
        except:
            website = "JUSTJOINIT" if JUSTJOINIT in search_link else "ROCKETJOBS"
            print(f"Error fetching data from record: {website} -> Salary")

    elif SOLIDJOBS in search_link:
        try:
            salary_container = html.find("sj-salary-display")
            if salary_container:
                salary = salary_container.text.strip()
        except:
            print("Error fetching data from record: SOLIDJOBS -> Salary")

    elif PRACUJPL in search_link:
        try:
            salary_container = html.find("span", {"data-test": "offer-salary"})
            if salary_container:
                salary = salary_container.text.strip()
        except:
            print("Error fetching data from record: PRACUJPL -> Salary")

    return salary
