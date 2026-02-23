from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path

from app.ingest import load_documents
from app.chunking import fixed_chunk
from app.embeddings import embed_texts
from app.vector_store import VectorStore
from app.api import create_routes

# Resolve project root and data path safely (works even if you run from VS Code)
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"

docs = load_documents(str(DATA_DIR))
all_chunks = []
sources = []

for doc in docs:
    chunks = fixed_chunk(doc["text"])
    all_chunks.extend(chunks)
    sources.extend([doc["source"]] * len(chunks))

embeddings = embed_texts(all_chunks)
dimension = len(embeddings[0])

vector_store = VectorStore(dimension)
vector_store.add(embeddings, all_chunks, sources)

app = FastAPI(title="Document Intelligence System")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(create_routes(vector_store))