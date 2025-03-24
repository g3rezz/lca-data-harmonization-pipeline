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


def clean_url(url):
    # Split on "https://"
    parts = url.split("https://")
    # If there are at least two occurrences, parts[0] is empty (if the URL starts with it)
    # and parts[1] is the part we want to keep.
    if len(parts) >= 3:
        return "https://" + parts[1]
    else:
        return url


def display_results(
    results_json,
    highlight_gwp=False,
    highlight_penrt=False,
    query_mode=False,
    selected_env="GWP-total",
    selected_lc="PENRT",
):
    """
    Displays the results in a dataframe:
    - We invert-minmax normalize ENV and LC, sort descending by the combined score.
    - We then reset the index to have final positions 0..N-1 in that sorted order.
    - Then we compute:
      * 3 rows closest to avg ENV (abs diff).
      * 3 rows closest to avg LC (abs diff).
      * 3 rows closest in Euclidean distance to (avg ENV, avg LC).
    - If highlight_gwp=True and highlight_penrt=True, we highlight the Euclidean set.
    - If only highlight_gwp=True, we highlight the ENV set.
    - If only highlight_penrt=True, we highlight the LC set.
    """
    display_table_bool = True
    avg_env = None
    avg_lc = None

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
    df["Name"] = df["Name"].str.strip()
    df["resourceURL"] = df["resourceURL"].apply(clean_url)

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
        # If ENV & LC exist, do the normalization & sort
        if "ENV" in df.columns and "LC" in df.columns:
            df["ENV_float"] = pd.to_numeric(df["ENV"], errors="coerce")
            df["LC_float"] = pd.to_numeric(df["LC"], errors="coerce")

            # Inverted min-max => lower => better => higher normalized
            min_gwp, max_gwp = df["ENV_float"].min(), df["ENV_float"].max()
            if max_gwp != min_gwp:
                df["ENV_norm"] = (max_gwp - df["ENV_float"]) / (max_gwp - min_gwp)
            else:
                df["ENV_norm"] = 1.0

            min_penrt, max_penrt = df["LC_float"].min(), df["LC_float"].max()
            if max_penrt != min_penrt:
                df["LC_norm"] = (max_penrt - df["LC_float"]) / (max_penrt - min_penrt)
            else:
                df["LC_norm"] = 1.0

            df["NormalizedSum"] = ((df["ENV_norm"] + df["LC_norm"]) / 2).round(2)
            # Sort by normalized score (descending => best is top)
            df.sort_values("NormalizedSum", ascending=False, inplace=True)

        # Reset to final arrangement with 0-based indices
        df.reset_index(drop=True, inplace=True)

        if "NormalizedSum" in df.columns:
            df["Rank"] = df["NormalizedSum"].apply(icon_from_score)

        # Put Rank before URL
        cols = list(df.columns)
        if "Rank" in cols and "resourceURL" in cols:
            # Remove 'Rank' from its current position
            cols.remove("Rank")
            # Find the index of 'resourceURL'
            resource_index = cols.index("resourceURL")
            # Insert 'Rank' before 'resourceURL'
            cols.insert(resource_index, "Rank")
            # Reassign the DataFrame with the new column order
            df = df[cols]

        # Compute average ENV, LC and find the top-3 closest
        # using the final arrangement (0-based).
        closest_gwp_indices = []
        closest_penrt_indices = []
        closest_euclid_indices = []
        if "ENV_float" in df.columns and "LC_float" in df.columns:
            avg_env = df["ENV_float"].mean()
            avg_lc = df["LC_float"].mean()

            # Closest by ENV => sort by abs(ENV_float - avg_env)
            temp_gwp = df.assign(DistENV=(df["ENV_float"] - avg_env).abs())
            temp_gwp.sort_values("DistENV", inplace=True)
            closest_gwp_indices = temp_gwp.head(3).index.tolist()

            # Closest by LC => sort by abs(LC_float - avg_lc)
            temp_pen = df.assign(DistLC=(df["LC_float"] - avg_lc).abs())
            temp_pen.sort_values("DistLC", inplace=True)
            closest_penrt_indices = temp_pen.head(3).index.tolist()

            # Closest by Euclidian => sqrt((ENV - avg_env)^2 + (LC - avg_lc)^2)
            temp_euc = df.assign(
                DistEuclid=np.sqrt(
                    (df["ENV_float"] - avg_env) ** 2 + (df["LC_float"] - avg_lc) ** 2
                )
            )
            temp_euc.sort_values("DistEuclid", inplace=True)
            closest_euclid_indices = temp_euc.head(3).index.tolist()

        # Decide which set of rows to highlight
        # If both toggles => Euclidian. If only ENV => ENV. If only LC => LC.
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
            "ENV_float",
            "LC_float",
            "ENV_norm",
            "LC_norm",
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
                    "ENV": st.column_config.NumberColumn(
                        f"{selected_env}", format="%.1f"
                    ),
                    "LC": st.column_config.NumberColumn(
                        f"{selected_lc}", format="%.1f"
                    ),
                    "Rank": st.column_config.TextColumn("Rank", width="small"),
                    "resourceURL": st.column_config.TextColumn("URL", width="small"),
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
                    "ENV": st.column_config.NumberColumn(
                        f"{selected_env}", format="%.1f"
                    ),
                    "LC": st.column_config.NumberColumn(
                        f"{selected_lc}", format="%.1f"
                    ),
                    "Rank": st.column_config.TextColumn("Rank", width="small"),
                    "resourceURL": st.column_config.TextColumn("URL", width="small"),
                },
            )

    else:
        df["avgENV_float"] = pd.to_numeric(df["avgENV"], errors="coerce")
        df["avgLC_float"] = pd.to_numeric(df["avgLC"], errors="coerce")
        avg_env = df["avgENV_float"].mean()
        avg_lc = df["avgLC_float"].mean()

        # Convert final 0-based index to 1-based for display
        df.index = df.index + 1

        # df["distSquared_float"] = pd.to_numeric(df["distSquared"], errors="coerce")
        # if "distSquared" in df.columns:
        #     df["Rank"] = df["distSquared_float"].apply(icon_from_score)

        # Drop columns we no longer want to show
        for col_drop in [
            "avgENV",
            "avgLC",
            "distSquared",
            "avgENV_float",
            "avgLC_float",
            "distSquared_float",
            "ENV_norm",
            "LC_norm",
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
                "SumENV": st.column_config.NumberColumn(
                    f"{selected_env}", format="%.1f"
                ),
                "SumLC": st.column_config.NumberColumn(f"{selected_lc}", format="%.1f"),
                "resourceURL": st.column_config.TextColumn("URL", width="small"),
            },
        )

    # Show averages in an info message below the table
    if avg_env != None and avg_lc != None:
        st.info(
            f"**Average {selected_env}**: {avg_env:.1f}  |  **Average {selected_lc}**: {avg_lc:.1f}\n\n"
        )

    return display_table_bool


