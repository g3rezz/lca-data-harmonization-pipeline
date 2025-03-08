import streamlit as st

# Only set page config here, as the first command
st.set_page_config(page_title="My 2-Page App", page_icon="⚪", layout="wide")

# Create page objects:
# Use a single-character emoji or remove `icon` if you don't want icons.
query_page = st.Page("query_page.py", title="Queries", icon="🔍", default=True)
schema_page = st.Page("schema_page.py", title="Schema", icon="📐")

# Navigation
pages = [query_page, schema_page]
nav = st.navigation(pages)

# Run whichever page is selected
nav.run()
