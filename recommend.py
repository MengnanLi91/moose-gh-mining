from sentence_transformers import SentenceTransformer, util
from pathlib import Path
import pandas as pd
import numpy as np

if __name__ == "__main__":
    # Model used for encoding posts
    # This model should be the same as the one used in build_db.py
    model = SentenceTransformer("all-MiniLM-L6-v2")
    # Database directory
    db_dir = Path("db")
    # Top N most similar posts to retrieve
    top_n = 5

    # Read database
    meta = pd.read_csv(db_dir / "meta.csv")
    encodings = np.load(db_dir / "encoding.npy")

    # Question
    questions = [
        "How do I make my code more efficient?",
        "Why is my simulation not converging?",
        "How to set up a fluid-structure interaction problem?",
    ]

    # Compute similarities
    question_encoding = model.encode(questions)
    similarities = util.pytorch_cos_sim(question_encoding, encodings)

    # Apply threshold
    print("-" * 79)
    for i, question in enumerate(questions):
        print("Question:", question)
        sorted_idx = similarities[i].argsort(descending=True)
        top_n_idx = sorted_idx[:top_n]
        for j, idx in enumerate(top_n_idx):
            print("    {}. Title: {}".format(j + 1, meta["title"].iloc[idx.item()]))
            print("        URL: {}".format(meta["url"].iloc[idx.item()]))
            print("        Similarity: {:.4f}".format(similarities[i][idx].item()))
        print("-" * 79)
