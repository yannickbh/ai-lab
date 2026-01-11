# Evaluation Guide: Enterprise Ticket Assistant

Este guia descreve como avaliar a qualidade e performance do sistema usando golden sets, testes regressivos e métricas objetivas.

---

## 1. Estrutura de Avaliação

### 1.1 Golden Set

Conjunto de exemplos rotulados manualmente usados para avaliar o sistema.

**Estrutura:**
```
tests/evaluation/golden_set/
├── tickets/
│   ├── ticket_001.json
│   ├── ticket_002.json
│   └── ...
└── expected_outputs/
    ├── ticket_001_expected.json
    ├── ticket_002_expected.json
    └── ...
```

**Formato de ticket:**
```json
{
  "ticket_id": "TICKET-001",
  "tenant_id": "acme-corp",
  "subject": "API timeout errors",
  "description": "Our API is experiencing timeout errors when processing large requests...",
  "priority": null,
  "category": null,
  "assigned_team": null
}
```

**Formato de output esperado:**
```json
{
  "ticket_id": "TICKET-001",
  "classification": {
    "category": "api_issue",
    "priority": "high",
    "assigned_team": "backend_team"
  },
  "resolution_plan": {
    "steps": ["Check API logs", "Review timeout config", "Test with smaller payloads"],
    "estimated_time": "2 hours"
  },
  "resolution_action": {
    "action_type": "update_config",
    "details": "Increased API timeout from 30s to 60s"
  }
}
```

---

## 2. Métricas de Avaliação

### 2.1 Classification Accuracy

**Métrica:** Taxa de classificação correta (category, priority, team)

```python
def evaluate_classification(predictions, golden_set):
    correct = 0
    total = 0
    
    for ticket_id, expected in golden_set.items():
        predicted = predictions[ticket_id]
        
        # Category accuracy
        if predicted["category"] == expected["category"]:
            correct += 1
        total += 1
    
    accuracy = correct / total
    return {
        "accuracy": accuracy,
        "correct": correct,
        "total": total
    }
```

### 2.2 Resolution Plan Quality

**Métrica:** Similaridade semântica do plano de resolução

```python
from sentence_transformers import SentenceTransformer
import numpy as np

def evaluate_resolution_plan_quality(predictions, golden_set):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    similarities = []
    
    for ticket_id, expected in golden_set.items():
        predicted = predictions[ticket_id]
        
        # Embed both plans
        pred_emb = model.encode(predicted["resolution_plan"]["steps"])
        exp_emb = model.encode(expected["resolution_plan"]["steps"])
        
        # Cosine similarity
        similarity = np.dot(pred_emb, exp_emb) / (
            np.linalg.norm(pred_emb) * np.linalg.norm(exp_emb)
        )
        similarities.append(similarity)
    
    return {
        "mean_similarity": np.mean(similarities),
        "std_similarity": np.std(similarities),
        "min_similarity": np.min(similarities),
        "max_similarity": np.max(similarities)
    }
```

### 2.3 Latency Metrics

**Métricas:**
- Tempo total de processamento
- Tempo por agente
- Tempo por task

```python
import time
from prometheus_client import Summary

execution_time = Summary('ticket_assistant_execution_time_seconds', 'Execution time')

def evaluate_latency(ticket_id, start_time, end_time):
    duration = end_time - start_time
    
    # Record metric
    execution_time.observe(duration)
    
    return {
        "ticket_id": ticket_id,
        "total_time_seconds": duration,
        "acceptable": duration < 30.0  # Threshold
    }
```

### 2.4 Cost Metrics

**Métricas:**
- Tokens por ticket
- Custo por ticket
- Custo por sucesso

```python
def evaluate_cost(predictions, token_usage):
    costs = []
    successful_costs = []
    
    for ticket_id, tokens in token_usage.items():
        cost = calculate_cost(tokens)  # Based on model pricing
        costs.append(cost)
        
        if predictions[ticket_id]["status"] == "success":
            successful_costs.append(cost)
    
    return {
        "mean_cost_per_ticket": np.mean(costs),
        "mean_cost_per_success": np.mean(successful_costs) if successful_costs else 0,
        "total_cost": sum(costs),
        "cost_per_success_rate": len(successful_costs) / len(costs)
    }
```

