import json

from llm_client import LLMClient

client = LLMClient()

PROMPT = """
Generate exactly 25 realistic customer support email conversations.

Return ONLY valid JSON.

Schema:

[
{
"id":1,
"category":"refund",
"tags":["refund","billing"],

"customer_email":"...",

"ideal_reply":"..."
}
]

Categories should include:

refund
shipping delay
password reset
duplicate charge
subscription cancellation
feature request
invoice request
damaged product
wrong item
account deletion

Emails should look realistic.

Replies should be professional, concise, empathetic and actionable.

NO markdown.

NO explanation.

ONLY JSON.
"""

response = client.generate(PROMPT)

with open("data/emails.json","w",encoding="utf-8") as f:
    f.write(response)

print("Dataset generated.")