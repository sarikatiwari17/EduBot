from langchain_community.llms import Ollama
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.utils import embedding_functions

# Load embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Setup ChromaDB
chroma_client = chromadb.PersistentClient(path="../rag_system/chroma_db")
embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

# Load subject-specific collections
collections = {
    "math": chroma_client.get_collection("math_docs", embedding_function=embedding_function),
    "science": chroma_client.get_collection("science_docs", embedding_function=embedding_function),
    "history": chroma_client.get_collection("history_docs", embedding_function=embedding_function),
}

def ask(question: str, subject: str = "math") -> str:
    if subject not in collections:  
        return "❌ Subject not found."

    collection = collections[subject]  # ✅ This is a ChromaDB collection

    query_embedding = embedding_model.encode([question])[0].tolist()
    results = collection.query(query_embeddings=[query_embedding], n_results=3)

    relevant_docs = [doc for doc in results["documents"][0]]
    context = "\n\n---\n\n".join(relevant_docs)

    prompt = f"""You are a helpful tutor chatbot.
Answer the following question using only the given context from textbook notes.
Make the answer interactive, clear, and give examples if possible.

Question: {question}

Context:
{context}

Answer:"""

    llm = Ollama(model="gemma:2b")
    return llm(prompt)

# Run
print("🔍 EduBot is ready!")
subject = input("📘 Subject (math/science/history): ").strip().lower()
question = input("📚 Ask your question: ")
answer = ask(question, subject=subject)
print("\n🤖 Bot:", answer, "\n")
