import pandas as pd
from .models import (
    # Incident,
    Narrative,
    Observable,
    Identity,
    Event,
    Campaign,
    Vulnerability,
    CourseOfAction,
    AttackPattern,
    ThreatActor,
    Report,
    get_opencti_client,
)
import uuid
import datetime
import os
import json
import random
import openpyxl
from dotenv import load_dotenv


load_dotenv()


now = datetime.datetime.now()
published = now.isoformat() + "Z"


def drop_duplicates(list_of_dicts):
    """Drops duplicates from a list of dictionaries"""
    unique_dicts = []
    # duplicates = []

    for d in list_of_dicts:
        if d and isinstance(d, dict):
            str_items = [item for item in d.values() if isinstance(item, str)]
            found_duplicate = False

            for existing_dict in unique_dicts:
                if all(item in existing_dict.values() for item in str_items):
                    found_duplicate = True
                    break

            if not found_duplicate:
                unique_dicts.append(d)

    return unique_dicts


def create_bundle(
    i, author_firstname, author_secondname, author_email, marking_definition
):
    bundle = {
        "type": "bundle",
        "id": "bundle--"
        + str(uuid.uuid5(uuid.NAMESPACE_DNS, "bundle" + str(random.random()))),
        "bundle_name": "unnamed",
        "objects": [
            {
                "id": "marking-definition--826578e1-40ad-459f-bc73-ede076f81f37",
                "entity_type": "Marking-Definition",
                "standard_id": "marking-definition--826578e1-40ad-459f-bc73-ede076f81f37",
                "definition_type": "TLP",
                "definition": marking_definition,
                "x_opencti_color": "#d84315",
                "x_opencti_order": 3,
                "name": marking_definition,
                "type": "marking-definition",
            }
        ],
    }
    print(f"Creating bundle for basic incident #{i}", flush=True)
    objects = []
    # Create object list
    object_list = [r.create_stix_dict() for r in i.relatedEntities if r]
    object_ids = [r["id"] for r in object_list if r]

    # Create the incident dictionary
    incident_dict = i.create_stix_dict()
    incident_dict["object_refs"] = object_ids
    bundle["bundle_name"] = incident_dict["name"]

    # Add the author if the incident is a report
    if isinstance(i, Report) and i.author:
        author_dict = i.find_author()
    else:
        author_dict = {
            "id": "identity--24f595b1-bb5b-5c05-a7d8-337a224de086",
            "identity_class": "individual",
            "name": author_firstname,
            "contact_information": author_email,
            "x_opencti_firstname": author_firstname,
            "x_opencti_lastname": author_secondname,
            "x_opencti_id": "f995efca-7522-438a-b68b-44b9b698a285",
            "x_opencti_type": "Individual",
            "type": "identity",
        }
    if author_dict:
        object_list.append(author_dict)
        object_ids.append(author_dict["id"])
        incident_dict["created_by_ref"] = author_dict["id"]

    # Add the incident to the bundle
    bundle["objects"].append(incident_dict)
    objects.extend(object_list)

    bundle["objects"].extend(
        drop_duplicates(objects)
    )  # Add the unique objects to the bundle
    return bundle


def parse_date(date):
    if isinstance(date, datetime.datetime):
        print(f"Date {date} is already a datetime object.")
        return date

    formats = [
        "%Y-%m-%d",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M:%S.%f",
        "%Y-%d-%m",
        "%Y-%d-%m %H:%M:%S",
        "%Y-%d-%m %H:%M:%S.%f",
    ]

    for fmt in formats:
        try:
            return datetime.datetime.strptime(date, fmt)
        except ValueError as e:
            print(f"ValueError: {e} does not match format {fmt}. Trying next format.")
            continue

    return now


def load_excel(file):
    # Load the workbook and get sheet names
    sheets = openpyxl.load_workbook(file).sheetnames
    df = {}
    print(f"Loading {file}...", flush=True)
    for sheet in sheets:
        # Read each sheet into a DataFrame
        sheet_df = pd.read_excel(file, sheet_name=sheet, engine="openpyxl")

        # Normalize column names by removing all whitespaces
        sheet_df.columns = [col.strip() for col in sheet_df.columns]

        df[sheet] = sheet_df

    df = {
        key.strip(): value.fillna("").rename(columns=lambda x: x.strip())
        for key, value in df.items()
    }
    return df


