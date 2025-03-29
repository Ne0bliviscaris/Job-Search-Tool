# Requests.get viable
NOFLUFFJOBS = "https://nofluffjobs.com"
PRACUJPL = "https://it.pracuj.pl"
BULLDOGJOB = "https://bulldogjob.pl"
# Selenium required
THEPROTOCOL = "https://theprotocol.it"
ROCKETJOBS = "https://rocketjobs.pl"
JUSTJOINIT = "https://justjoin.it"
SOLIDJOBS = "https://solid.jobs"

search_links = {
    # # Remote offers
    # Junior offers
    "nofluffjobs_data-python-trainee-junior-remote": "https://nofluffjobs.com/pl/praca-zdalna/data?criteria=requirement%3DPython%20%20seniority%3Dtrainee,junior",
    "nofluffjobs_ai-python-trainee-junior-remote": "https://nofluffjobs.com/pl/praca-zdalna/artificial-intelligence?criteria=requirement%3DPython%20%20seniority%3Dtrainee,junior",
    "pracujpl_data-ai-python-junior-remote": "https://it.pracuj.pl/praca/praca%20zdalna;wm,home-office?et=17&ap=true&its=ai-ml%2Cbig-data-science&itth=37",
    "bulldogjob_data-junior-python-remote": "https://bulldogjob.pl/companies/jobs/s/city,Remote/experienceLevel,junior,intern/skills,Python/role,data",
    "theprotocol_python-data-ai-python-junior-remote": "https://theprotocol.it/filtry/python;t/big-data-science,ai-ml;sp/junior,assistant,trainee;p/zdalna;rw",
    #     "rocketjobs_data-junior-remote": "https://rocketjobs.pl/oferty-pracy/wszystkie-lokalizacje/bi-data?doswiadczenie=staz-junior&praca-zdalna=tak&orderBy=DESC&sortBy=published&from=0",
    #     "justjoinit_data-python-junior-remote": "https://justjoin.it/job-offers/all-locations/data?experience-level=junior&remote=yes&orderBy=DESC&sortBy=published&keyword=python&from=0",
    #     "justjoinit_ai-python-junior-remote": "https://justjoin.it/job-offers/all-locations/ai?experience-level=junior&remote=yes&orderBy=DESC&sortBy=published&keyword=python&from=0",
    #     "solidjobs_data-junior-remote": "https://solid.jobs/offers/it;cities=Praca%20zdalna;categories=Data%20Science;experiences=Junior",
    #     "solidjobs_python-junior-remote": "https://solid.jobs/offers/it;cities=Praca%20zdalna;subcategories=Python;experiences=Junior",
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
