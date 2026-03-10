from app.rag.vector_store import VectorStore


def test_vector_store_search():

    store = VectorStore(dimension=3)

    embeddings = [
        [0.1, 0.2, 0.3],
        [0.9, 0.8, 0.7],
        [0.05, 0.1, 0.2]
    ]

    texts = [
        "doc1",
        "doc2",
        "doc3"
    ]

    store.add(embeddings, texts)

    result = store.search([0.1, 0.2, 0.25], k=2)

    assert len(result) == 2