import streamlit as st
import pandas as pd
from SPARQLWrapper import SPARQLWrapper, JSON

# Update this to match your Fuseki SPARQL endpoint:
ENDPOINT_URL = "http://localhost:3030/EPD_RDF/sparql"


def run_query(query: str):
    sparql = SPARQLWrapper(ENDPOINT_URL)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results


def display_results(results_json):
    bindings = results_json["results"]["bindings"]
    var_names = results_json["head"]["vars"]
    table_rows = []
    for row in bindings:
        row_data = []
        for var in var_names:
            cell_value = row[var]["value"] if var in row else ""
            row_data.append(cell_value)
        table_rows.append(row_data)
    df = pd.DataFrame(table_rows, columns=var_names)
    df.index = df.index + 1
    st.table(df)
