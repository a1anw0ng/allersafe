# AllerSafe Evaluation System

Comprehensive evaluation framework for testing and measuring the performance of the AllerSafe allergen detection and alternative finding pipeline.

## Overview

This evaluation system provides:
- **Accuracy metrics** for allergen detection (Safe/Caution/Dangerous/NotDetected)
- **Precision/Recall** for allergen identification
- **Alternative finding quality** metrics
- **Performance benchmarks** (latency tracking)
- **Cost analysis** (API token usage and costs)
- **Safety-critical metrics** (false negative tracking)

## Quick Start

### 1. Add Test Images

Place your test images in the `evaluation/test_images/` directory:

```bash
backend/evaluation/test_images/
├── dangerous_product.jpg
├── safe_product.jpg
├── caution_product.jpg
├── non_product.jpg
├── dairy_product.jpg
└── hidden_allergen.jpg
```

### 2. Run Evaluation

```bash
cd backend
python -m evaluation.run_evaluation --verbose
```

### 3. View Results

Results will be printed to the console. To save to a file:

```bash
python -m evaluation.run_evaluation --output evaluation_results.json
```

## Usage

### Run All Tests

```bash
python -m evaluation.run_evaluation --verbose
```

### Run Specific Test

```bash
python -m evaluation.run_evaluation --test-id 001
```

### Run Multiple Specific Tests

```bash
python -m evaluation.run_evaluation --test-id 001 --test-id 003
```

### Save Results to File

```bash
python -m evaluation.run_evaluation --output results.json
```

### Custom Test Cases File

```bash
python -m evaluation.run_evaluation --test-cases my_tests.json
```

## Test Case Format

Test cases are defined in `test_cases.json`:

```json
{
  "test_id": "001",
  "name": "Dangerous - Contains user allergens",
  "description": "Product that contains allergens the user is allergic to",
  "image_path": "evaluation/test_images/dangerous_product.jpg",
  "user_allergens": ["peanuts", "dairy"],
  "ground_truth": {
    "severity": "Dangerous",
    "allergens_detected": ["peanuts", "dairy"],
    "contains_product": true,
    "product_category": "snack",
    "alternatives": {
      "min_count": 3,
      "should_be_safe": true,
      "should_avoid_allergens": ["peanuts", "dairy"]
    }
  }
}
```

### Ground Truth Fields

**Required:**
- `severity`: Expected severity level (`Safe`, `Caution`, `Dangerous`, or `NotDetected`)
- `allergens_detected`: List of allergens that should be detected
- `contains_product`: Boolean indicating if image contains a food product

**Optional:**
- `product_category`: Product category (e.g., "snack", "dairy", "beverage")
- `alternatives`: Criteria for evaluating alternative products
  - `min_count`: Minimum number of alternatives expected
  - `should_be_safe`: Whether alternatives should all be marked as "Safe"
  - `should_avoid_allergens`: List of allergens alternatives should avoid

## Adding New Test Cases

1. Add your test image to `evaluation/test_images/`
2. Edit `test_cases.json` and add a new entry:

```json
{
  "test_id": "007",
  "name": "Your test name",
  "description": "Description of what this tests",
  "image_path": "evaluation/test_images/your_image.jpg",
  "user_allergens": ["allergen1", "allergen2"],
  "ground_truth": {
    "severity": "Dangerous",
    "allergens_detected": ["allergen1"],
    "contains_product": true,
    "alternatives": {
      "min_count": 3,
      "should_be_safe": true,
      "should_avoid_allergens": ["allergen1", "allergen2"]
    }
  }
}
```

3. Update the `total_cases` in metadata section
4. Run the evaluation

## Metrics Explained

### Allergen Detection Metrics

**Severity Accuracy**
- Percentage of tests where the predicted severity (Safe/Caution/Dangerous/NotDetected) matches ground truth
- **Target:** >90%

**Precision**
- Of all allergens detected, what percentage were actually present?
- Formula: `True Positives / (True Positives + False Positives)`
- **Target:** >85%

**Recall**
- Of all allergens actually present, what percentage were detected?
- Formula: `True Positives / (True Positives + False Negatives)`
- **Target:** >95% (critical for safety!)

**F1 Score**
- Harmonic mean of precision and recall
- Formula: `2 * (Precision * Recall) / (Precision + Recall)`
- **Target:** >90%

**False Negative Rate** ⚠️
- Percentage of allergens that were missed
- Formula: `False Negatives / (True Positives + False Negatives)`
- **Target:** <5% (CRITICAL - missed allergens are dangerous!)

### Alternative Finding Metrics

