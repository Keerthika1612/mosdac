import os

# Base project directory
base_dir = "mosdac_chatbot"

# Folder structure
dirs = [
    "data/raw/static",
    "data/raw/dynamic",
    "data/processed",
    "data/embeddings",
    "crawler",
    "preprocessing",
    "knowledge_graph",
    "intent_engine/rasa_nlu",
    "intent_engine/dialogflow",
    "rag_pipeline",
    "ui",
    "retraining",
    "logs"
]

# Files to create in each directory
files = {
    "data/processed": ["cleaned_text.json"],
    "data/embeddings": ["faiss_index.idx", "keys.json"],
    "crawler": ["crawl_mosdac.py"],
    "preprocessing": ["preprocess.py"],
    "knowledge_graph": ["build_kg.py", "visualize_kg.py"],
    "intent_engine": ["classify_intent.py"],
    "rag_pipeline": ["create_embeddings.py", "langchain_handler.py", "nvidia_nemo_integration.py"],
    "ui": ["app.py"],
    "retraining": ["retrain_pipeline.py"],
    "logs": ["unmatched_queries.txt"]
}

# Root-level files
root_files = ["requirements.txt", ".env"]

# Create directories
for d in dirs:
    os.makedirs(os.path.join(base_dir, d), exist_ok=True)

# Create files inside respective directories
for folder, file_list in files.items():
    for file in file_list:
        file_path = os.path.join(base_dir, folder, file)
        with open(file_path, "w") as f:
            if file.endswith(".py"):
                f.write(f"# {file.replace('_', ' ').title()} - Placeholder\n")
            elif file.endswith(".json"):
                f.write("{}")
            elif file.endswith(".idx"):
                f.write("")  # Binary file placeholder
            elif file.endswith(".txt"):
                f.write("# Log unmatched queries here\n")

# Create root-level files
for file in root_files:
    file_path = os.path.join(base_dir, file)
    with open(file_path, "w") as f:
        if file == "requirements.txt":
            f.write("# Add all Python dependencies here\n")
        elif file == ".env":
            f.write("# API keys, model paths, Neo4j credentials\n")

print(f"✅ Project structure created successfully in '{base_dir}'")
