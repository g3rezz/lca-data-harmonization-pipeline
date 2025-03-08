from pyvis.network import Network
from streamlit_theme import st_theme


def create_network(results_json, query_name, height):
    """
    Create a pyvis network graph based on query results.
    Sets the font color dynamically based on the active theme.
    """
    # Retrieve active theme, fallback to light if None.
    theme = st_theme() or {"base": "light"}
    base_theme = theme.get("base", "light").lower()

    # Set dynamic colors
    bg_color = "#0E1117" if base_theme == "dark" else "#ffffff"
    font_color = "white" if base_theme == "dark" else "black"

    height = str(height) + "px"

    # Create the network with dynamic font_color
    net = Network(
        height=height,
        neighborhood_highlight=True,
        directed=True,
        notebook=False,
        cdn_resources="in_line",
        bgcolor=bg_color,
        font_color=font_color,
    )

    net.repulsion(
        node_distance=300,  # Increase if you want more separation.
        central_gravity=0.01,  # Lower gravity for a softer pull to center.
        spring_length=250,  # A longer spring length gives more room.
        spring_strength=0.01,  # Lower strength for gentler edge forces.
        damping=0.9,  # Increase damping for slower, more fluid motion.
    )

    # Process query bindings (example logic)
    bindings = results_json["results"]["bindings"]
    if query_name == "Query 1":
        for row in bindings:
            product = row.get("Product", {}).get("value")
            category = row.get("Category", {}).get("value")
            database = row.get("Database", {}).get("value")
            if product:
                net.add_node(product, label=product, color="lightblue")
            if category:
                net.add_node(category, label=category, color="lightgreen")
            if database:
                net.add_node(database, label=database, color="lightcoral")
            if product and category:
                net.add_edge(product, category)
            if product and database:
                net.add_edge(product, database)
    elif query_name == "Query 2":
        for row in bindings:
            product = row.get("name", {}).get("value")
            score = row.get("lciaSumRounded", {}).get("value")
            unit = row.get("unit", {}).get("value")
            if product:
                net.add_node(product, label=product, color="lightblue")
            if score:
                score_label = f"Score: {score}"
                net.add_node(score_label, label=score_label, color="lightgreen")
            if unit:
                unit_label = f"Unit: {unit}"
                net.add_node(unit_label, label=unit_label, color="lightcoral")
            if product and score:
                net.add_edge(product, score_label)
            if product and unit:
                net.add_edge(product, unit_label)
    else:
        for row in bindings:
            subject = row.get("sub", {}).get("value")
            object_ = row.get("obj", {}).get("value")
            if subject:
                net.add_node(subject, label=subject)
            if object_:
                net.add_node(object_, label=object_)
            if subject and object_:
                net.add_edge(subject, object_)

    # Generate HTML output.
    html_content = net.generate_html()
    with open("graph.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    with open("graph.html", "r", encoding="utf-8") as f:
        html_content = f.read()

    # Remove unwanted CSS and center the graph.
    html_content = html_content.replace("border: 1px solid lightgray;", "")
    # html_content = html_content.replace("float: left;", "")
    # html_content = html_content.replace("#mynetwork {", "#mynetwork { margin: 0 auto; ")

    # Inject a call to network.fit() right after the graph is drawn.
    # This assumes the template contains "drawGraph();"
    # html_content = html_content.replace("drawGraph();", "drawGraph(); network.fit();")

    # Inject JavaScript to reload the iframe when it becomes visible.
    # Inject an IntersectionObserver to call network.fit() when #mynetwork becomes visible.
    observer_injection = """
    <script>
    (function() {
        const target = document.getElementById('mynetwork');
        if (target && typeof network !== 'undefined') {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
            if(entry.isIntersecting) {
                drawGraph();
                network.fit();
            }
            });
        }, { threshold: 0.5 });
        observer.observe(target);
        }
    })();
    </script>
    """
    html_content = html_content.replace("</body>", observer_injection + "\n</body>")

    injection = f"""
    <style>
    html, body {{
        margin: 0 !important;
        padding: 0 !important;
        background-color: {bg_color} !important;
    }}
    #mynetwork {{
        margin: 0 auto !important;
        display: block !important;
    }}
    /* Remove Bootstrap card styling around the graph */
    .card, .card-body {{
        border: none !important;
        box-shadow: none !important;
        background: transparent !important;
    }}
    </style>
    """
    html_content = html_content.replace("<head>", f"<head>{injection}")

    # Also call network.fit() after drawing the graph.
    html_content = html_content.replace("drawGraph();", "drawGraph(); network.fit();")

    return html_content
