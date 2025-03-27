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

st.sidebar.title(
    "**EPD.**_finder_",
    help="""**EPDfinder:**\n\n- Find EPDs from multiple datasets.\n- Select one or more filters to start. If none are selected, all results will be displayed.""",
)

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
        "310",
        "312",
        "320",
        "322",
        "323",
        "326",
        "330",
        "331",
        "332",
        "333",
        "335",
        "337",
        "340",
        "341",
        "342",
        "343",
        "346",
        "350",
        "351",
        "353",
        "355",
        "360",
        "361",
        "365",
        "370",
        "371",
        "372",
        "373",
        "374",
        "375",
        "376",
        "377",
        "378",
        "379",
    ]

    selected_din = st.multiselect(
        "DIN 276 (CG)",
        options=din_options,
        help="""
    **DIN 276 (CG):**
    - **310:** Trenchwork/Earthworks
    - **312:** Enclosure (support work)
    - **320:** Foundations/substructures
    - **322:** Shallow foundations and base slabs
    - **323:** Deep foundations
    - **326:** Drainage
    - **330:** External walls/vertical components, external
    - **331:** Loadbearing external walls
    - **332:** Non-loadbearing external walls
    - **333:** External columns
    - **335:** Cladding, external
    - **337:** Prefabricated external wall units
    - **340:** Internal walls/internal vertical components
    - **341:** Loadbearing internal walls
    - **342:** Non-loadbearing internal walls
    - **343:** Internal columns
    - **346:** Prefabricated internal wall units
    - **350:** Floors and ceilings/horizontal components
    - **351:** Floor components
    - **353:** Floorings
    - **355:** Prefabricated floor and ceiling units
    - **360:** Roofs
    - **361:** Roof structures
    - **365:** Prefabricated roof constructions
    - **370:** Infrastructure systems
    - **371:** Road traffic systems
    - **372:** Rail traffic systems
    - **373:** Air traffic systems
    - **374:** Hydraulic engineering systems
    - **375:** Waste water systems
    - **376:** Water supply systems
    - **377:** Energy supply and telecommunications systems
    - **378:** Waste disposal systems
    - **379:** Other items for CG 370
        """,
    )

    # -- Strict DIN 276 Cost Group Filtering Toggle
    strict_din = st.checkbox(
        "Strict cost group filtering",
        help="""
    **Strict Cost Group Filtering:**
    - **Enabled:** Only display EPDs that include all of the selected cost groups.
    - **Disabled:** Display EPDs matching any of the selected groups.
        """,
    )

    # -- Module Filter (multi-select)
    module_options = ["A1-A3", "A4", "A5", "B1", "C1", "C2", "C3", "C4", "D"]
    selected_modules = st.multiselect(
        "Module",
        options=module_options,
        help="""
    **Module Filter:**
    - **A1-A3**: Raw Materials Acquisition, Transport, and Manufacturing (Cradle-to-Gate)
    - **A4**: Transportation to Construction Site
    - **A5**: Installation
    - **B1**: Usage
    - **C1**: Demolition or Deconstruction
    - **C2**: Waste Transportation
    - **C3**: Waste Processing
    - **C4**: Waste Disposal
    - **D**: Recycling Potential
        """,
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
        "Environmental Impact Indicator",
        options=environmental_options,
        index=1,
        help="""
    **Environmental Impact Indicators:**
    - **AP**: Acidification potential, Accumulated Exceedance _mol H⁺ eqv._
    - **GWP-total**: Global Warming Potential – total _kg CO₂ eqv._
    - **GWP-biogenic**: Global Warming Potential – biogenic _kg CO₂ eqv._
    - **GWP-fossil**: Global Warming Potential – fossil fuels _kg CO₂ eqv._
    - **GWP-luluc**: Global Warming Potential – land use/change _kg CO₂ eqv._
    - **ETP-fw**: Potential Toxic Unit for ecosystems _CTUe_
    - **PM**: Disease incidence from PM emissions _disease incidence_
    - **EP-marine**: Eutrophication potential – marine _kg N eqv._
    - **EP-freshwater**: Eutrophication potential – freshwater _kg P eqv._
    - **EP-terrestrial**: Eutrophication potential – terrestrial _mol N eqv._
    - **HTP-c**: Toxic Unit for cancer effects _CTUh_
    - **HTP-nc**: Toxic Unit for non-cancer effects _CTUh_
    - **IRP**: Human exposure efficiency relative to U235 _kBq U235 eqv._
    - **SQP**: Soil quality index _unitless_
    - **ODP**: Ozone Depletion Potential _kg CFC-11 eqv._
    - **POCP**: Photochemical Ozone Creation Potential _kg NMVOC eqv._
    - **ADPF**: Abiotic depletion potential – fossil resources _MJ_
    - **ADPE**: Abiotic depletion potential – non-fossil resources _kg Sb-eqv._
    - **WDP**: Water deprivation potential _m³ world eqv._
        """,
    )

    # -- Environmental Impact Indicator Threshold Filter
    environmental_indicator_threshold = st.slider(
        f"{selected_environmental}", min_value=0, max_value=1000, value=1000
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
        "Life Cycle Indicator",
        options=lifecycle_options,
        index=5,
        help="""
    **Life Cycle Indicators:**
    - **PERE**: Use of renewable primary energy (_MJ_)
    - **PERM**: Renewable primary energy resources as raw materials (_MJ_)
    - **PERT**: Total renewable primary energy use (_MJ_)
    - **PENRE**: Use of non renewable primary energy (_MJ_)
    - **PENRM**: Non renewable primary energy resources as raw materials (_MJ_)
    - **PENRT**: Total non renewable primary energy use (_MJ_)
    - **SM**: Use of secondary material (_kg_)
    - **RSF**: Use of renewable secondary fuels (_MJ_)
    - **NRSF**: Use of non renewable secondary fuels (_MJ_)
    - **FW**: Use of net fresh water (_m³_)
    - **HWD**: Hazardous waste disposed (_kg_)
    - **NHWD**: Non hazardous waste disposed (_kg_)
    - **RWD**: Radioactive waste disposed (_kg_)
    - **CRU**: Components for re-use (_kg_)
    - **MFR**: Materials for recycling (_kg_)
    - **MER**: Materials for energy recovery (_kg_)
    - **EEE**: Exported electrical energy (_MJ_)
    - **EET**: Exported thermal energy (_MJ_)
        """,
    )

    # -- Life Cycle Indicator Threshold Filter
    lifecycle_indicator_threshold = st.slider(
        f"{selected_lifecycle}", min_value=0, max_value=5000, value=5000
    )

    # -- Scenario Toggle (Recycled)
    scenario_recycled = st.checkbox(
        "Recycled",
        help="""
    **Recycled:**
    - **Enabled:** Only display EPDs that are labeled as recycled.
    - **Disabled:** Display all EPDs, regardless of recycling status.
        """,
    )


