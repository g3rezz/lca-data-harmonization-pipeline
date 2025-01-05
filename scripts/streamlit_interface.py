import streamlit as st
import json
import os


# Load JSON file
def load_json(file_path):
    with open(file_path, "r") as file:
        return json.load(file)


# Save the validation results
def save_validation_results(results, output_file):
    with open(output_file, "w") as file:
        json.dump(results, file, indent=4)


# Load the LLM's JSON output
input_file = "data/response_gpt-4o-mini.json"
output_file = "data/validated_response_gpt-4o-mini.json"

if os.path.exists(input_file):
    data = load_json(input_file)
else:
    st.error("Input file not found.")
    st.stop()

# Streamlit interface
st.set_page_config(layout="wide")
st.title("Human-in-the-Loop Validation")

# Load existing results if available
if os.path.exists(output_file):
    validation_results = load_json(output_file)
else:
    validation_results = []

# Convert JSON data to a list of dictionaries for display
data_table = []
validation_dict = {item["attribute"]: item for item in validation_results}

for item in data:
    attribute = item["attribute"]
    match_type = item["match_type"]
    field_name = item["field_name"]

    validation_status = validation_dict.get(attribute, {}).get(
        "correct_match", "Pending"
    )

    data_table.append(
        {
            "Attribute": attribute,
            "Match Type": match_type,
            "Field Name": field_name,
            "Validation": validation_status,
        }
    )

# Initialize session state for validation results if not already set
if "validation_results" not in st.session_state:
    st.session_state.validation_results = validation_dict

# Create the table with buttons in separate columns
data_table_header = [
    "Attribute",
    "Match Type",
    "Field Name",
    "Validation",
    "Button Yes",
    "Button No",
    "Button Almost",
]
st.write("### Table with Validation Buttons")

for row in data_table:
    color = (
        "green"
        if st.session_state.validation_results.get(row["Attribute"], {}).get(
            "correct_match"
        )
        == "yes"
        else (
            "red"
            if st.session_state.validation_results.get(row["Attribute"], {}).get(
                "correct_match"
            )
            == "no"
            else (
                "orange"
                if st.session_state.validation_results.get(row["Attribute"], {}).get(
                    "correct_match"
                )
                == "almost"
                else "white"
            )
        )
    )

    col1, col2, col3, col4, col5, col6, col7 = st.columns([2, 2, 2, 1, 1, 1, 1])

    with col1:
        st.markdown(
            f"<span style='color: {color}; font-weight: bold;'>{row['Attribute']}</span>",
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            f"<span style='color: {color}; font-weight: bold;'>{row['Match Type']}</span>",
            unsafe_allow_html=True,
        )
    with col3:
        st.markdown(
            f"<span style='color: {color}; font-weight: bold;'>{row['Field Name']}</span>",
            unsafe_allow_html=True,
        )
    with col4:
        st.markdown(
            f"<span style='color: {color}; font-weight: bold;'>{row['Validation']}</span>",
            unsafe_allow_html=True,
        )
    with col5:
        if st.button("Yes", key=f"yes_{row['Attribute']}"):
            st.session_state.validation_results[row["Attribute"]] = {
                "attribute": row["Attribute"],
                "match_type": row["Match Type"],
                "field_name": row["Field Name"],
                "correct_match": "yes",
            }
            save_validation_results(
                list(st.session_state.validation_results.values()), output_file
            )
            st.session_state.validation_results_updated = True
            st.rerun()
    with col6:
        if st.button("No", key=f"no_{row['Attribute']}"):
            st.session_state.validation_results[row["Attribute"]] = {
                "attribute": row["Attribute"],
                "match_type": row["Match Type"],
                "field_name": row["Field Name"],
                "correct_match": "no",
            }
            save_validation_results(
                list(st.session_state.validation_results.values()), output_file
            )
            st.session_state.validation_results_updated = True
            st.rerun()
    with col7:
        if st.button("Almost", key=f"almost_{row['Attribute']}"):
            st.session_state.validation_results[row["Attribute"]] = {
                "attribute": row["Attribute"],
                "match_type": row["Match Type"],
                "field_name": row["Field Name"],
                "correct_match": "almost",
            }
            save_validation_results(
                list(st.session_state.validation_results.values()), output_file
            )
            st.session_state.validation_results_updated = True
            st.rerun()
