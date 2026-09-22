#!/usr/bin/env python3
"""Find safe alternative products using multi-phase AI analysis with web search"""

import sys
import json
import base64
import litellm
import os
from typing import List, Dict
from urllib.parse import quote_plus
from pydantic import ValidationError, TypeAdapter
from dotenv import load_dotenv

# Import shared utilities
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import clean_sources_list, tavily_search
from schemas import (
    Phase4Output,
    Phase5Output,
    Phase6Output,
    Phase7Output,
    FinalAlternative,
)

load_dotenv()

BEDROCK_MODEL = "bedrock/us.anthropic.claude-haiku-4-5-20251001-v1:0"

# TypeAdapter for phase 8 (which returns a JSON array, not a JSON object)
_FinalAlternativesAdapter = TypeAdapter(List[FinalAlternative])

def validate_and_fix_purchase_links(alternatives: List[Dict]) -> List[Dict]:
    """Replace hallucinated product URLs with reliable search URLs, and drop
    hallucinated image_url fields (Claude cannot know real product image URLs)."""
    for alt in alternatives:
        product_name = alt.get('alternative_name', '')

        alt.pop('image_url', None)

        if not product_name:
            alt['purchase_links'] = []
            continue

        encoded_name = quote_plus(product_name)
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
        model=BEDROCK_MODEL,
        messages=[{
            "role": "user",
            "content": prompt1
        }]
    )

    content1 = response1.choices[0].message.content
    print(f"Call 1 Response: {content1}\n")

    start = content1.find('{')
    end = content1.rfind('}') + 1
    json_str = content1[start:end] if start >= 0 else content1

    try:
        category_analysis = Phase4Output.model_validate_json(json_str).model_dump()
    except (ValidationError, json.JSONDecodeError) as e:
        print(f"Phase 4 parse error: {type(e).__name__}: {e}")
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

    strategy = category_analysis.get("search_strategy", {}) or {}
    llm_terms = strategy.get("search_terms") or []
    original_name = (category_analysis.get("original_product") or {}).get("name") or ""
    if llm_terms:
        search_query = llm_terms[0]
    elif original_name and allergens:
        search_query = f"{allergens[0]}-free alternative to {original_name}"
    else:
        search_query = "allergen-free snack alternatives"
    search_context, sources_call2 = tavily_search(search_query, max_results=5)
    if search_context:
        prompt2 = (
            f"{prompt2}\n\nWeb search results (use these to find real alternative products):\n"
            f"{search_context}\n\n"
            "IMPORTANT: Return ONLY a valid JSON object matching the schema. "
            "Do not include prose, explanations, apologies, or markdown code fences. "
            "If the search results are insufficient, still return valid JSON using known safe brands from the search_strategy."
        )

    response2 = litellm.completion(
        model=BEDROCK_MODEL,
        messages=[{
            "role": "user",
            "content": prompt2
        }]
    )

    content2 = response2.choices[0].message.content
    print(f"Call 2 Response: {content2}\n")

    start = content2.find('{')
    end = content2.rfind('}') + 1
    json_str = content2[start:end] if start >= 0 else content2

    try:
        candidates_data = Phase5Output.model_validate_json(json_str).model_dump()
        candidates = candidates_data.get('candidates', [])
    except (ValidationError, json.JSONDecodeError) as e:
        print(f"Phase 5 parse error: {type(e).__name__}: {e}")
        candidates = []

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

    candidate_names = [c.get("product_name") or c.get("alternative_name") or c.get("name") or "" for c in candidates]
    candidate_names = [n for n in candidate_names if n][:3]
    verify_context = ""
    sources_call3 = []
    for name in candidate_names:
        ctx, srcs = tavily_search(f"{name} ingredients allergens", max_results=3)
        if ctx:
            verify_context += f"\n\n--- Search for: {name} ---\n{ctx}"
            sources_call3.extend(srcs)
    if verify_context:
        prompt3 = (
            f"{prompt3}\n\nWeb search results (use these to verify ingredient safety):\n"
            f"{verify_context}\n\n"
            "IMPORTANT: Return ONLY a valid JSON object matching the schema. "
            "No prose, no markdown code fences."
        )

    response3 = litellm.completion(
        model=BEDROCK_MODEL,
        messages=[{
            "role": "user",
            "content": prompt3
        }]
    )

    content3 = response3.choices[0].message.content
    print(f"Call 3 Response: {content3}\n")

    start = content3.find('{')
    end = content3.rfind('}') + 1
    json_str = content3[start:end] if start >= 0 else content3

    try:
        safety_data = Phase6Output.model_validate_json(json_str).model_dump()
        safety_results = safety_data.get('safety_results', [])
        # Filter out dangerous products
        safe_products = [p for p in safety_results if p.get('safety_status') != 'Dangerous']
    except (ValidationError, json.JSONDecodeError) as e:
        print(f"Phase 6 parse error: {type(e).__name__}: {e}")
        safe_products = candidates  # Fallback to candidates if safety check fails
        safety_results = []

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

    safe_names = [p.get("product_name") or p.get("alternative_name") or p.get("name") or "" for p in safe_products]
    safe_names = [n for n in safe_names if n][:3]
    price_context = ""
    sources_call4 = []
    for name in safe_names:
        ctx, srcs = tavily_search(f"{name} price buy", max_results=3)
        if ctx:
            price_context += f"\n\n--- Search for: {name} ---\n{ctx}"
            sources_call4.extend(srcs)
    if price_context:
        prompt4 = (
            f"{prompt4}\n\nWeb search results (use these for pricing and store availability):\n"
            f"{price_context}\n\n"
            "IMPORTANT: Return ONLY a valid JSON object matching the schema. "
            "No prose, no markdown code fences."
        )

    response4 = litellm.completion(
        model=BEDROCK_MODEL,
        messages=[{
            "role": "user",
            "content": prompt4
        }]
    )

    content4 = response4.choices[0].message.content
    print(f"Call 4 Response: {content4}\n")

    start = content4.find('{')
    end = content4.rfind('}') + 1
    json_str = content4[start:end] if start >= 0 else content4

    try:
        pricing_data = Phase7Output.model_validate_json(json_str).model_dump()
        pricing_results = pricing_data.get('pricing_results', [])
    except (ValidationError, json.JSONDecodeError) as e:
        print(f"Phase 7 parse error: {type(e).__name__}: {e}")
        pricing_results = []

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
        model=BEDROCK_MODEL,
        messages=[{
            "role": "user",
            "content": prompt5
        }]
    )

    content5 = response5.choices[0].message.content
    print(f"Call 5 Response: {content5}\n")

    # Extract JSON array from Call 5
    start = content5.find('[')
    end = content5.rfind(']') + 1

    try:
        if start >= 0 and end > 0:
            json_str = content5[start:end]
            try:
                validated = _FinalAlternativesAdapter.validate_json(json_str)
                final_alternatives = [alt.model_dump() for alt in validated]
            except ValidationError as ve:
                print(f"Phase 8 Pydantic validation error: {ve}")
                # Fall back to raw json.loads so we still return something usable
                final_alternatives = json.loads(json_str)

            # Merge all sources and clean/deduplicate (removes invalid/redirect URLs)
            all_sources = sources_call2 + sources_call3 + sources_call4
            unique_sources = clean_sources_list(all_sources)

            # Add sources to each alternative if needed
            for alt in final_alternatives:
                if 'sources' not in alt:
                    alt['sources'] = unique_sources

            # Validate and fix purchase links (also strips hallucinated image_url)
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