with st.sidebar.expander("**Concrete Filters**", expanded=False):
    # -- Concrete Strength Filter (multi-select)
    strength_options = ["Low", "Medium", "High"]
    selected_strength = st.multiselect(
        "Concrete Strength",
        options=strength_options,
        help="""
    **Concrete Strength:**
    - **Low**: ≤ 25 _MPa_ (e.g., ≤ C16/20)
    - **Medium**: 25 – 40 _MPa_ (e.g., C20/25 – C30/37)
    - **High**: ≥ 40 _MPa_ (e.g., ≥ C35/45)
        """,
    )

    # -- Bulk Density Filter (multi-select)
    density_options = ["Light", "Normal", "Heavy"]
    selected_density = st.multiselect(
        "Concrete Weight",
        options=density_options,
        help="""
    **Concrete Weight:**
    - **Light**: 800–2000 _kg/m³_
    - **Normal**: 2000–2600 _kg/m³_
    - **Heavy**: >2600 _kg/m³_
        """,
    )

with st.sidebar.expander("**Dataset Filters**", expanded=False):
    # -- Country Filter (multi-select)
    country_options = ["DE", "IT", "NO", "DK", "GB"]
    selected_countries = st.multiselect(
        "Country",
        options=country_options,
        help="""
        **Country:**
        - Country or region the dataset represents.
            """,
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
        help="""
    **Dataset Type:**
    - **specific:** Company-specific data for a product from one production site.
    - **average:** Industry average data from multiple manufacturers, productions sites, or products.
    - **representative:** Data representing a country or region (e.g., national average for Germany).
    - **template:** Sample EPD data used as a reference.
    - **generic:** Data based other non-industry data sources (e.g. expert/literature sources).
        """,
    )


# -- Query Mode Toggle
mode = st.sidebar.toggle(
    "Average EPD Mode",
    help="""
    **Average EPD Mode:**
    - **Enabled:** Display three EPDs closest to the average of the selection criteria.
    - **Disabled:** Display all EPDs without average filtering.

    _Intended for early-phase Life Cycle Assessment (LCA)._
        """,
)


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
        st.error(f"**Error**: {e}", icon="🚨")

# 2) DISPLAY RESULTS

# tabs = st.tabs(["Table", "Graph", "SPARQL"])
height = 600

if "results" not in st.session_state:
    st.info("Adjust filters in the sidebar and click 'Run Query'.", icon="ℹ️")
else:
    # with tabs[0]:
    # Use the query_mode that was used to produce these results
    mode_for_display = st.session_state.get("query_mode_used", False)

    # Read existing highlight states or use defaults
    current_env = st.session_state.get("highlight_env", False)
    current_lc = st.session_state.get("highlight_lc", False)

    # Render the table using the *current* states
    if "results" in st.session_state and st.session_state["results"]:
        display_table = display_results(
            st.session_state["results"],
            highlight_env=current_env,
            highlight_lc=current_lc,
            query_mode=mode_for_display,
            selected_env=selected_environmental,
            selected_lc=selected_lifecycle,
        )

    # If table is empty and mode is semantic do not show checkboxes
    if display_table and mode_for_display == False:
        new_env = st.checkbox(
            f"Highlight top 3 average {selected_environmental} EPDs", value=current_env
        )
        new_lc = st.checkbox(
            f"Highlight top 3 average {selected_lifecycle} EPDs", value=current_lc
        )

        # If user changed something, update session_state and rerun
        if (new_env != current_env) or (new_lc != current_lc):
            st.session_state["highlight_env"] = new_env
            st.session_state["highlight_lc"] = new_lc
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

# st.write("**SPARQL Query**:")
# st.code(dynamic_query, language="sparql")
