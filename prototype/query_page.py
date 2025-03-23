import streamlit as st
import streamlit.components.v1 as components
from utils import (
    run_query,
    display_results,
    build_dynamic_query,
    run_cost_group_query,
    sparql_results_to_dataframe,
)
from streamlit_agraph import agraph, Node, Edge, Config, ConfigBuilder


# (1) SIDEBAR CONTROLS


with st.sidebar.expander("**Main Filters**", expanded=False):
    # -- Category Filter (selectbox)
    selected_category = st.selectbox(
        "EPD Category",
        options=["ready-mixed concrete"],
        placeholder="ready-mixed concrete",
        disabled=True,
    )

    # -- DIN 276 Cost Group Filter (multi-select)
    din_options = [
        "320",
        "322",
        "323",
        "330",
        "331",
        "340",
        "341",
        "343",
        "350",
        "351",
        "360",
        "361",
        "370",
        "371",
    ]
    selected_din = st.multiselect(
        "DIN 276 (CG)",
        options=din_options,
    )

    # -- Strict DIN 276 Cost Group Filtering Toggle
    strict_din = st.checkbox(
        "Strict cost group filtering",
        help="""
    **Strict Cost Group Filtering:**
    - **Enabled:** Only display EPDs that include all of the selected cost groups.
    - **Disabled:** EPDs matching any of the selected groups will be shown.
    """,
    )

    # -- Module Filter (multi-select)
    module_options = ["A1-A3", "A4", "A5", "B1", "C1", "C2", "C3", "C4", "D"]
    selected_modules = st.multiselect(
        "Module",
        options=module_options,
        # default=["A1-A3"],
    )

    # -- Environmental Impact Filter (selectbox)
    environmental_options = [
        "AP",
        "GWP-total",
        "GWP-biogenic",
        "GWP-fossil",
        "GWP-luluc",
        "ETP-fw",
        "PM",
        "EP-marine",
        "EP-freshwater",
        "EP-terrestrial",
        "HTP-c",
        "HTP-nc",
        "IRP",
        "SQP",
        "ODP",
        "POCP",
        "ADPF",
        "ADPE",
        "WDP",
    ]
    selected_environmental = st.selectbox(
        "Environmental Impact Indicator", options=environmental_options, index=1
    )

    # -- Life Cycle Filter (selectbox)
    lifecycle_options = [
        "PERE",
        "PERM",
        "PERT",
        "PENRE",
        "PENRM",
        "PENRT",
        "SM",
        "RSF",
        "NRSF",
        "FW",
        "HWD",
        "NHWD",
        "RWD",
        "CRU",
        "MFR",
        "MER",
        "EEE",
        "EET",
    ]
    selected_lifecycle = st.selectbox(
        "Life Cycle Indicator", options=lifecycle_options, index=5
    )

    # -- GWP Threshold Filter
    environmental_indicator_threshold = st.slider(
        f"{selected_environmental}", min_value=0, max_value=1000, value=250
    )

    # -- PENRT Threshold Filter
    lifecycle_indicator_threshold = st.slider(
        f"{selected_lifecycle}", min_value=0, max_value=5000, value=2000
    )

    # -- Scenario Toggle (Recycled)
    scenario_recycled = st.checkbox("Recycled")

with st.sidebar.expander("**Concrete Filters**", expanded=False):
    # -- Concrete Strength Filter (multi-select)
    strength_options = ["Low", "Medium", "High"]
    selected_strength = st.multiselect(
        "Concrete Strength",
        options=strength_options,
    )

    # -- Bulk Density Filter (multi-select)
    density_options = ["Light", "Normal", "Heavy"]
    selected_density = st.multiselect(
        "Concrete Weight",
        options=density_options,
    )

with st.sidebar.expander("**Dataset Filters**", expanded=False):
    # -- Country Filter (multi-select)
    country_options = ["DE", "IT"]
    selected_countries = st.multiselect(
        "Country",
        options=country_options,
    )

    # -- subType Filter (multi-select)
    subtype_options = [
        "specific",
        "average",
        "representative",
        "template",
        "generic",
    ]
    selected_subtypes = st.multiselect(
        "Dataset Type",
        options=subtype_options,
    )


