import streamlit as st
import json
import streamlit.components.v1 as components
from pyvis_utils import create_network
from utils import run_query, display_results


# Load queries once
with open("prototype/queries.json", "r") as f:
    queries = json.load(f)

# Sidebar: Create a button for each query with its description.
st.sidebar.header("Queries")
for qid, content in queries.items():
    if st.sidebar.button(qid, key=qid):
        try:
            st.session_state.current_query = qid
            st.session_state.results_json = run_query(content["query"])
        except Exception as e:
            st.sidebar.error(f"Error running query {qid}: {e}")
    st.sidebar.markdown(content["description"])
    st.sidebar.write("")  # spacer

# Main area: Create tabs for Graph, Table, Code, and Schema.
tabs = st.tabs(["Graph", "Table", "Code"])
height = 750

# Only render Graph, Table, and Code if a query has been executed.
if "current_query" not in st.session_state or st.session_state.results_json is None:
    st.info("Select a query from the sidebar to execute it.")
else:
    current_id = st.session_state.current_query
    with tabs[0]:
        html_graph = create_network(
            st.session_state.results_json, current_id, height=height
        )
        components.html(html_graph, height=height + 10)
    with tabs[1]:
        display_results(st.session_state.results_json)
    with tabs[2]:
        st.code(queries[current_id]["query"], language="sparql")