---

## 3. Testes Regressivos

### 3.1 Regression Test Suite

```python
# tests/evaluation/test_regression.py

import pytest
from pathlib import Path
from src.main import process_ticket
from src.evaluation.metrics import evaluate_classification, evaluate_latency

GOLDEN_SET_PATH = Path(__file__).parent / "golden_set"

@pytest.mark.regression
def test_golden_set_classification():
    """Regression test: Classification accuracy should not degrade."""
    golden_set = load_golden_set(GOLDEN_SET_PATH)
    predictions = {}
    
    for ticket in golden_set:
        result = process_ticket(ticket["ticket_id"], ticket["tenant_id"])
        predictions[ticket["ticket_id"]] = result
    
    metrics = evaluate_classification(predictions, golden_set)
    
    # Assert accuracy threshold
    assert metrics["accuracy"] >= 0.85, f"Accuracy {metrics['accuracy']} below threshold 0.85"
```

### 3.2 Performance Regression

```python
@pytest.mark.regression
def test_latency_regression():
    """Regression test: Latency should not increase significantly."""
    golden_set = load_golden_set(GOLDEN_SET_PATH)
    latencies = []
    
    for ticket in golden_set[:10]:  # Sample
        start = time.time()
        process_ticket(ticket["ticket_id"], ticket["tenant_id"])
        end = time.time()
        latencies.append(end - start)
    
    mean_latency = np.mean(latencies)
    
    # Assert latency threshold (e.g., < 30s)
    assert mean_latency < 30.0, f"Mean latency {mean_latency}s exceeds threshold"
```

---

## 4. Evaluation Harness

### 4.1 Estrutura do Harness

```python
# src/evaluation/harness.py

from dataclasses import dataclass
from typing import List, Dict
import json

@dataclass
class EvaluationResult:
    ticket_id: str
    accuracy: float
    latency_seconds: float
    cost_usd: float
    tokens_used: int
    status: str  # success, failure, timeout
    
class EvaluationHarness:
    def __init__(self, golden_set_path: Path):
        self.golden_set = self.load_golden_set(golden_set_path)
        self.results: List[EvaluationResult] = []
    
    def run_evaluation(self, agent_version: str) -> Dict:
        """Run full evaluation suite."""
        for ticket in self.golden_set:
            result = self.evaluate_ticket(ticket, agent_version)
            self.results.append(result)
        
        return self.aggregate_results()
    
    def evaluate_ticket(self, ticket: Dict, agent_version: str) -> EvaluationResult:
        """Evaluate single ticket."""
        start_time = time.time()
        
        try:
            # Process ticket
            prediction = process_ticket(ticket["ticket_id"], ticket["tenant_id"])
            
            # Calculate metrics
            latency = time.time() - start_time
            accuracy = self.calculate_accuracy(prediction, ticket["expected_output"])
            cost = self.calculate_cost(prediction)
            
            return EvaluationResult(
                ticket_id=ticket["ticket_id"],
                accuracy=accuracy,
                latency_seconds=latency,
                cost_usd=cost,
                tokens_used=prediction["tokens_used"],
                status="success"
            )
        except Exception as e:
            return EvaluationResult(
                ticket_id=ticket["ticket_id"],
                accuracy=0.0,
                latency_seconds=time.time() - start_time,
                cost_usd=0.0,
                tokens_used=0,
                status=f"failure: {str(e)}"
            )
    
    def aggregate_results(self) -> Dict:
        """Aggregate evaluation results."""
        successful = [r for r in self.results if r.status == "success"]
        
        return {
            "total_tickets": len(self.results),
            "successful": len(successful),
            "success_rate": len(successful) / len(self.results),
            "mean_accuracy": np.mean([r.accuracy for r in successful]) if successful else 0,
            "mean_latency_seconds": np.mean([r.latency_seconds for r in successful]) if successful else 0,
            "mean_cost_usd": np.mean([r.cost_usd for r in successful]) if successful else 0,
            "total_tokens": sum([r.tokens_used for r in successful]),
            "failures": [r.ticket_id for r in self.results if r.status != "success"]
        }
```

