#!/usr/bin/env python3
"""
Comprehensive test for the unified product analyzer

Shows complete output from all 8 phases:
- Phase 1-3: Allergen Detection
- Phase 4-8: Alternative Finding
"""

import sys
import os
import json

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from product_analyzer import analyze_product

def print_section(title, char="="):
    """Print a formatted section header"""
    print(f"\n{char * 80}")
    print(title)
    print(f"{char * 80}\n")

def print_allergen_details(allergen_analysis):
    """Print detailed allergen analysis results"""
    print_section("ALLERGEN DETECTION RESULTS", "-")

    print(f"Product Name: {allergen_analysis.get('product_name', 'Unknown')}")
    print(f"Safety Level: {allergen_analysis.get('severity', 'Unknown')}")
    print(f"Allergens Detected: {', '.join(allergen_analysis.get('allergens_detected', [])) or 'None'}")
    print(f"\nWarnings:")
    print(f"  {allergen_analysis.get('warnings', 'No warnings')}")

    sources = allergen_analysis.get('sources', [])
    if sources:
        print(f"\nSources from Allergen Detection ({len(sources)}):")
        for i, source in enumerate(sources[:5], 1):  # Show first 5
            print(f"  {i}. {source.get('title', 'Unknown')}")
            print(f"     {source.get('url', 'No URL')}")
        if len(sources) > 5:
            print(f"  ... and {len(sources) - 5} more sources")

def print_alternatives_details(alternatives):
    """Print detailed alternative products results"""
    print_section("ALTERNATIVE PRODUCTS FOUND", "-")

    if not alternatives:
        print("No alternatives found.")
        return

    safe_alternatives = [alt for alt in alternatives if alt.get('warning_level') == 'Safe']
    caution_alternatives = [alt for alt in alternatives if alt.get('warning_level') == 'Caution']

    if safe_alternatives:
        print(f"SAFE ALTERNATIVES ({len(safe_alternatives)}):")
        print()
        for i, alt in enumerate(safe_alternatives, 1):
            print(f"{i}. {alt.get('alternative_name', 'Unknown')}")
            print(f"   Company: {alt.get('company', 'N/A')}")
            print(f"   Price: {alt.get('price', 'N/A')}")
            print(f"   Tags: {', '.join(alt.get('tags', []))}")
            print(f"   Purchase Links:")
            for link in alt.get('purchase_links', [])[:2]:  # Show first 2 links
                print(f"     - {link}")
            print()

    if caution_alternatives:
        print(f"CAUTION ALTERNATIVES ({len(caution_alternatives)}):")
        print()
        for i, alt in enumerate(caution_alternatives, 1):
            print(f"{i}. {alt.get('alternative_name', 'Unknown')}")
            print(f"   Company: {alt.get('company', 'N/A')}")
            print(f"   Price: {alt.get('price', 'N/A')}")
            print(f"   Tags: {', '.join(alt.get('tags', []))}")
            print(f"   ⚠️  May have cross-contamination risks")
            print()

def print_summary(summary):
    """Print analysis summary"""
    print_section("ANALYSIS SUMMARY", "=")

    print(f"Original Product: {summary.get('original_product', 'Unknown')}")
    print(f"Safety Status: {summary.get('safety_status', 'Unknown')}")
    print(f"Allergens Found: {', '.join(summary.get('allergens_found', [])) or 'None'}")
    print()
    print(f"Alternatives Found: {summary.get('alternatives_found', 0)}")
    print(f"  ✓ Safe: {summary.get('safe_alternatives', 0)}")
    print(f"  ⚠️  Caution: {summary.get('caution_alternatives', 0)}")
    print()
    print(f"Total Unique Sources: {summary.get('total_sources', 0)}")
    print(f"Analysis Time: {summary.get('analysis_time_seconds', 0)} seconds")

def test_with_allergens():
    """Test with allergens specified"""
    print_section("TEST 1: Product Analysis WITH Allergens", "=")

    image_path = "allergen_detector/test_product_caution.jpg"
    allergens = ["nuts", "dairy"]

    print(f"Test Image: {image_path}")
    print(f"Allergens to Avoid: {', '.join(allergens)}")

    # Run full analysis
    result = analyze_product(image_path, allergens, verbose=True)

    # Print detailed results
    print_allergen_details(result['allergen_analysis'])
    print_alternatives_details(result['alternatives'])
    print_summary(result['summary'])

    # Print all sources
    print_section("ALL UNIQUE SOURCES CITED", "-")
    for i, source in enumerate(result['all_sources'], 1):
        print(f"{i}. {source.get('title', 'Unknown')}")
        print(f"   {source.get('url', 'No URL')}")

    print("\n" + "=" * 80)
    print("JSON OUTPUT")
    print("=" * 80)
    print(json.dumps(result, indent=2))

def test_without_allergens():
    """Test without allergens (general alternatives)"""
    print_section("TEST 2: Product Analysis WITHOUT Allergens", "=")

    image_path = "allergen_detector/test_product_caution.jpg"
    allergens = []

    print(f"Test Image: {image_path}")
    print(f"Allergens to Avoid: None (general alternatives)")

    # Run full analysis
    result = analyze_product(image_path, allergens, verbose=True)

    # Print results
    print_allergen_details(result['allergen_analysis'])
    print_alternatives_details(result['alternatives'])
    print_summary(result['summary'])

if __name__ == "__main__":
    # Check if test image exists
    test_image = "allergen_detector/test_product_caution.jpg"
    if not os.path.exists(test_image):
        print(f"Error: Test image not found at {test_image}")
        print("Please ensure the test image exists or update the path.")
        sys.exit(1)

    try:
        # Run tests
        test_with_allergens()

        print("\n\n\n")

        test_without_allergens()

        print_section("ALL TESTS COMPLETED SUCCESSFULLY!", "=")

    except Exception as e:
        print(f"\nError during testing: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
