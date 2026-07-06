import json

from evaluation.metrics.semantic import SemanticScorer
from evaluation.metrics.rules import RuleScorer
from evaluation.metrics.safety import SafetyScorer
from evaluation.metrics.llm_judge import LLMJudge
from evaluation.metrics.aggregator import final_score

from config import GENERATED_PATH

semantic = SemanticScorer()
rules = RuleScorer()
safety = SafetyScorer()
judge = LLMJudge()


def evaluate():

    print("\n" + "=" * 90)
    print("RESPONSE QUALITY EVALUATION")
    print("=" * 90)

    with open(GENERATED_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    results = []
    total = 0

    for idx, sample in enumerate(data, start=1):

        print(f"\n[{idx}/{len(data)}] Evaluating Email #{sample['id']}")
        print("-" * 90)

        print("\nCustomer Email:\n")
        print(sample["customer_email"])

        print("\nGenerated Reply:\n")
        print(sample["generated_reply"])

        semantic_score = semantic.score(
            sample["reference_reply"],
            sample["generated_reply"]
        )

        rule_score = rules.score(
            sample["generated_reply"]
        )

        safety_score = safety.score(
            sample["customer_email"],
            sample["generated_reply"]
        )

        judge_score = judge.score(
            sample["customer_email"],
            sample["reference_reply"],
            sample["generated_reply"]
        )

        overall = final_score(
            semantic_score,
            rule_score,
            safety_score,
            judge_score
        )

        total += overall

        print("\nEvaluation Metrics")
        print("-" * 40)
        print(f"Semantic Similarity : {semantic_score}")
        print(f"Rule Score          : {rule_score}")
        print(f"Safety Score        : {safety_score}")

        print("\nLLM Judge")
        print("-" * 40)
        print(f"Correctness     : {judge_score['correctness']}")
        print(f"Completeness    : {judge_score['completeness']}")
        print(f"Professionalism : {judge_score['professionalism']}")
        print(f"Tone            : {judge_score['tone']}")
        print(f"Hallucination   : {judge_score['hallucination']}")

        if "reason" in judge_score:
            print(f"\nReason: {judge_score['reason']}")

        print(f"\nOverall Response Quality Score : {overall}/100")

        print("=" * 90)

        results.append({

            "id": sample["id"],

            "category": sample["category"],

            "customer_email": sample["customer_email"],

            "generated_reply": sample["generated_reply"],

            "reference_reply": sample["reference_reply"],

            "semantic_similarity": semantic_score,

            "rule_score": rule_score,

            "safety_score": safety_score,

            "llm_judge": judge_score,

            "overall_score": overall

        })

    report = {

        "average_score": round(
            total / max(len(results), 1),
            2
        ),

        "responses": results

    }

    with open(
        "evaluation/report.json",
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            report,
            f,
            indent=4,
            ensure_ascii=False
        )

    print("\n" + "=" * 90)
    print("FINAL SUMMARY")
    print("=" * 90)
    print(f"Responses Evaluated : {len(results)}")
    print(f"Average Quality Score : {report['average_score']}/100")
    print("Detailed report saved to evaluation/report.json")
    print("=" * 90)