from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import json

class Retriever:

    def __init__(self, dataset_path):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        with open(dataset_path, "r", encoding="utf-8") as f:
            self.dataset = json.load(f)

        self.email_texts = [
            item["customer_email"]
            for item in self.dataset
        ]

        self.embeddings = self.model.encode(
            self.email_texts,
            convert_to_numpy=True
        )

    def retrieve(self, query,exclude_id=None, top_k=3):

        query_embedding = self.model.encode(
            [query],
            convert_to_numpy=True
        )

        similarities = cosine_similarity(
            query_embedding,
            self.embeddings
        )[0]

        ranked = np.argsort(similarities)[::-1]
        results = []

        for idx in ranked:

            if exclude_id is not None:

                if self.dataset[idx]["id"] == exclude_id:
                    continue

            results.append(self.dataset[idx])

            if len(results) == top_k:
                break

        return results