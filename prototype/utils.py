import streamlit as st
import pandas as pd
import numpy as np
from SPARQLWrapper import SPARQLWrapper, JSON
from typing import List, Optional, Union
import re

# Your Fuseki endpoint:
ENDPOINT_URL = "http://localhost:3030/EPD_RDF/sparql"


def run_query(query: str):
    sparql = SPARQLWrapper(ENDPOINT_URL)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results


def display_results(
    results_json, highlight_gwp=False, highlight_penrt=False, query_mode=False
):
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
    display_table_bool = True
    avg_gwp = None
    avg_penrt = None

    # Convert SPARQL JSON "bindings" into a DataFrame
    bindings = results_json["results"]["bindings"]
    if not bindings:
        st.warning(
            "No table data. Please adjust filters in the sidebar and click 'Run Query'."
        )
        # Set to false when no results are available to hide checkboxes
        display_table_bool = False
        return display_table_bool
    var_names = results_json["head"]["vars"]

    table_rows = []
    for row in bindings:
        row_data = []
        for var in var_names:
            cell_value = row[var]["value"] if var in row else ""
            row_data.append(cell_value)
        table_rows.append(row_data)

    df = pd.DataFrame(table_rows, columns=var_names)

    # Create a "Rank" column from the normalized score
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

    if not query_mode:
        # If GWP & PENRT exist, do the normalization & sort
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
                df["PENRT_norm"] = (max_penrt - df["PENRT_float"]) / (
                    max_penrt - min_penrt
                )
            else:
                df["PENRT_norm"] = 1.0

            df["NormalizedSum"] = ((df["GWP_norm"] + df["PENRT_norm"]) / 2).round(2)
            # Sort by normalized score (descending => best is top)
            df.sort_values("NormalizedSum", ascending=False, inplace=True)

        # Reset to final arrangement with 0-based indices
        df.reset_index(drop=True, inplace=True)

        if "NormalizedSum" in df.columns:
            df["Rank"] = df["NormalizedSum"].apply(icon_from_score)

        # Compute average GWP, PENRT and find the top-3 closest
        # using the final arrangement (0-based).
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
                    (df["GWP_float"] - avg_gwp) ** 2
                    + (df["PENRT_float"] - avg_penrt) ** 2
                )
            )
            temp_euc.sort_values("DistEuclid", inplace=True)
            closest_euclid_indices = temp_euc.head(3).index.tolist()

        # Decide which set of rows to highlight
        # If both toggles => Euclidian. If only GWP => GWP. If only PENRT => PENRT.
        highlight_indices = set()
        if highlight_gwp and highlight_penrt:
            highlight_indices = set(closest_euclid_indices)
        elif highlight_gwp:
            highlight_indices = set(closest_gwp_indices)
        elif highlight_penrt:
            highlight_indices = set(closest_penrt_indices)
        # else => no highlight

        # Drop columns we no longer want to show
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

        # Convert final 0-based index to 1-based for display
        df.index = df.index + 1

        # Build a row-based style function that checks if (row.name - 1) is in highlight_indices
        def highlight_rows(row):
            zero_based_idx = row.name - 1
            if zero_based_idx in highlight_indices:
                # #007acc with white text is fairly visible in both modes
                return ["background-color: #007acc; color: white"] * len(row)
            else:
                return [""] * len(row)

        # Show the table with or without highlighting
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

    else:
        df["avgGWP_float"] = pd.to_numeric(df["avgGWP"], errors="coerce")
        df["avgPENRT_float"] = pd.to_numeric(df["avgPENRT"], errors="coerce")
        avg_gwp = df["avgGWP_float"].mean()
        avg_penrt = df["avgPENRT_float"].mean()

        # Convert final 0-based index to 1-based for display
        df.index = df.index + 1

        df["distSquared_float"] = pd.to_numeric(df["distSquared"], errors="coerce")
        if "distSquared" in df.columns:
            df["Rank"] = df["distSquared_float"].apply(icon_from_score)

        # Drop columns we no longer want to show
        for col_drop in [
            "avgGWP",
            "avgPENRT",
            "distSquared",
            "avgGWP_float",
            "avgPENRT_float",
            "distSquared_float",
            "GWP_norm",
            "PENRT_norm",
            "NormalizedSum",
            # no Dist* columns in final; we used .assign(...) for them
        ]:
            if col_drop in df.columns:
                df.drop(columns=[col_drop], inplace=True)

        st.dataframe(
            df,
            use_container_width=True,
            height=600,
            column_config={
                "Name": st.column_config.TextColumn("Name"),
                "DIN276CostGroupList": st.column_config.TextColumn("DIN 276 (CG)"),
                "SumGWP": st.column_config.NumberColumn("GWP-total", format="%.1f"),
                "SumPENRT": st.column_config.NumberColumn("PENRT", format="%.1f"),
                "Rank": st.column_config.TextColumn("Rank"),
            },
        )

    # Show averages in an info message below the table
    if avg_gwp != None and avg_penrt != None:
        st.info(
            f"**Average GWP**: {avg_gwp:.1f}  |  **Average PENRT**: {avg_penrt:.1f}\n\n"
        )

    return display_table_bool


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
    query_mode: bool = False,
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
    module_filter_gwp2 = ""
    module_filter_penrt2 = ""
    if modules:
        joined_modules = '","'.join(modules)
        module_filter_gwp = f'FILTER(?modGwp IN ("{joined_modules}"))'
        module_filter_penrt = f'FILTER(?modPen IN ("{joined_modules}"))'
        module_filter_gwp2 = f'FILTER(?modGwp2 IN ("{joined_modules}"))'
        module_filter_penrt2 = f'FILTER(?modPen2 IN ("{joined_modules}"))'

    # Country Filter
    country_filter = ""
    if countries:
        joined = '","'.join(countries)
        country_filter = f"""
  # -- Filter Country
  ?pInfo ilcd:geography ?geo .
  ?geo ilcd:locationOfOperationSupplyOrProduction ?loc .
  ?loc ilcd:location ?country .
  FILTER(?country IN ("{joined}"))
  """

    # Dataset Type Filter
    subtype_filter = ""
    if subtypes:
        joined_subtypes = '","'.join([f"{s} dataset" for s in subtypes])
        subtype_filter = f"""
  # -- Filter dataset type (subType)
  ?epd ilcd:modellingAndValidation ?mVal .
  ?mVal ilcd:LCIMethodAndAllocation ?lciaMa .
  ?lciaMa ilcd:otherMAA ?maa .
  ?maa ilcd:anies ?subTypeNode .
  ?subTypeNode ilcd:name "subType" ;
               ilcd:value ?subType .
  FILTER(?subType IN ("{joined_subtypes}"))
  """

    # Concrete Strength Filter (e.g. compressive strength)
    str_filter = ""
    if str_groups:
        joined_str_groups = '","'.join([f"{s} Strength Concrete" for s in str_groups])
        str_filter = f"""
  # -- Filter Compressive Strength & Grouping
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
  FILTER(?strengthGroup IN ("{joined_str_groups}"))
  """

    # Concrete Weight Filter (e.g. bulk/gross density)
    density_filter = ""
    if density_groups:
        joined_density_groups = '","'.join(
            [f"{s} Weight Concrete" for s in density_groups]
        )
        density_filter = f"""
  # -- Filter Bulk Density & Grouping
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
  FILTER(?densityGroup IN ("{joined_density_groups}"))
  """

    # DIN 276 Cost Group Filter
    din_filter = ""
    din_strict_count = ""
    if din_groups:
        din_groups_number = len(din_groups)
        joined = '","'.join(din_groups)
        din_filter = f"""
  # -- Filter DIN 276 cost groups
  ?epd din:hasDIN276CostGroup ?cg .
  ?cg skos:notation ?notation .
  FILTER(?notation IN ("{joined}"))
  """
        if not query_mode:
            if strict_din:
                din_strict_count = (
                    f"&&\n  (COUNT(DISTINCT ?notation) = {din_groups_number})"
                )
        else:
            if strict_din:
                din_strict_count = (
                    f"&&\n  (COUNT(DISTINCT ?notation) = {din_groups_number})"
                )

    # Scenario Filter (Recycled)
    scenario_filter = ""
    if scenario_recycled:
        scenario_filter = """
    # -- Filter scenario "Recycled" 
    FILTER EXISTS {
      ?epd (ilcd:lciaResults|ilcd:exchanges) ?z1 .
      ?z1 (ilcd:LCIAResult|ilcd:exchange)   ?z2 .
      ?z2 (ilcd:otherLCIA|ilcd:otherEx)     ?z3 .
      ?z3 ilcd:anies ?z4 .
      ?z4 ilcd:scenario "Recycled" .
    }
    """

    # Build a list of filters
    filters = [
        country_filter.strip(),
        subtype_filter.strip(),
        str_filter.strip(),
        density_filter.strip(),
        scenario_filter.strip(),
        din_filter.strip(),
    ]

    # Filter out any empty strings
    filters = [f for f in filters if f]

    # Join the filters with a newline
    filters_section = "\n\n  ".join(filters)

    if not query_mode:

        # SPARQL + Python logic query
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
  # (1) Get the filtered EPD set
  ?epd a ilcd:ProcessDataSet ;
       ilcd:processInformation ?pInfo .
  ?pInfo ilcd:dataSetInformation ?dsi .
  ?dsi ilcd:dataSetName ?dsName .
  ?dsName ilcd:baseName ?baseName .
  ?baseName ilcd:value ?Name ;
            ilcd:lang "en" .
  {filters_section}
    
  # (2) Compute GWP per filtered EPD
  OPTIONAL {{
    {{
      SELECT ?epdGw (SUM(DISTINCT ?valGwp) AS ?SumGWP)
      WHERE 
      {{
      ?epdGw a ilcd:ProcessDataSet ;
              ilcd:lciaResults ?lr .
      ?lr ilcd:LCIAResult ?lciaRes .
      ?lciaRes ilcd:referenceToLCIAMethodDataSet ?methodDs .
      ?methodDs ilcd:shortDescription ?methodName .
      ?methodName ilcd:value ?methodReg .
      FILTER(regex(?methodReg, "(GWP-total)", "i"))
      ?lciaRes ilcd:otherLCIA ?oLCIA .
      ?oLCIA ilcd:anies ?mValG .
      ?mValG ilcd:module ?modGwp ;
              ilcd:value ?valGwpStr .
      BIND(IF(?valGwpStr = "ND", 0.0, xsd:float(?valGwpStr)) AS ?valGwp)
      {module_filter_gwp}
      }}
      GROUP BY ?epdGw
    }}
    FILTER(?epdGw = ?epd)
    BIND(?SumGWP AS ?SumGWP_)
  }}

  # (3) Compute PENRT per filtered EPD
  OPTIONAL {{
    {{
      SELECT ?epdPen (SUM(DISTINCT ?valPen) AS ?SumPENRT)
      WHERE 
      {{
        ?epdPen a ilcd:ProcessDataSet ;
                ilcd:exchanges ?ex .
        ?ex ilcd:exchange ?exEntry .
        ?exEntry ilcd:referenceToFlowDataSet ?flowDs .
        ?flowDs ilcd:shortDescription ?flowName .
        ?flowName ilcd:value ?flowReg .
        FILTER(regex(?flowReg, "(PENRT)", "i"))
        ?exEntry ilcd:otherEx ?oEx .
        ?oEx ilcd:anies ?mValPen .
        ?mValPen ilcd:module ?modPen ;
                ilcd:value ?valPenStr .
        BIND(IF(?valPenStr = "ND", 0.0, xsd:float(?valPenStr)) AS ?valPen)
        {module_filter_penrt}
      }}
      GROUP BY ?epdPen
    }}
    FILTER(?epdPen = ?epd)
    BIND(?SumPENRT AS ?SumPENRT_)
  }}
}}
GROUP BY ?Name ?SumGWP_ ?SumPENRT_
HAVING (
  COALESCE(?SumGWP_, 0.0) < {gwp_thr}
  &&
  COALESCE(?SumPENRT_, 0.0) < {penrt_thr}
  {din_strict_count}
)
"""
    else:
        # Semantic query
        query = f"""