def process_threat_actor(threat_actor_data, instructions):
    # Drop first row with instructions
    if instructions:
        threat_actor_data = threat_actor_data.drop(0)

    # Create a list of threat actors
    threat_actors = []
    for _, row in threat_actor_data.iterrows():
        threat_actors.append(ThreatActor(name=row["Name"]))
    return threat_actors


def process_observables(observables_data, instructions):
    # Drop first row with instructions
    if instructions:
        observables_data = observables_data.drop(0)

    # Create a list of observables
    observables = []
    for _, row in observables_data.iterrows():
        if row["URL"] == "":
            break
        observable_date = parse_date(row["Datetime"])
        print(
            f"Processing observable {row['URL']} with date {observable_date}.",
            flush=True,
        )
        observable = Observable(
            url=row["URL"],
            date=observable_date,
            archivedUrl=row["Archived link"],
            language=row["Language"],
        )
        observables.append(observable)
        print("Observable processed.", flush=True)
    return observables


def process_identity(identity_data, instructions):
    opencti_client = get_opencti_client()
    # Drop first row with instructions
    if instructions:
        identity_data = identity_data.drop(0)

    # Create a list of identities
    identities = []
    for _, row in identity_data.iterrows():
        identity_name = row["Name"]
        lookup_filters = {
            "mode": "and",
            "filters": [
                {
                    "key": "alias",
                    "values": identity_name,
                    "operator": "contains",
                },
                {
                    "key": "name",
                    "values": identity_name,
                },
            ],
            "filterGroups": [],
        }

        lookup_location = opencti_client.location.read(filters=lookup_filters)
        if lookup_location:
            identities.append(
                Identity(
                    name=lookup_location[0]["name"],
                    idClass=lookup_location[0]["identity_class"],
                )
            )
            break

        lookup_identity = opencti_client.identity.read(filters=lookup_filters)
        if lookup_identity:
            identities.append(
                Identity(
                    name=lookup_identity[0]["name"],
                    idClass=lookup_identity[0]["identity_class"],
                )
            )
            break

        identities.append(
            Identity(
                name=row["Name"],
                idClass="Unknown",
                description=row["Description"],
            )
        )
    return identities


def process_event(event_data, instructions):
    # Drop first row with instructions
    if instructions:
        event_data = event_data.drop(0)

    # Create a list of events
    events = []
    for _, row in event_data.iterrows():
        start_date = parse_date(row["Start date"])
        end_date = parse_date(row["End date"])
        print(
            f"Processing event. Start date: {start_date}, End date: {end_date}",
            flush=True,
        )
        event = Event(
            name=row["Name"],
            description=row["Description"],
            start_date=start_date,
            end_date=end_date,
        )
        events.append(event)
        print("Event processed.", flush=True)
    return events


def process_attack_pattern(attack_pattern_df):
    # Find TTPs used in Incident
    attack_pattern_df["Used in Incident"] = attack_pattern_df[
        "Used in Incident"
    ].str.upper()
    attack_pattern_df = attack_pattern_df[
        attack_pattern_df["Used in Incident"] == "X"
    ].reset_index()

    # Return all attack patterns used in the incident
    attack_patterns = [
        AttackPattern(technique=row["Technique"].split(": ")[-1].strip())
        for _, row in attack_pattern_df.iterrows()
    ]
    return attack_patterns


def process_narratives(narratives_data, instructions):
    # Drop first row with instructions
    if instructions:
        narratives_data = narratives_data.drop(0)

    # Create a list of narratives
    narratives = []
    for _, row in narratives_data.iterrows():
        narrative = Narrative(
            name=row["Name"],
            description=row["Description"],
        )
        narratives.append(narrative)
    return narratives


def process_course_of_action(coa_df, external_ref_list, instructions):
    # Drop first row with instructions
    if instructions:
        coa_df = coa_df.drop(0)

    # Create a list of COAs
    coas = []
    for _, row in coa_df.iterrows():
        if row["Name"] == "":
            break
        if row["External Reference"]:
            external_ref_list.append(row["External Reference"])
        coas.append(
            CourseOfAction(
                name=row["Name"],
                description=row["Description"],
                extRef=row["External Reference"],
            )
        )
    return coas


