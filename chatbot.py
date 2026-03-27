import pickle
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

INDEX_PATH = "vectorstore/faiss_index.bin"
META_PATH = "vectorstore/metadata.pkl"

model = SentenceTransformer("all-MiniLM-L6-v2")


def load_data():
    index = faiss.read_index(INDEX_PATH)
    with open(META_PATH, "rb") as f:
        metadata = pickle.load(f)
    return index, metadata


def search(question, top_k=2):
    index, metadata = load_data()

    question_embedding = model.encode([question])
    question_embedding = np.array(question_embedding).astype("float32")

    distances, indices = index.search(question_embedding, top_k)

    results = []
    for idx in indices[0]:
        results.append(metadata[idx])

    return results


def answer(question):
    results = search(question)

    response = f"Resposta para: {question}\n\n"

    for r in results:
        response += f"📄 Fonte: {r['source']}\n"
        response += f"{r['text']}\n\n"

    return response

if __name__ == "__main__":
    pergunta = "Como redefinir senha?"
    print(answer(pergunta))