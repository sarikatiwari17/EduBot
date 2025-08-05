import chromadb
from chromadb.utils import embedding_functions
from sentence_transformers import SentenceTransformer
import requests

# Setup ChromaDB client and collections
chroma_client = chromadb.PersistentClient(path="../rag_system/chroma_db")

embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

collections = {
    "math": chroma_client.get_collection("math_docs", embedding_function=embedding_function),
    "science": chroma_client.get_collection("science_docs", embedding_function=embedding_function),
    "history": chroma_client.get_collection("history_docs", embedding_function=embedding_function),
}

def ask_question(subject, query, top_k=3):
    if subject not in collections:
        return "❌ Subject not found."

    # Step 1: Query ChromaDB
    results = collections[subject].query(
        query_texts=[query],
        n_results=top_k
    )

    if not results["documents"] or not results["documents"][0]:
        return "⚠️ No relevant information found for the question."

    context = "\n".join(results['documents'][0]).strip()

    # Step 2: Prepare prompt
    prompt = f"""You are a helpful tutor. Use the context below to answer the question.

Context:
{context}

Question: {query}
Answer:"""

    # Step 3: Call local LLM (Ollama)
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "gemma:2b", "prompt": prompt, "stream": False}
        )

        print("🔁 LLM raw response:", response.status_code, response.text)  # Debug

        if response.status_code == 200:
            data = response.json()

            # Handle variations in Ollama response
            return data.get("response") or data.get("text") or "⚠️ Unexpected LLM response format."

        else:
            return f"⚠️ Error from LLM: {response.status_code} - {response.text}"

    except Exception as e:
        return f"❌ Exception while calling LLM: {str(e)}"
