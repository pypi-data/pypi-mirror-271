from chatbot import DATA_DIR
import re

connection_string = f"sqlite:///{DATA_DIR}/enhanced_enrichment.db"
tables = ["people", "companies", "technologies", "company_2_technologies"]

technologies = {
    "Salesforce": "Salesforce",
    "Marketo": "Marketo",
    "Hubspot": "Hubspot",
    "Pardot": "Pardot",
    "Eloqua": "Eloqua",
    "ChiliPiper": "ChiliPiper",
    "Drift": "Drift",
}


def camel_case_split(identifier):
    matches = re.finditer(".+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)", identifier)
    return [m.group(0) for m in matches]


def add_mispellings_to_technologies():
    d = {}
    for tech, proper_name in technologies.items():
        split = camel_case_split(tech)
        if len(split) > 1:
            d[" ".join(split)] = proper_name
    technologies.update(d)


add_mispellings_to_technologies()


people_columns = [
    "github_url",
    "location_street_address",
    "job_last_updated",
    "experience",
    "last_name",
    "personal_emails",
    "first_name",
    "location_locality",
    "skills",
    "twitter_username",
    "job_title_role",
    "last_initial",
    "linkedin_username",
    "regions",
    "job_title",
    "industry",
    "version_status",
    "facebook_id",
    "job_title_levels",
    "location_metro",
    "location_last_updated",
    "full_name",
    "id",
    "job_start_date",
    "location_name",
    "location_address_line_2",
    "birth_year",
    "birth_date",
    "interests",
    "location_country",
    "recommended_personal_email",
    "phone_numbers",
    "profiles",
    "education",
    "company_id",
    "twitter_url",
    "middle_initial",
    "middle_name",
    "emails",
    "location_names",
    "street_addresses",
    "location_region",
    "facebook_username",
    "linkedin_id",
    "work_email",
    "location_postal_code",
    "countries",
    "mobile_phone",
    "gender",
    "linkedin_url",
    "location_continent",
    "location_geo",
    "facebook_url",
    "github_username",
    "job_title_sub_role",
]
people_columns_2_idx = {col: i for i, col in enumerate(people_columns)}

