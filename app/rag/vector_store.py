import faiss
import numpy as np


class VectorStore:

    def __init__(self, dimension: int):
        self.index = faiss.IndexFlatL2(dimension)
        self.texts = []

    def add(self, embeddings: list[list[float]], texts: list[str]):
        vectors = np.array(embeddings).astype("float32")
        self.index.add(vectors)
        self.texts.extend(texts)

    def search(self, embedding: list[float], k: int = 3) -> list[str]:
        query = np.array([embedding]).astype("float32")
        distances, indices = self.index.search(query, k)

        results = []
        for idx in indices[0]:
            if idx < len(self.texts):
                results.append(self.texts[idx])
        return results