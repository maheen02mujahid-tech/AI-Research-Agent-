from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


def load_and_split_pdf(pdf_path):
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()

    print(f"Loaded {len(documents)} pages from {pdf_path}")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = splitter.split_documents(documents)

    print(f"Created {len(chunks)} chunks from {pdf_path}")

    return chunks


def load_and_split_all_pdfs(data_folder="data"):
    all_chunks = []
    pdf_files = list(Path(data_folder).glob("*.pdf"))

    if not pdf_files:
        print("No PDF files found in data folder.")
        return []

    for pdf_file in pdf_files:
        chunks = load_and_split_pdf(str(pdf_file))
        all_chunks.extend(chunks)

    print(f"\nTotal PDFs loaded: {len(pdf_files)}")
    print(f"Total chunks created: {len(all_chunks)}")

    return all_chunks