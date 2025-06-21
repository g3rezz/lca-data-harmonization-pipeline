from SPARQLWrapper import SPARQLWrapper, JSON
import urllib.error

# Your Fuseki endpoint:
ENDPOINT_URL = "http://localhost:3030/EPD_RDF/sparql"


def run_query(query: str):
    try:
        sparql = SPARQLWrapper(ENDPOINT_URL)
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        return results
    except urllib.error.HTTPError as e:
        if e.code == 404:
            error_msg = (
                "Error: The SPARQL endpoint was not found. "
                "Please verify the endpoint URL and your network connection."
            )
            print(error_msg)
            # Optionally, raise a custom exception if you want to stop further processing:
            raise RuntimeError(error_msg) from e
        else:
            raise
    except Exception as e:
        error_msg = (
            "An error occurred while querying the SPARQL endpoint. "
            "Please try again later."
        )
        print(error_msg)
        raise RuntimeError(error_msg) from e
