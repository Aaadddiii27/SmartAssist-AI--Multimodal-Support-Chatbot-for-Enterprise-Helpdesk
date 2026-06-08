import os
import pickle

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from sentence_transformers import SentenceTransformer

import faiss


PDF_FOLDER = "data/pdfs"
VECTOR_FOLDER = "data/vector_db"

EMBED_MODEL = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


def load_pdf_documents():

    documents = []

    for file in os.listdir(PDF_FOLDER):

        if file.endswith(".pdf"):

            path = os.path.join(
                PDF_FOLDER,
                file
            )

            loader = PyPDFLoader(path)

            docs = loader.load()

            documents.extend(docs)

    return documents


def chunk_documents(documents):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    chunks = splitter.split_documents(
        documents
    )

    return chunks


def create_vector_store():

    documents = load_pdf_documents()

    chunks = chunk_documents(
        documents
    )

    chunk_data = []

    for chunk in chunks:

        source = os.path.basename(
            chunk.metadata.get(
            "source",
            "Unknown"
        )
    )

        page = chunk.metadata.get(
        "page",
        0
    ) + 1

        chunk_data.append({

        "text":
        chunk.page_content,

        "source":
        source,

        "page":
        page

    })

    texts = [
    chunk["text"]
    for chunk in chunk_data
]

    embeddings = EMBED_MODEL.encode(texts)

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(
        dimension
    )

    index.add(
        embeddings
    )

    faiss.write_index(
        index,
        f"{VECTOR_FOLDER}/faiss_index.bin"
    )

    with open(
        f"{VECTOR_FOLDER}/chunks.pkl",
        "wb"
    ) as f:

        pickle.dump(
            chunk_data,
            f
        )

    return len(texts)

def search_documents(
    query,
    top_k=3
):

    index = faiss.read_index(
        f"{VECTOR_FOLDER}/faiss_index.bin"
    )

    with open(
        f"{VECTOR_FOLDER}/chunks.pkl",
        "rb"
    ) as f:

        chunks = pickle.load(f)

    query_embedding = EMBED_MODEL.encode(
        [query]
    )

    distances, indices = index.search(
        query_embedding,
        top_k
    )

    results = []

    for idx in indices[0]:

        if idx < len(chunks):

            results.append(
                chunks[idx]
            )

    return results
def search_documents_with_scores(
    query,
    top_k=3
):

    index = faiss.read_index(
        f"{VECTOR_FOLDER}/faiss_index.bin"
    )

    with open(
        f"{VECTOR_FOLDER}/chunks.pkl",
        "rb"
    ) as f:

        chunks = pickle.load(f)

    query_embedding = EMBED_MODEL.encode(
        [query]
    )

    distances, indices = index.search(
        query_embedding,
        top_k
    )

    results = []

    for rank, idx in enumerate(indices[0]):

        if idx < len(chunks):

            item = chunks[idx].copy()

            item["distance"] = float(
                distances[0][rank]
            )

            results.append(item)

    return results