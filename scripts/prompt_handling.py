from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama, OllamaEmbeddings
import json

# Define the JSON schema for structured output
json_schema = {
    "title": "AlignmentResponse",
    "description": "Response containing alignment mappings.",
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "attribute": {
                "type": "string",
                "description": "The attribute from dataset A",
            },
            "match_type": {
                "type": "string",
                "description": "The type of SKOS match",
                "enum": ["skos:exactMatch", "skos:closeMatch", "skos:relatedMatch"],
            },
            "field_name": {
                "type": "string",
                "description": "The exact Field Name (de) or Field Name (en) from Schema B without additional information",
            },
        },
        "required": ["attribute", "match_type", "field_name_de"],
    },
}


def determine_schema_filter(question):
    schema_keywords = {
        "EPD_DataSet": ["UUID", "Version", "Name"],
        "EPD_FlowDataSet": ["PERE", "FW", "RSF"],
        "ILCD_FlowPropertyDataSet": ["Bezugsgroesse", "Rohdichte", "Schichtdicke"],
        "ILCD_LCIAMethodDataSet": ["GWP", "ODP", "POCP"],
    }

    for schema_type, keywords in schema_keywords.items():
        if any(keyword in question for keyword in keywords):
            return schema_type

    return "EPD_DataSet"  # Default to EPD_DataSet if no match is found


def query_system(question, vectorstore_path, schema_filter=None):
    # Allow manual override of schema filter
    if not schema_filter:
        schema_filter = determine_schema_filter(question)

    # Load the single vector store
    embeddings = OllamaEmbeddings(model="bge-m3:latest")
    vectorstore = FAISS.load_local(
        vectorstore_path, embeddings=embeddings, allow_dangerous_deserialization=True
    )

    # Debugging: Check the total number of documents in the vector store
    all_docs = vectorstore.similarity_search("", k=1000)
    print(f"Total documents in vector store: {len(all_docs)}")

    # Define the prompt template
    RAG_TEMPLATE = """
You are an expert in semantic data alignment and ontology matching. Your task is to map the provided attributes from dataset A to their corresponding fields in Schema B. Use the SKOS relationship types to indicate the alignment:
- skos:exactMatch: Attributes are identical in meaning.
- skos:closeMatch: Attributes are strongly similar, differing only in minor details.
- skos:relatedMatch: Attributes are conceptually related but not hierarchically or equivalently aligned.

Attribute Schema B:
<context>
{context}
</context>

Answer the following question:
{question}

Return the response in JSON format adhering to the defined schema:
[
    {{
        "attribute": "string",
        "match_type": "string (one of 'skos:exactMatch', 'skos:closeMatch', 'skos:relatedMatch')",
        "field_name": "string (exact value of 'Field Name (de)' or 'Field Name (de)' without any additional information)"
    }}
]
"""
    prompt = ChatPromptTemplate.from_template(RAG_TEMPLATE)

    # Retrieve documents with metadata filtering
    retriever = vectorstore.as_retriever(
        search_kwargs={"filter": {"schema_type": schema_filter}}
    )
    print(f"Applying filter: schema_type={schema_filter}")
    retrieved_docs = retriever.invoke(question)

    # Ensure the retrieved_docs are valid
    if not retrieved_docs:
        print("No relevant documents found for the given query.")
        return None

    print(f"Number of documents retrieved: {len(retrieved_docs)}")
    context = "\n\n".join(doc.page_content for doc in retrieved_docs)

    # Generate the final prompt
    final_prompt = prompt.format_prompt(context=context, question=question).to_string()
    print("Final Prompt:\n", final_prompt)

    # Query the model with structured output
    model = ChatOllama(model="llama3.1:8b")
    structured_llm = model.with_structured_output(
        json_schema, method="json_schema", include_raw=True
    )
    raw_response = structured_llm.invoke(final_prompt)

    # Debugging: Print raw response
    print("Raw Response:\n", raw_response.get("raw", None))

    # Extract and return parsed structured response
    structured_response = raw_response.get("parsed", None)
    if structured_response is None:
        print("Parsing Error:", raw_response.get("parsing_error", None))
    else:
        print("Structured Response:", structured_response)
        # Save the structured response to a JSON file
        with open("data/response.json", "w") as json_file:
            json.dump(structured_response, json_file, indent=4)
            print("Response saved to data/response.json")
    return structured_response


if __name__ == "__main__":
    question = """Match the following attributes from Dataset A:

    Schuettdichte (kg/m3)
    Flaechengewicht (kg/m2)
    Rohdichte (kg/m3)
    Schichtdicke (m)
    Ergiebigkeit (m2)
    Laengengewicht (kg/m)
    Stueckgewicht (kg)
    Umrechungsfaktor auf 1kg
    biogener Kohlenstoffgehalt in kg
    biogener Kohlenstoffgehalt (Verpackung) in kg
    
    to Schema B."""
    vectorstore_path = "embeddings/faiss_index"
    response = query_system(
        question, vectorstore_path, schema_filter="ILCD_FlowPropertyDataSet"
    )
    print("Response:\n", response)
