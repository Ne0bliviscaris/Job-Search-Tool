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
    "rocketjobs_data-junior-remote": "https://rocketjobs.pl/wszystkie-lokalizacje/bi-data/doswiadczenie_staz-junior/praca-zdalna_tak",
    "justjoinit_data-python-junior-remote": "https://justjoin.it/all-locations/data/experience-level_junior/remote_yes?keyword=python",
    "justjoinit_ai-python-junior-remote": "https://justjoin.it/all-locations/ai/experience-level_junior/remote_yes?keyword=python",
    "solidjobs_data-junior-remote": "https://solid.jobs/offers/it;cities=Praca%20zdalna;categories=Data%20Science;experiences=Junior",
    "solidjobs_python-junior-remote": "https://solid.jobs/offers/it;cities=Praca%20zdalna;subcategories=Python;experiences=Junior",
    # Mid offers
    "solidjobs_python-regular-remote": "https://solid.jobs/offers/it;cities=Praca%20zdalna;subcategories=Python;experiences=Regular",
    "theprotocol-hybrid-test": "https://theprotocol.it/filtry/python;t/big-data-science,ai-ml;sp/zdalna,hybrydowa;rw",
    # Hybrid/local offers
    "nofluffjobs_data-ai-trainee-junior-poznan": "https://nofluffjobs.com/pl/hybrid/artificial-intelligence?criteria=city%3Dpoznan%20category%3Ddata%20seniority%3Dtrainee,junior",
    "nofluffjobs-test": "https://nofluffjobs.com/pl/hybrid/artificial-intelligence?criteria=city%3Dpoznan%20category%3Ddata%20seniority%3Dtrainee,junior,mid,senior",
    "theprotocol_python-big-data-ai-ml-junior-assistant-trainee-poznan": "https://theprotocol.it/filtry/python;t/big-data-science,ai-ml;sp/junior,assistant,trainee;p/poznan;wp/hybrydowa,zdalna;rw",
    "bulldogjob_data-poznan": "https://bulldogjob.pl/companies/jobs/s/locationDistance,50/role,data/city,Pozna%C5%84",
    "pracujpl_data-ai-junior-poznan": "https://it.pracuj.pl/praca/poznan;wp/praca%20hybrydowa;wm,hybrid?rd=30&et=17&ap=true&its=ai-ml%2Cbig-data-science",
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
