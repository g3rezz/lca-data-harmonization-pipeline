import pandas as pd
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings


def load_and_store(csv_paths, vectorstore_path):
    documents = []

    # Process each CSV
    for csv_path in csv_paths:
        df = pd.read_csv(csv_path)

        # Check for required columns and handle missing columns gracefully
        required_columns = [
            "Field Name (de)",
            "Field Name (en)",
            "Element/Attribute Name",
            "Datatype",
            "Definition (de)",
            "Definition (en)",
            "Original ILCD Format Definition (en)",
        ]
        for column in required_columns:
            if column not in df.columns:
                print(
                    f"Warning: Missing column '{column}' in {csv_path}. Skipping this file."
                )
                continue

        # Add schema_type based on file name
        schema_type = csv_path.split("/")[-1].split(".")[0]

        for _, row in df.iterrows():
            content = (
                f"Field Name (de): {row.get('Field Name (de)', 'N/A')}\n"
                f"Field Name (en): {row.get('Field Name (en)', 'N/A')}\n"
                f"Element/Attribute Name: {row.get('Element/Attribute Name', 'N/A')}\n"
                f"Datatype: {row.get('Datatype', 'N/A')}\n"
                f"Definition (de): {row.get('Definition (de)', 'N/A')}\n"
                f"Definition (en): {row.get('Definition (en)', 'N/A')}\n"
                f"Original ILCD Format Definition (en): {row.get('Original ILCD Format Definition (en)', 'N/A')}\n"
            )
            documents.append(
                Document(
                    page_content=content.strip(),
                    metadata={"source": csv_path, "schema_type": schema_type},
                )
            )

    # Split into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=3000, chunk_overlap=0)
    all_splits = text_splitter.split_documents(documents)

    # Write the split chunks to a text file with metadata
    with open("data/chunks/all_chunks_output.txt", "w") as file:
        for i, chunk in enumerate(all_splits):
            file.write(f"Chunk {i+1}:\n")
            file.write(chunk.page_content + "\n")
            file.write("Metadata:\n")
            file.write(str(chunk.metadata) + "\n")
            file.write("-" * 50 + "\n")

    # Create and save FAISS vector store
    embeddings = OllamaEmbeddings(model="bge-m3:latest")
    vectorstore = FAISS.from_documents(all_splits, embedding=embeddings)
    vectorstore.save_local(vectorstore_path)
    print(f"Vector store saved to {vectorstore_path}")


if __name__ == "__main__":
    # Example usage with schema-specific CSV files
    csv_files = [
        "data/csv/EPD_DataSet.csv",
        "data/csv/EPD_FlowDataSet.csv",
        "data/csv/ILCD_FlowPropertyDataSet.csv",
        "data/csv/ILCD_LCIAMethodDataSet.csv",
    ]
    vectorstore_dir = "embeddings/faiss_index"
    load_and_store(csv_files, vectorstore_dir)
