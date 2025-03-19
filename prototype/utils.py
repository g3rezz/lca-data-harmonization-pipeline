import streamlit as st
import pandas as pd
import numpy as np
from SPARQLWrapper import SPARQLWrapper, JSON
from typing import List, Optional, Union

# Your Fuseki endpoint:
ENDPOINT_URL = "http://localhost:3030/EPD_RDF/sparql"


def run_query(query: str):
    sparql = SPARQLWrapper(ENDPOINT_URL)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results


def display_results(results_json, highlight_gwp=False, highlight_penrt=False):
    """
    Displays the results in a dataframe:
    - We invert-minmax normalize GWP and PENRT, sort descending by the combined score.
    - We then reset the index to have final positions 0..N-1 in that sorted order.
    - Then we compute:
      * 3 rows closest to avg GWP (abs diff).
      * 3 rows closest to avg PENRT (abs diff).
      * 3 rows closest in Euclidean distance to (avg GWP, avg PENRT).
    - If highlight_gwp=True and highlight_penrt=True, we highlight the Euclidean set.
    - If only highlight_gwp=True, we highlight the GWP set.
    - If only highlight_penrt=True, we highlight the PENRT set.
    """
    display_table = True

    # 1) Convert SPARQL JSON "bindings" into a DataFrame
    bindings = results_json["results"]["bindings"]
    if not bindings:
        st.warning(
            "No table data. Please adjust filters in the sidebar and click 'Run Query'."
        )
        # Set to false when no results are available to hide checkboxes
        display_table = False
        return display_table
    var_names = results_json["head"]["vars"]

    table_rows = []
    for row in bindings:
        row_data = []
        for var in var_names:
            cell_value = row[var]["value"] if var in row else ""
            row_data.append(cell_value)
        table_rows.append(row_data)

    df = pd.DataFrame(table_rows, columns=var_names)

    # 2) If GWP & PENRT exist, do the normalization & sort
    if "GWP" in df.columns and "PENRT" in df.columns:
        df["GWP_float"] = pd.to_numeric(df["GWP"], errors="coerce")
        df["PENRT_float"] = pd.to_numeric(df["PENRT"], errors="coerce")

        # Inverted min-max => lower => better => higher normalized
        min_gwp, max_gwp = df["GWP_float"].min(), df["GWP_float"].max()
        if max_gwp != min_gwp:
            df["GWP_norm"] = (max_gwp - df["GWP_float"]) / (max_gwp - min_gwp)
        else:
            df["GWP_norm"] = 1.0

        min_penrt, max_penrt = df["PENRT_float"].min(), df["PENRT_float"].max()
        if max_penrt != min_penrt:
            df["PENRT_norm"] = (max_penrt - df["PENRT_float"]) / (max_penrt - min_penrt)
        else:
            df["PENRT_norm"] = 1.0

        df["NormalizedSum"] = ((df["GWP_norm"] + df["PENRT_norm"]) / 2).round(2)
        # Sort by normalized score (descending => best is top)
        df.sort_values("NormalizedSum", ascending=False, inplace=True)

    # 3) Reset to final arrangement with 0-based indices
    df.reset_index(drop=True, inplace=True)

    # 4) Create a "Rank" column from the normalized score
    def icon_from_score(score):
        if pd.isna(score):
            return ""
        if score >= 0.9:
            return "🟢🟢🟢🟢🟢"
        elif score >= 0.75:
            return "🟢🟢🟢🟢"
        elif score >= 0.5:
            return "🟢🟢🟢"
        elif score >= 0.25:
            return "🟢🟢"
        else:
            return "🟢"

    if "NormalizedSum" in df.columns:
        df["Rank"] = df["NormalizedSum"].apply(icon_from_score)

    # 5) Compute average GWP, PENRT and find the top-3 closest
    #    using the final arrangement (0-based).
    closest_gwp_indices = []
    closest_penrt_indices = []
    closest_euclid_indices = []
    if "GWP_float" in df.columns and "PENRT_float" in df.columns:
        avg_gwp = df["GWP_float"].mean()
        avg_penrt = df["PENRT_float"].mean()

        # Closest by GWP => sort by abs(GWP_float - avg_gwp)
        temp_gwp = df.assign(DistGWP=(df["GWP_float"] - avg_gwp).abs())
        temp_gwp.sort_values("DistGWP", inplace=True)
        closest_gwp_indices = temp_gwp.head(3).index.tolist()

        # Closest by PENRT => sort by abs(PENRT_float - avg_penrt)
        temp_pen = df.assign(DistPENRT=(df["PENRT_float"] - avg_penrt).abs())
        temp_pen.sort_values("DistPENRT", inplace=True)
        closest_penrt_indices = temp_pen.head(3).index.tolist()

        # Closest by Euclidian => sqrt((GWP - avg_gwp)^2 + (PENRT - avg_penrt)^2)
        temp_euc = df.assign(
            DistEuclid=np.sqrt(
                (df["GWP_float"] - avg_gwp) ** 2 + (df["PENRT_float"] - avg_penrt) ** 2
            )
        )
        temp_euc.sort_values("DistEuclid", inplace=True)
        closest_euclid_indices = temp_euc.head(3).index.tolist()

    # 6) Decide which set of rows to highlight
    #    If both toggles => Euclidian. If only GWP => GWP. If only PENRT => PENRT.
    highlight_indices = set()
    if highlight_gwp and highlight_penrt:
        highlight_indices = set(closest_euclid_indices)
    elif highlight_gwp:
        highlight_indices = set(closest_gwp_indices)
    elif highlight_penrt:
        highlight_indices = set(closest_penrt_indices)
    # else => no highlight

    # 7) Drop columns we no longer want to show
    for col_drop in [
        "GWP_float",
        "PENRT_float",
        "GWP_norm",
        "PENRT_norm",
        "NormalizedSum",
        # no Dist* columns in final; we used .assign(...) for them
    ]:
        if col_drop in df.columns:
            df.drop(columns=[col_drop], inplace=True)

    # 8) Convert final 0-based index to 1-based for display
    df.index = df.index + 1

    # 9) Build a row-based style function that checks if (row.name - 1) is in highlight_indices
    def highlight_rows(row):
        zero_based_idx = row.name - 1
        if zero_based_idx in highlight_indices:
            # #007acc with white text is fairly visible in both modes
            return ["background-color: #007acc; color: white"] * len(row)
        else:
            return [""] * len(row)

    # 10) Show the table with or without highlighting
    if highlight_indices:
        styler = df.style.apply(highlight_rows, axis=1)
        st.dataframe(
            styler,
            use_container_width=True,
            height=600,
            column_config={
                "Name": st.column_config.TextColumn("Name"),
                "DIN276CostGroupList": st.column_config.TextColumn("DIN 276 (CG)"),
                "GWP": st.column_config.NumberColumn("GWP", format="%.1f"),
                "PENRT": st.column_config.NumberColumn("PENRT", format="%.1f"),
                "Rank": st.column_config.TextColumn("Rank"),
            },
        )
    else:
        st.dataframe(
            df,
            use_container_width=True,
            height=600,
            column_config={
                "Name": st.column_config.TextColumn("Name"),
                "DIN276CostGroupList": st.column_config.TextColumn("DIN 276 (CG)"),
                "GWP": st.column_config.NumberColumn("GWP-total", format="%.1f"),
                "PENRT": st.column_config.NumberColumn("PENRT", format="%.1f"),
                "Rank": st.column_config.TextColumn("Rank"),
            },
        )

    # 7) Show averages in an info message below the table
    st.info(
        f"**Average GWP**: {avg_gwp:.1f}  |  **Average PENRT**: {avg_penrt:.1f}\n\n"
    )

    return display_table


