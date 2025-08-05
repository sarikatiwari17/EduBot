import os
import chromadb
from chromadb.utils import embedding_functions
from sentence_transformers import SentenceTransformer

# Define data path and subjects
data_path = "./data"
subjects = ["math", "science", "history"]

# Load embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

# Create Chroma client
chroma_client = chromadb.PersistentClient(path="../rag_system/chroma_db")

# Create or get collections
collections = {
    "math": chroma_client.get_or_create_collection(name="math_docs", embedding_function=embedding_function),
    "science": chroma_client.get_or_create_collection(name="science_docs", embedding_function=embedding_function),
    "history": chroma_client.get_or_create_collection(name="history_docs", embedding_function=embedding_function)
}

# Loop through .txt files and add to subject collections
for filename in os.listdir(data_path):
    if filename.endswith(".txt"):
        subject = filename.replace(".txt", "").lower()  # e.g. "math.txt" → "math"
        file_path = os.path.join(data_path, filename)

        if subject not in collections:
            print(f"⚠️ Skipping unknown subject: {subject}")
            continue

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Prepare data
        texts = [content]
        ids = [f"{subject}_1"]  # You can improve this for multiple chunks later

        # Add to collection
        collections[subject].add(ids=ids, documents=texts)
        print(f"✅ Added {filename} to {subject}_docs collection.")

