import json


def recursive_rename_uri(obj):
    """
    Recursively rename any key 'uri' to 'refObjectUri' in the given object.
    """
    if isinstance(obj, dict):
        new_obj = {}
        for key, value in obj.items():
            new_key = "refObjectUri" if key == "uri" else key
            new_obj[new_key] = recursive_rename_uri(value)
        return new_obj
    elif isinstance(obj, list):
        return [recursive_rename_uri(item) for item in obj]
    else:
        return obj


def remove_raw_strings_in_anies(obj):
    """
    Recursively traverse the object and remove any raw string elements found in lists
    that are assigned to an 'anies' key.
    """
    if isinstance(obj, dict):
        new_obj = {}
        for key, value in obj.items():
            if key == "anies" and isinstance(value, list):
                # Filter out raw string elements and recursively process each remaining item.
                new_obj[key] = [
                    remove_raw_strings_in_anies(item)
                    for item in value
                    if not isinstance(item, str)
                ]
            else:
                new_obj[key] = remove_raw_strings_in_anies(value)
        return new_obj
    elif isinstance(obj, list):
        return [remove_raw_strings_in_anies(item) for item in obj]
    else:
        return obj


def transform_json(data):
    """
    Transform an Environmental Product Declaration (EPD) JSON instance file by renaming keys
    and restructuring its contents to standardize the schema.

    Detailed transformations include:

    - Global Transformation:
      - Rename every occurrence of the key "uri" to "refObjectUri" wherever that key is present.
      - Remove any raw string elements from lists under any key named "anies" in the entire JSON.

    - processInformation:
      - Rename "dataSetInformation.name" to "dataSetName".
      - Rename "dataSetInformation.other" to "otherDSI".
        - If any item in "otherDSI.anies" contains the key "componentsAndMaterialsAndSubstances",
          remove the entire "anies" key.
      - For each classification in "dataSetInformation.classificationInformation.classification",
        rename "class" to "classEntries".
      - Rename "time" to "timeInformation", then:
        - Rename "other" under "timeInformation" to "otherTime".
        - In each entry of "otherTime.anies", rename "value" to "timestampValue".

    - modellingAndValidation:
      - In "LCIMethodAndAllocation", rename "other" to "otherMAA".
      - In "dataSourcesTreatmentAndRepresentativeness":
        - Rename "other" to "otherDSTAR".
        - Rename the inner "anies" list to "aniesDSTAR".
        - For each item in "aniesDSTAR":
          - If the "value" holds an object (dict), rename "value" to "valueDSTAR" and update its subkeys:
            - Rename "shortDescription" to "shortDescriptionExtended".
            - In "version", rename "version" to "versionInt" and reassign to "versionDict".
            - In "uuid", rename "uuid" to "uuidValue" and reassign to "uuidDict".
      - Rename "validation" to "validationInfo".
      - Rename "other" to "otherMAV" and for each item in its "anies":
          - If the "value" holds an object (dict), rename "value" to "objectValue".

    - administrativeInformation:
      - In each item of "dataEntryBy.referenceToDataSetFormat", keys (like "uri") will be renamed globally.
      - In "publicationAndOwnership":
        - Rename "other" to "otherPAO".
        - For each item in "otherPAO.anies":
          - If the "value" holds an object (dict), rename "value" to "objectValue".
      - (Other keys such as "referenceToPersonOrEntityEnteringTheData",
         "referenceToRegistrationAuthority", and "referenceToOwnershipOfDataSet" will have their "uri" keys
         renamed globally.)

    - exchanges:
      - For each exchange in "exchanges.exchange":
        - For each item in "flowProperties", rename "name" to "nameFP" and "uuid" to "uuidFP".
        - Rename "exchange direction" to "exchangeDirection".
        - Rename "other" to "otherEx" and update inner keys for each item in "anies":
          - If the "value" holds an object (dict), rename "value" to "objectValue".
        - Rename "classification" to "classificationEx" and within it, rename "name" to "nameClass".

    - LCIAResults:
      - Rename the top-level key "LCIAResults" to "lciaResults".
      - For each result in "lciaResults.LCIAResult":
        - Rename "other" to "otherLCIA" and update inner keys for each item in "anies":
          - If the "value" holds an object (dict), rename "value" to "objectValue".
        - In "referenceToLCIAMethodDataSet", keys (like "uri") will be renamed globally.

    - Removal:
      - Remove the top-level "otherAttributes" key and its contents.

    Args:
      data (dict): The original EPD JSON data.

    Returns:
      dict: The transformed JSON data with standardized key names and structure.
    """
    # --- processInformation transformations ---
    process_info = data.get("processInformation", {})
    data_set_info = process_info.get("dataSetInformation", {})

    # Rename "name" to "dataSetName"
    if "name" in data_set_info:
        data_set_info["dataSetName"] = data_set_info.pop("name")

    # Rename "other" under dataSetInformation to "otherDSI"
    if "other" in data_set_info:
        data_set_info["otherDSI"] = data_set_info.pop("other")
        # If any item in otherDSI.anies contains "componentsAndMaterialsAndSubstances", remove the entire "anies" key.
        if "anies" in data_set_info["otherDSI"]:
            for item in data_set_info["otherDSI"]["anies"]:
                if (
                    isinstance(item, dict)
                    and "componentsAndMaterialsAndSubstances" in item
                ):
                    data_set_info["otherDSI"].pop("anies")
                    break

    # For each classification entry, rename "class" to "classEntries"
    classification_info = data_set_info.get("classificationInformation", {})
    classifications = classification_info.get("classification", [])
    for cls in classifications:
        if "class" in cls:
            cls["classEntries"] = cls.pop("class")

    # Rename "time" to "timeInformation" and update its subkeys
    if "time" in process_info:
        process_info["timeInformation"] = process_info.pop("time")
        time_info = process_info["timeInformation"]
        if "other" in time_info:
            time_info["otherTime"] = time_info.pop("other")
            for item in time_info["otherTime"].get("anies", []):
                if isinstance(item, dict) and "value" in item:
                    # Rename "value" to "timestampValue" regardless of its type.
                    item["timestampValue"] = item.pop("value")

    # --- modellingAndValidation transformations ---
    mod_val = data.get("modellingAndValidation", {})

    # In LCIMethodAndAllocation, rename "other" to "otherMAA"
    lci_method = mod_val.get("LCIMethodAndAllocation", {})
    if "other" in lci_method:
        lci_method["otherMAA"] = lci_method.pop("other")

    # In dataSourcesTreatmentAndRepresentativeness, rename "other" to "otherDSTAR"
    dstar = mod_val.get("dataSourcesTreatmentAndRepresentativeness", {})
    if "other" in dstar:
        dstar["otherDSTAR"] = dstar.pop("other")
        if "anies" in dstar["otherDSTAR"]:
            # Rename inner "anies" list to "aniesDSTAR"
            dstar["otherDSTAR"]["aniesDSTAR"] = dstar["otherDSTAR"].pop("anies")
            for item in dstar["otherDSTAR"]["aniesDSTAR"]:
                if (
                    isinstance(item, dict)
                    and "value" in item
                    and isinstance(item["value"], dict)
                ):
                    item["valueDSTAR"] = item.pop("value")
                    val = item["valueDSTAR"]
                    if "shortDescription" in val:
                        val["shortDescriptionExtended"] = val.pop("shortDescription")
                    if "version" in val:
                        version = val.pop("version")
                        if "version" in version:
                            version["versionInt"] = version.pop("version")
                        val["versionDict"] = version
                    if "uuid" in val:
                        uuid_obj = val.pop("uuid")
                        if "uuid" in uuid_obj:
                            uuid_obj["uuidValue"] = uuid_obj.pop("uuid")
                        val["uuidDict"] = uuid_obj

    # Rename "validation" to "validationInfo"
    if "validation" in mod_val:
        mod_val["validationInfo"] = mod_val.pop("validation")

    # Rename "other" to "otherMAV" and update inner keys for each item
    if "other" in mod_val:
        mod_val["otherMAV"] = mod_val.pop("other")
        for item in mod_val["otherMAV"].get("anies", []):
            if (
                isinstance(item, dict)
                and "value" in item
                and isinstance(item["value"], dict)
            ):
                item["objectValue"] = item.pop("value")

    # --- administrativeInformation transformations ---
    admin_info = data.get("administrativeInformation", {})

    # In publicationAndOwnership, rename "other" to "otherPAO" and update inner keys
    pub_own = admin_info.get("publicationAndOwnership", {})
    if "other" in pub_own:
        pub_own["otherPAO"] = pub_own.pop("other")
        for item in pub_own["otherPAO"].get("anies", []):
            if (
                isinstance(item, dict)
                and "value" in item
                and isinstance(item["value"], dict)
            ):
                item["objectValue"] = item.pop("value")

    # --- exchanges transformations ---
    exchanges = data.get("exchanges", {}).get("exchange", [])
    for exchange in exchanges:
        # For each exchange's flowProperties, rename "name" to "nameFP" and "uuid" to "uuidFP"
        for fp in exchange.get("flowProperties", []):
            if "name" in fp:
                fp["nameFP"] = fp.pop("name")
            if "uuid" in fp:
                fp["uuidFP"] = fp.pop("uuid")

        # Rename "exchange direction" to "exchangeDirection"
        if "exchange direction" in exchange:
            exchange["exchangeDirection"] = exchange.pop("exchange direction")

        # Rename "other" to "otherEx" and update inner keys for each item in "anies"
        if "other" in exchange:
            exchange["otherEx"] = exchange.pop("other")
            for item in exchange["otherEx"].get("anies", []):
                if (
                    isinstance(item, dict)
                    and "value" in item
                    and isinstance(item["value"], dict)
                ):
                    item["objectValue"] = item.pop("value")

        # Rename "classification" to "classificationEx" and inside, rename "name" to "nameClass"
        if "classification" in exchange:
            exchange["classificationEx"] = exchange.pop("classification")
            if "name" in exchange["classificationEx"]:
                exchange["classificationEx"]["nameClass"] = exchange[
                    "classificationEx"
                ].pop("name")

    # --- LCIAResults transformations ---
    # Rename "LCIAResults" to "lciaResults" at the top-level if present
    if "LCIAResults" in data:
        data["lciaResults"] = data.pop("LCIAResults")

    lcia_results = data.get("lciaResults", {}).get("LCIAResult", [])
    for result in lcia_results:
        # Rename "other" to "otherLCIA" and update inner keys for each item in "anies"
        if "other" in result:
            result["otherLCIA"] = result.pop("other")
            for item in result["otherLCIA"].get("anies", []):
                if (
                    isinstance(item, dict)
                    and "value" in item
                    and isinstance(item["value"], dict)
                ):
                    item["objectValue"] = item.pop("value")
        # In referenceToLCIAMethodDataSet, keys (like "uri") will be renamed globally

    # --- Removal ---
    # Remove the top-level "otherAttributes" key and its contents.
    if "otherAttributes" in data:
        data.pop("otherAttributes")

    # --- Global Removal of Raw Strings from any "anies" key ---
    data = remove_raw_strings_in_anies(data)

    # --- Global URI Renaming ---
    # Recursively rename any key "uri" to "refObjectUri" throughout the JSON.
    data = recursive_rename_uri(data)

    return data


if __name__ == "__main__":
    # Load the JSON file from disk
    with open(
        "data/pipeline2/json/epds/0db12903-1403-4c9a-817e-b48299d17aba.json",
        "r",
        encoding="utf-8",
    ) as infile:
        json_data = json.load(infile)

    # Apply all key renaming transformations
    transformed_data = transform_json(json_data)

    # Write the updated JSON to a new file with an indent of 2
    with open(
        "data/pipeline2/json/epds/0db12903-1403-4c9a-817e-b48299d17aba_RN.json",
        "w",
        encoding="utf-8",
    ) as outfile:
        json.dump(transformed_data, outfile, indent=2)
