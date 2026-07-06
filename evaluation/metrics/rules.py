import re


class RuleScorer:

    GREETINGS = [
        "hi",
        "hello",
        "dear"
    ]

    CLOSINGS = [
        "regards",
        "best",
        "thank you",
        "thanks"
    ]

    def score(self, reply):

        score = 0
        total = 4

        lower = reply.lower()

        if any(g in lower for g in self.GREETINGS):
            score += 1

        if any(c in lower for c in self.CLOSINGS):
            score += 1

        words = len(reply.split())

        if 40 <= words <= 180:
            score += 1

        if not re.search(r"\[(.*?)\]", reply):
            score += 1

        return round(score / total, 2)