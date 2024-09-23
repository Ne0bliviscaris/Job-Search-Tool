NOFLUFFJOBS = "https://nofluffjobs.com"
THEPROTOCOL = "https://theprotocol.it"
BULLDOGJOB = "https://bulldogjob.pl"
ROCKETJOBS = "https://rocketjobs.pl"
JUSTJOINIT = "https://justjoin.it"
SOLIDJOBS = "https://solid.jobs"
PRACUJPL = "https://it.pracuj.pl"

search_links = {
    "nofluffjobs_data-ai-trainee-junior": "https://nofluffjobs.com/pl/artificial-intelligence?criteria=category%3Ddata%20seniority%3Dtrainee,junior",
    "theprotocol_big-data-ai-ml-junior-assistant-trainee": "https://theprotocol.it/filtry/big-data-science,ai-ml;sp/junior,assistant,trainee;p",
    "bulldogjob_remote-data": "https://bulldogjob.pl/companies/jobs/s/locationDistance,50/role,data/city,Remote",
    "rocketjobs_remote-data": "https://rocketjobs.pl/wszystkie-lokalizacje/bi-data/praca-zdalna_tak",
    "justjoinit_data-junior-remote": "https://justjoin.it/all-locations/data/experience-level_junior/remote_yes?orderBy=DESC&sortBy=newest",
    "solidjobs_data-regular-remote": "https://solid.jobs/offers/it;categories=Data%20Science;cities=Praca%20zdalna;experiences=Regular",
    "pracujpl_data-ai-junior-remote": "https://it.pracuj.pl/praca/praca%20zdalna;wm,home-office?et=17&ap=true&its=ai-ml%2Cbig-data-science",
}

websites = {
    "nofluffjobs": NOFLUFFJOBS,
    "bulldogjob": BULLDOGJOB,
    "theprotocol": THEPROTOCOL,
    "rocketjobs": ROCKETJOBS,
    "justjoin": JUSTJOINIT,
    "solid": SOLIDJOBS,
    "pracuj": PRACUJPL,
}


def identify_website(search_link: str) -> str:
    """
    Set current website based on search link
    """
    # Iterate over the website_map to find the matching website
    for key, website in websites.items():
        if key in search_link:
            return website
    return "Error: Website not recognized"