### 4.2 Executar Evaluation

```bash
# Run evaluation harness
python -m src.evaluation.harness --golden-set tests/evaluation/golden_set --output results.json

# Run regression tests
pytest tests/evaluation/test_regression.py -v

# Generate evaluation report
python -m src.evaluation.report --results results.json --output report.html
```

---

## 5. Offline Evaluation

### 5.1 Batch Processing

```python
def offline_evaluation(golden_set_path: Path, output_path: Path):
    """Run evaluation on entire golden set offline."""
    harness = EvaluationHarness(golden_set_path)
    results = harness.run_evaluation(agent_version="v0.1.0")
    
    # Save results
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)
    
    return results
```

### 5.2 A/B Testing (Comparar Versões)

```python
def compare_versions(version_a: str, version_b: str, golden_set_path: Path):
    """Compare two agent versions."""
    harness_a = EvaluationHarness(golden_set_path)
    harness_b = EvaluationHarness(golden_set_path)
    
    results_a = harness_a.run_evaluation(version_a)
    results_b = harness_b.run_evaluation(version_b)
    
    # Compare metrics
    comparison = {
        "accuracy_diff": results_b["mean_accuracy"] - results_a["mean_accuracy"],
        "latency_diff": results_b["mean_latency_seconds"] - results_a["mean_latency_seconds"],
        "cost_diff": results_b["mean_cost_usd"] - results_a["mean_cost_usd"]
    }
    
    return comparison
```

---

## 6. Scoring Rubric

### 6.1 Classification Score

```
Correct category: +2 points
Correct priority: +2 points
Correct team: +1 point
Total: 5 points max
```

### 6.2 Resolution Plan Score

```
- Semantic similarity > 0.8: 5 points
- Semantic similarity > 0.6: 3 points
- Semantic similarity > 0.4: 1 point
- Semantic similarity <= 0.4: 0 points
```

### 6.3 Overall Score

```python
def calculate_overall_score(result: EvaluationResult) -> float:
    """Calculate overall score (0-100)."""
    classification_score = result.accuracy * 50  # Max 50 points
    plan_score = result.similarity * 30  # Max 30 points
    latency_score = max(0, 20 - (result.latency_seconds / 30) * 20)  # Max 20 points
    
    return classification_score + plan_score + latency_score
```

---

## 7. Continuous Evaluation

### 7.1 CI/CD Integration

```yaml
# .github/workflows/evaluation.yml
name: Evaluation

on:
  pull_request:
    branches: [main]

jobs:
  evaluate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run evaluation
        run: |
          python -m src.evaluation.harness --golden-set tests/evaluation/golden_set
      - name: Check regression
        run: |
          pytest tests/evaluation/test_regression.py
```

---

## 8. Relatórios

### 8.1 Evaluation Report Template

```markdown
# Evaluation Report - Enterprise Ticket Assistant

**Date:** 2026-01-10
**Version:** v0.1.0
**Golden Set Size:** 100 tickets

## Summary
- **Total Tickets:** 100
- **Success Rate:** 95%
- **Mean Accuracy:** 87.3%
- **Mean Latency:** 12.5s
- **Mean Cost:** $0.023 per ticket

## Detailed Metrics

### Classification
- Category Accuracy: 89%
- Priority Accuracy: 85%
- Team Assignment Accuracy: 88%

### Performance
- P50 Latency: 11.2s
- P95 Latency: 28.4s
- P99 Latency: 35.1s

### Cost
- Total Cost: $2.30
- Cost per Success: $0.024
- Token Efficiency: 1,234 tokens/ticket

## Failures
- 5 tickets failed (see failures.json)

## Recommendations
1. Improve priority classification accuracy
2. Optimize latency for P95 cases
3. Reduce token usage for cost optimization
```

---

## 9. Próximos Passos

- [ ] Criar golden set inicial (10-20 tickets)
- [ ] Implementar evaluation harness básico
- [ ] Adicionar testes regressivos
- [ ] Configurar CI/CD para avaliação automática
- [ ] Implementar scoring rubric
- [ ] Criar dashboard de métricas (Grafana)