# -- Query Mode Toggle
mode = st.sidebar.toggle("Average EPD Mode")

# -- Button to run the dynamic query
if st.sidebar.button(
    "Run Query",
    # help="Select one or more filters. \n\nIf none are selected, all results will be displayed.",
    use_container_width=True,
    type="primary",
):
    # Build the query
    dynamic_query = build_dynamic_query(
        category=selected_category,
        modules=selected_modules,
        countries=selected_countries,
        subtypes=selected_subtypes,
        str_groups=selected_strength,
        density_groups=selected_density,
        din_groups=selected_din,
        environ_thr=environmental_indicator_threshold,
        lifecycle_thr=lifecycle_indicator_threshold,
        scenario_recycled=scenario_recycled,
        strict_din=strict_din,
        query_mode=mode,
        environmental_indicator=selected_environmental,
        lifecycle_indicator=selected_lifecycle,
    )

    # Store the mode used for this App run
    st.session_state["query_mode_used"] = mode

    # Uncomment to show the query for troubleshooting
    # st.write("**SPARQL Query**:")
    # st.code(dynamic_query, language="sparql")

    # Execute query
    try:
        st.session_state.results = run_query(dynamic_query)
        st.session_state.query_string = dynamic_query
    except Exception as e:
        st.error(f"Error running dynamic query: {e}")

# 2) DISPLAY RESULTS

# tabs = st.tabs(["Table", "Graph", "SPARQL"])
height = 600

if "results" not in st.session_state:
    st.info("Adjust filters in the sidebar and click 'Run Query'.")
else:
    # with tabs[0]:
    # Use the query_mode that was used to produce these results
    mode_for_display = st.session_state.get("query_mode_used", False)

    # Read existing highlight states or use defaults
    current_gwp = st.session_state.get("highlight_gwp", False)
    current_penrt = st.session_state.get("highlight_penrt", False)

    # Render the table using the *current* states
    if "results" in st.session_state and st.session_state["results"]:
        display_table = display_results(
            st.session_state["results"],
            highlight_gwp=current_gwp,
            highlight_penrt=current_penrt,
            query_mode=mode_for_display,
            selected_env=selected_environmental,
            selected_lc=selected_lifecycle,
        )

    # If table is empty and mode is semantic do not show checkboxes
    if display_table and mode_for_display == False:
        new_gwp = st.checkbox(
            f"Highlight top 3 average {selected_environmental} EPDs", value=current_gwp
        )
        new_penrt = st.checkbox(
            f"Highlight top 3 average {selected_lifecycle} EPDs", value=current_penrt
        )

        # If user changed something, update session_state and rerun
        if (new_gwp != current_gwp) or (new_penrt != current_penrt):
            st.session_state["highlight_gwp"] = new_gwp
            st.session_state["highlight_penrt"] = new_penrt
            st.rerun()

    # print(st.session_state["results"])
    # print("-" * 50)

    if display_table:
        results_json = st.session_state["results"]
        bindings = results_json.get("results", {}).get("bindings", [])
        if bindings:
            first_binding = bindings[0]
            if first_binding.get("DIN276CostGroupList"):
                with st.expander("**BKI Elements Details**", expanded=True):
                    cost_group_results_query = run_cost_group_query(results_json)
                    st.session_state.cost_group_results = cost_group_results_query
                    cost_group_results = run_query(cost_group_results_query)
                    if cost_group_results:
                        sparql_results_to_dataframe(cost_group_results)

# with tabs[1]:
#     # (Optional) Graph placeholder
#     st.info("No graph visualization is implemented for the dynamic query.")
#     # If you want a graph, integrate your PyVis or similar approach here:
#     # html_graph = create_network(st.session_state["results"], "dynamic", height=height)
#     # components.html(html_graph, height=height + 10)

# with tabs[2]:
#     # Show the generated SPARQL
#     st.write("EPD Query:")
#     st.code(st.session_state["query_string"], language="sparql")
#     results_json = st.session_state["results"]
#     bindings = results_json.get("results", {}).get("bindings", [])
#     if bindings:
#         first_binding = bindings[0]
#         if first_binding.get("DIN276CostGroupList"):
#             st.write("BKI Query:")
#             st.code(st.session_state["cost_group_results"], language="sparql")
