from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


class SemanticScorer:

    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def score(self, reference, generated):

        embeddings = self.model.encode(
            [reference, generated],
            convert_to_numpy=True
        )

        similarity = cosine_similarity(
            [embeddings[0]],
            [embeddings[1]]
        )[0][0]

        return round(float(similarity), 4)