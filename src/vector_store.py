from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings


CHROMA_PATH = "chroma_db"
COLLECTION_NAME = "research_documents"


def get_embeddings():
    return OpenAIEmbeddings(model="text-embedding-3-small")


def create_vector_store(chunks):
    embeddings = get_embeddings()

    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_PATH,
        collection_name=COLLECTION_NAME
    )

    print("Vector store created successfully")

    return vector_store


def load_vector_store():
    embeddings = get_embeddings()

    vector_store = Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=embeddings,
        collection_name=COLLECTION_NAME
    )

    return vector_store


def add_documents_to_vector_store(chunks):
    vector_store = load_vector_store()
    vector_store.add_documents(chunks)

    print("Documents added to existing vector store")

    return vector_store