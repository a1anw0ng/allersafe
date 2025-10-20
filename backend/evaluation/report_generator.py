#!/usr/bin/env python3
"""
Report Generator for AllerSafe Evaluation

Generates evaluation reports in various formats (JSON, Markdown, HTML).
"""

import json
from typing import Dict, Any


def generate_report(results: Dict[str, Any], format: str = 'json') -> str:
    """Generate evaluation report

    Args:
        results: Evaluation results dict from EvaluationRunner
        format: Report format ('json', 'markdown', or 'html')

    Returns:
        Formatted report string
    """
    if format == 'json':
        return generate_json_report(results)
    elif format == 'markdown':
        return generate_markdown_report(results)
    elif format == 'html':
        return generate_html_report(results)
    else:
        raise ValueError(f"Unsupported format: {format}")


def generate_json_report(results: Dict[str, Any]) -> str:
    """Generate JSON report

    Args:
        results: Evaluation results dict

    Returns:
        JSON-formatted report string
    """
    return json.dumps(results, indent=2)


def generate_markdown_report(results: Dict[str, Any]) -> str:
    """Generate Markdown report

    Args:
        results: Evaluation results dict

    Returns:
        Markdown-formatted report string
    """
    metrics = results['metrics']
    summary = metrics['summary']
    allergen = metrics['allergen_detection']
    alternatives = metrics['alternatives']
    performance = metrics['performance']
    costs = metrics['costs']

    lines = []
    lines.append("# AllerSafe Evaluation Report")
    lines.append("")
    lines.append(f"**Date:** {results['metadata']['timestamp']}")
    lines.append(f"**Test Cases:** {results['metadata']['test_cases_file']}")
    lines.append(f"**Total Tests:** {results['metadata']['total_tests']}")
    lines.append("")

    # Summary
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- **Tests Passed:** {summary['tests_passed']}/{summary['total_tests']}")
    lines.append(f"- **Pass Rate:** {summary['pass_rate_percent']}%")
    lines.append(f"- **Total Cost:** ${costs['total_cost_usd']:.4f}")
    lines.append(f"- **Average Latency:** {performance['average_latency_seconds']}s")
    lines.append("")

    # Allergen Detection Metrics
    lines.append("## Allergen Detection Metrics")
    lines.append("")
    lines.append(f"- **Severity Accuracy:** {allergen['severity_accuracy_percent']}%")
    lines.append(f"- **Precision:** {allergen['allergen_precision_percent']}%")
    lines.append(f"- **Recall:** {allergen['allergen_recall_percent']}%")
    lines.append(f"- **F1 Score:** {allergen['allergen_f1_score']}")
    lines.append(f"- **False Negative Rate:** {allergen['false_negative_rate_percent']}% ⚠️")
    lines.append("")
    lines.append("### Confusion Matrix")
    lines.append("")
    lines.append("| Actual / Predicted | Safe | Caution | Dangerous | NotDetected |")
    lines.append("|-------------------|------|---------|-----------|-------------|")

    cm = allergen['confusion_matrix']
    for actual in ['Safe', 'Caution', 'Dangerous', 'NotDetected']:
        row = cm[actual]
        lines.append(f"| **{actual}** | {row['Safe']} | {row['Caution']} | {row['Dangerous']} | {row['NotDetected']} |")

    lines.append("")

    # Alternative Finding Metrics
    lines.append("## Alternative Finding Metrics")
    lines.append("")
    lines.append(f"- **Average Alternatives Found:** {alternatives['average_alternatives_found']}")
    lines.append(f"- **Coverage:** {alternatives['coverage_percent']}%")
    lines.append(f"- **Total Alternatives:** {alternatives['total_alternatives_found']}")
    lines.append(f"- **Safe Alternatives:** {alternatives['safe_alternatives']}")
    lines.append("")
    lines.append("### Safety Verification")
    lines.append("")
    lines.append(f"- **Alternatives Verified Safe:** {alternatives['alternatives_verified_safe']}")
    lines.append(f"- **Alternatives Failed Verification:** {alternatives['alternatives_failed_verification']}")
    lines.append(f"- **Safety Verification Rate:** {alternatives['safety_verification_rate_percent']}% ✅")
    lines.append("")

    # Performance Metrics
    lines.append("## Performance Metrics")
    lines.append("")
    lines.append(f"- **Average Latency:** {performance['average_latency_seconds']}s")
    lines.append(f"- **Min Latency:** {performance['min_latency_seconds']}s")
    lines.append(f"- **Max Latency:** {performance['max_latency_seconds']}s")
    lines.append(f"- **Total Time:** {performance['total_time_seconds']}s")
    lines.append("")

    # Cost Metrics
    lines.append("## Cost Metrics")
    lines.append("")
    lines.append(f"- **Total Cost:** ${costs['total_cost_usd']:.4f}")
    lines.append(f"- **Average Cost per Test:** ${costs['average_cost_per_test_usd']:.4f}")
    lines.append(f"- **Total Tokens:** {costs['total_tokens']:,}")
    lines.append(f"  - Input: {costs['total_input_tokens']:,}")
    lines.append(f"  - Output: {costs['total_output_tokens']:,}")
    lines.append("")

    # Failures
    if metrics['failures']:
        lines.append("## Failures")
        lines.append("")
        for failure in metrics['failures']:
            lines.append(f"### Test {failure['test_id']} - {failure['type']}")
            lines.append(f"**Severity:** {failure['severity']}")
            lines.append(f"**Message:** {failure['message']}")
            lines.append("")

    # Individual Test Results
    lines.append("## Individual Test Results")
    lines.append("")
    for test_result in results['test_results']:
        test_id = test_result['test_id']
        status = test_result['status']

        if status == 'error':
            lines.append(f"### Test {test_id} - ❌ ERROR")
            lines.append(f"**Error:** {test_result['error']}")
        else:
            predictions = test_result['predictions']
            correct = test_result['correct']
            severity_icon = "✅" if correct['severity'] else "❌"
            allergens_icon = "✅" if correct['allergens'] else "❌"

            lines.append(f"### Test {test_id} - {severity_icon}")
            lines.append(f"- **Predicted Severity:** {predictions['severity']} {severity_icon}")
            lines.append(f"- **Predicted Allergens:** {predictions['allergens_detected']} {allergens_icon}")
            lines.append(f"- **Alternatives Found:** {predictions['alternatives_count']}")
            lines.append(f"- **Latency:** {test_result['latency_seconds']}s")

        lines.append("")

    return "\n".join(lines)


