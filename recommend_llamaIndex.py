import argparse
from numbers import Real
from pathlib import Path
import os
from llama_index.core import QueryBundle
from sentence_transformers import SentenceTransformer, CrossEncoder
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.postprocessor.llm_rerank import LLMRerank
from llama_index.core.postprocessor import SimilarityPostprocessor
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import StorageContext, load_index_from_storage, QueryBundle, Settings
from llama_index.core.storage.docstore import SimpleDocumentStore
from llama_index.core.storage.index_store import SimpleIndexStore
from llama_index.vector_stores.hnswlib import HnswlibVectorStore


def load_model(load_local, model_path, model_name):
    if load_local:
        model_path_full = os.path.join(model_path, model_name)
        embed_model = HuggingFaceEmbedding(model_name=model_path_full)
    else:
        embed_model = SentenceTransformer(model_name)
    return embed_model

def load_index(db_dir):

    # Read database
    hnswlib_vector_store = HnswlibVectorStore.from_params(
        space="ip",
        dimension=embed_model._model.get_sentence_embedding_dimension(),
        max_elements=10000,
    )
    vector_store = hnswlib_vector_store.from_persist_dir(db_dir)
    storage_context = StorageContext.from_defaults(
        vector_store=vector_store, persist_dir=db_dir
    )
    index = load_index_from_storage(storage_context=storage_context)

    return index

def query_index(index, top_n, questions):
    for query in questions:
        query_bundle = QueryBundle(query)
        retriever = VectorIndexRetriever(index=index, similarity_metric='cosine', similarity_top_k=top_n)
        retrieved_nodes = retriever.retrieve(query_bundle)

        print("Question:", query)
        for node in retrieved_nodes:
            print(f"Score: {node.score:.3f} - {node.metadata}...")
        print("-" * 79)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Choose LLM and embedding model.')
    parser.add_argument('--load_local', action='store_true', help="Load model locally.")
    parser.add_argument('--model_path', type=str, default="<model path>", help="Path to the local model.")
    parser.add_argument('--model_name', type=str, default="all-MiniLM-L12-v2", help="Model name for SentenceTransformer.")
    parser.add_argument('--database', type=str, default="database", help="Path to store the index database.")
    parser.add_argument('--top_n', type=Real, default=5, help="Pick the number of relevent discussion to retrivive")
    args = parser.parse_args()

    questions = [
        "How do I make my code more efficient?",
        "Why is my simulation not converging?",
        "How to set up a fluid-structure interaction problem?",
    ]

    db_dir = Path(args.database)

    embed_model = load_model(args.load_local, args.model_path, args.model_name)
    Settings.embed_model = embed_model

    index = load_index(args.database)
    query_index(index, args.top_n, questions)
