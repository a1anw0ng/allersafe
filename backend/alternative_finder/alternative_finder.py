#!/usr/bin/env python3
"""Find safe alternative products using multi-phase AI analysis with web search"""

import sys
import json
import base64
import litellm
import os
from typing import List, Dict
from urllib.parse import quote_plus
from dotenv import load_dotenv

# Import shared utilities
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import extract_grounding_sources, clean_sources_list

load_dotenv()

def validate_and_fix_purchase_links(alternatives: List[Dict]) -> List[Dict]:
    """Create reliable search-based purchase links

    Instead of using potentially broken direct product URLs, we always use
    search URLs which are guaranteed to work and find current products.

    Args:
        alternatives: List of alternative products with purchase_links

    Returns:
        Updated alternatives with reliable search-based purchase links
    """
    for alt in alternatives:
        product_name = alt.get('alternative_name', '')

        if not product_name:
            alt['purchase_links'] = []
            continue

        # URL-encode the product name for search queries
        encoded_name = quote_plus(product_name)

        # Always use search URLs - they're more reliable than direct product URLs
        # which can become outdated, have wrong IDs, or be discontinued
        alt['purchase_links'] = [
            f"https://www.amazon.com/s?k={encoded_name}",
            f"https://www.walmart.com/search?q={encoded_name}",
            f"https://www.target.com/s?searchTerm={encoded_name}"
        ]

    return alternatives