def generate_html_report(results: Dict[str, Any]) -> str:
    """Generate HTML report

    Args:
        results: Evaluation results dict

    Returns:
        HTML-formatted report string
    """
    # Simple HTML report (can be enhanced with charts, styling, etc.)
    metrics = results['metrics']
    summary = metrics['summary']

    html = f"""<!DOCTYPE html>
<html>
<head>
    <title>AllerSafe Evaluation Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        h1 {{ color: #2c3e50; }}
        h2 {{ color: #34495e; border-bottom: 2px solid #3498db; padding-bottom: 10px; }}
        .metric {{ background: #ecf0f1; padding: 15px; margin: 10px 0; border-radius: 5px; }}
        .success {{ color: #27ae60; }}
        .warning {{ color: #f39c12; }}
        .error {{ color: #e74c3c; }}
        table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
        th, td {{ border: 1px solid #bdc3c7; padding: 12px; text-align: left; }}
        th {{ background-color: #3498db; color: white; }}
        tr:nth-child(even) {{ background-color: #ecf0f1; }}
    </style>
</head>
<body>
    <h1>AllerSafe Evaluation Report</h1>
    <p><strong>Date:</strong> {results['metadata']['timestamp']}</p>
    <p><strong>Total Tests:</strong> {results['metadata']['total_tests']}</p>

    <h2>Summary</h2>
    <div class="metric">
        <p><strong>Pass Rate:</strong> <span class="{'success' if summary['pass_rate_percent'] >= 80 else 'warning'}">{summary['pass_rate_percent']}%</span></p>
        <p><strong>Tests Passed:</strong> {summary['tests_passed']}/{summary['total_tests']}</p>
        <p><strong>Total Cost:</strong> ${metrics['costs']['total_cost_usd']:.4f}</p>
    </div>

    <h2>Metrics</h2>
    <table>
        <tr>
            <th>Metric</th>
            <th>Value</th>
        </tr>
        <tr>
            <td>Severity Accuracy</td>
            <td>{metrics['allergen_detection']['severity_accuracy_percent']}%</td>
        </tr>
        <tr>
            <td>Allergen Precision</td>
            <td>{metrics['allergen_detection']['allergen_precision_percent']}%</td>
        </tr>
        <tr>
            <td>Allergen Recall</td>
            <td>{metrics['allergen_detection']['allergen_recall_percent']}%</td>
        </tr>
        <tr>
            <td>False Negative Rate</td>
            <td class="{'error' if metrics['allergen_detection']['false_negative_rate_percent'] > 5 else 'success'}">{metrics['allergen_detection']['false_negative_rate_percent']}%</td>
        </tr>
        <tr>
            <td>Average Latency</td>
            <td>{metrics['performance']['average_latency_seconds']}s</td>
        </tr>
        <tr>
            <td>Safety Verification Rate</td>
            <td class="{'success' if metrics['alternatives']['safety_verification_rate_percent'] >= 95 else 'warning'}">{metrics['alternatives']['safety_verification_rate_percent']}%</td>
        </tr>
    </table>

    <h2>Test Results</h2>
    <table>
        <tr>
            <th>Test ID</th>
            <th>Status</th>
            <th>Severity Correct</th>
            <th>Allergens Correct</th>
            <th>Latency</th>
        </tr>
"""

    for test_result in results['test_results']:
        test_id = test_result['test_id']
        if test_result['status'] == 'error':
            html += f"""
        <tr>
            <td>{test_id}</td>
            <td class="error">ERROR</td>
            <td>-</td>
            <td>-</td>
            <td>-</td>
        </tr>
"""
        else:
            correct = test_result['correct']
            severity_class = 'success' if correct['severity'] else 'error'
            allergens_class = 'success' if correct['allergens'] else 'error'

            html += f"""
        <tr>
            <td>{test_id}</td>
            <td class="success">SUCCESS</td>
            <td class="{severity_class}">{'✓' if correct['severity'] else '✗'}</td>
            <td class="{allergens_class}">{'✓' if correct['allergens'] else '✗'}</td>
            <td>{test_result['latency_seconds']}s</td>
        </tr>
"""

    html += """
    </table>
</body>
</html>
"""

    return html
