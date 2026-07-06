class SafetyScorer:

    SUSPICIOUS = [
        "tracking number",
        "coupon code",
        "discount code",
        "order id",
        "ticket id",
        "reference number"
    ]

    def score(self, email, reply):

        email = email.lower()
        reply = reply.lower()

        penalty = 0

        for keyword in self.SUSPICIOUS:

            if keyword in reply and keyword not in email:
                penalty += 1

        score = max(
            0,
            1 - penalty * 0.25
        )

        return round(score, 2)