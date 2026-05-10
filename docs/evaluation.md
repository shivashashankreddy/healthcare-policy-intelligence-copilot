# Evaluation

The evaluation module runs sample role-aware questions against the synthetic corpus and checks whether expected source documents appear in citations.

Outputs:

- `reports/rag_evaluation.json`
- `reports/rag_evaluation.md`

The evaluation is intentionally lightweight. In a production implementation, this would expand to include curated golden datasets, answer faithfulness scoring, citation precision, retrieval recall, regression thresholds, and human review workflows.