def find_alternatives(image_path: str, allergens: List[str], allergen_result: Dict = None, progress_callback=None) -> List[Dict]:
    """Find safe alternative products using 5-phase AI analysis

    Call 1: Product category analysis (no web tool)
    Call 2: Find alternative candidates (with web tool)
    Call 3: Verify allergen safety (with web tool)
    Call 4: Get pricing & availability (with web tool)
    Call 5: Final selection & synthesis (no web tool)

    Args:
        image_path: Path to product image
        allergens: List of allergens to avoid (can be empty for general alternatives)
        allergen_result: Results from allergen_detector (optional)
        progress_callback: Optional callback function(phase, message) for progress updates

    Returns:
        List of alternative products (max 5) with details
    """
    module_dir = os.path.dirname(os.path.abspath(__file__))

    # Format allergen info
    if allergens and len(allergens) > 0:
        allergen_list = ', '.join(allergens)
    else:
        allergen_list = "none"

    # Use allergen_result if provided, otherwise create a basic one
    if not allergen_result:
        allergen_result = {
            "severity": "Unknown",
            "allergens_detected": [],
            "warnings": "No allergen detection data provided",
            "product_name": "Unknown product"
        }

    # ============================================================
    # CALL 1: Product Category Analysis (No Web Search)
    # ============================================================
    if progress_callback:
        progress_callback(4, "Analyzing product category...")
    print("Call 1: Analyzing product category...")
    with open(os.path.join(module_dir, "prompt_call1_category_analysis.md"), "r") as f:
        prompt1 = f.read().format(
            allergen_result=json.dumps(allergen_result, indent=2),
            allergens=allergen_list
        )

    response1 = litellm.completion(
        model="openrouter/google/gemini-2.5-flash-preview-09-2025",
        messages=[{
            "role": "user",
            "content": prompt1
        }]
        # No web_search_options for Call 1
    )

    content1 = response1.choices[0].message.content
    print(f"Call 1 Response: {content1}\n")

    start = content1.find('{')
    end = content1.rfind('}') + 1

    try:
        category_analysis = json.loads(content1[start:end] if start >= 0 else content1)
    except:
        return [{"alternative_name": "Category analysis failed", "company": "N/A", "purchase_links": [], "price": "N/A", "warning_level": "Caution", "tags": ["Error"]}]

    # ============================================================
    # CALL 2: Find Alternative Candidates (With Web Search)
    # ============================================================
    if progress_callback:
        progress_callback(5, "Finding alternative candidates...")
    print("Call 2: Finding alternative candidates...")
    with open(os.path.join(module_dir, "prompt_call2_find_candidates.md"), "r") as f:
        prompt2 = f.read().format(
            category_analysis=json.dumps(category_analysis, indent=2)
        )

    response2 = litellm.completion(
        model="openrouter/google/gemini-2.5-flash-preview-09-2025",  # Phase 5 requires web search
        messages=[{
            "role": "user",
            "content": prompt2
        }],
        web_search_options={
            "search_context_size": "low"
        }
    )

    content2 = response2.choices[0].message.content
    print(f"Call 2 Response: {content2}\n")

    start = content2.find('{')
    end = content2.rfind('}') + 1

    try:
        candidates_data = json.loads(content2[start:end] if start >= 0 else content2)
        candidates = candidates_data.get('candidates', [])
    except:
        candidates = []

    sources_call2 = extract_grounding_sources(response2)

    if not candidates:
        return []

    # ============================================================
    # CALL 3: Verify Allergen Safety (With Web Search)
    # ============================================================
    if progress_callback:
        progress_callback(6, "Verifying allergen safety...")
    print("Call 3: Verifying allergen safety...")
    with open(os.path.join(module_dir, "prompt_call3_verify_safety.md"), "r") as f:
        prompt3 = f.read().format(
            allergen_constraints=json.dumps(category_analysis.get('allergen_constraints', {}), indent=2),
            candidates=json.dumps(candidates, indent=2)
        )

    response3 = litellm.completion(
        model="openrouter/google/gemini-2.5-flash-preview-09-2025",  # Phase 6 requires web search
        messages=[{
            "role": "user",
            "content": prompt3
        }],
        web_search_options={
            "search_context_size": "low"
        }
    )

    content3 = response3.choices[0].message.content
    print(f"Call 3 Response: {content3}\n")

    start = content3.find('{')
    end = content3.rfind('}') + 1

    try:
        safety_data = json.loads(content3[start:end] if start >= 0 else content3)
        safety_results = safety_data.get('safety_results', [])
        # Filter out dangerous products
        safe_products = [p for p in safety_results if p.get('safety_status') != 'Dangerous']
    except:
        safe_products = candidates  # Fallback to candidates if safety check fails

    sources_call3 = extract_grounding_sources(response3)

    if not safe_products:
        return []

    # ============================================================
    # CALL 4: Get Pricing & Availability (With Web Search)
    # ============================================================
    if progress_callback:
        progress_callback(7, "Checking pricing and availability...")
    print("Call 4: Researching pricing and availability...")
    with open(os.path.join(module_dir, "prompt_call4_pricing_links.md"), "r") as f:
        prompt4 = f.read().format(
            safe_products=json.dumps(safe_products, indent=2)
        )

    response4 = litellm.completion(
        model="openrouter/google/gemini-2.5-flash-preview-09-2025",  # Phase 7 requires web search
        messages=[{
            "role": "user",
            "content": prompt4
        }],
        web_search_options={
            "search_context_size": "low"
        }
    )

    content4 = response4.choices[0].message.content
    print(f"Call 4 Response: {content4}\n")

    start = content4.find('{')
    end = content4.rfind('}') + 1

    try:
        pricing_data = json.loads(content4[start:end] if start >= 0 else content4)
        pricing_results = pricing_data.get('pricing_results', [])
    except:
        pricing_results = []

    sources_call4 = extract_grounding_sources(response4)

    # ============================================================
    # CALL 5: Final Selection & Synthesis (No Web Search)
    # ============================================================
    if progress_callback:
        progress_callback(8, "Selecting best alternatives...")
    print("Call 5: Synthesizing final selection...")
    with open(os.path.join(module_dir, "prompt_call5_final_selection.md"), "r") as f:
        prompt5 = f.read().format(
            category_analysis=json.dumps(category_analysis, indent=2),
            candidates=json.dumps(candidates, indent=2),
            safety_verification=json.dumps(safety_results if 'safety_results' in locals() else safe_products, indent=2),
            pricing_info=json.dumps(pricing_results, indent=2)
        )

    response5 = litellm.completion(
        model="openrouter/google/gemini-2.5-flash-preview-09-2025",
        messages=[{
            "role": "user",
            "content": prompt5
        }]
        # No web_search_options for Call 5
    )

    content5 = response5.choices[0].message.content
    print(f"Call 5 Response: {content5}\n")

    # Extract JSON array from Call 5
    start = content5.find('[')
    end = content5.rfind(']') + 1

    try:
        if start >= 0 and end > 0:
            final_alternatives = json.loads(content5[start:end])

            # Merge all sources and clean/deduplicate (removes invalid/redirect URLs)
            all_sources = sources_call2 + sources_call3 + sources_call4
            unique_sources = clean_sources_list(all_sources)

            # Add sources to each alternative if needed
            for alt in final_alternatives:
                if 'sources' not in alt:
                    alt['sources'] = unique_sources

            # Validate and fix purchase links
            final_alternatives = validate_and_fix_purchase_links(final_alternatives)

            return final_alternatives[:5]  # Limit to 5
        else:
            return []
    except Exception as e:
        print(f"Error parsing final alternatives: {e}")
        print(f"Raw response content: {content5}")
        return [{
            "alternative_name": "Analysis failed",
            "company": "N/A",
            "purchase_links": [],
            "price": "N/A",
            "warning_level": "Caution",
            "tags": ["Error"]
        }]

if __name__ == "__main__":
    # Hard-coded test values
    image_path = "test_product.jpg"
    allergens = ["nuts", "dairy"]

    # Example allergen_result from allergen_detector
    # In practice, this would come from running allergen_detector first
    allergen_result = {
        "severity": "Dangerous",
        "allergens_detected": ["dairy", "nuts"],
        "warnings": "This product contains milk and may contain tree nuts.",
        "product_name": "Example Chocolate Bar",
        "sources": []
    }

    alternatives = find_alternatives(image_path, allergens, allergen_result)
    print(json.dumps(alternatives, indent=2))