import faiss
import numpy as np

class VectorStore:
    def __init__(self, dimension):
        self.index = faiss.IndexFlatIP(dimension)
        self.text_chunks = []
        self.metadata = []

    def add(self, embeddings, chunks, sources):
        self.index.add(np.array(embeddings))
        self.text_chunks.extend(chunks)
        self.metadata.extend(sources)

    def search(self, query_embedding, top_k=3):
        scores, indices = self.index.search(query_embedding, top_k)
        results = []

        for idx, score in zip(indices[0], scores[0]):
            results.append({
                "text": self.text_chunks[idx],
                "source": self.metadata[idx],
                "score": float(score)
            })

        return results