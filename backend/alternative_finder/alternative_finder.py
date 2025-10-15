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
        # model="gemini/gemini-2.5-flash",
        model="cerebras/qwen-3-235b-a22b-thinking-2507",
        messages=[{
            "role": "user",
            "content": prompt1
        }]
        # No web_search_options for Call 1
    )

    content1 = response1.choices[0].message.content
    print(f"Call 1 Response (length: {len(content1)}): {content1[:500]}...\n")

    # For thinking models, extract the LAST complete JSON object (skip reasoning text)
    def extract_last_json_object(text):
        """Extract the last complete JSON object from text (handles thinking models)"""
        # Find the last occurrence of a JSON object pattern
        brace_count = 0
        json_start = -1

        # Scan backwards to find the last complete JSON object
        for i in range(len(text) - 1, -1, -1):
            if text[i] == '}':
                if brace_count == 0:
                    json_end = i + 1
                brace_count += 1
            elif text[i] == '{':
                brace_count -= 1
                if brace_count == 0:
                    json_start = i
                    # Found a complete JSON object, try to parse it
                    try:
                        obj = json.loads(text[json_start:json_end])
                        return obj
                    except:
                        continue  # Keep searching backwards
        return None

    try:
        category_analysis = extract_last_json_object(content1)
        if not category_analysis:
            raise ValueError("No valid JSON object found")
    except Exception as e:
        # Enhanced debugging for Phase 4 failure
        print(f"{'='*80}")
        print(f"ERROR: Phase 4 (Category Analysis) JSON parsing failed")
        print(f"{'='*80}")
        print(f"Exception: {str(e)}")
        print(f"Response length: {len(content1)} characters")
        print(f"Last 1000 chars of response: {content1[-1000:]}")
        print(f"{'='*80}\n")
        # Switch to Gemini fallback
        print("Retrying Phase 4 with Gemini...")
        response1_retry = litellm.completion(
            model="gemini/gemini-2.5-pro",
            messages=[{
                "role": "user",
                "content": prompt1
            }]
        )
        content1_retry = response1_retry.choices[0].message.content
        start = content1_retry.find('{')
        end = content1_retry.rfind('}') + 1
        try:
            category_analysis = json.loads(content1_retry[start:end] if start >= 0 else content1_retry)
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
        model="gemini/gemini-2.5-pro",  # Phase 5 requires web search
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
        model="gemini/gemini-2.5-pro",  # Phase 6 requires web search
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
        model="gemini/gemini-2.5-pro",  # Phase 7 requires web search
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
        # model="gemini/gemini-2.5-flash",
        model="cerebras/qwen-3-235b-a22b-thinking-2507",
        messages=[{
            "role": "user",
            "content": prompt5
        }]
        # No web_search_options for Call 5
    )

    content5 = response5.choices[0].message.content
    print(f"Call 5 Response (length: {len(content5)}): {content5[:500]}...\n")

    # For thinking models, extract the LAST complete JSON array (skip reasoning text)
    def extract_last_json_array(text):
        """Extract the last complete JSON array from text (handles thinking models)"""
        bracket_count = 0
        json_start = -1

        # Scan backwards to find the last complete JSON array
        for i in range(len(text) - 1, -1, -1):
            if text[i] == ']':
                if bracket_count == 0:
                    json_end = i + 1
                bracket_count += 1
            elif text[i] == '[':
                bracket_count -= 1
                if bracket_count == 0:
                    json_start = i
                    # Found a complete JSON array, try to parse it
                    try:
                        arr = json.loads(text[json_start:json_end])
                        return arr
                    except:
                        continue  # Keep searching backwards
        return None

    try:
        final_alternatives = extract_last_json_array(content5)
        if not final_alternatives:
            raise ValueError("No valid JSON array found")

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
    except Exception as e:
        # Enhanced debugging for Phase 8 failure
        print(f"{'='*80}")
        print(f"ERROR: Phase 8 (Final Selection) JSON parsing failed")
        print(f"{'='*80}")
        print(f"Exception: {str(e)}")
        print(f"Response length: {len(content5)} characters")
        print(f"Last 1000 chars of response: {content5[-1000:]}")
        print(f"{'='*80}\n")
        # Switch to Gemini fallback
        print("Retrying Phase 8 with Gemini...")
        response5_retry = litellm.completion(
            model="gemini/gemini-2.5-pro",
            messages=[{
                "role": "user",
                "content": prompt5
            }]
        )
        content5_retry = response5_retry.choices[0].message.content
        start = content5_retry.find('[')
        end = content5_retry.rfind(']') + 1
        try:
            final_alternatives = json.loads(content5_retry[start:end] if start >= 0 else content5_retry)
            # Merge sources
            all_sources = sources_call2 + sources_call3 + sources_call4
            unique_sources = clean_sources_list(all_sources)
            for alt in final_alternatives:
                if 'sources' not in alt:
                    alt['sources'] = unique_sources
            final_alternatives = validate_and_fix_purchase_links(final_alternatives)
            return final_alternatives[:5]
        except:
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