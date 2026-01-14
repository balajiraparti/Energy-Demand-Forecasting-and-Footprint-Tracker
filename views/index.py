from pathlib import Path
from dotenv import load_dotenv
from langchain_community.document_loaders.csv_loader import CSVLoader

from langchain_text_splitters import RecursiveCharacterTextSplitter as rs
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
import os
load_dotenv()


# pdf_dir = Path(__file__).parent / "data"

# docs = []
# for pdf_file in pdf_dir.glob("*.pdf"):
#     loader = Py(pdf_file)
#     docs.extend(loader.load())
loader=CSVLoader("electricity_demand.csv")
text_splitter = rs(
    chunk_size=1000,
    chunk_overlap=400
)
docs=loader.load()
chunks = text_splitter.split_documents(docs)


embedding_model = OpenAIEmbeddings(model="text-embedding-3-large")

vector_store = QdrantVectorStore.from_documents(
    documents=chunks,
    embedding=embedding_model,
    url="http://localhost:6333",
    collection_name="dataset_collection"
)
