import os
import pickle
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

DOCS_PATH = "data/docs"
INDEX_PATH = "vectorstore/faiss_index.bin"
META_PATH = "vectorstore/metadata.pkl"

model = SentenceTransformer("all-MiniLM-L6-v2")


def read_documents(folder):
    docs = []
    for file in os.listdir(folder):
        if file.endswith(".txt"):
            with open(os.path.join(folder, file), "r", encoding="utf-8") as f:
                docs.append((file, f.read()))
    return docs


def chunk_text(text, chunk_size=300):
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]


def build_index():
    documents = read_documents(DOCS_PATH)

    chunks = []
    metadata = []

    for filename, text in documents:
        text_chunks = chunk_text(text)
        for chunk in text_chunks:
            chunks.append(chunk)
            metadata.append({
                "source": filename,
                "text": chunk
            })

    embeddings = model.encode(chunks)
    embeddings = np.array(embeddings).astype("float32")

    os.makedirs("vectorstore", exist_ok=True)

    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

    faiss.write_index(index, INDEX_PATH)

    with open(META_PATH, "wb") as f:
        pickle.dump(metadata, f)

    print("Base vetorial criada com sucesso!")
    print(f"Documentos processados: {len(documents)}")
    print(f"Chunks gerados: {len(chunks)}")


if __name__ == "__main__":
    build_index()