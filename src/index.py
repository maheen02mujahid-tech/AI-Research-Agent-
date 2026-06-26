from dotenv import load_dotenv

from src.document_loader import load_and_split_all_pdfs
from src.vector_store import create_vector_store

load_dotenv()

chunks = load_and_split_all_pdfs("data")
create_vector_store(chunks)

print("\nFinished indexing all PDFs.")