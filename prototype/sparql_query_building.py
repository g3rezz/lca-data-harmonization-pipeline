from typing import List, Optional, Union
import re


def build_main_query(
    category: Optional[str] = None,
    modules: Optional[List[str]] = None,
    countries: Optional[List[str]] = None,
    subtypes: Optional[Union[List[str], str]] = None,
    str_groups: Optional[Union[List[str], str]] = None,
    density_groups: Optional[Union[List[str], str]] = None,
    din_groups: Optional[List[str]] = None,
    environ_thr: int = 1000,
    lifecycle_thr: int = 5000,
    scenario_recycled: bool = False,
    strict_din: bool = False,
    query_mode: bool = False,
    environmental_indicator: str = None,
    lifecycle_indicator: str = None,
) -> str:
    """
    Build a SPARQL query string based on the provided user inputs.

    The function uses a suffix-based approach to generate filters for two
    separate subselect queries (subselect #1 with suffix="", and subselect #2
    with suffix="2"). Each filter function appends the suffix to its variable
    references, ensuring the second subselect can replicate the filter logic
    under distinct variable names (e.g. ?pInfo2, ?country2, etc.).

    Filters included:
      - Category (classification)
      - Modules (for ENV/Lifecycle modules)
      - Countries
      - Subtypes (e.g. 'specific dataset')
      - Strength (compressive strength)
      - Density
      - DIN 276 cost groups
      - Scenario filter (recycled)

    The function returns a SPARQL query with two subselects:
      1) retrieving the filtered EPD set (plus e.g. GWP & PENRT sums),
      2) computing the overall average (using the same filter logic, but
         suffixed variable references),
    plus a final calculation step for distance-squared. The query can
    be further customized by specifying environment/lifecycle thresholds
    and indicators.

    Parameters:
      category:
          Mandatory filter on a material category label
          (e.g. "ready mixed concrete").
      modules (Optional[List[str]]):
          A list of module names used to filter the query. The filter is
          applied to both ?modEnv / ?modLc in subselect #1, and
          ?modEnv2 / ?modLc2 in subselect #2.
      countries (Optional[List[str]]):
          A list of country codes used to filter the query. Each subselect
          references ?country (or ?country2) accordingly.
      subtypes:
          E.g. 'specific dataset' or 'average dataset' – appended with " dataset".
      str_groups:
          E.g. 'Medium Strength Concrete' – appended with " Strength Concrete".
      density_groups:
          E.g. 'Normal Weight Concrete' – appended with " Weight Concrete".
      din_groups:
          List of DIN 276 cost group notations used to filter the query,
          applied to ?notation and ?notation2. If 'strict_din' is True,
          also require an exact count of distinct notations.
      environ_thr (int):
          Threshold for GWP-like indicator in HAVING clause.
      lifecycle_thr (int):
          Threshold for PENRT-like indicator in HAVING clause.
      scenario_recycled (bool):
          If True, adds an additional filter to only include
          scenario "Recycled".
      strict_din (bool):
          If True, require that the distinct DIN cost groups
          match the length of 'din_groups'.
      query_mode (bool):
          If False, produce SPARQL query #1 logic. If True, produce
          SPARQL query #2 logic (with the average & distance steps).
      environmental_indicator (str):
          E.g. "GWP-total" for the environment measure.
      lifecycle_indicator (str):
          E.g. "PENRT" for the lifecycle measure.

    Returns:
      A fully constructed SPARQL query string, ensuring each filter
      is applied consistently in both subselect #1 and subselect #2.
    """

    # Define filters
    def build_category_filter(suffix: str, category: str) -> str:
        """
        Build a SPARQL FILTER clause for category filtering.

        Parameters:
        suffix: Suffix to append to variable names (e.g. "" or "2").
        category: The target category string (e.g., "ready mixed concrete"). Hyphens will be replaced with spaces.

        Returns:
        A SPARQL snippet that filters canonical category labels to match the given category (case-insensitive).
        """
        category = category.replace("-", " ")
        return f"""
    # -- Filter Category
    ?dsi{suffix} ilcd:classificationInformation ?ci{suffix} .
    ?ci{suffix} ilcd:classification ?class{suffix} .
    ?class{suffix} ilcd:classEntries ?entry{suffix} .
    ?entry{suffix} a ilcd:ClassificationEntry ;
            ilcd:value ?entryValue{suffix} ;
            obd:hasCanonicalCategory ?canon{suffix} .
    ?canon{suffix} skos:prefLabel ?canonLabel{suffix} .
    FILTER(lcase(str(?canonLabel{suffix})) = "{category}")
    """

    def build_country_filter(suffix: str, countries: list) -> str:
        """
        Build a SPARQL FILTER clause for country filtering.

        Parameters:
        suffix: Suffix to append to variable names (e.g. "" or "2").
        countries: List of country names or codes to filter on.

        Returns:
        A SPARQL snippet that filters the country variable against the provided list.
        """
        joined = '","'.join(countries)
        return f"""
    # -- Filter Country
    ?pInfo{suffix} ilcd:geography ?geo{suffix} .
    ?geo{suffix} ilcd:locationOfOperationSupplyOrProduction ?loc{suffix} .
    ?loc{suffix} ilcd:location ?country{suffix} .
    FILTER(?country{suffix} IN ("{joined}"))
    """

    def build_subtype_filter(suffix: str, subtypes: list) -> str:
        """
        Build a SPARQL FILTER clause for dataset subtype filtering.

        Parameters:
        suffix: Suffix to append to variable names (e.g. "" or "2").
        subtypes: List of dataset subtype strings; " dataset" is appended to each.

        Returns:
        A SPARQL snippet that filters the subtype variable to the provided values.
        """
        joined_subtypes = '","'.join([f"{s} dataset" for s in subtypes])
        return f"""
    # -- Filter dataset type (subType)
    ?epd ilcd:modellingAndValidation ?mVal{suffix} .
    ?mVal{suffix} ilcd:LCIMethodAndAllocation ?lciaMa{suffix} .
    ?lciaMa{suffix} ilcd:otherMAA ?maa{suffix} .
    ?maa{suffix} ilcd:anies ?subTypeNode{suffix} .
    ?subTypeNode{suffix} ilcd:name "subType" ;
                    ilcd:value ?subType{suffix} .
    FILTER(?subType{suffix} IN ("{joined_subtypes}"))
    """

    def build_str_filter(suffix: str, str_groups: list) -> str:
        """
        Build a SPARQL FILTER clause for compressive strength filtering.

        Parameters:
        suffix: Suffix to append to variable names (e.g. "" or "2").
        str_groups: List of strength group identifiers; " Strength Concrete" is appended to each.

        Returns:
        A SPARQL snippet that filters the computed strength group to the provided values.
        """
        joined_str_groups = '","'.join([f"{s} Strength Concrete" for s in str_groups])
        return f"""
    # -- Filter Compressive Strength & Grouping
    ?epd ilcd:exchanges ?exForStrength{suffix} .
    ?exForStrength{suffix} ilcd:exchange ?exchS{suffix} .
    ?exchS{suffix} ilcd:materialProperties ?mpS{suffix} .
    ?mpS{suffix} ilcd:name "compressive strength" ;
            ilcd:value ?strengthValStr{suffix} .
    BIND(xsd:float(?strengthValStr{suffix}) AS ?csVal{suffix})
    BIND(
        IF(?csVal{suffix} < 25, "Low Strength Concrete",
        IF(?csVal{suffix} <= 40, "Medium Strength Concrete", "High Strength Concrete")
        )
        AS ?strengthGroup{suffix}
    )
    FILTER(?strengthGroup{suffix} IN ("{joined_str_groups}"))
    """

    def build_density_filter(suffix: str, density_groups: list) -> str:
        """
        Build a SPARQL FILTER clause for bulk density filtering.

        Parameters:
        suffix: Suffix to append to variable names (e.g. "" or "2").
        density_groups: List of density group identifiers; " Weight Concrete" is appended to each.

        Returns:
        A SPARQL snippet that filters the computed density group to the provided values.
        """
        joined_density_groups = '","'.join(
            [f"{s} Weight Concrete" for s in density_groups]
        )
        return f"""
    # -- Filter Bulk Density & Grouping
    ?epd ilcd:exchanges ?exForDensity{suffix} .
    ?exForDensity{suffix} ilcd:exchange ?exchD{suffix} .
    ?exchD{suffix} ilcd:materialProperties ?mpD{suffix} .
    ?mpD{suffix} ilcd:name "gross density" ;
            ilcd:value ?densityValStr{suffix} .
    BIND(xsd:float(?densityValStr{suffix}) AS ?bdVal{suffix})
    BIND(
        IF(?bdVal{suffix} < 2000, "Light Weight Concrete",
        IF(?bdVal{suffix} <= 2600, "Normal Weight Concrete", "Heavy Weight Concrete")
        )
        AS ?densityGroup{suffix}
    )
    FILTER(?densityGroup{suffix} IN ("{joined_density_groups}"))
    """

    def build_din_filter(
        suffix: str, din_groups: list, strict_din: bool = False
    ) -> tuple[str, str]:
        """
        Build a SPARQL FILTER clause for DIN 276 cost group filtering.

        Parameters:
        suffix: Suffix to append to variable names (e.g. "" or "2").
        din_groups: List of DIN 276 cost group notations.
        strict_din: If True, a strict count check snippet is generated for HAVING.

        Returns:
        A tuple (din_filter_code, din_strict_code) where:
        - din_filter_code is the SPARQL snippet filtering the DIN cost groups.
        - din_strict_code is a snippet to enforce a strict count (or empty if strict_din is False).
        """
        joined = '","'.join(din_groups)
        din_filter_code = f"""
    # -- Filter DIN 276 cost groups
    ?epd din:hasDIN276CostGroup ?cg{suffix} .
    ?cg{suffix} skos:notation ?notation{suffix} .
    FILTER(?notation{suffix} IN ("{joined}"))
        """
        din_groups_number = len(din_groups)
        din_strict_code = ""
        if strict_din:
            # Usually you'd do something like AND COUNT(DISTINCT ?notation{suffix}) = {din_groups_number}
            # in your HAVING clause. We'll just return that snippet:
            din_strict_code = (
                f"&&\n  (COUNT(DISTINCT ?notation{suffix}) = {din_groups_number})"
            )
        return (din_filter_code, din_strict_code)

    def build_scenario_filter(suffix: str) -> str:
        """
        Build a SPARQL FILTER clause for filtering scenarios to "Recycled".

        Parameters:
        suffix: Suffix to append to variable names (e.g. "" or "2").

        Returns:
        A SPARQL snippet using FILTER EXISTS that restricts results to scenarios with "Recycled".
        """
        return f"""
    # -- Filter scenario "Recycled"
    FILTER EXISTS {{
        ?epd (ilcd:lciaResults|ilcd:exchanges) ?resultExchange{suffix} .
        ?resultExchange{suffix} (ilcd:LCIAResult|ilcd:exchange) ?otherOtherEx{suffix} .
        ?otherOtherEx{suffix} (ilcd:otherLCIA|ilcd:otherEx) ?anies{suffix} .
        ?anies{suffix} ilcd:anies ?scenario{suffix} .
        ?scenario{suffix} ilcd:scenario "Recycled" .
    }}
    """

    def build_module_filters(
        suffix: str,
        mod_list: List[str],
        mod_type: str,
    ) -> str:
        """
        Build a SPARQL FILTER clause for module filtering.

        Parameters:
        suffix: Suffix to append to variable names (e.g. "" or "2").
        mod_list: List of module names.
        mod_type: "env" for ?modEnv or "lc" for ?modLc.

        Returns:
        A SPARQL snippet that filters the corresponding module variable.
        """
        if not mod_list:
            return ""
        joined_mods = '","'.join(mod_list)
        if mod_type == "env":
            return f"""
        FILTER(?modEnv{suffix} IN ("{joined_mods}"))
        """
        if mod_type == "lc":
            return f"""
        FILTER(?modLc{suffix} IN ("{joined_mods}"))
        """

    # Modules Filter
    module_filter_env = ""
    module_filter_lc = ""
    module_filter_env_2 = ""
    module_filter_lc_2 = ""
    if modules:
        module_filter_env = build_module_filters("", modules, "env")
        module_filter_lc = build_module_filters("", modules, "lc")
        module_filter_env_2 = build_module_filters("2", modules, "env")
        module_filter_lc_2 = build_module_filters("2", modules, "lc")

    # Build a list of filters
    filters_1 = []
    filters_2 = []
    din_strict_count = ""
    din_strict_count_2 = ""
    if category:
        filters_1.append(build_category_filter("", category))
        filters_2.append(build_category_filter("2", category))
    if countries:
        filters_1.append(build_country_filter("", countries))
        filters_2.append(build_country_filter("2", countries))
    if subtypes:
        filters_1.append(build_subtype_filter("", subtypes))
        filters_2.append(build_subtype_filter("2", subtypes))
    if str_groups:
        filters_1.append(build_str_filter("", str_groups))
        filters_2.append(build_str_filter("2", str_groups))
    if density_groups:
        filters_1.append(build_density_filter("", density_groups))
        filters_2.append(build_density_filter("2", density_groups))
    if scenario_recycled:
        filters_1.append(build_scenario_filter(""))
        filters_2.append(build_scenario_filter("2"))
    if din_groups:
        din_filter, din_strict_count = build_din_filter("", din_groups, strict_din)
        filters_1.append(din_filter)
        din_filter_2, din_strict_count_2 = build_din_filter("2", din_groups, strict_din)
        filters_2.append(din_filter_2)

    # Filter out any empty strings
    filters_1 = [f for f in filters_1 if f]
    filters_2 = [f for f in filters_2 if f]

    # Join the filters with a newline
    filters_1_section = "\n\n  ".join(filters_1)
    filters_2_section = "\n\n  ".join(filters_2)

    if not query_mode:

        # Build SPARLQ query #1 (e.g. SPARQL requiring Python logic)
        query = f"""
PREFIX ilcd: <https://example.org/ilcd/>
PREFIX obd: <https://example.org/obd/>
PREFIX din:  <https://example.org/din276/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX xsd:  <http://www.w3.org/2001/XMLSchema#>

SELECT
  (SAMPLE(?nameLit) AS ?Name)
  (GROUP_CONCAT(DISTINCT ?notation ; separator=", ") AS ?DIN276CostGroupList)
  (COALESCE(?SumENV_, 0.0) AS ?ENV)
  (COALESCE(?SumLC_, 0.0) AS ?LC)
  (SAMPLE(?resourceURLValue) AS ?resourceURL)
WHERE {{
  # (1) Get the filtered EPD set
  ?epd a ilcd:ProcessDataSet ;
       ilcd:processInformation ?pInfo ;
       ilcd:modellingAndValidation ?modVal .
  # -- Get Name
  ?pInfo ilcd:dataSetInformation ?dsi .
  ?dsi ilcd:dataSetName ?dsName .
  ?dsName ilcd:baseName ?baseName .
  ?baseName ilcd:value ?nameLit .
  # -- Get resourceURL     
  ?modVal ilcd:dataSourcesTreatmentAndRepresentativeness ?dst .
  ?dst ilcd:otherDSTAR ?dstarRoot .
  ?dstarRoot ilcd:aniesDSTAR ?dstarEntry .
  ?dstarEntry ilcd:name "referenceToOriginalEPD" ;
              ilcd:valueDSTAR ?dstarRef .
  ?dstarRef a ilcd:DSTARReference ;
              ilcd:resourceURLs ?resourceURLValue .
  {filters_1_section}
    
  # (2) Compute ENV per filtered EPD
  OPTIONAL {{
    {{
      SELECT ?epdEnv (SUM(DISTINCT ?valEnv) AS ?SumENV)
      WHERE 
      {{
      ?epdEnv a ilcd:ProcessDataSet ;
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
      {module_filter_env}
      }}
      GROUP BY ?epdEnv
    }}
    FILTER(?epdEnv = ?epd)
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
        {module_filter_lc}
      }}
      GROUP BY ?epdLc
    }}
    FILTER(?epdLc = ?epd)
    BIND(?SumLC AS ?SumLC_)
  }}
}}
GROUP BY ?Name ?SumENV_ ?SumLC_
HAVING (
  COALESCE(?SumENV_, 0.0) < {environ_thr}
  &&
  COALESCE(?SumLC_, 0.0) < {lifecycle_thr}
  {din_strict_count}
)
"""
    else:
        # Build SPARLQ query #2 (e.g. all-in-one SPARQL query)
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
           (SAMPLE(?resourceURLValue) AS ?resourceURL)
    WHERE {{
      # -- Get EPD name (English)
      ?epd a ilcd:ProcessDataSet ;
           ilcd:processInformation ?pInfo ;
           ilcd:modellingAndValidation ?modVal .
      # -- Get Name
      ?pInfo ilcd:dataSetInformation ?dsi .
      ?dsi ilcd:dataSetName ?dsName .
      ?dsName ilcd:baseName ?baseName .
      ?baseName ilcd:value ?nameLit .
      # -- Get resourceURL     
      ?modVal ilcd:dataSourcesTreatmentAndRepresentativeness ?dst .
      ?dst ilcd:otherDSTAR ?dstarRoot .
      ?dstarRoot ilcd:aniesDSTAR ?dstarEntry .
      ?dstarEntry ilcd:name "referenceToOriginalEPD" ;
                  ilcd:valueDSTAR ?dstarRef .
      ?dstarRef a ilcd:DSTARReference ;
                  ilcd:resourceURLs ?resourceURLValue .

      {filters_1_section}

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
        {module_filter_env}
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
        {module_filter_lc}
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
              ilcd:processInformation ?pInfo2 ;
              ilcd:modellingAndValidation ?modVal2 .
          # -- Get Name
          ?pInfo2 ilcd:dataSetInformation ?dsi2 .
          ?dsi2 ilcd:dataSetName ?dsName2 .
          ?dsName2 ilcd:baseName ?baseName2 .
          ?baseName2 ilcd:value ?nameLit2 .
          # -- Get resourceURL     
          ?modVal2 ilcd:dataSourcesTreatmentAndRepresentativeness ?dst2 .
          ?dst2 ilcd:otherDSTAR ?dstarRoot2 .
          ?dstarRoot2 ilcd:aniesDSTAR ?dstarEntry2 .
          ?dstarEntry2 ilcd:name "referenceToOriginalEPD" ;
                       ilcd:valueDSTAR ?dstarRef2 .
          ?dstarRef2 a ilcd:DSTARReference ;
                       ilcd:resourceURLs ?resourceURLValue2 .

          {filters_2_section}

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
            {module_filter_env_2}
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
            {module_filter_lc_2}
          }}
        }}
        GROUP BY ?epd
        HAVING (
          COALESCE(SUM(DISTINCT ?valEnv), 0.0) < {environ_thr} 
          &&
          COALESCE(SUM(DISTINCT ?valLc), 0.0) < {lifecycle_thr}
          {din_strict_count_2}
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


def build_bki_query(results_json: dict):
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
