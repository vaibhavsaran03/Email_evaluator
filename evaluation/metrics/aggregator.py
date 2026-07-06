def final_score(
    semantic,
    rules,
    safety,
    judge
):

    llm = (
        judge["correctness"] +
        judge["completeness"] +
        judge["professionalism"] +
        judge["tone"] +
        judge["hallucination"]
    ) / 50

    score = (

        0.50 * llm +

        0.25 * semantic +

        0.15 * rules +

        0.10 * safety

    )

    return round(score * 100, 2)