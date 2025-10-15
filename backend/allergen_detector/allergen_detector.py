#!/usr/bin/env python3
"""Ultra-simple allergen detection using GPT-4o with search"""

import sys
import json
import base64
import litellm
import os
from pathlib import Path
from dotenv import load_dotenv

# Import shared utilities
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import extract_grounding_sources, clean_sources_list

load_dotenv()

def detect_allergens(image_path, allergens, progress_callback=None):
    """Detect allergens in product image using AI with 3-call pattern

    Call 1: Image analysis (no web tool)
    Call 2: Web research (with web tool)
    Call 3: Final analysis and synthesis (no web tool)

    Args:
        image_path: Path to product image
        allergens: List of allergens to check
        progress_callback: Optional callback function(phase, message) for progress updates

    Returns:
        Dict with severity, allergens_detected, warnings, and sources
    """
    # Read and encode image
    with open(image_path, "rb") as f:
        image_b64 = base64.b64encode(f.read()).decode()

    module_dir = os.path.dirname(os.path.abspath(__file__))

    # Format allergen info
    if allergens and len(allergens) > 0:
        allergen_list = ', '.join(allergens)
        allergen_instruction = f"User's allergen profile: {allergen_list}"
    else:
        allergen_list = "none"
        allergen_instruction = "User has no dietary restrictions."

    # ============================================================
    # CALL 1: Image Analysis (No Web Search)
    # ============================================================
    if progress_callback:
        progress_callback(1, "Analyzing product image...")
    print("Call 1: Analyzing image...")
    with open(os.path.join(module_dir, "prompt_call1_image_analysis.md"), "r") as f:
        prompt1 = f.read().format(allergen_instruction=allergen_instruction)

    response1 = litellm.completion(
        model="gemini/gemini-2.5-pro",  # Phase 1 requires vision support
        messages=[{
            "role": "user",
            "content": [
                {"type": "text", "text": prompt1},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"}}
            ],
        }]
        # No web_search_options for Call 1
    )

    # Extract JSON from Call 1
    content1 = response1.choices[0].message.content
    print(f"Call 1 Response: {content1}\n")

    start = content1.find('{')
    end = content1.rfind('}') + 1

    try:
        image_analysis = json.loads(content1[start:end] if start >= 0 else content1)
    except:
        return {"severity": "Caution", "allergens_detected": [], "warnings": "Image analysis failed", "sources": []}

    # If no product detected, return early
    if not image_analysis.get("is_product", True):
        return {
            "severity": "NotDetected",
            "allergens_detected": [],
            "warnings": f"No food product detected. {image_analysis.get('description', 'Image does not contain a product package.')}",
            "sources": []
        }

    # ============================================================
    # CALL 2: Web Research (With Web Search)
    # ============================================================
    if progress_callback:
        progress_callback(2, "Researching ingredients online...")
    print("Call 2: Researching product details online...")
    with open(os.path.join(module_dir, "prompt_call2_web_research.md"), "r") as f:
        prompt2 = f.read().format(
            image_analysis_result=json.dumps(image_analysis, indent=2),
            allergens=allergen_list
        )

    response2 = litellm.completion(
        model="gemini/gemini-2.5-pro",  # Phase 2 requires web search
        messages=[{
            "role": "user",
            "content": prompt2
        }],
        web_search_options={
            "search_context_size": "low"
        }
    )

    # Extract JSON from Call 2
    content2 = response2.choices[0].message.content
    print(f"Call 2 Response: {content2}\n")

    start = content2.find('{')
    end = content2.rfind('}') + 1

    try:
        web_research = json.loads(content2[start:end] if start >= 0 else content2)
    except:
        web_research = {"complete_ingredients": "not_found", "sources": []}

    # Extract sources from grounding metadata for Call 2
    sources_call2 = extract_grounding_sources(response2)

    # ============================================================
    # CALL 3: Final Analysis (No Web Search)
    # ============================================================
    if progress_callback:
        progress_callback(3, "Finalizing allergen analysis...")
    print("Call 3: Synthesizing final analysis...")
    with open(os.path.join(module_dir, "prompt_call3_final_analysis.md"), "r") as f:
        prompt3 = f.read().format(
            allergens=allergen_list,
            image_analysis_result=json.dumps(image_analysis, indent=2),
            web_research_result=json.dumps(web_research, indent=2)
        )

    response3 = litellm.completion(
        # model="gemini/gemini-2.5-flash",
        model="cerebras/qwen-3-235b-a22b-thinking-2507",
        messages=[{
            "role": "user",
            "content": prompt3
        }]
        # No web_search_options for Call 3
    )

    # Extract JSON from Call 3
    content3 = response3.choices[0].message.content
    print(f"Call 3 Response (length: {len(content3)}): {content3[:500]}...\n")

    # For thinking models, extract the LAST complete JSON object (skip reasoning text)
    def extract_last_json_object(text):
        """Extract the last complete JSON object from text (handles thinking models)"""
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
        final_result = extract_last_json_object(content3)
        if not final_result:
            raise ValueError("No valid JSON object found")

        # Merge sources from web research and grounding metadata
        all_sources = sources_call2 if sources_call2 else []
        if 'sources' in web_research and web_research['sources']:
            all_sources.extend(web_research['sources'])
        if 'sources' in final_result and final_result['sources']:
            all_sources.extend(final_result['sources'])

        # Clean and deduplicate sources (removes invalid/redirect URLs)
        unique_sources = clean_sources_list(all_sources)

        final_result['sources'] = unique_sources
        return final_result
    except Exception as e:
        # Enhanced debugging for Phase 3 failure
        print(f"{'='*80}")
        print(f"ERROR: Phase 3 (Final Analysis) JSON parsing failed")
        print(f"{'='*80}")
        print(f"Exception: {str(e)}")
        print(f"Response length: {len(content3)} characters")
        print(f"Last 1000 chars of response: {content3[-1000:]}")
        print(f"{'='*80}\n")
        # Switch to Gemini fallback
        print("Retrying Phase 3 with Gemini...")
        response3_retry = litellm.completion(
            model="gemini/gemini-2.5-pro",
            messages=[{
                "role": "user",
                "content": prompt3
            }]
        )
        content3_retry = response3_retry.choices[0].message.content
        start = content3_retry.find('{')
        end = content3_retry.rfind('}') + 1
        try:
            final_result = json.loads(content3_retry[start:end] if start >= 0 else content3_retry)
            # Merge sources
            all_sources = sources_call2 if sources_call2 else []
            if 'sources' in web_research and web_research['sources']:
                all_sources.extend(web_research['sources'])
            if 'sources' in final_result and final_result['sources']:
                all_sources.extend(final_result['sources'])
            unique_sources = clean_sources_list(all_sources)
            final_result['sources'] = unique_sources
            return final_result
        except:
            return {
                "severity": "Caution",
                "allergens_detected": [],
                "warnings": "Final analysis failed",
                "sources": sources_call2 if sources_call2 else []
            }

if __name__ == "__main__":
    # Hard-coded test values
    image_path = "test_product_caution.jpg"
    allergens = ["nuts", "dairy"]

    result = detect_allergens(image_path, allergens)
    print(json.dumps(result, indent=2))