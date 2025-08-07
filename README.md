The Classroom Tutor Agent is an AI-powered educational assistant designed to help students learn effectively through interactive question-answering, subject-wise support, and progress tracking. It uses ChromaDB for document storage and retrieval and a local LLM (Gemma 2B via Ollama) to generate accurate and context-aware answers from study materials.

🚀 Features
✅ Subject-based Routing: Supports multiple subjects like Math, Science, English, History, and Computer.
🧠 Document-based QA: Answers questions by retrieving information from custom .txt files stored in data/ folder.
📈 Progress Tracking: Tracks user performance over time (correct/incorrect answers).
🧾 Topic Selector (coming soon): Allows students to select specific topics within a subject.
🎨 Streamlit Frontend: Intuitive chat-like UI built with Streamlit for a smooth user experience.
🔍 Embeddings & Vector Search: Uses SentenceTransformer for embeddings and ChromaDB for efficient semantic search

 Tech Stack
Backend: Python, ChromaDB, SentenceTransformers, Local LLM via Ollama (Gemma 2B)
Frontend: Streamlit
LLM: Gemma 2B (via Ollama)
Database: ChromaDB for vector search
Deployment: Local system

🧪 How it Works

User selects a subject from the UI.

Their question is embedded using SentenceTransformer.

ChromaDB retrieves relevant documents from the selected subject.

The local LLM (Gemma 2B) generates an answer.

If the answer is incorrect, a hint is generated and shown.

Performance data is stored for progress tracking.



