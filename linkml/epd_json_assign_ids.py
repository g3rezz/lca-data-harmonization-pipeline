import json
import yaml
import re

# === Configuration: file paths ===
SCHEMA_PATH = (
    "linkml/data/yaml/linkml_ILCDmergedSchemas_schema.yaml"  # Consolidated YAML schema
)
JSON_FILE_PATH = "data/pipeline2/json/epds/63a79af1-1ab0-4677-45a8-08dc6fc9d4ca_RN.json"  # Input JSON instance for the EPD
OUTPUT_JSON_PATH = (
    "data/pipeline2/json/epds/63a79af1-1ab0-4677-45a8-08dc6fc9d4ca_RN_ID.json"
)

# --- Schema Utilities (kept for future extension) ---


def load_yaml_schema(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def build_classes_mapping(schema):
    """Returns a mapping of class names to definitions from the consolidated YAML schema."""
    return schema.get("classes", {})


def build_slot_to_range_mapping(schema):
    """Builds a mapping from slot name to its expected range (class name) from the schema."""
    mapping = {}
    for slot_name, slot_def in schema.get("slots", {}).items():
        if "range" in slot_def:
            mapping[slot_name] = slot_def["range"]
    return mapping


def class_requires_id(class_name, classes_map, visited=None):
    """
    Determines if a given class (or one of its ancestors) requires an ID.
    (This function is available if you want to consult the schema.)
    """
    if visited is None:
        visited = set()
    if class_name in visited:
        return False
    visited.add(class_name)
    class_def = classes_map.get(class_name, {})
    attributes = class_def.get("attributes", {})
    if attributes.get("id", {}).get("identifier", False):
        return True
    parent = class_def.get("is_a")
    if parent:
        if isinstance(parent, list):
            return any(class_requires_id(p, classes_map, visited) for p in parent)
        else:
            return class_requires_id(parent, classes_map, visited)
    return False


# --- ID Generation and Helper Functions ---


def generate_id_from_path(acc_path, prefix="ilcd"):
    """
    Given an accumulated path, returns the full ID as: prefix:acc_path
    """
    return f"{prefix}:{acc_path}"


def get_suffix(item, index):
    """
    If the list element (item) is a dict with a 'module' field,
    return 'module' + its value (dashes removed);
    otherwise, return the 1-based index as a two-digit string.
    """
    if isinstance(item, dict) and "module" in item:
        return f"module{item['module'].replace('-', '')}"
    return f"{index + 1:02d}"


def reorder_dict_keys(d):
    """
    Reorders a dictionary so that if 'id' exists, it appears as the first key.
    (For human readability.)
    """
    if "id" in d:
        id_value = d.pop("id")
        new_d = {"id": id_value}
        new_d.update(d)
        d.clear()
        d.update(new_d)


def clean_epd_name(name):
    """
    Cleans the EPD name by replacing non-alphanumeric characters with underscores,
    collapsing multiple underscores, and stripping leading/trailing underscores.
    """
    cleaned = re.sub(r"[^A-Za-z0-9]", "_", name)
    return re.sub(r"_+", "_", cleaned).strip("_")


# --- Recursive ID Assignment Based on Full Parent Path Only for List Elements ---


def assign_ids_by_path(obj, epd_uuid, acc_path, parent_is_list, prefix="ilcd"):
    """
    Recursively assigns IDs based on the accumulated path.

    Parameters:
      - obj: the current object.
      - epd_uuid: the UUID string (without dashes) from the top level.
      - acc_path: the accumulated path.
      - parent_is_list: boolean indicating whether the immediate container was a list.
      - prefix: default prefix (e.g. "ilcd").

    Rule:
      * If the current container is a dictionary and parent_is_list is False, then the new accumulated path is reset to the property key.
      * If parent_is_list is True, then the new accumulated path becomes: acc_path + "_" + property key.
      * For list elements, the suffix (from module or index) is appended.
    """
    # If this object is a dictionary and does not yet have an id, assign one:
    if isinstance(obj, dict) and "id" not in obj:
        # The top-level id is built as: prefix:epd_uuid + "_" + acc_path
        obj["id"] = generate_id_from_path(f"{epd_uuid}_{acc_path}", prefix)
        reorder_dict_keys(obj)

    if isinstance(obj, dict):
        for key, value in obj.items():
            if key == "id":
                continue
            # Determine new accumulated path:
            if isinstance(value, dict):
                # For a dictionary value, if the parent is a list, we keep parent's acc_path and append the key.
                # Otherwise, we reset to just the key.
                new_acc = f"{acc_path}_{key}" if parent_is_list else key
                assign_ids_by_path(
                    value, epd_uuid, new_acc, parent_is_list=False, prefix=prefix
                )
            elif isinstance(value, list):
                # For a list value, we always want to append the property key to the parent's accumulated path.
                new_acc = f"{acc_path}_{key}"
                for i, item in enumerate(value):
                    suffix = get_suffix(item, i)
                    # For each list element, the new accumulated path is: new_acc + "_" + suffix.
                    element_acc = f"{new_acc}_{suffix}"
                    assign_ids_by_path(
                        item, epd_uuid, element_acc, parent_is_list=True, prefix=prefix
                    )
            # If value is primitive, nothing to do.
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            suffix = get_suffix(item, i)
            new_acc = f"{acc_path}_{suffix}"
            assign_ids_by_path(
                item, epd_uuid, new_acc, parent_is_list=True, prefix=prefix
            )


# --- Main Processing ---


def main():
    # Load the consolidated YAML schema.
    schema = load_yaml_schema(SCHEMA_PATH)
    default_prefix = schema.get("default_prefix")
    if not default_prefix:
        raise ValueError("No default_prefix found in the YAML schema.")

    # (Schema-based mappings are still available if needed.)
    classes_map = build_classes_mapping(schema)
    slot_to_range = build_slot_to_range_mapping(schema)

    print("Default prefix (dynamically loaded):", default_prefix)

    # Load the JSON instance.
    with open(JSON_FILE_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Extract the UUID from the JSON and remove dashes.
    try:
        raw_uuid = data["processInformation"]["dataSetInformation"]["UUID"]
    except KeyError as e:
        raise KeyError(
            "Missing required field: processInformation.dataSetInformation.UUID"
        ) from e
    epd_uuid = raw_uuid.replace("-", "")

    # Set the top-level ID to the UUID (only the UUID; no extra keys).
    top_id = f"{default_prefix.lower()}:{epd_uuid}"
    data["id"] = top_id
    print("Top-level ID set to:", top_id)

    # Process each top-level section (except 'id' and 'version'):
    for top_key, top_obj in data.items():
        if top_key in ["id", "version"]:
            continue
        if isinstance(top_obj, dict):
            # For top-level sections (which are dictionary values), the new accumulated path is just the property key.
            section_acc = top_key
            # Set the section's ID as: prefix:epd_uuid + "_" + section_acc
            top_obj["id"] = f"{default_prefix.lower()}:{epd_uuid}_{section_acc}"
            reorder_dict_keys(top_obj)
            # Recurse into the section with parent_is_list = False.
            assign_ids_by_path(
                top_obj,
                epd_uuid,
                section_acc,
                parent_is_list=False,
                prefix=default_prefix.lower(),
            )
        elif isinstance(top_obj, list):
            # For a top-level list, each element gets a suffix.
            for i, item in enumerate(top_obj):
                suffix = get_suffix(item, i)
                section_acc = f"{top_key}_{suffix}"
                assign_ids_by_path(
                    item,
                    epd_uuid,
                    section_acc,
                    parent_is_list=True,
                    prefix=default_prefix.lower(),
                )

    # Save the updated JSON.
    with open(OUTPUT_JSON_PATH, "w", encoding="utf-8") as out_f:
        json.dump(data, out_f, indent=2, ensure_ascii=False)

    print(f"Updated IDs have been assigned and saved to {OUTPUT_JSON_PATH}")


if __name__ == "__main__":
    main()
