from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core import StorageContext, load_index_from_storage, QueryBundle, Settings
from llama_index.vector_stores.hnswlib import HnswlibVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from pathlib import Path


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

    questions = [
        "How do I make my code more efficient?",
        "Why is my simulation not converging?",
        "How to set up a fluid-structure interaction problem?",
    ]

    db_dir = Path("/database")
    top_n = 5

    embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L12-v2")
    Settings.embed_model = embed_model

    index = load_index(db_dir)
    query_index(index, top_n, questions)