**Average Alternatives Found**
- Average number of alternatives provided per test
- **Target:** ≥5

**Coverage**
- Percentage of expected alternatives that were found
- **Target:** >80%

**Safe Alternatives**
- Number of alternatives correctly marked as "Safe"
- **Target:** 100% (all suggested alternatives should be safe!)

### Performance Metrics

**Average Latency**
- Average time taken to complete full analysis
- Includes allergen detection (phases 1-3) + alternative finding (phases 4-8)

**Cost Metrics**
- Total API token usage (input + output)
- Estimated cost in USD based on Anthropic pricing
- Cost per test case

## Interpreting Results

### Critical Failures

**False Negatives (Missed Allergens)**
```json
{
  "type": "false_negative",
  "severity": "CRITICAL",
  "message": "Missed allergens: ['peanuts']"
}
```
- **Action:** Investigate why allergen was missed
- **Priority:** HIGH - Safety risk

**Unsafe Alternatives**
```json
{
  "type": "unsafe_alternative",
  "severity": "HIGH",
  "message": "2 alternatives not marked as Safe"
}
```
- **Action:** Review alternative finding logic
- **Priority:** HIGH - Safety risk

**Insufficient Alternatives**
```json
{
  "type": "insufficient_alternatives",
  "severity": "WARNING",
  "message": "Found 2 alternatives, expected 5"
}
```
- **Action:** Review alternative finding coverage
- **Priority:** MEDIUM - User experience issue

## Report Formats

### JSON (Default)
Machine-readable format for automation and CI/CD:
```bash
python -m evaluation.run_evaluation --output results.json
```

### Markdown
Human-readable text format:
```python
from evaluation.report_generator import generate_report
report = generate_report(results, format='markdown')
```

### HTML
Visual dashboard with charts:
```python
from evaluation.report_generator import generate_report
report = generate_report(results, format='html')
with open('report.html', 'w') as f:
    f.write(report)
```

## Best Practices

### 1. Regular Testing
- Run evaluations after any prompt changes
- Track metrics over time to detect regressions

### 2. Diverse Test Cases
- Include edge cases (hidden allergens, derivatives, cross-contamination)
- Test all severity levels (Safe, Caution, Dangerous, NotDetected)
- Include non-product images

### 3. Safety-First Approach
- **Zero tolerance for false negatives** - Missing an allergen is dangerous
- Monitor false negative rate closely
- Investigate any false negatives immediately

### 4. Cost Monitoring
- Track API costs to avoid surprises
- Optimize prompts to reduce token usage
- Balance cost vs accuracy

### 5. Version Control
- Commit test cases to git
- Track evaluation results over time
- Document changes to prompts and their impact on metrics

## Troubleshooting

### "Image file not found"
- Ensure test images are in `evaluation/test_images/`
- Check file paths in `test_cases.json` are correct

### "No module named 'evaluation'"
- Run from `backend/` directory: `cd backend && python -m evaluation.run_evaluation`

### High API Costs
- Run fewer tests during development: `--test-id 001`
- Use estimated token counts (already implemented)
- Consider caching results for unchanged test cases

## File Structure

```
backend/evaluation/
├── README.md                 # This file
├── test_cases.json          # Test dataset
├── metrics.py               # Metrics calculation
├── run_evaluation.py        # Main test runner
├── report_generator.py      # Report generation
└── test_images/             # Test image directory
    ├── .gitkeep
    ├── dangerous_product.jpg
    ├── safe_product.jpg
    ├── caution_product.jpg
    ├── non_product.jpg
    ├── dairy_product.jpg
    └── hidden_allergen.jpg
```

## Example Output

```
================================================================================
EVALUATION COMPLETE
================================================================================
Tests run: 6
Tests passed: 5
Tests failed: 1
Pass rate: 83.33%
Total cost: $0.4200
Average latency: 12.5s
================================================================================
```

## Integration with CI/CD

Add to your CI pipeline:

```bash
# Run evaluation
python -m evaluation.run_evaluation --output results.json

# Check if pass rate meets threshold
pass_rate=$(jq '.metrics.summary.pass_rate_percent' results.json)
if (( $(echo "$pass_rate < 80" | bc -l) )); then
  echo "Evaluation failed: pass rate $pass_rate% < 80%"
  exit 1
fi
```

## Contributing

To add new metrics:

1. Update `metrics.py` with new calculation methods
2. Update `report_generator.py` to include new metrics in reports
3. Update this README with metric explanations

## Support

For issues or questions:
- Check this README first
- Review test case format above
- Ensure images exist and paths are correct
- Run with `--verbose` for detailed logging