def build_dynamic_query(
    modules: Optional[List[str]] = None,
    countries: Optional[List[str]] = None,
    subtypes: Optional[Union[List[str], str]] = None,
    str_groups: Optional[Union[List[str], str]] = None,
    density_groups: Optional[Union[List[str], str]] = None,
    din_groups: Optional[List[str]] = None,
    gwp_thr: int = 250,
    penrt_thr: int = 1000,
    scenario_recycled: bool = False,
    strict_din: bool = False,
) -> str:
    """
    Build a SPARQL query string based on the provided user inputs.

    For each filter parameter that is provided, a corresponding
    FILTER clause is generated. If a parameter is empty, its filter is omitted,
    ensuring that no empty filters are included in the final query.

    Parameters:
      modules (Optional[List[str]]):
          A list of module names used to filter the query. The filter is applied to both
          ?modGwp and ?modPen.
      countries (Optional[List[str]]):
          A list of country names used to filter the query, applied to ?country.
      subtypes (Optional[Union[List[str], str]]):
          Either a list of dataset subtype names or the string "All". When a list is provided,
          each subtype will have " dataset" appended to it and will be used to filter ?subType.
      str_groups (Optional[Union[List[str], str]]):
          Either a list of strength group identifiers or the string "All". When a list is provided,
          each value will have " Strength Concrete" appended to it and will be used to filter ?strengthGroup.
      din_groups (Optional[List[str]]):
          A list of DIN 276 cost group notations used to filter the query, applied to ?notation.
      gwp_thr (int):
          Threshold for Global Warming Potential (currently not integrated in filtering logic).
      penrt_thr (int):
          Threshold for PEN-related results (currently not integrated in filtering logic).
      scenario_recycled (bool):
          If True, adds an additional filter to only include scenarios where the value is "Recycled".

    Returns:
      str:
          A SPARQL query string that incorporates the provided filters.
    """

    # Modules Filter
    module_filter_gwp = ""
    module_filter_penrt = ""
    if modules:
        joined_modules = '","'.join(modules)
        module_filter_gwp = f'FILTER(?modGwp IN ("{joined_modules}"))'
        module_filter_penrt = f'FILTER(?modPen IN ("{joined_modules}"))'

    # Country Filter
    country_filter = ""
    if countries:
        joined = '","'.join(countries)
        country_filter = f'FILTER(?country IN ("{joined}"))'

    # Dataset Type Filter
    subtype_filter = ""
    if subtypes:
        joined_subtypes = '","'.join([f"{s} dataset" for s in subtypes])
        subtype_filter = f'FILTER(?subType IN ("{joined_subtypes}"))'

    # Concrete Strength Filter (e.g. compressive strength)
    str_filter = ""
    if str_groups:
        joined_str_groups = '","'.join([f"{s} Strength Concrete" for s in str_groups])
        str_filter = f'FILTER(?strengthGroup IN ("{joined_str_groups}"))'

    # Concrete Weight Filter (e.g. bulk/gross density)
    density_filter = ""
    if density_groups:
        joined_density_groups = '","'.join(
            [f"{s} Weight Concrete" for s in density_groups]
        )
        density_filter = f'FILTER(?densityGroup IN ("{joined_density_groups}"))'

    # DIN 276 Cost Group Filter
    din_filter = ""
    din_strict_count = ""
    if din_groups:
        joined = '","'.join(din_groups)
        din_filter = f'FILTER(?notation IN ("{joined}"))'
        if strict_din:
            din_groups_number = len(din_groups)
            din_strict_count = (
                f"&&\n  (COUNT(DISTINCT ?notation) = {din_groups_number})"
            )

    # Scenario Filter (Recycled)
    scenario_filter = ""
    if scenario_recycled:
        scenario_filter = """
    FILTER EXISTS {
      ?epd (ilcd:lciaResults|ilcd:exchanges) ?z1 .
      ?z1 (ilcd:LCIAResult|ilcd:exchange)   ?z2 .
      ?z2 (ilcd:otherLCIA|ilcd:otherEx)     ?z3 .
      ?z3 ilcd:anies ?z4 .
      ?z4 ilcd:scenario "Recycled" .
    }
    """

    # Final Query
    query = f"""
PREFIX ilcd: <https://example.org/ilcd/>
PREFIX din:  <https://example.org/din276/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX xsd:  <http://www.w3.org/2001/XMLSchema#>

SELECT
  ?Name
  (GROUP_CONCAT(DISTINCT ?notation ; separator=", ") AS ?DIN276CostGroupList)
  (COALESCE(?SumGWP_, 0.0)   AS ?GWP)
  (COALESCE(?SumPENRT_, 0.0) AS ?PENRT)
WHERE {{
  ##############################################################################
  # (1) EPD basic info & cost groups
  ##############################################################################
  ?epd a ilcd:ProcessDataSet ;
       ilcd:processInformation ?pInfo .
  
  ?pInfo ilcd:dataSetInformation ?dsi .
  ?dsi ilcd:dataSetName ?dsName .
  ?dsName ilcd:baseName ?baseName .
  ?baseName ilcd:value ?Name ;
            ilcd:lang "en" .

  # Country Filter
  ?pInfo ilcd:geography ?geo .
  ?geo ilcd:locationOfOperationSupplyOrProduction ?loc .
  ?loc ilcd:location ?country .
  {country_filter}

  # subType Filter
  ?epd ilcd:modellingAndValidation ?mVal .
  ?mVal ilcd:LCIMethodAndAllocation ?lciaMa .
  ?lciaMa ilcd:otherMAA ?maa .
  ?maa ilcd:anies ?subTypeNode .
  ?subTypeNode ilcd:name "subType" ;
               ilcd:value ?subType .
  {subtype_filter}

  # Compressive Strength & Grouping
  ?epd ilcd:exchanges ?exForStrength .
  ?exForStrength ilcd:exchange ?exchS .
  ?exchS ilcd:materialProperties ?mpS .
  ?mpS ilcd:name "compressive strength" ;
      ilcd:value ?strengthValStr .
  BIND(xsd:float(?strengthValStr) AS ?csVal)
  BIND(
    IF(?csVal < 25, "Low Strength Concrete",
      IF(?csVal <= 40, "Medium Strength Concrete", "High Strength Concrete")
    )
    AS ?strengthGroup
  )
  {str_filter}

  # Bulk Density & Grouping
  ?epd ilcd:exchanges ?exForDensity .
  ?exForDensity ilcd:exchange ?exchD .
  ?exchD ilcd:materialProperties ?mpD .
  ?mpD ilcd:name "gross density" ;
     ilcd:value ?densityValStr .
  BIND(xsd:float(?densityValStr) AS ?bdVal)
  BIND(
    IF(?bdVal < 2000, "Light Weight Concrete",
      IF(?bdVal <= 2600, "Normal Weight Concrete", "Heavy Weight Concrete")
    )
    AS ?densityGroup
  )
  {density_filter}

  # DIN 276 cost groups
  ?epd din:hasDIN276CostGroup ?cg .
  ?cg skos:notation ?notation .
  {din_filter}
 
  ##############################################################################
  # (2) Sub-SELECT for GWP
  ##############################################################################
  OPTIONAL {{
    {{
        SELECT
        ?epdGw
        (SUM(?valGwp) AS ?SumGWP)
        WHERE 
        {{
            ?epdGw a ilcd:ProcessDataSet ;
                    ilcd:lciaResults ?lr .
            ?lr ilcd:LCIAResult ?lciaRes .
            
            ?lciaRes ilcd:referenceToLCIAMethodDataSet ?methodDs .
            ?methodDs ilcd:shortDescription ?methodName .
            ?methodName ilcd:value "Global Warming Potential - total (GWP-total)" .
            
            ?lciaRes ilcd:otherLCIA ?oLCIA .
            ?oLCIA ilcd:anies ?mValG .
            ?mValG ilcd:module ?modGwp ;
                    ilcd:value ?valGwpStr .

            # Convert "ND" -> 0.0
            BIND(
                IF(?valGwpStr = "ND", 0.0, xsd:float(?valGwpStr))
                AS ?valGwp
            )

            {module_filter_gwp}
        }}
        GROUP BY ?epdGw
    }}
    FILTER(?epdGw = ?epd)
    BIND(?SumGWP AS ?SumGWP_)
  }}

  ##############################################################################
  # (3) Sub-SELECT for PENRT
  ##############################################################################
  OPTIONAL {{
    {{
        SELECT
        ?epdPen
        (SUM(?valPen) AS ?SumPENRT)
        WHERE 
        {{
            ?epdPen a ilcd:ProcessDataSet ;
                    ilcd:exchanges ?ex .
            ?ex ilcd:exchange ?exEntry .

            ?exEntry ilcd:referenceToFlowDataSet ?flowDs .
            ?flowDs ilcd:shortDescription ?flowName .
            ?flowName ilcd:value ?flowReg .
            FILTER(regex(?flowReg, "PENRT", "i"))

            ?exEntry ilcd:otherEx ?oEx .
            ?oEx ilcd:anies ?mValPen .
            ?mValPen ilcd:module ?modPen ;
                    ilcd:value ?valPenStr .

            BIND(
                IF(?valPenStr = "ND", 0.0, xsd:float(?valPenStr))
                AS ?valPen
            )

            {module_filter_penrt}
        }}
        GROUP BY ?epdPen
    }}
    FILTER(?epdPen = ?epd)
    BIND(?SumPENRT AS ?SumPENRT_)
  }}
  

  ##############################################################################
  # (4) Scenario Filter (Recycled)
  ##############################################################################
  {scenario_filter}
}}
GROUP BY ?Name ?SumGWP_ ?SumPENRT_
HAVING (
  COALESCE(?SumGWP_, 0.0) < {gwp_thr}
  &&
  COALESCE(?SumPENRT_, 0.0) < {penrt_thr}
  {din_strict_count}
)
"""
    return query