PREFIX ilcd: <https://example.org/ilcd/>
PREFIX din:  <https://example.org/din276/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX xsd:  <http://www.w3.org/2001/XMLSchema#>

SELECT
  ?Name
  ?DIN276CostGroupList
  ?SumGWP
  ?SumPENRT
  ?avgGWP
  ?avgPENRT
  ?distSquared
WHERE {{
  # (1) Get the filtered EPD set with correct sums
  {{
    SELECT ?epd 
           (SAMPLE(?nameLit) AS ?Name)
           (GROUP_CONCAT(DISTINCT ?notation; separator=", ") AS ?DIN276CostGroupList)
           (SUM(DISTINCT ?valGwp) AS ?SumGWP)
           (SUM(DISTINCT ?valPen) AS ?SumPENRT)
    WHERE {{
      # -- Get EPD name (English)
      ?epd a ilcd:ProcessDataSet ;
           ilcd:processInformation ?pInfo .
      ?pInfo ilcd:dataSetInformation ?dsi .
      ?dsi ilcd:dataSetName ?dsName .
      ?dsName ilcd:baseName ?base .
      ?base ilcd:value ?nameLit ;
            ilcd:lang "en" .

      {filters_section}

      # -- GWP pattern
      OPTIONAL {{
        ?epd ilcd:lciaResults ?lr .
        ?lr ilcd:LCIAResult ?lciaRes .
        ?lciaRes ilcd:referenceToLCIAMethodDataSet ?methodDs .
        ?methodDs ilcd:shortDescription ?methodName .
        ?methodName ilcd:value ?methodReg .
        FILTER(regex(?methodReg, "(GWP-total)", "i"))
        ?lciaRes ilcd:otherLCIA ?oLCIA .
        ?oLCIA ilcd:anies ?mValG .
        ?mValG ilcd:module ?modGwp ;
              ilcd:value ?valGwpStr .
        BIND( IF(?valGwpStr = "ND", 0.0, xsd:float(?valGwpStr)) AS ?valGwp )
        {module_filter_gwp}
      }}

      # -- PENRT pattern
      OPTIONAL {{
        ?epd ilcd:exchanges ?ex .
        ?ex ilcd:exchange ?exEntry .
        ?exEntry ilcd:referenceToFlowDataSet ?flowDs .
        ?flowDs ilcd:shortDescription ?flowName .
        ?flowName ilcd:value ?flowReg .
        FILTER(regex(?flowReg, "(PENRT)", "i"))
        ?exEntry ilcd:otherEx ?oEx .
        ?oEx ilcd:anies ?mValPen .
        ?mValPen ilcd:module ?modPen ;
                ilcd:value ?valPenStr .
        BIND( IF(?valPenStr = "ND", 0.0, xsd:float(?valPenStr)) AS ?valPen )
        {module_filter_penrt}
      }}
    }}
    GROUP BY ?epd
    HAVING (
      COALESCE(SUM(DISTINCT ?valGwp), 0.0) < {gwp_thr} 
      &&
      COALESCE(SUM(DISTINCT ?valPen), 0.0) < {penrt_thr}
      {din_strict_count}
    )
  }}

  # (2) Compute overall average values over the SAME filtered set (by reusing  the identical filtering logic)
  {{
    SELECT
      (AVG(?sumGwp)  AS ?avgGWP)
      (AVG(?sumPen)  AS ?avgPENRT)
    WHERE {{
      {{
        SELECT ?epd (SUM(DISTINCT ?valGwp) AS ?sumGwp) (SUM(DISTINCT ?valPen) AS ?sumPen)
        WHERE {{
          # -- EPD name (English) again to ensure we match the same set
          ?epd a ilcd:ProcessDataSet ;
               ilcd:processInformation ?pInfo2 .
          ?pInfo2 ilcd:dataSetInformation ?dsi2 .
          ?dsi2 ilcd:dataSetName ?dsName2 .
          ?dsName2 ilcd:baseName ?base2 .
          ?base2 ilcd:value ?nameLit2 ;
                 ilcd:lang "en" .

          {filters_section}

          # -- GWP pattern
          OPTIONAL {{
            ?epd ilcd:lciaResults ?lr2 .
            ?lr2 ilcd:LCIAResult ?lciaRes2 .
            ?lciaRes2 ilcd:referenceToLCIAMethodDataSet ?methodDs2 .
            ?methodDs2 ilcd:shortDescription ?methodName2 .
            ?methodName2 ilcd:value ?methodReg2 .
            FILTER(regex(?methodReg2, "(GWP-total)", "i"))
            ?lciaRes2 ilcd:otherLCIA ?oLCIA2 .
            ?oLCIA2 ilcd:anies ?mValG2 .
            ?mValG2 ilcd:module ?modGwp2 ;
              ilcd:value ?valGwpStr2 .
            BIND( IF(?valGwpStr2 = "ND", 0.0, xsd:float(?valGwpStr2)) AS ?valGwp )
            {module_filter_gwp2}
          }}

          # -- PENRT pattern
          OPTIONAL {{
            ?epd ilcd:exchanges ?ex2 .
            ?ex2 ilcd:exchange ?exEntry2 .
            ?exEntry2 ilcd:referenceToFlowDataSet ?flowDs2 .
            ?flowDs2 ilcd:shortDescription ?flowName2 .
            ?flowName2 ilcd:value ?flowReg2 .
            FILTER(regex(?flowReg2, "(PENRT)", "i"))
            ?exEntry2 ilcd:otherEx ?oEx2 .
            ?oEx2 ilcd:anies ?mValPen2 .
            ?mValPen2 ilcd:module ?modPen2 ;
                ilcd:value ?valPenStr2 .
            BIND( IF(?valPenStr2 = "ND", 0.0, xsd:float(?valPenStr2)) AS ?valPen )
            {module_filter_penrt2}
          }}
        }}
        GROUP BY ?epd
        HAVING (
          COALESCE(SUM(DISTINCT ?valGwp), 0.0) < {gwp_thr} 
          &&
          COALESCE(SUM(DISTINCT ?valPen), 0.0) < {penrt_thr}
          {din_strict_count}
        )
      }}
    }}
  }}

  # (3) Compute the squared Euclidean distance using the overall averages
  BIND(
    (
      (COALESCE(?SumGWP, 0.0) - ?avgGWP) * (COALESCE(?SumGWP, 0.0) - ?avgGWP)
    + (COALESCE(?SumPENRT, 0.0) - ?avgPENRT) * (COALESCE(?SumPENRT, 0.0) - ?avgPENRT)
    )
    AS ?distSquared
  )
}}
ORDER BY ?distSquared
LIMIT 3
"""
    query = re.sub(r"\n\s*\n", "\n", query)
    return query


def run_cost_group_query(results_json: dict):
    """
    Extracts DIN276 cost groups from the provided JSON, builds a SPARQL query
    using those cost groups in a FILTER clause, and returns the query results.

    Parameters:
      results_json (dict): JSON dictionary containing the DIN276CostGroupList.
                           Expected format:
                           {
                             "DIN276CostGroupList": {
                               "type": "literal",
                               "value": "322, 330, 331"
                             }
                           }

    Returns:
      dict: The results of the SPARQL query in JSON format.
    """

    def extract_cost_groups(results_json: dict) -> list:
        """
        Extract unique DIN276 cost groups from all SPARQL result bindings.

        This function splits any comma-separated cost groups, builds a set of unique values,
        and returns a sorted list.

        Returns:
        list: A list of unique cost group strings.
        """
        cost_group_set = set()
        bindings = results_json.get("results", {}).get("bindings", [])
        for binding in bindings:
            if "DIN276CostGroupList" in binding:
                cost_groups_raw = binding["DIN276CostGroupList"].get("value", "")
                # Split by comma and add each trimmed value to the set.
                for group in cost_groups_raw.split(","):
                    group = group.strip()
                    if group:
                        cost_group_set.add(group)
        return sorted(cost_group_set)

    cost_groups = extract_cost_groups(results_json)

    # Build the FILTER clause if cost groups are provided.
    if cost_groups:
        # Create a comma-separated list of values enclosed in double quotes.
        joined = '","'.join(cost_groups)
        din_filter = f'FILTER(?notation IN ("{joined}"))'
    else:
        din_filter = ""

    # Build the SPARQL query string.
    bki_query = f"""
