#!/usr/bin/env python3
"""Test the 3-call allergen detection system"""

import json
from allergen_detector import detect_allergens

# Test case 1: Product with allergens
print("=" * 60)
print("TEST 1: Product with potential allergens (nuts, dairy)")
print("=" * 60)
result1 = detect_allergens("test_product_caution.jpg", ["nuts", "dairy"])
print("\nFinal Result:")
print(json.dumps(result1, indent=2))

print("\n" + "=" * 60)
print("TEST 2: Product with no allergens specified")
print("=" * 60)
result2 = detect_allergens("test_product_safe.jpg", [])
print("\nFinal Result:")
print(json.dumps(result2, indent=2))

print("\n" + "=" * 60)
print("TEST 3: Product with specific allergen profile")
print("=" * 60)
result3 = detect_allergens("test_product_caution.jpg", ["gluten", "soy"])
print("\nFinal Result:")
print(json.dumps(result3, indent=2))

print("\n" + "=" * 60)
print("All tests completed!")
print("=" * 60)
