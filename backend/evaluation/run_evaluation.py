#!/usr/bin/env python3
"""
AllerSafe Evaluation Runner

Runs evaluation tests on the allergen detection and alternative finding pipeline.
Generates comprehensive metrics and reports.

Usage:
    python -m evaluation.run_evaluation
    python -m evaluation.run_evaluation --test-id 001
    python -m evaluation.run_evaluation --verbose --output results.json
"""

import sys
import os
import json
import time
import argparse
from pathlib import Path
from typing import Dict, List, Any, Optional

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from product_analyzer import analyze_product
from evaluation.metrics import EvaluationMetrics
from evaluation.report_generator import generate_report


class EvaluationRunner:
    """Run evaluation tests and collect metrics"""

    def __init__(self, test_cases_path: str, verbose: bool = False):
        """
        Args:
            test_cases_path: Path to test cases JSON file
            verbose: Whether to print detailed output
        """
        self.test_cases_path = test_cases_path
        self.verbose = verbose
        self.metrics = EvaluationMetrics()
        self.results = []

    def load_test_cases(self) -> List[Dict[str, Any]]:
        """Load test cases from JSON file

        Returns:
            List of test case dicts
        """
        if not os.path.exists(self.test_cases_path):
            raise FileNotFoundError(f"Test cases file not found: {self.test_cases_path}")

        with open(self.test_cases_path, 'r') as f:
            data = json.load(f)

        test_cases = data.get('test_cases', [])
        if self.verbose:
            print(f"Loaded {len(test_cases)} test cases from {self.test_cases_path}")

        return test_cases

    def run_single_test(self, test_case: Dict[str, Any]) -> Dict[str, Any]:
        """Run a single test case

        Args:
            test_case: Test case configuration

        Returns:
            Test result with predictions and metrics
        """
        test_id = test_case['test_id']
        image_path = test_case['image_path']
        user_allergens = test_case['user_allergens']
        ground_truth = test_case['ground_truth']

        if self.verbose:
            print(f"\n{'='*80}")
            print(f"Running Test {test_id}: {test_case['name']}")
            print(f"{'='*80}")
            print(f"Image: {image_path}")
            print(f"User allergens: {user_allergens}")
            print(f"Expected severity: {ground_truth['severity']}")

        # Check if image exists
        if not os.path.exists(image_path):
            error_msg = f"Image file not found: {image_path}"
            if self.verbose:
                print(f"❌ ERROR: {error_msg}")
            return {
                "test_id": test_id,
                "status": "error",
                "error": error_msg,
                "ground_truth": ground_truth
            }

        # Run analysis with timing
        start_time = time.time()

        try:
            result = analyze_product(image_path, user_allergens, verbose=self.verbose)
            end_time = time.time()
            latency = end_time - start_time

            allergen_analysis = result['allergen_analysis']
            alternatives = result['alternatives']

            # Extract predictions
            predicted_severity = allergen_analysis.get('severity', 'Unknown')
            predicted_allergens = allergen_analysis.get('allergens_detected', [])

            if self.verbose:
                print(f"\n{'─'*80}")
                print(f"RESULTS:")
                print(f"  Predicted severity: {predicted_severity}")
                print(f"  Predicted allergens: {predicted_allergens}")
                print(f"  Alternatives found: {len(alternatives)}")
                print(f"  Time taken: {latency:.2f}s")
                print(f"{'─'*80}")

            # Check correctness
            severity_correct = predicted_severity == ground_truth['severity']
            allergens_correct = set(a.lower() for a in predicted_allergens) == set(a.lower() for a in ground_truth['allergens_detected'])

            if self.verbose:
                if severity_correct:
                    print(f"✅ Severity classification: CORRECT")
                else:
                    print(f"❌ Severity classification: INCORRECT (expected {ground_truth['severity']})")

                if allergens_correct:
                    print(f"✅ Allergen detection: CORRECT")
                else:
                    print(f"❌ Allergen detection: INCORRECT (expected {ground_truth['allergens_detected']})")

            # Update metrics
            self.metrics.add_allergen_detection_result(
                test_id=test_id,
                predicted_severity=predicted_severity,
                expected_severity=ground_truth['severity'],
                predicted_allergens=predicted_allergens,
                expected_allergens=ground_truth['allergens_detected']
            )

            # Add alternative metrics if applicable
            alt_ground_truth = ground_truth.get('alternatives', {})
            if alt_ground_truth.get('min_count', 0) > 0:
                self.metrics.add_alternative_result(
                    test_id=test_id,
                    alternatives=alternatives,
                    min_expected=alt_ground_truth['min_count'],
                    should_be_safe=alt_ground_truth.get('should_be_safe', True),
                    avoid_allergens=alt_ground_truth.get('should_avoid_allergens', [])
                )

            # Add latency
            self.metrics.add_latency(test_id, latency)

            # Estimate token usage (rough estimate based on typical usage)
            # You can enhance this by actually tracking token usage from the API
            # For now, we'll use rough estimates
            estimated_input_tokens = 5000  # Typical for image + text
            estimated_output_tokens = 2000  # Typical for detailed analysis
            self.metrics.add_cost(test_id, estimated_input_tokens, estimated_output_tokens)

            return {
                "test_id": test_id,
                "status": "success",
                "predictions": {
                    "severity": predicted_severity,
                    "allergens_detected": predicted_allergens,
                    "alternatives_count": len(alternatives)
                },
                "ground_truth": ground_truth,
                "correct": {
                    "severity": severity_correct,
                    "allergens": allergens_correct
                },
                "latency_seconds": round(latency, 2),
                "full_result": result
            }

        except Exception as e:
            error_msg = f"Error running test: {str(e)}"
            if self.verbose:
                print(f"❌ ERROR: {error_msg}")
                import traceback
                traceback.print_exc()

            return {
                "test_id": test_id,
                "status": "error",
                "error": error_msg,
                "ground_truth": ground_truth
            }

    def run_all_tests(self, test_ids: Optional[List[str]] = None) -> Dict[str, Any]:
        """Run all test cases

        Args:
            test_ids: Optional list of specific test IDs to run. If None, run all tests.

        Returns:
            Evaluation results with metrics
        """
        test_cases = self.load_test_cases()

        # Filter test cases if specific IDs provided
        if test_ids:
            test_cases = [tc for tc in test_cases if tc['test_id'] in test_ids]
            if self.verbose:
                print(f"Running {len(test_cases)} specific test(s): {test_ids}")

        # Run each test
        for i, test_case in enumerate(test_cases, 1):
            if self.verbose:
                print(f"\n\nTest {i}/{len(test_cases)}")

            result = self.run_single_test(test_case)
            self.results.append(result)

        # Calculate summary metrics
        summary = self.metrics.calculate_summary()

        if self.verbose:
            print(f"\n\n{'='*80}")
            print("EVALUATION COMPLETE")
            print(f"{'='*80}")
            print(f"Tests run: {summary['summary']['total_tests']}")
            print(f"Tests passed: {summary['summary']['tests_passed']}")
            print(f"Tests failed: {summary['summary']['tests_failed']}")
            print(f"Pass rate: {summary['summary']['pass_rate_percent']}%")
            print(f"Total cost: ${summary['costs']['total_cost_usd']:.4f}")
            print(f"Average latency: {summary['performance']['average_latency_seconds']}s")
            print(f"{'='*80}\n")

        return {
            "metadata": {
                "test_cases_file": self.test_cases_path,
                "total_tests": len(test_cases),
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            },
            "metrics": summary,
            "test_results": self.results
        }


def main():
    """Main entry point for evaluation runner"""
    parser = argparse.ArgumentParser(
        description="Run AllerSafe evaluation tests"
    )
    parser.add_argument(
        '--test-cases',
        type=str,
        default='evaluation/test_cases.json',
        help='Path to test cases JSON file (default: evaluation/test_cases.json)'
    )
    parser.add_argument(
        '--test-id',
        type=str,
        action='append',
        help='Specific test ID to run (can be used multiple times)'
    )
    parser.add_argument(
        '--output',
        type=str,
        help='Output file for results (default: print to stdout)'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Print detailed output'
    )

    args = parser.parse_args()

    # Create runner
    runner = EvaluationRunner(
        test_cases_path=args.test_cases,
        verbose=args.verbose
    )

    # Run tests
    try:
        results = runner.run_all_tests(test_ids=args.test_id)

        # Generate report
        report = generate_report(results, format='json')

        # Output results
        if args.output:
            with open(args.output, 'w') as f:
                f.write(report)
            print(f"Results written to {args.output}")
        else:
            print(report)

    except Exception as e:
        print(f"Error running evaluation: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