PREFIX bki: <https://example.org/bki#>
PREFIX din: <https://example.org/din276/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

SELECT ?notation ?name ?description ?layerName ?layerSize ?layerLife
WHERE {{
  ?element a bki:BKIElement ;
           bki:name ?name ;
           bki:description ?description ;
           din:hasDIN276CostGroup ?cg ;
           bki:hasLayer ?layer .
           
  ?cg skos:notation ?notation .
  
  ?layer a bki:Layer ;
         bki:processConfigName ?layerName .
  
  OPTIONAL {{ ?layer bki:lifeTime ?layerLife. }}
  OPTIONAL {{ ?layer bki:layerSize ?layerSize. }}

  {din_filter}
}}
ORDER BY ?name ?notation
"""
    # Run the query using the existing run_query() function.
    bki_query = re.sub(r"\n\s*\n", "\n", bki_query)
    return bki_query


def sparql_results_to_dataframe(results_json: dict) -> pd.DataFrame:
    """
    Convert SPARQL query JSON results to a pandas DataFrame with columns:
    element name, element description, layer name, layer size, layer lifetime, and cost group.

    Then, group the results by the element’s unique fields (name, description, notation)
    so that each element appears only once. The layer fields are aggregated into newline‐separated
    strings.

    Parameters:
      results_json (dict): SPARQL query JSON results.

    Returns:
      pd.DataFrame: A grouped DataFrame with one row per BKI element.
    """
    bindings = results_json.get("results", {}).get("bindings", [])
    if not bindings:
        st.warning(
            "No BKI data available for the selected DIN 276 cost group(s). Please adjust filters and try again."
        )
        return pd.DataFrame()

    var_names = results_json["head"]["vars"]
    table_rows = []
    for row in bindings:
        row_data = {}
        for var in var_names:
            row_data[var] = row[var]["value"] if var in row else ""
        table_rows.append(row_data)
    df = pd.DataFrame(table_rows)

    # Group the rows so each element (identified by name, description, notation) appears once.
    # The layer columns are aggregated (unique values joined by newline).
    if not df.empty:
        grouped_df = df.groupby(
            ["notation", "name", "description"], as_index=False
        ).agg(
            {
                "layerName": lambda x: ", ".join(sorted(set(x))),
                "layerSize": lambda x: ", ".join(sorted(set(x))),
                "layerLife": lambda x: ", ".join(sorted(set(x))),
            }
        )
    else:
        grouped_df = df

    # Display the grouped DataFrame using Streamlit's st.dataframe with custom column configuration.
    st.dataframe(
        grouped_df,
        use_container_width=True,
        height=300,
        column_config={
            "notation": st.column_config.TextColumn("DIN 276 (CG)"),
            "name": st.column_config.TextColumn("Name"),
            "description": st.column_config.TextColumn("Description"),
            "layerName": st.column_config.TextColumn("Layer Name(s)"),
            "layerSize": st.column_config.TextColumn("Layer Size(s)"),
            "layerLife": st.column_config.TextColumn("Layer Life(s)"),
        },
        hide_index=True,
    )

    return grouped_df
