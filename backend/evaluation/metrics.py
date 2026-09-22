#!/usr/bin/env python3
"""
Evaluation Metrics for AllerSafe LLM System

Calculates metrics for:
- Allergen detection accuracy (Safe/Caution/Dangerous/NotDetected)
- Alternative finding quality
- System performance (latency, cost)
"""

from typing import Dict, List, Any


class EvaluationMetrics:
    """Calculate evaluation metrics for AllerSafe system"""

    # LLM Model pricing (as of 2025)
    # Google Gemini: https://ai.google.dev/gemini-api/docs/pricing
    # Anthropic Claude: https://www.anthropic.com/pricing
    PRICING = {
        "gemini-2.5-flash": {
            "input_per_mtok": 0.30,   # $0.30 per million input tokens
            "output_per_mtok": 2.50   # $2.50 per million output tokens
        },
        "claude-3-5-sonnet-20241022": {
            "input_per_mtok": 3.00,   # $3 per million input tokens
            "output_per_mtok": 15.00  # $15 per million output tokens
        },
        "claude-3-5-haiku-20241022": {
            "input_per_mtok": 0.80,
            "output_per_mtok": 4.00
        },
        "claude-haiku-4-5-20251001": {
            "input_per_mtok": 1.00,
            "output_per_mtok": 5.00
        }
    }

    def __init__(self):
        self.reset()

    def reset(self):
        """Reset all metrics"""
        self.total_tests = 0
        self.severity_correct = 0
        self.allergen_tp = 0  # True positives
        self.allergen_fp = 0  # False positives
        self.allergen_fn = 0  # False negatives
        self.confusion_matrix = {
            "Safe": {"Safe": 0, "Caution": 0, "Dangerous": 0, "NotDetected": 0},
            "Caution": {"Safe": 0, "Caution": 0, "Dangerous": 0, "NotDetected": 0},
            "Dangerous": {"Safe": 0, "Caution": 0, "Dangerous": 0, "NotDetected": 0},
            "NotDetected": {"Safe": 0, "Caution": 0, "Dangerous": 0, "NotDetected": 0}
        }
        self.alternative_metrics = {
            "total_tests_with_alternatives": 0,
            "safe_alternatives_correct": 0,
            "alternatives_found": 0,
            "expected_alternatives": 0,
            "alternatives_verified_safe": 0,
            "alternatives_failed_verification": 0
        }
        self.latency_metrics = {
            "total_time": 0,
            "min_time": float('inf'),
            "max_time": 0,
            "times": []
        }
        self.cost_metrics = {
            "total_input_tokens": 0,
            "total_output_tokens": 0,
            "total_cost_usd": 0.0,
            "per_test_costs": []
        }
        self.failures = []

    def add_allergen_detection_result(
        self,
        test_id: str,
        predicted_severity: str,
        expected_severity: str,
        predicted_allergens: List[str],
        expected_allergens: List[str]
    ):
        """Add allergen detection result for evaluation

        Args:
            test_id: Test case identifier
            predicted_severity: Predicted severity (Safe/Caution/Dangerous/NotDetected)
            expected_severity: Ground truth severity
            predicted_allergens: List of allergens detected by system
            expected_allergens: List of allergens that should be detected
        """
        self.total_tests += 1

        # Severity accuracy
        if predicted_severity == expected_severity:
            self.severity_correct += 1

        # Update confusion matrix
        if expected_severity in self.confusion_matrix:
            if predicted_severity in self.confusion_matrix[expected_severity]:
                self.confusion_matrix[expected_severity][predicted_severity] += 1

        # Allergen detection metrics (precision/recall)
        predicted_set = set(a.lower() for a in predicted_allergens)
        expected_set = set(a.lower() for a in expected_allergens)

        # True positives: allergens correctly identified
        tp = len(predicted_set & expected_set)
        # False positives: allergens detected but not actually present
        fp = len(predicted_set - expected_set)
        # False negatives: allergens missed (CRITICAL for safety!)
        fn = len(expected_set - predicted_set)

        self.allergen_tp += tp
        self.allergen_fp += fp
        self.allergen_fn += fn

        # Track critical false negatives
        if fn > 0:
            self.failures.append({
                "test_id": test_id,
                "type": "false_negative",
                "severity": "CRITICAL",
                "message": f"Missed allergens: {list(expected_set - predicted_set)}",
                "predicted": list(predicted_set),
                "expected": list(expected_set)
            })

    def _verify_alternative_safety(
        self,
        alternative: Dict[str, Any],
        avoid_allergens: List[str]
    ) -> tuple[bool, List[str]]:
        """Verify an alternative doesn't contain avoided allergens

        Args:
            alternative: Alternative product dict
            avoid_allergens: List of allergens to avoid

        Returns:
            Tuple of (is_safe, found_allergens)
        """
        found_allergens = []

        # Check alternative name for allergen keywords
        alt_name = alternative.get("alternative_name", "").lower()

        # Check tags for allergen keywords
        tags = [tag.lower() for tag in alternative.get("tags", [])]

        # Check reasoning for allergen keywords
        reasoning = alternative.get("reasoning", "").lower()

        # Common allergen keywords mapping
        allergen_keywords = {
            "peanuts": ["peanut", "peanuts"],
            "peanut": ["peanut", "peanuts"],
            "dairy": ["dairy", "milk", "cheese", "butter", "cream", "whey", "casein", "lactose"],
            "milk": ["dairy", "milk", "cheese", "butter", "cream", "whey", "casein", "lactose"],
            "tree nuts": ["almond", "cashew", "walnut", "pecan", "hazelnut", "pistachio", "tree nut"],
            "tree nut": ["almond", "cashew", "walnut", "pecan", "hazelnut", "pistachio", "tree nut"],
            "eggs": ["egg", "eggs"],
            "egg": ["egg", "eggs"],
            "soy": ["soy", "soya"],
            "wheat": ["wheat", "gluten"],
            "gluten": ["wheat", "gluten"],
            "shellfish": ["shellfish", "shrimp", "crab", "lobster"],
            "fish": ["fish", "salmon", "tuna", "cod"]
        }

        # Check each allergen to avoid
        for allergen in avoid_allergens:
            allergen_lower = allergen.lower()
            keywords = allergen_keywords.get(allergen_lower, [allergen_lower])

            # Check if any keyword appears in name, tags, or reasoning
            for keyword in keywords:
                # Skip if it's explicitly marked as free from this allergen
                if f"{keyword}-free" in alt_name or f"{keyword}-free" in tags or f"{keyword}-free" in reasoning:
                    continue

                # Skip negations like "milkless", "eggless", etc.
                if f"{keyword}less" in alt_name or f"{keyword}less" in reasoning:
                    continue

                # Check for positive mentions (contains the allergen)
                if (keyword in alt_name or
                    any(keyword in tag for tag in tags) or
                    (keyword in reasoning and "free" not in reasoning and "without" not in reasoning)):
                    # Additional check: make sure it's not a "butter" alternative (like sunflower butter, sunbutter)
                    if keyword == "butter" and any(safe_word in alt_name for safe_word in ["sunflower", "sunbutter", "sun butter", "seed", "almond", "cashew"]):
                        continue
                    # Skip if it's in a dairy-free context
                    if keyword in ["milk", "dairy", "butter", "cheese", "cream"] and ("dairy-free" in alt_name or "dairy-free" in tags or "dairy free" in reasoning):
                        continue
                    found_allergens.append(allergen)
                    break

        is_safe = len(found_allergens) == 0
        return is_safe, found_allergens

    def add_alternative_result(
        self,
        test_id: str,
        alternatives: List[Dict[str, Any]],
        min_expected: int,
        should_be_safe: bool,
        avoid_allergens: List[str]
    ):
        """Add alternative finding result for evaluation

        Args:
            test_id: Test case identifier
            alternatives: List of alternatives found by system
            min_expected: Minimum number of alternatives expected
            should_be_safe: Whether alternatives should be safe
            avoid_allergens: Allergens that should be avoided
        """
        self.alternative_metrics["total_tests_with_alternatives"] += 1
        self.alternative_metrics["alternatives_found"] += len(alternatives)
        self.alternative_metrics["expected_alternatives"] += min_expected

        # Check if enough alternatives were found
        if len(alternatives) < min_expected:
            self.failures.append({
                "test_id": test_id,
                "type": "insufficient_alternatives",
                "severity": "WARNING",
                "message": f"Found {len(alternatives)} alternatives, expected {min_expected}",
                "found": len(alternatives),
                "expected": min_expected
            })

        # Check safety of alternatives
        if should_be_safe:
            safe_count = sum(1 for alt in alternatives if alt.get("warning_level") == "Safe")
            self.alternative_metrics["safe_alternatives_correct"] += safe_count

            # Flag alternatives that are not safe when they should be
            unsafe = [alt for alt in alternatives if alt.get("warning_level") != "Safe"]
            if unsafe:
                self.failures.append({
                    "test_id": test_id,
                    "type": "unsafe_alternative",
                    "severity": "HIGH",
                    "message": f"{len(unsafe)} alternatives not marked as Safe",
                    "unsafe_products": [alt.get("alternative_name") for alt in unsafe]
                })

        # Verify alternatives don't contain avoided allergens
        for alt in alternatives:
            is_safe, found_allergens = self._verify_alternative_safety(alt, avoid_allergens)

            if is_safe:
                self.alternative_metrics["alternatives_verified_safe"] += 1
            else:
                self.alternative_metrics["alternatives_failed_verification"] += 1

                # Flag alternatives that contain allergens they should avoid
                self.failures.append({
                    "test_id": test_id,
                    "type": "alternative_contains_allergen",
                    "severity": "CRITICAL",
                    "message": f"Alternative may contain avoided allergens: {found_allergens}",
                    "alternative_name": alt.get("alternative_name"),
                    "company": alt.get("company"),
                    "found_allergens": found_allergens,
                    "avoid_allergens": avoid_allergens
                })

    def add_latency(self, test_id: str, latency_seconds: float):
        """Record test latency

        Args:
            test_id: Test case identifier
            latency_seconds: Time taken for test in seconds
        """
        self.latency_metrics["total_time"] += latency_seconds
        self.latency_metrics["min_time"] = min(self.latency_metrics["min_time"], latency_seconds)
        self.latency_metrics["max_time"] = max(self.latency_metrics["max_time"], latency_seconds)
        self.latency_metrics["times"].append(latency_seconds)

    def add_cost(
        self,
        test_id: str,
        input_tokens: int,
        output_tokens: int,
        model: str = "claude-haiku-4-5-20251001"
    ):
        """Record API cost for test

        Args:
            test_id: Test case identifier
            input_tokens: Number of input tokens used
            output_tokens: Number of output tokens used
            model: Model name for pricing (default: claude-haiku-4-5-20251001)
        """
        self.cost_metrics["total_input_tokens"] += input_tokens
        self.cost_metrics["total_output_tokens"] += output_tokens

        # Calculate cost
        if model in self.PRICING:
            pricing = self.PRICING[model]
            input_cost = (input_tokens / 1_000_000) * pricing["input_per_mtok"]
            output_cost = (output_tokens / 1_000_000) * pricing["output_per_mtok"]
            test_cost = input_cost + output_cost

            self.cost_metrics["total_cost_usd"] += test_cost
            self.cost_metrics["per_test_costs"].append({
                "test_id": test_id,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "cost_usd": round(test_cost, 4)
            })

    def calculate_summary(self) -> Dict[str, Any]:
        """Calculate summary metrics

        Returns:
            Dict with all calculated metrics
        """
        # Severity accuracy
        severity_accuracy = (self.severity_correct / self.total_tests * 100) if self.total_tests > 0 else 0

        # Allergen detection precision/recall
        precision = (self.allergen_tp / (self.allergen_tp + self.allergen_fp) * 100) if (self.allergen_tp + self.allergen_fp) > 0 else 0
        recall = (self.allergen_tp / (self.allergen_tp + self.allergen_fn) * 100) if (self.allergen_tp + self.allergen_fn) > 0 else 0
        f1_score = (2 * precision * recall / (precision + recall)) if (precision + recall) > 0 else 0

        # False negative rate (CRITICAL metric)
        fn_rate = (self.allergen_fn / (self.allergen_tp + self.allergen_fn) * 100) if (self.allergen_tp + self.allergen_fn) > 0 else 0

        # Alternative metrics
        avg_alternatives_found = (
            self.alternative_metrics["alternatives_found"] /
            self.alternative_metrics["total_tests_with_alternatives"]
        ) if self.alternative_metrics["total_tests_with_alternatives"] > 0 else 0

        alternative_coverage = (
            self.alternative_metrics["alternatives_found"] /
            self.alternative_metrics["expected_alternatives"] * 100
        ) if self.alternative_metrics["expected_alternatives"] > 0 else 0

        # Safety verification rate
        total_alternatives_checked = (
            self.alternative_metrics["alternatives_verified_safe"] +
            self.alternative_metrics["alternatives_failed_verification"]
        )
        safety_verification_rate = (
            self.alternative_metrics["alternatives_verified_safe"] /
            total_alternatives_checked * 100
        ) if total_alternatives_checked > 0 else 0

        # Latency metrics
        avg_latency = (
            self.latency_metrics["total_time"] / len(self.latency_metrics["times"])
        ) if self.latency_metrics["times"] else 0

        # Cost metrics
        avg_cost_per_test = (
            self.cost_metrics["total_cost_usd"] / self.total_tests
        ) if self.total_tests > 0 else 0

        return {
            "summary": {
                "total_tests": self.total_tests,
                "tests_passed": self.severity_correct,
                "tests_failed": self.total_tests - self.severity_correct,
                "pass_rate_percent": round(severity_accuracy, 2)
            },
            "allergen_detection": {
                "severity_accuracy_percent": round(severity_accuracy, 2),
                "allergen_precision_percent": round(precision, 2),
                "allergen_recall_percent": round(recall, 2),
                "allergen_f1_score": round(f1_score, 2),
                "false_negative_rate_percent": round(fn_rate, 2),
                "confusion_matrix": self.confusion_matrix,
                "true_positives": self.allergen_tp,
                "false_positives": self.allergen_fp,
                "false_negatives": self.allergen_fn
            },
            "alternatives": {
                "average_alternatives_found": round(avg_alternatives_found, 2),
                "coverage_percent": round(alternative_coverage, 2),
                "total_alternatives_found": self.alternative_metrics["alternatives_found"],
                "safe_alternatives": self.alternative_metrics["safe_alternatives_correct"],
                "alternatives_verified_safe": self.alternative_metrics["alternatives_verified_safe"],
                "alternatives_failed_verification": self.alternative_metrics["alternatives_failed_verification"],
                "safety_verification_rate_percent": round(safety_verification_rate, 2)
            },
            "performance": {
                "average_latency_seconds": round(avg_latency, 2),
                "min_latency_seconds": round(self.latency_metrics["min_time"], 2) if self.latency_metrics["min_time"] != float('inf') else 0,
                "max_latency_seconds": round(self.latency_metrics["max_time"], 2),
                "total_time_seconds": round(self.latency_metrics["total_time"], 2)
            },
            "costs": {
                "total_input_tokens": self.cost_metrics["total_input_tokens"],
                "total_output_tokens": self.cost_metrics["total_output_tokens"],
                "total_tokens": self.cost_metrics["total_input_tokens"] + self.cost_metrics["total_output_tokens"],
                "total_cost_usd": round(self.cost_metrics["total_cost_usd"], 4),
                "average_cost_per_test_usd": round(avg_cost_per_test, 4),
                "per_test_breakdown": self.cost_metrics["per_test_costs"]
            },
            "failures": self.failures
        }
