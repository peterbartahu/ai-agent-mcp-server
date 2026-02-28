from app.rag.embedder import Embedder
from app.rag.vector_store import VectorStore


class KnowledgeBase:

    def __init__(self):
        self.embedder = Embedder()
        self.vector_store = None

    def build(self, documents: list[str]):
        embeddings = self.embedder.embed(documents)
        dimension = len(embeddings[0])

        self.vector_store = VectorStore(dimension)
        self.vector_store.add(embeddings, documents)

    def retrieve(self, query: str, k: int = 3) -> list[str]:
        query_embedding = self.embedder.embed([query])[0]
        return self.vector_store.search(query_embedding, k)