def build_dynamic_query(
    category: Optional[str] = None,
    modules: Optional[List[str]] = None,
    countries: Optional[List[str]] = None,
    subtypes: Optional[Union[List[str], str]] = None,
    str_groups: Optional[Union[List[str], str]] = None,
    density_groups: Optional[Union[List[str], str]] = None,
    din_groups: Optional[List[str]] = None,
    environ_thr: int = 250,
    lifecycle_thr: int = 1000,
    scenario_recycled: bool = False,
    strict_din: bool = False,
    query_mode: bool = False,
    environmental_indicator: str = None,
    lifecycle_indicator: str = None,
) -> str:
    """
    Build a SPARQL query string based on the provided user inputs.

    For each filter parameter that is provided, a corresponding
    FILTER clause is generated. If a parameter is empty, its filter is omitted,
    ensuring that no empty filters are included in the final query.

    Parameters:
      modules (Optional[List[str]]):
          A list of module names used to filter the query. The filter is applied to both
          ?modEnv and ?modLc.
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
      environ_thr (int):
          Threshold for Global Warming Potential (currently not integrated in filtering logic).
      lifecycle_thr (int):
          Threshold for PEN-related results (currently not integrated in filtering logic).
      scenario_recycled (bool):
          If True, adds an additional filter to only include scenarios where the value is "Recycled".

    Returns:
      str:
          A SPARQL query string that incorporates the provided filters.
    """

    # Category Filter
    category_filter = ""
    if category:
        category = category.replace("-", " ")
        category_filter = f"""
  # -- Get classification information
  ?dsi ilcd:classificationInformation ?ci .
  ?ci ilcd:classification ?class .
  ?class ilcd:classEntries ?entry .
  ?entry a ilcd:ClassificationEntry ;
          ilcd:value ?entryValue ;
          obd:hasCanonicalCategory ?canon .  
  # --- Get canonical category label
  ?canon skos:prefLabel ?canonLabel .
  FILTER(lcase(str(?canonLabel)) = "{category}")
  """

    # Modules Filter
    module_filter_gwp = ""
    module_filter_penrt = ""
    module_filter_gwp2 = ""
    module_filter_penrt2 = ""
    if modules:
        joined_modules = '","'.join(modules)
        module_filter_gwp = f'FILTER(?modEnv IN ("{joined_modules}"))'
        module_filter_penrt = f'FILTER(?modLc IN ("{joined_modules}"))'
        module_filter_gwp2 = f'FILTER(?modEnv2 IN ("{joined_modules}"))'
        module_filter_penrt2 = f'FILTER(?modLc2 IN ("{joined_modules}"))'

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
        category_filter.strip(),
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
PREFIX obd: <https://example.org/obd/>
PREFIX din:  <https://example.org/din276/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX xsd:  <http://www.w3.org/2001/XMLSchema#>

