import streamlit as st
import pandas as pd
import numpy as np


def display_results(
    results_json,
    highlight_env=False,
    highlight_lc=False,
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
    - If highlight_env=True and highlight_lc=True, we highlight the Euclidean set.
    - If only highlight_env=True, we highlight the ENV set.
    - If only highlight_lc=True, we highlight the LC set.
    """
    display_table_bool = True
    avg_env = None
    avg_lc = None

    # Convert SPARQL JSON "bindings" into a DataFrame
    bindings = results_json["results"]["bindings"]
    if not bindings:
        st.warning(
            "No table data. Please adjust filters in the sidebar and click 'Run Query'.",
            icon="⚠️",
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

    def clean_url(url):
        # Split on "https://"
        parts = url.split("https://")
        # If there are at least two occurrences, parts[0] is empty (if the URL starts with it)
        # and parts[1] is the part we want to keep.
        if len(parts) >= 3:
            return "https://" + parts[1]
        else:
            return url

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
            min_env, max_env = df["ENV_float"].min(), df["ENV_float"].max()
            if max_env != min_env:
                df["ENV_norm"] = (max_env - df["ENV_float"]) / (max_env - min_env)
            else:
                df["ENV_norm"] = 1.0

            min_lc, max_lc = df["LC_float"].min(), df["LC_float"].max()
            if max_lc != min_lc:
                df["LC_norm"] = (max_lc - df["LC_float"]) / (max_lc - min_lc)
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
        closest_env_indices = []
        closest_lc_indices = []
        closest_euclid_indices = []
        if "ENV_float" in df.columns and "LC_float" in df.columns:
            avg_env = df["ENV_float"].mean()
            avg_lc = df["LC_float"].mean()

            # Closest by ENV => sort by abs(ENV_float - avg_env)
            temp_env = df.assign(DistENV=(df["ENV_float"] - avg_env).abs())
            temp_env.sort_values("DistENV", inplace=True)
            closest_env_indices = temp_env.head(3).index.tolist()

            # Closest by LC => sort by abs(LC_float - avg_lc)
            temp_pen = df.assign(DistLC=(df["LC_float"] - avg_lc).abs())
            temp_pen.sort_values("DistLC", inplace=True)
            closest_lc_indices = temp_pen.head(3).index.tolist()

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
        if highlight_env and highlight_lc:
            highlight_indices = set(closest_euclid_indices)
        elif highlight_env:
            highlight_indices = set(closest_env_indices)
        elif highlight_lc:
            highlight_indices = set(closest_lc_indices)
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
            "No BKI data available for the selected DIN 276 cost group(s). Please adjust filters and try again.",
            icon="⚠️",
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
