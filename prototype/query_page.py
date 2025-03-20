import streamlit as st
import streamlit.components.v1 as components
from utils import run_query, display_results, build_dynamic_query
from streamlit_agraph import agraph, Node, Edge, Config, ConfigBuilder

##############################################################################
# 1) SIDEBAR CONTROLS
##############################################################################

st.sidebar.title(
    "Filters",
    help="Select one or more filters. \n\nIf none are selected, all results will be displayed.",
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
selected_din = st.sidebar.multiselect("DIN 276 (CG)", options=din_options)

# -- Strict DIN 276 Cost Group Filtering Toggle
strict_din = st.sidebar.checkbox(
    "Strict cost group",
    help="Show EPDs that include every specified cost group. Otherwise, EPDs with any of these groups are shown.",
)

# -- Module Filter (multi-select)
module_options = ["A1-A3", "A4", "A5", "B1", "C1", "C2", "C3", "C4", "D"]
selected_modules = st.sidebar.multiselect(
    "Module",
    options=module_options,
    default=["A1-A3"],
)

# -- Country Filter (multi-select)
country_options = ["DE", "IT"]
selected_countries = st.sidebar.multiselect(
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
selected_subtypes = st.sidebar.multiselect(
    "Dataset Type",
    options=subtype_options,
)

# -- Concrete Strength Filter (multi-select)
strength_options = ["Low", "Medium", "High"]
selected_strength = st.sidebar.multiselect(
    "Concrete Strength",
    options=strength_options,
)

# -- Bulk Density Filter (multi-select)
density_options = ["Light", "Normal", "Heavy"]
selected_density = st.sidebar.multiselect(
    "Concrete Weight",
    options=density_options,
)


# -- GWP Threshold Filter
gwp_threshold = st.sidebar.slider("GWP", min_value=0, max_value=1000, value=250)

# -- PENRT Threshold Filter
penrt_threshold = st.sidebar.slider("PENRT", min_value=0, max_value=5000, value=2000)

# -- Scenario Toggle (Recycled)
scenario_recycled = st.sidebar.checkbox("Recycled")

# -- Query Mode Toggle
mode = st.sidebar.toggle("Average EPD")

# -- Button to run the dynamic query
if st.sidebar.button("Run Query"):
    # Build the query
    dynamic_query = build_dynamic_query(
        modules=selected_modules,
        countries=selected_countries,
        subtypes=selected_subtypes,
        str_groups=selected_strength,
        density_groups=selected_density,
        din_groups=selected_din,
        gwp_thr=gwp_threshold,
        penrt_thr=penrt_threshold,
        scenario_recycled=scenario_recycled,
        strict_din=strict_din,
        query_mode=mode,
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

# -- Highlight Average Toggle
# highlight_gwp = st.sidebar.checkbox("Highlight closest GWP?")
# highlight_penrt = st.sidebar.checkbox("Highlight closest PENRT?")

##############################################################################
# 2) DISPLAY RESULTS
##############################################################################

tabs = st.tabs(["Table", "Graph", "SPARQL"])
height = 600

if "results" not in st.session_state:
    st.info("Adjust filters in the sidebar and click 'Run Query'.")
else:
    with tabs[0]:
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
            )

        # If table is empty and mode is semantic do not show checkboxes
        if display_table and mode_for_display == False:
            new_gwp = st.checkbox("Highlight closest GWP rows?", value=current_gwp)
            new_penrt = st.checkbox(
                "Highlight closest PENRT rows?", value=current_penrt
            )

            # If user changed something, update session_state and rerun
            if (new_gwp != current_gwp) or (new_penrt != current_penrt):
                st.session_state["highlight_gwp"] = new_gwp
                st.session_state["highlight_penrt"] = new_penrt
                st.rerun()

    with tabs[1]:
        # (Optional) Graph placeholder
        st.info("No graph visualization is implemented for the dynamic query.")
        # If you want a graph, integrate your PyVis or similar approach here:
        # html_graph = create_network(st.session_state["results"], "dynamic", height=height)
        # components.html(html_graph, height=height + 10)

    with tabs[2]:
        # Show the generated SPARQL
        st.code(st.session_state["query_string"], language="sparql")