SELECT
  ?Name
  (GROUP_CONCAT(DISTINCT ?notation ; separator=", ") AS ?DIN276CostGroupList)
  (COALESCE(?SumENV_, 0.0) AS ?ENV)
  (COALESCE(?SumLC_, 0.0) AS ?LC)
  ?resourceURL
WHERE {{
  # (1) Get the filtered EPD set
  ?epd a ilcd:ProcessDataSet ;
       ilcd:processInformation ?pInfo ;
       ilcd:modellingAndValidation ?modVal .
  # -- Get Name
  ?pInfo ilcd:dataSetInformation ?dsi .
  ?dsi ilcd:dataSetName ?dsName .
  ?dsName ilcd:baseName ?baseName .
  ?baseName ilcd:value ?Name ;
            ilcd:lang "en" .
  # -- Get resourceURL     
  ?modVal ilcd:dataSourcesTreatmentAndRepresentativeness ?dst .
  ?dst ilcd:otherDSTAR ?dstarRoot .
  ?dstarRoot ilcd:aniesDSTAR ?dstarEntry .
  ?dstarEntry ilcd:name "referenceToOriginalEPD" ;
              ilcd:valueDSTAR ?dstarRef .
  ?dstarRef a ilcd:DSTARReference ;
             ilcd:resourceURLs ?resourceURL .
  {filters_section}
    
  # (2) Compute ENV per filtered EPD
  OPTIONAL {{
    {{
      SELECT ?epdGw (SUM(DISTINCT ?valEnv) AS ?SumENV)
      WHERE 
      {{
      ?epdGw a ilcd:ProcessDataSet ;
              ilcd:lciaResults ?lr .
      ?lr ilcd:LCIAResult ?lciaRes .
      ?lciaRes ilcd:referenceToLCIAMethodDataSet ?methodDs .
      ?methodDs ilcd:shortDescription ?methodName .
      ?methodName ilcd:value ?methodReg .
      FILTER(regex(?methodReg, "({environmental_indicator})", "i"))
      ?lciaRes ilcd:otherLCIA ?oLCIA .
      ?oLCIA ilcd:anies ?mValG .
      ?mValG ilcd:module ?modEnv ;
              ilcd:value ?valEnvStr .
      BIND(IF(?valEnvStr = "ND", 0.0, xsd:float(?valEnvStr)) AS ?valEnv)
      {module_filter_gwp}
      }}
      GROUP BY ?epdGw
    }}
    FILTER(?epdGw = ?epd)
    BIND(?SumENV AS ?SumENV_)
  }}

  # (3) Compute LC per filtered EPD
  OPTIONAL {{
    {{
      SELECT ?epdLc (SUM(DISTINCT ?valLc) AS ?SumLC)
      WHERE 
      {{
        ?epdLc a ilcd:ProcessDataSet ;
                ilcd:exchanges ?ex .
        ?ex ilcd:exchange ?exEntry .
        ?exEntry ilcd:referenceToFlowDataSet ?flowDs .
        ?flowDs ilcd:shortDescription ?flowName .
        ?flowName ilcd:value ?flowReg .
        FILTER(regex(?flowReg, "({lifecycle_indicator})", "i"))
        ?exEntry ilcd:otherEx ?oEx .
        ?oEx ilcd:anies ?mValLc .
        ?mValLc ilcd:module ?modLc ;
                ilcd:value ?valLcStr .
        BIND(IF(?valLcStr = "ND", 0.0, xsd:float(?valLcStr)) AS ?valLc)
        {module_filter_penrt}
      }}
      GROUP BY ?epdLc
    }}
    FILTER(?epdLc = ?epd)
    BIND(?SumLC AS ?SumLC_)
  }}
}}
GROUP BY ?Name ?SumENV_ ?SumLC_ ?resourceURL
HAVING (
  COALESCE(?SumENV_, 0.0) < {environ_thr}
  &&
  COALESCE(?SumLC_, 0.0) < {lifecycle_thr}
  {din_strict_count}
)
"""
    else:
        # Semantic query
        query = f"""
