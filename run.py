from data.load_qa_data import main as load_embeddings

print("Loading embeddings...")
load_embeddings()

from src.main import run

run()