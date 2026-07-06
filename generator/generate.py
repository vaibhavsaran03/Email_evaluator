import json

from generator.llm_client import LLMClient
from generator.prompt_builder import build_prompt
from retrieval.retriever import Retriever

from config import DATASET_PATH
from config import GENERATED_PATH
from config import TEST_DATASET_PATH


retriever = Retriever(DATASET_PATH)

llm = LLMClient()


def generate_responses():

    with open(TEST_DATASET_PATH, "r", encoding="utf-8") as f:
        dataset = json.load(f)

    outputs = []

    TEST_LIMIT = 3

    for item in dataset[:TEST_LIMIT]:
        print("=" * 80)
        print(f"Email #{item['id']}")
        print("=" * 80)
        print("\nIncoming Email:\n")
        print(item["customer_email"])

        retrieved = retriever.retrieve(
            item["customer_email"],
        )

        print("\nTop Retrieved Examples:\n")

        for i, example in enumerate(retrieved, 1):
            print(f"{i}. [{example['category']}]")
            print(example["customer_email"][:120])
            print("-" * 60)

        prompt = build_prompt(
            item["customer_email"],
            retrieved
        )

        response = llm.generate(prompt)

        print("\nGenerated Reply:\n")
        print(response)
        print("\n")

        outputs.append({

            "id": item["id"],

            "category": item["category"],

            "customer_email": item["customer_email"],

            "reference_reply": item["reference_reply"],

            "generated_reply": response

        })

    with open(GENERATED_PATH, "w", encoding="utf-8") as f:

        json.dump(
            outputs,
            f,
            indent=4,
            ensure_ascii=False
        )

    print("Generated", len(outputs), "responses.")