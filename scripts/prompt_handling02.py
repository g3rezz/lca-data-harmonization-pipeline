import json
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama, OllamaEmbeddings

# Define attribute-schema mapping
attribute_schema_mapping = {
    "EPD_DataSet": [
        "UUID",
        "Version",
        "Name (de)",
        "Name (en)",
        "Kategorie (original)",
        "Kategorie (en)",
        "Konformität",
        "Laenderkennung",
        "Typ",
        "Referenzjahr",
        "Gueltig bis",
        "URL",
        "Declaration owner",
        "Veroeffentlicht am",
        "Registrierungsnummer",
        "Registrierungsstelle",
        "UUID des Vorgängers",
        "Version des Vorgängers",
        "URL des Vorgängers",
    ],
    "EPD_FlowDataSet": [
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
    ],
    "ILCD_FlowPropertyDataSet": [
        "Bezugsgroesse",
        "Bezugseinheit",
        "Referenzfluss-UUID",
        "Referenzfluss-Name",
        "Schuettdichte (kg/m3)",
        "Flaechengewicht (kg/m2)",
        "Rohdichte (kg/m3)",
        "Schichtdicke (m)",
        "Ergiebigkeit (m2)",
        "Laengengewicht (kg/m)",
        "Stueckgewicht (kg)",
        "Umrechungsfaktor auf 1kg",
        "biogener Kohlenstoffgehalt in kg",
        "biogener Kohlenstoffgehalt (Verpackung) in kg",
    ],
    "ILCD_LCIAMethodDataSet": [
        "GWP",
        "ODP",
        "POCP",
        "AP",
        "EP",
        "ADPE",
        "ADPF",
        "AP (A2)",
        "GWPtotal (A2)",
        "GWPbiogenic (A2)",
        "GWPfossil (A2)",
        "GWPluluc (A2)",
        "ETPfw (A2)",
        "PM (A2)",
        "EPmarine (A2)",
        "EPfreshwater (A2)",
        "EPterrestrial (A2)",
        "HTPc (A2)",
        "HTPnc (A2)",
        "IRP (A2)",
        "SOP (A2)",
        "ODP (A2)",
        "POCP (A2)",
        "ADPF (A2)",
        "ADPE (A2)",
        "WDP (A2)",
    ],
}

# Define JSON schema
json_schema = {
    "title": "AlignmentResponse",
    "description": "Response containing alignment mappings.",
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "attribute": {
                "type": "string",
                "description": "The attribute from dataset A without additional information",
            },
            "match_type": {
                "type": "string",
                "description": "The type of SKOS match",
                "enum": ["skos:exactMatch", "skos:closeMatch", "skos:relatedMatch"],
            },
            "field_name": {
                "type": "string",
                "description": "The exact Field Name (en) from Schema B without additional information",
            },
        },
        "required": ["attribute", "match_type", "field_name"],
    },
}


def query_system(attributes, vectorstore_path, schema_filter):
    embeddings = OllamaEmbeddings(model="bge-m3:latest")
    vectorstore = FAISS.load_local(
        vectorstore_path, embeddings=embeddings, allow_dangerous_deserialization=True
    )

    retriever = vectorstore.as_retriever(
        search_kwargs={"filter": {"schema_type": schema_filter}, "k": len(attributes)}
    )
    retrieved_docs = retriever.invoke("\n".join(attributes))

    print(f"Number of attributes: {len(attributes)}")

    num_retrieved_docs = len(retrieved_docs)
    print(f"Number of retrieved documents: {num_retrieved_docs}")

    if not retrieved_docs:
        return None

    context = "\n\n".join(doc.page_content for doc in retrieved_docs)

    prompt_template = ChatPromptTemplate.from_template(
        """
You are an expert in semantic data alignment and ontology matching. Your task is to map the provided attributes from dataset A to their corresponding fields in Schema B. Use the SKOS relationship types to indicate the alignment:
- skos:exactMatch: Attributes are identical in meaning.
- skos:closeMatch: Attributes are strongly similar, differing only in minor details.
- skos:relatedMatch: Attributes are conceptually related but not hierarchically or equivalently aligned.

Attribute Schema B:
<context>
{context}
</context>

Match the following attributes to Schema B:
<attributes>
{attributes}
</attributes>
Return the response in JSON format adhering to the defined schema.
"""
    )

    final_prompt = prompt_template.format_prompt(
        context=context, attributes="\n".join(attributes)
    ).to_string()

    with open("data/prompts/prompts_ollama.txt", "a") as prompt_file:
        prompt_file.write(final_prompt + "\n\n" + ("-" * 50) + "\n\n")

    print(final_prompt)

    model = ChatOllama(model="llama3.1:8b")
    structured_llm = model.with_structured_output(
        json_schema, method="json_schema", include_raw=True
    )
    raw_response = structured_llm.invoke(final_prompt)

    structured_response = raw_response.get("parsed", None)

    print(structured_response)
    print("-" * 50 + "\n")

    return structured_response


if __name__ == "__main__":
    vectorstore_path = "embeddings/bge-m3_faiss_index"
    output_file = "data/responses/response_ollama.json"

    # Reset the JSON file
    with open(output_file, "w") as file:
        json.dump([], file)

    # Reset the prompts text file
    with open("data/prompts/prompts_ollama.txt", "w") as prompt_file:
        prompt_file.write("")

    all_responses = []

    for schema, attributes in attribute_schema_mapping.items():
        response = query_system(attributes, vectorstore_path, schema)
        if response:
            all_responses.extend(response)

    with open(output_file, "w") as file:
        json.dump(all_responses, file, indent=2)

    print(f"All responses saved to {output_file}")
