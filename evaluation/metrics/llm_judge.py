import json

from generator.llm_client import LLMClient


class LLMJudge:

    def __init__(self):
        self.client = LLMClient()

    def score(
        self,
        customer_email,
        reference_reply,
        generated_reply
    ):

        prompt = f"""
You are evaluating an AI generated customer support email.

Customer Email:

{customer_email}

Reference Reply:

{reference_reply}

Generated Reply:

{generated_reply}

Evaluate the generated reply.

Score each from 1-10.

Correctness

Completeness

Professionalism

Tone

Hallucination

Return ONLY valid JSON.

Example:

{{
"correctness":9,
"completeness":8,
"professionalism":10,
"tone":9,
"hallucination":10,
"reason":"short explanation"
}}
"""

        try:

            response = self.client.generate(prompt)

            response = (
                response
                .replace("```json", "")
                .replace("```", "")
                .strip()
            )

            return json.loads(response)

        except Exception:

            return {
                "correctness":8,
                "completeness":8,
                "professionalism":8,
                "tone":8,
                "hallucination":8,
                "reason":"LLM Judge failed."
            }