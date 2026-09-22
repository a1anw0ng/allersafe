#!/usr/bin/env python3
"""Ultra-simple allergen detection using GPT-4o with search"""

import sys
import json
import base64
import litellm
import os
import re
from pathlib import Path
from dotenv import load_dotenv

# Import shared utilities
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import clean_sources_list, tavily_search

load_dotenv()

BEDROCK_MODEL = "bedrock/us.anthropic.claude-haiku-4-5-20251001-v1:0"

def extract_json_from_text(text):
    """Extract JSON from text that might contain markdown or extra content

    Handles cases like:
    - Text with JSON object
    - ```json ... ``` code blocks
    - Text before and after JSON

    Returns: tuple (json_str, error_message)
    """
    # First try to find markdown code block
    json_block_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', text, re.DOTALL)
    if json_block_match:
        return json_block_match.group(1).strip(), None

    # Try to find JSON object by matching braces
    start = text.find('{')
    if start < 0:
        return None, "No JSON object found (no opening brace)"

    # Find matching closing brace
    brace_count = 0
    end = start
    for i in range(start, len(text)):
        if text[i] == '{':
            brace_count += 1
        elif text[i] == '}':
            brace_count -= 1
            if brace_count == 0:
                end = i + 1
                break

    if brace_count != 0:
        return None, "Mismatched braces in JSON"

    return text[start:end].strip(), None

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
        image_bytes = f.read()
    image_b64 = base64.b64encode(image_bytes).decode()
    # Detect MIME type from magic bytes — Claude validates this strictly
    if image_bytes[:8] == b"\x89PNG\r\n\x1a\n":
        image_mime = "image/png"
    elif image_bytes[:3] == b"\xff\xd8\xff":
        image_mime = "image/jpeg"
    elif image_bytes[:4] == b"RIFF" and image_bytes[8:12] == b"WEBP":
        image_mime = "image/webp"
    elif image_bytes[:6] in (b"GIF87a", b"GIF89a"):
        image_mime = "image/gif"
    else:
        image_mime = "image/jpeg"

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
        model=BEDROCK_MODEL,
        messages=[{
            "role": "user",
            "content": [
                {"type": "text", "text": prompt1},
                {"type": "image_url", "image_url": {"url": f"data:{image_mime};base64,{image_b64}"}}
            ],
        }]
    )

    # Extract JSON from Call 1
    content1 = response1.choices[0].message.content
    print(f"Call 1 Response: {content1}\n")

    json_str, extract_error = extract_json_from_text(content1)
    if extract_error:
        print(f"JSON extraction error in Call 1: {extract_error}")
        print(f"Full response: {content1}")
        return {"severity": "Caution", "allergens_detected": [], "warnings": "Image analysis failed - could not parse response", "sources": []}

    try:
        image_analysis = json.loads(json_str)
    except json.JSONDecodeError as e:
        print(f"JSON parsing error in Call 1: {e}")
        print(f"Full response: {content1}")
        return {"severity": "Caution", "allergens_detected": [], "warnings": "Image analysis failed - invalid JSON format", "sources": []}

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

    product_name = image_analysis.get("product_name") or image_analysis.get("brand") or ""
    search_query = f"{product_name} ingredients allergens" if product_name else "product ingredients allergens"
    search_context, sources_call2 = tavily_search(search_query, max_results=5)
    if search_context:
        prompt2 = f"{prompt2}\n\nWeb search results (use these as ground truth for ingredients and allergens):\n{search_context}"

    response2 = litellm.completion(
        model=BEDROCK_MODEL,
        messages=[{
            "role": "user",
            "content": prompt2
        }]
    )

    # Extract JSON from Call 2
    content2 = response2.choices[0].message.content
    print(f"Call 2 Response: {content2}\n")

    json_str, extract_error = extract_json_from_text(content2)
    if extract_error:
        print(f"JSON extraction error in Call 2: {extract_error}")
        print(f"Full response: {content2}")
        web_research = {"complete_ingredients": "not_found", "sources": []}
    else:
        try:
            web_research = json.loads(json_str)
        except json.JSONDecodeError as e:
            print(f"JSON parsing error in Call 2: {e}")
            print(f"Full response: {content2}")
            web_research = {"complete_ingredients": "not_found", "sources": []}

    # sources_call2 was captured above from tavily_search

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
        model=BEDROCK_MODEL,
        messages=[{
            "role": "user",
            "content": prompt3
        }]
    )

    # Extract JSON from Call 3
    content3 = response3.choices[0].message.content
    print(f"Call 3 Response: {content3}\n")

    json_str, extract_error = extract_json_from_text(content3)
    if extract_error:
        print(f"JSON extraction error in Call 3: {extract_error}")
        print(f"Full response: {content3}")
        return {
            "severity": "Caution",
            "allergens_detected": [],
            "warnings": f"Analysis completed but could not parse response: {extract_error}. Please try again.",
            "sources": sources_call2 if sources_call2 else []
        }

    try:
        print(f"Attempting to parse JSON (length: {len(json_str)} chars)")
        print(f"First 200 chars: {json_str[:200]}")

        final_result = json.loads(json_str)

        # Validate severity matches warnings content
        warnings_text = final_result.get('warnings', '').lower()
        severity = final_result.get('severity', 'Caution')
        allergens_detected = final_result.get('allergens_detected', [])

        # Check if warnings text contradicts severity
        if 'safety status: safe' in warnings_text and severity != 'Safe':
            print(f"⚠️  WARNING: Severity mismatch detected!")
            print(f"   Warnings text indicates: SAFE")
            print(f"   But severity field is: {severity}")
            print(f"   Correcting severity to: Safe")
            final_result['severity'] = 'Safe'
            # Also clear allergens_detected if marked as safe
            final_result['allergens_detected'] = []
        elif 'safety status: dangerous' in warnings_text and severity != 'Dangerous':
            print(f"⚠️  WARNING: Severity mismatch detected!")
            print(f"   Warnings text indicates: DANGEROUS")
            print(f"   But severity field is: {severity}")
            print(f"   Correcting severity to: Dangerous")
            final_result['severity'] = 'Dangerous'
        elif 'safety status: caution' in warnings_text and severity != 'Caution':
            print(f"⚠️  WARNING: Severity mismatch detected!")
            print(f"   Warnings text indicates: CAUTION")
            print(f"   But severity field is: {severity}")
            print(f"   Correcting severity to: Caution")
            final_result['severity'] = 'Caution'

        # Validate allergens_detected consistency with Safety Status line
        # Extract allergens mentioned in Safety Status line
        safety_status_match = re.search(r'\*\*safety status:\*\* (.*?) for individuals with (.*?) allerg', warnings_text)
        if safety_status_match and allergens_detected:
            mentioned_allergens_text = safety_status_match.group(2)
            # Extract individual allergen names from the text (handles "X and Y" or "X, Y, and Z")
            mentioned_allergens_raw = re.split(r',? and |, ', mentioned_allergens_text)
            mentioned_allergens = [a.strip().lower().rstrip('s') for a in mentioned_allergens_raw]  # Remove plural 's'

            # Normalize allergens_detected for comparison
            detected_normalized = [a.strip().lower().rstrip('s') for a in allergens_detected]

            # Check if they match (order doesn't matter)
            if set(mentioned_allergens) != set(detected_normalized):
                print(f"⚠️  WARNING: Allergen consistency issue detected!")
                print(f"   allergens_detected array: {allergens_detected}")
                print(f"   Safety Status mentions: {mentioned_allergens_raw}")
                print(f"   These should match! The Safety Status should only mention allergens in allergens_detected.")
                # Note: We don't auto-correct this as it's more complex - flag it for review

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
    except json.JSONDecodeError as e:
        print(f"JSON parsing error in Call 3: {e}")
        print(f"Error at position {e.pos}: {e.msg}")
        print(f"Extracted JSON string: {json_str}")
        return {
            "severity": "Caution",
            "allergens_detected": [],
            "warnings": f"Analysis completed but response has invalid JSON format (error at position {e.pos}: {e.msg}). Please try again.",
            "sources": sources_call2 if sources_call2 else []
        }
    except Exception as e:
        print(f"Unexpected error in Call 3: {type(e).__name__}: {e}")
        print(f"Full response content: {content3}")
        return {
            "severity": "Caution",
            "allergens_detected": [],
            "warnings": f"Analysis completed but an unexpected error occurred: {type(e).__name__}. Please try again.",
            "sources": sources_call2 if sources_call2 else []
        }

if __name__ == "__main__":
    # Hard-coded test values
    image_path = "test_product_caution.jpg"
    allergens = ["nuts", "dairy"]

    result = detect_allergens(image_path, allergens)
    print(json.dumps(result, indent=2))