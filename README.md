## Overview

This project implements an AI-powered customer support email suggestion system that generates professional email replies grounded in historical customer support conversations.

Rather than relying solely on prompt engineering, the system first retrieves semantically similar historical email-response pairs and uses them as context for the LLM. This ensures that generated responses are informed by previous support interactions.

Evaluation: Instead of measuring lexical similarity alone, the system evaluates generated responses using multiple complementary metrics that better reflect real-world customer support quality.

---

# Architecture

```
Historical Email Dataset
          │
          ▼
 Sentence Embeddings
          │
          ▼
 Semantic Retrieval
    (Top-3 Similar Emails)
          │
          ▼
     Prompt Builder
          │
          ▼
      Gemini LLM
          │
          ▼
 Generated Response
          │
          ▼
Evaluation Engine
 ├── Semantic Similarity
 ├── Rule-based Checks
 ├── Safety Checks
 └── LLM-as-a-Judge
          │
          ▼
 Response Quality Score
```

---

# Dataset

The project separates **historical knowledge** from **evaluation data**.

### 1. Historical Dataset

```
data/historical_emails.json
```

Contains historical customer support conversations.

Each record includes:

- Category
- Customer Email
- Ideal Reply
- Tags

These conversations act as the knowledge base for retrieval.

---

### 2. Test Dataset

```
data/test_emails.json
```

Contains unseen incoming customer emails used to simulate new support requests.

Each test record contains:

- Customer Email
- Reference Reply

The reference reply is **not** used during generation.

Instead, it is used only during evaluation to compare the generated response against a high-quality human-written response.

This separation here better reflects a real production system where historical conversations are used for grounding while new customer emails are answered by the model.

---

# Response Generation

The system uses Retrieval-Augmented Generation (RAG).

Workflow:

1. Load historical customer support conversations.
2. Generate semantic embeddings using Sentence Transformers.
3. Embed the incoming customer email.
4. Retrieve the Top-3 most similar historical conversations using cosine similarity.
5. Build a prompt containing those examples.
6. Generate a suggested reply using Gemini.

Using retrieval grounds the LLM in previous customer support interactions instead of relying solely on the model's internal knowledge.

This lightweight retrieval approach was chosen over a vector database because the dataset is intentionally small and can be searched efficiently in memory.

For larger production datasets, the retrieval layer can be replaced with a vector database such as:

- FAISS
- ChromaDB
- Pinecone
- Weaviate

---

# Evaluation Approach

The challenge emphasizes measuring response quality rather than exact matching.

A customer support email often has multiple equally valid responses.
Therefore the system evaluates responses using multiple complementary metrics.

## 1. Semantic Similarity

Measures how closely the generated response matches the meaning of the reference response using Sentence Transformers.

---

## 2. Rule-based Quality Checks

Checks practical email quality including:

- Greeting present
- Closing present
- Appropriate length
- No placeholder text

---

## 3. Safety Checks

Applies lightweight heuristics to detect unsupported claims such as fabricated:

- Tracking numbers
- Order IDs
- Coupon codes
- Reference IDs

This discourages hallucinated customer support actions.

---

## 4. LLM-as-a-Judge

The generated response is evaluated by an LLM across multiple dimensions:

- Correctness
- Completeness
- Professionalism
- Tone
- Hallucination Risk

Rather than asking for a single score, each criterion is scored independently and combined later.

This produces more interpretable evaluations.

---

# Final Response Quality Score

The final score is a weighted combination of all evaluation metrics.

```
Overall Score =
0.50 × LLM Judge
+ 0.25 × Semantic Similarity
+ 0.15 × Rule Checks
+ 0.10 × Safety Checks
```

This weightage to scores is given by what I think is right.

This approach reflects both semantic quality and practical customer support requirements.

---

# Trade-offs

### Why Retrieval instead of Fine-tuning?

Fine-tuning requires significantly more data and infrastructure.
Semantic retrieval provides grounding while remaining lightweight and easy to reproduce.

---

### Why not BLEU or ROUGE?

Customer support emails frequently have many valid responses.
Two excellent replies may share little lexical overlap.

Semantic similarity and LLM-based evaluation better capture actual response quality.

---

### Why Sentence Transformers?

I learned that sentence Transformers provide fast, high-quality semantic embeddings and are well suited for small datasets without requiring external infrastructure. So for this assessment this is the best choice.

---

# How to Run

## Install dependencies

```bash
pip install -r requirements.txt
```

## Configure API key

Create a `.env` file:

```
GEMINI_API_KEY=YOUR_API_KEY
```

## Run

```bash
python main.py
```

The pipeline will:

1. Load the historical dataset.
2. Retrieve similar customer conversations.
3. Generate responses for incoming emails.
4. Evaluate each generated response.
5. Produce a detailed evaluation report.

---

# Output

The system generates:

```
data/generated.json
```

Generated responses.

and

```
evaluation/report.json
```

Detailed per-response evaluation including:

- Semantic Similarity
- Rule Score
- Safety Score
- LLM Judge Scores
- Overall Response Quality Score

---

# Future Improvements

-Better Guardrails
-Adding a dedicated Validation Agent
-Downloadable Reports
