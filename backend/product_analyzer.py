#!/usr/bin/env python3
"""
Unified Product Analyzer - Orchestrates allergen detection and alternative finding

This module provides a single entry point for complete product analysis:
1. Allergen Detection (3 phases)
2. Alternative Finding (5 phases)

Total: 8-phase comprehensive analysis
"""

import sys
import os
import json
import time
from typing import List, Dict

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from allergen_detector.allergen_detector import detect_allergens
from alternative_finder.alternative_finder import find_alternatives
from utils import clean_sources_list

def analyze_product(image_path: str, allergens: List[str], verbose: bool = True) -> Dict:
    """Complete product analysis: allergen detection + alternative finding

    This orchestrates both modules to provide comprehensive product analysis:
    - Phase 1-3: Allergen detection with web research
    - Phase 4-8: Alternative product finding with web research

    Args:
        image_path: Path to product image
        allergens: List of allergens to avoid (e.g., ["nuts", "dairy"])
        verbose: If True, print detailed output during analysis

    Returns:
        Dict containing:
        {
            "allergen_analysis": {
                "severity": "Safe|Caution|Dangerous|NotDetected",
                "allergens_detected": [...],
                "warnings": "...",
                "product_name": "...",
                "sources": [...]
            },
            "alternatives": [
                {
                    "alternative_name": "...",
                    "company": "...",
                    "purchase_links": [...],
                    "price": "...",
                    "warning_level": "Safe|Caution",
                    "tags": [...],
                    "sources": [...]
                }
            ],
            "summary": {
                "original_product": "...",
                "safety_status": "...",
                "allergens_found": [...],
                "alternatives_found": 5,
                "safe_alternatives": 3,
                "caution_alternatives": 2,
                "total_sources": 15,
                "analysis_time": 45.2
            }
        }
    """
    start_time = time.time()

    if verbose:
        print("=" * 80)
        print("PRODUCT ANALYSIS - Full 8-Phase Pipeline")
        print("=" * 80)
        print(f"Image: {image_path}")
        print(f"Allergens to avoid: {', '.join(allergens) if allergens else 'None'}")
        print("=" * 80)
        print()

    # ============================================================
    # PHASE 1-3: Allergen Detection
    # ============================================================
    if verbose:
        print("STAGE 1: ALLERGEN DETECTION (Phases 1-3)")
        print("-" * 80)

    allergen_result = detect_allergens(image_path, allergens)

    if verbose:
        print("\nAllergen Detection Complete!")
        print(f"  Product: {allergen_result.get('product_name', 'Unknown')}")
        print(f"  Safety: {allergen_result.get('severity', 'Unknown')}")
        print(f"  Allergens Detected: {', '.join(allergen_result.get('allergens_detected', [])) or 'None'}")
        print(f"  Sources Found: {len(allergen_result.get('sources', []))}")
        print()

    # ============================================================
    # PHASE 4-8: Alternative Finding
    # ============================================================
    if verbose:
        print("STAGE 2: ALTERNATIVE FINDING (Phases 4-8)")
        print("-" * 80)

    alternatives = find_alternatives(image_path, allergens, allergen_result)

    if verbose:
        print("\nAlternative Finding Complete!")
        print(f"  Alternatives Found: {len(alternatives)}")

        # Count safe vs caution
        safe_count = sum(1 for alt in alternatives if alt.get('warning_level') == 'Safe')
        caution_count = sum(1 for alt in alternatives if alt.get('warning_level') == 'Caution')
        print(f"  Safe: {safe_count}, Caution: {caution_count}")
        print()

    # ============================================================
    # Generate Summary
    # ============================================================
    end_time = time.time()
    analysis_time = round(end_time - start_time, 2)

    # Collect all unique sources and clean (removes invalid/redirect URLs)
    all_sources = allergen_result.get('sources', [])
    for alt in alternatives:
        all_sources.extend(alt.get('sources', []))

    # Clean and deduplicate sources
    unique_sources = clean_sources_list(all_sources)

    safe_count = sum(1 for alt in alternatives if alt.get('warning_level') == 'Safe')
    caution_count = sum(1 for alt in alternatives if alt.get('warning_level') == 'Caution')

    result = {
        "allergen_analysis": allergen_result,
        "alternatives": alternatives,
        "summary": {
            "original_product": allergen_result.get('product_name', 'Unknown'),
            "safety_status": allergen_result.get('severity', 'Unknown'),
            "allergens_found": allergen_result.get('allergens_detected', []),
            "alternatives_found": len(alternatives),
            "safe_alternatives": safe_count,
            "caution_alternatives": caution_count,
            "total_sources": len(unique_sources),
            "analysis_time_seconds": analysis_time
        },
        "all_sources": unique_sources
    }

    if verbose:
        print("=" * 80)
        print("ANALYSIS COMPLETE")
        print("=" * 80)
        print(f"Total Analysis Time: {analysis_time} seconds")
        print(f"Total Unique Sources: {len(unique_sources)}")
        print()

    return result

if __name__ == "__main__":
    # Test with example values
    image_path = "allergen_detector/test_product_caution.jpg"
    allergens = ["nuts", "dairy"]

    result = analyze_product(image_path, allergens, verbose=True)

    print("=" * 80)
    print("FULL RESULTS (JSON)")
    print("=" * 80)
    print(json.dumps(result, indent=2))
