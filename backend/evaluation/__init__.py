"""
AllerSafe Evaluation Package

Comprehensive evaluation framework for testing allergen detection
and alternative finding pipelines.
"""

from .metrics import EvaluationMetrics
from .report_generator import generate_report

__all__ = ['EvaluationMetrics', 'generate_report']
__version__ = '1.0.0'
