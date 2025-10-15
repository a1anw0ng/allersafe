#!/usr/bin/env python3
"""Test script for alternative_finder with multi-phase approach"""

import sys
import os
import json

# Add parent directory to path to import allergen_detector
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from alternative_finder import find_alternatives
from allergen_detector.allergen_detector import detect_allergens

def test_alternative_finder_standalone():
    """Test alternative_finder without allergen_detector results"""
    print("=" * 80)
    print("TEST 1: Alternative Finder (Standalone - No Allergen Detection)")
    print("=" * 80)

    image_path = "../allergen_detector/test_product_caution.jpg"
    allergens = ["nuts", "dairy"]

    # Test without allergen_result
    alternatives = find_alternatives(image_path, allergens)

    print("\n" + "=" * 80)
    print("RESULTS:")
    print("=" * 80)
    print(json.dumps(alternatives, indent=2))
    print("\n")

def test_full_pipeline():
    """Test the full pipeline: allergen_detector → alternative_finder"""
    print("=" * 80)
    print("TEST 2: Full Pipeline (Allergen Detection → Alternative Finder)")
    print("=" * 80)

    image_path = "../allergen_detector/test_product_caution.jpg"
    allergens = ["nuts", "dairy"]

    # Step 1: Run allergen detection
    print("\nSTEP 1: Running Allergen Detection...")
    print("-" * 80)
    allergen_result = detect_allergens(image_path, allergens)

    print("\nAllergen Detection Result:")
    print(json.dumps(allergen_result, indent=2))

    # Step 2: Find alternatives using allergen detection results
    print("\n" + "-" * 80)
    print("STEP 2: Finding Safe Alternatives...")
    print("-" * 80)
    alternatives = find_alternatives(image_path, allergens, allergen_result)

    print("\n" + "=" * 80)
    print("FINAL RESULTS - SAFE ALTERNATIVES:")
    print("=" * 80)
    print(json.dumps(alternatives, indent=2))

    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY:")
    print("=" * 80)
    print(f"Original Product: {allergen_result.get('product_name', 'Unknown')}")
    print(f"Safety Level: {allergen_result.get('severity', 'Unknown')}")
    print(f"Allergens Detected: {', '.join(allergen_result.get('allergens_detected', []))}")
    print(f"Number of Alternatives Found: {len(alternatives)}")

    if alternatives:
        safe_count = sum(1 for alt in alternatives if alt.get('warning_level') == 'Safe')
        caution_count = sum(1 for alt in alternatives if alt.get('warning_level') == 'Caution')
        print(f"  - Safe alternatives: {safe_count}")
        print(f"  - Caution alternatives: {caution_count}")

        print("\nAlternative Products:")
        for i, alt in enumerate(alternatives, 1):
            print(f"  {i}. {alt.get('alternative_name', 'Unknown')} ({alt.get('warning_level', 'Unknown')})")
            print(f"     Company: {alt.get('company', 'N/A')}")
            print(f"     Price: {alt.get('price', 'N/A')}")
            print(f"     Tags: {', '.join(alt.get('tags', []))}")
    print("\n")

def test_no_allergens():
    """Test with no allergens (general alternatives)"""
    print("=" * 80)
    print("TEST 3: No Allergens (General Alternatives)")
    print("=" * 80)

    image_path = "../allergen_detector/test_product_caution.jpg"
    allergens = []  # No allergens

    # Run allergen detection first
    allergen_result = detect_allergens(image_path, allergens)

    # Find alternatives
    alternatives = find_alternatives(image_path, allergens, allergen_result)

    print("\n" + "=" * 80)
    print("RESULTS (No Allergen Restrictions):")
    print("=" * 80)
    print(json.dumps(alternatives, indent=2))
    print("\n")

if __name__ == "__main__":
    # Check if test image exists
    test_image = "../allergen_detector/test_product_caution.jpg"
    if not os.path.exists(test_image):
        print(f"Error: Test image not found at {test_image}")
        print("Please ensure the test image exists or update the path.")
        sys.exit(1)

    # Run tests
    try:
        # Test 1: Standalone alternative finder
        test_alternative_finder_standalone()

        # Test 2: Full pipeline
        test_full_pipeline()

        # Test 3: No allergens
        test_no_allergens()

        print("=" * 80)
        print("ALL TESTS COMPLETED!")
        print("=" * 80)

    except Exception as e:
        print(f"\nError during testing: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
