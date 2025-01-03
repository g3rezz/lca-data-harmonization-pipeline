from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama, OllamaEmbeddings
import json
import os

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
            "field_name_de": {
                "type": "string",
                "description": "The exact Field Name (de) from Schema B without additional information",
            },
        },
        "required": ["attribute", "match_type", "field_name_de"],
    },
}


def query_system(question, vectorstore_base_path):
    # Determine the schema type to filter by
    if "UUID" in question or "Version" in question:
        schema_filter = "EPD_DataSet"
    elif "PERE" in question or "FW" in question:
        schema_filter = "EPD_FlowDataSet"
    elif "Bezugsgroesse" in question or "Rohdichte" in question:
        schema_filter = "ILCD_FlowPropertyDataSet"
    else:
        schema_filter = "ILCD_LCIAMethodDataSet"

    # Construct the path to the appropriate vector store
    vectorstore_path = os.path.join(
        vectorstore_base_path, f"{schema_filter}_faiss_index"
    )

    # Load the vector store with deserialization permission
    embeddings = OllamaEmbeddings(model="bge-m3:latest")
    vectorstore = FAISS.load_local(
        vectorstore_path, embeddings=embeddings, allow_dangerous_deserialization=True
    )

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
        "field_name_de": "string (exact value of 'Field Name (de)' without any additional information)"
    }}
]
"""
    prompt = ChatPromptTemplate.from_template(RAG_TEMPLATE)

    # Retrieve documents with metadata filtering
    retriever = vectorstore.as_retriever()
    retrieved_docs = retriever.invoke(question)  # Pass the question as a plain string
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
    # question = """Match the following attributes from Dataset A: 'UUID'; 'Version'; 'Name (de)'; 'Name (en)'; to Schema B."""
    question = """Match the following attributes from Dataset A: 
    'GWP';'ODP';'POCP';'AP';'EP';'ADPE';'ADPF'; 
    to Schema B."""
    vectorstore_base_path = "embeddings"
    response = query_system(question, vectorstore_base_path)
    print("Response:\n", response)