def process_campaign(campaign_data, external_ref_list, instructions):
    # Drop first row with instructions
    if instructions:
        campaign_data = campaign_data.drop(0)

    # Create a list of campaigns
    campaigns = []
    for _, row in campaign_data.iterrows():
        if row["External Reference"]:
            external_ref_list.append(row["External Reference"])
        campaign = Campaign(
            name=row["Name"],
            description=row["Description"],
            extRef=row["External Reference"],
        )
        campaigns.append(campaign)
    return campaigns


def process_vulnerabilities(vulnerabilities_data, instructions):
    # Drop first row with instructions
    if instructions:
        vulnerabilities_data = vulnerabilities_data.drop(0)

    # Create a list of vulnerabilities
    vulnerabilities = []
    for _, row in vulnerabilities_data.iterrows():
        vulnerability = Vulnerability(
            name=row["Name"],
            description=row["Description"],
        )
        vulnerabilities.append(vulnerability)
    return vulnerabilities


def process_report(
    df, author_firstname, author_secondname, author_email, marking_definition
):
    # Initialize related objects and external references
    related_objects = []
    external_ref_list = []
    data = df["Incident"]
    instructions = True
    print("Processing Report...", flush=True)
    # Check length of data
    if len(data) == 1:
        instructions = False
    else:
        print("Dropping first row with instructions for all sheets.", flush=True)

    data = data.iloc[-1]

    # Retrieve related objects
    for key in df.keys():
        if key == "Threat Actor":
            related_objects.extend(process_threat_actor(df[key], instructions))
        if key == "Identity":
            related_objects.extend(process_identity(df[key], instructions))
        if key == "Event":
            related_objects.extend(process_event(df[key], instructions))
        if key == "Narratives":
            related_objects.extend(process_narratives(df[key], instructions))
        if key == "Observables":
            related_objects.extend(process_observables(df[key], instructions))
        if key == "Attack Pattern":
            related_objects.extend(process_attack_pattern(df[key]))
        if key == "Course of Action":
            related_objects.extend(
                process_course_of_action(df[key], external_ref_list, instructions)
            )
        if key == "Campaign":
            related_objects.extend(
                process_campaign(df[key], external_ref_list, instructions)
            )
        if key == "Vulnerabilities":
            related_objects.extend(process_vulnerabilities(df[key], instructions))

    return Report(
        name=data["Name"].replace("/", "-"),
        description=data["Description"].replace("/", "-"),
        objectLabel=[],
        first_seen=now,
        confidence=90,
        objective=[],
        objectMarking=marking_definition,
        extRef=[data["External Reference"]].extend(external_ref_list),
        author=author_firstname,
        relatedEntities=related_objects,
    )


def excel_to_json(
    file, author_firstname, author_secondname, author_email, marking_definition
):
    df = load_excel(file)
    report = process_report(
        df, author_firstname, author_secondname, author_email, marking_definition
    )
    bundle = create_bundle(
        report, author_firstname, author_secondname, author_email, marking_definition
    )
    for item in bundle["objects"]:
        print(item)
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    with open(os.path.join(desktop_path, f"{report.name}.json"), "w") as f:
        print(f"Writing {report.name}.json to the desktop.", flush=True)
        json.dump(bundle, f)


def folder_to_json(
    folder, author_firstname, author_secondname, author_email, marking_definition
):
    print(f"Converting all Excel files in {folder} to JSON", flush=True)
    for root, _, files in os.walk(folder):
        print(f"Searching {root} for Excel files.", flush=True)
        # If the folder has no xlsx files, skip
        if not any(file.endswith(".xlsx") for file in files):
            print(f"No Excel files found in {root}. Moving to next folder.", flush=True)
            continue
        for file in files:
            if file.endswith(".xlsx"):
                print(f"Converting {os.path.join(root, file)} to JSON", flush=True)
                excel_to_json(
                    os.path.join(root, file),
                    author_firstname,
                    author_secondname,
                    author_email,
                    marking_definition,
                )