PREFIX ilcd: <https://example.org/ilcd/>
PREFIX obd: <https://example.org/obd/>
PREFIX din:  <https://example.org/din276/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX xsd:  <http://www.w3.org/2001/XMLSchema#>

SELECT
  ?Name
  ?DIN276CostGroupList
  ?SumENV
  ?SumLC
  ?avgENV
  ?avgLC
  ?distSquared
  ?resourceURL
WHERE {{
  # (1) Get the filtered EPD set with sums
  {{
    SELECT ?epd 
           (SAMPLE(?nameLit) AS ?Name)
           (GROUP_CONCAT(DISTINCT ?notation; separator=", ") AS ?DIN276CostGroupList)
           (SUM(DISTINCT ?valEnv) AS ?SumENV)
           (SUM(DISTINCT ?valLc) AS ?SumLC)
           (SAMPLE(?resourceURLs) AS ?resourceURL)
    WHERE {{
      # -- Get EPD name (English)
      ?epd a ilcd:ProcessDataSet ;
           ilcd:processInformation ?pInfo ;
           ilcd:modellingAndValidation ?modVal .
      # -- Get Name
      ?pInfo ilcd:dataSetInformation ?dsi .
      ?dsi ilcd:dataSetName ?dsName .
      ?dsName ilcd:baseName ?baseName .
      ?baseName ilcd:value ?nameLit ;
                ilcd:lang "en" .
      # -- Get resourceURL     
      ?modVal ilcd:dataSourcesTreatmentAndRepresentativeness ?dst .
      ?dst ilcd:otherDSTAR ?dstarRoot .
      ?dstarRoot ilcd:aniesDSTAR ?dstarEntry .
      ?dstarEntry ilcd:name "referenceToOriginalEPD" ;
                  ilcd:valueDSTAR ?dstarRef .
      ?dstarRef a ilcd:DSTARReference ;
                ilcd:resourceURLs ?resourceURLs .

      {filters_section}

      # -- ENV pattern
      OPTIONAL {{
        ?epd ilcd:lciaResults ?lr .
        ?lr ilcd:LCIAResult ?lciaRes .
        ?lciaRes ilcd:referenceToLCIAMethodDataSet ?methodDs .
        ?methodDs ilcd:shortDescription ?methodName .
        ?methodName ilcd:value ?methodReg .
        FILTER(regex(?methodReg, "({environmental_indicator})", "i"))
        ?lciaRes ilcd:otherLCIA ?oLCIA .
        ?oLCIA ilcd:anies ?mValG .
        ?mValG ilcd:module ?modEnv ;
              ilcd:value ?valEnvStr .
        BIND( IF(?valEnvStr = "ND", 0.0, xsd:float(?valEnvStr)) AS ?valEnv )
        {module_filter_gwp}
      }}

      # -- LC pattern
      OPTIONAL {{
        ?epd ilcd:exchanges ?ex .
        ?ex ilcd:exchange ?exEntry .
        ?exEntry ilcd:referenceToFlowDataSet ?flowDs .
        ?flowDs ilcd:shortDescription ?flowName .
        ?flowName ilcd:value ?flowReg .
        FILTER(regex(?flowReg, "({lifecycle_indicator})", "i"))
        ?exEntry ilcd:otherEx ?oEx .
        ?oEx ilcd:anies ?mValLc .
        ?mValLc ilcd:module ?modLc ;
                ilcd:value ?valLcStr .
        BIND( IF(?valLcStr = "ND", 0.0, xsd:float(?valLcStr)) AS ?valLc )
        {module_filter_penrt}
      }}
    }}
    GROUP BY ?epd
    HAVING (
      COALESCE(SUM(DISTINCT ?valEnv), 0.0) < {environ_thr} 
      &&
      COALESCE(SUM(DISTINCT ?valLc), 0.0) < {lifecycle_thr}
      {din_strict_count}
    )
  }}

  # (2) Compute overall average values over the SAME filtered set (by reusing the filtering logic from (1))
  {{
    SELECT
      (AVG(?sumEnv)  AS ?avgENV)
      (AVG(?sumLc)  AS ?avgLC)
    WHERE {{
      {{
        SELECT ?epd (SUM(DISTINCT ?valEnv) AS ?sumEnv) (SUM(DISTINCT ?valLc) AS ?sumLc)
        WHERE {{
          # -- EPD name (English) again to ensure we match the same set          
          ?epd a ilcd:ProcessDataSet ;
              ilcd:processInformation ?pInfo2 .
          # -- Get Name
          ?pInfo2 ilcd:dataSetInformation ?dsi2 .
          ?dsi2 ilcd:dataSetName ?dsName2 .
          ?dsName2 ilcd:baseName ?baseName2 .
          ?baseName2 ilcd:value ?nameLit2 ;
                    ilcd:lang "en" .

          {filters_section}

          # -- ENV pattern
          OPTIONAL {{
            ?epd ilcd:lciaResults ?lr2 .
            ?lr2 ilcd:LCIAResult ?lciaRes2 .
            ?lciaRes2 ilcd:referenceToLCIAMethodDataSet ?methodDs2 .
            ?methodDs2 ilcd:shortDescription ?methodName2 .
            ?methodName2 ilcd:value ?methodReg2 .
            FILTER(regex(?methodReg2, "({environmental_indicator})", "i"))
            ?lciaRes2 ilcd:otherLCIA ?oLCIA2 .
            ?oLCIA2 ilcd:anies ?mValG2 .
            ?mValG2 ilcd:module ?modEnv2 ;
              ilcd:value ?valEnvStr2 .
            BIND( IF(?valEnvStr2 = "ND", 0.0, xsd:float(?valEnvStr2)) AS ?valEnv )
            {module_filter_gwp2}
          }}

          # -- LC pattern
          OPTIONAL {{
            ?epd ilcd:exchanges ?ex2 .
            ?ex2 ilcd:exchange ?exEntry2 .
            ?exEntry2 ilcd:referenceToFlowDataSet ?flowDs2 .
            ?flowDs2 ilcd:shortDescription ?flowName2 .
            ?flowName2 ilcd:value ?flowReg2 .
            FILTER(regex(?flowReg2, "({lifecycle_indicator})", "i"))
            ?exEntry2 ilcd:otherEx ?oEx2 .
            ?oEx2 ilcd:anies ?mValLc2 .
            ?mValLc2 ilcd:module ?modLc2 ;
                ilcd:value ?valLcStr2 .
            BIND( IF(?valLcStr2 = "ND", 0.0, xsd:float(?valLcStr2)) AS ?valLc )
            {module_filter_penrt2}
          }}
        }}
        GROUP BY ?epd
        HAVING (
          COALESCE(SUM(DISTINCT ?valEnv), 0.0) < {environ_thr} 
          &&
          COALESCE(SUM(DISTINCT ?valLc), 0.0) < {lifecycle_thr}
          {din_strict_count}
        )
      }}
    }}
  }}

  # (3) Compute the squared Euclidean distance using the overall averages
  BIND(
    (
      (COALESCE(?SumENV, 0.0) - ?avgENV) * (COALESCE(?SumENV, 0.0) - ?avgENV)
    + (COALESCE(?SumLC, 0.0) - ?avgLC) * (COALESCE(?SumLC, 0.0) - ?avgLC)
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
PREFIX bki: <https://example.org/bki/>
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
