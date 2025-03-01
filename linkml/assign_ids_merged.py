import json
import yaml
import re

# === Configuration: file paths ===
SCHEMA_PATH = (
    "linkml/data/yaml/linkml_ILCDmergedSchemas_schema.yaml"  # Consolidated YAML schema
)
JSON_FILE_PATH = "linkml/data/json/5b6b44e0-f5e4-451f-54a3-08dcec2f0f89_renamedScript.json"  # Input JSON instance for the EPD
OUTPUT_JSON_PATH = (
    "linkml/data/json/5b6b44e0-f5e4-451f-54a3-08dcec2f0f89_renamedScript_newID02.json"
)

# === Utility Functions ===


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
    Checks for an explicit attribute or inherited 'id: identifier: true'.
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


def generate_id(parent_id, slot_name, index_or_key=None, prefix="ilcd", in_list=False):
    """
    Generates a new ID using the pattern:
       {prefix}:{ParentBase}_{SlotName}_{StableKeyOrIndex}  (if in_list is True)
    For non-list objects (in_list is False), the ID is based solely on the key.
    """
    if parent_id is None:
        # Top-level: use only the key (and index if in a list)
        if in_list:
            key = index_or_key if index_or_key is not None else "1"
            return f"{prefix}:{slot_name}_{key}"
        else:
            return f"{prefix}:{slot_name}"
    else:
        parent_base = parent_id.replace(f"{prefix}:", "")
        if in_list:
            key = index_or_key if index_or_key is not None else "1"
            return f"{prefix}:{parent_base}_{slot_name}_{key}"
        else:
            return f"{prefix}:{parent_base}_{slot_name}"


def get_stable_key(obj, index):
    """
    Checks for a 'module' field in the object.
    If not found, returns a 1-based index as a string.
    """
    if isinstance(obj, dict) and "module" in obj:
        return f"module{obj['module'].replace("-", "")}"
    return str(index + 1)


def reorder_dict_keys(d):
    """
    Reorders a dictionary so that if 'id' exists, it appears as the first key.
    (For human readability only.)
    """
    if "id" in d:
        id_value = d.pop("id")
        new_dict = {"id": id_value}
        new_dict.update(d)
        d.clear()
        d.update(new_dict)


def clean_epd_name(name):
    """
    Cleans the EPD name by replacing non-alphanumeric characters with underscores,
    collapsing multiple underscores, and stripping leading/trailing underscores.
    """
    cleaned = re.sub(r"[^A-Za-z0-9]", "_", name)
    cleaned = re.sub(r"_+", "_", cleaned).strip("_")
    return cleaned


# === ID Assignment: Recursive Traversal ===


def assign_ids(
    obj,
    current_class,
    parent_id=None,
    slot_name=None,
    index=None,
    classes_map=None,
    slot_to_range=None,
    prefix="ilcd",
):
    """
    Recursively traverses the JSON structure.
    If the expected class (or its ancestors) requires an ID,
    generates a new ID based on the parent's context and slot name.
    The in_list flag is True when processing an element from a list (i.e. index is not None).
    """
    in_list = index is not None
    # Only generate an ID if the object's expected class requires one.
    if (
        isinstance(obj, dict)
        and current_class is not None
        and class_requires_id(current_class, classes_map)
    ):
        stable_key = get_stable_key(obj, index) if in_list else None
        new_id = generate_id(
            parent_id,
            slot_name if slot_name else current_class,
            stable_key,
            prefix=prefix,
            in_list=in_list,
        )
        obj["id"] = new_id
        parent_id = new_id  # For nested items, use this as the parent's id.

    if isinstance(obj, dict):
        for key, value in obj.items():
            child_class = slot_to_range.get(key, None)
            if isinstance(value, list):
                for i, item in enumerate(value):
                    assign_ids(
                        item,
                        current_class=child_class,
                        parent_id=parent_id,
                        slot_name=key,
                        index=i,
                        classes_map=classes_map,
                        slot_to_range=slot_to_range,
                        prefix=prefix,
                    )
            elif isinstance(value, dict):
                assign_ids(
                    value,
                    current_class=child_class,
                    parent_id=parent_id,
                    slot_name=key,
                    classes_map=classes_map,
                    slot_to_range=slot_to_range,
                    prefix=prefix,
                )
        reorder_dict_keys(obj)
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            assign_ids(
                item,
                current_class=current_class,
                parent_id=parent_id,
                slot_name=slot_name,
                index=i,
                classes_map=classes_map,
                slot_to_range=slot_to_range,
                prefix=prefix,
            )


# === Main Processing ===


def main():
    # --- Load the consolidated YAML schema ---
    schema = load_yaml_schema(SCHEMA_PATH)

    # Dynamically extract the default prefix from the YAML schema.
    default_prefix = schema.get("default_prefix")
    if not default_prefix:
        raise ValueError("No default_prefix found in the YAML schema.")

    # Build classes mapping and slot-to-range mapping.
    classes_map = build_classes_mapping(schema)
    slot_to_range = build_slot_to_range_mapping(schema)

    print("Default prefix (dynamically loaded):", default_prefix)
    print("Classes Mapping:", list(classes_map.keys()))
    print("Slot-to-range mapping:", slot_to_range)

    # --- Load the JSON instance ---
    with open(JSON_FILE_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Automatically generate the top-level EPD id from the cleaned EPD name.
    if "id" not in data:
        try:
            # baseName is a list; take the first element.
            epd_name = data["processInformation"]["dataSetInformation"]["dataSetName"][
                "baseName"
            ][0]["value"]
        except (KeyError, IndexError) as e:
            raise KeyError(
                "Missing required field: processInformation.dataSetInformation.dataSetName.baseName[0].value"
            ) from e
        cleaned_name = clean_epd_name(epd_name)
        top_epd_id = f"{default_prefix.lower()}:{cleaned_name}"
        data["id"] = top_epd_id
        print("Generated top-level EPD id:", top_epd_id)

    # Process each top-level section except 'id' and 'version'.
    # For top-level sections, do not append any number (they're not in a list).
    for top_key, top_obj in data.items():
        if top_key in ["id", "version"]:
            continue
        if isinstance(top_obj, dict) and "id" not in top_obj:
            top_obj["id"] = generate_id(
                None, top_key, prefix=default_prefix.lower(), in_list=False
            )
        # Now propagate IDs to nested objects. For nested objects that are not in a list, no number is appended.
        assign_ids(
            top_obj,
            current_class=top_key,
            parent_id=top_obj["id"],
            slot_name=top_key,
            classes_map=classes_map,
            slot_to_range=slot_to_range,
            prefix=default_prefix.lower(),
        )

    # --- Save the updated JSON ---
    with open(OUTPUT_JSON_PATH, "w", encoding="utf-8") as out_f:
        json.dump(data, out_f, indent=2, ensure_ascii=False)

    print(f"Updated IDs have been assigned and saved to {OUTPUT_JSON_PATH}")


if __name__ == "__main__":
    main()
