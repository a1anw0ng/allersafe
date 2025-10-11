#!/usr/bin/env python3
"""Ultra-simple allergen detection using GPT-4o with search"""

import sys
import json
import base64
import litellm
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

def detect_allergens(image_path, allergens):
    """Detect allergens in product image using AI with web search

    Args:
        image_path: Path to product image
        allergens: List of allergens to check

    Returns:
        Dict with severity, allergens_detected, and warnings
    """
    # Read and encode image
    with open(image_path, "rb") as f:
        image_b64 = base64.b64encode(f.read()).decode()

    # Load prompt from file (relative to this module's directory)
    module_dir = os.path.dirname(os.path.abspath(__file__))
    prompt_path = os.path.join(module_dir, "allergen_prompt.md")
    with open(prompt_path, "r") as f:
        prompt_template = f.read()

    # Format prompt based on whether allergens are provided
    if allergens and len(allergens) > 0:
        allergen_list = ', '.join(allergens)
        allergen_instruction = f"Analyze this product image for these specific allergens: {allergen_list}"
    else:
        allergen_list = "none"
        allergen_instruction = "Analyze this image. The user has no dietary restrictions, but first verify if this image contains a food product."

    prompt = prompt_template.format(allergens=allergen_list, allergen_instruction=allergen_instruction)

    # Single API call
    response = litellm.completion(
        model="gemini/gemini-2.5-flash",
        messages=[{
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"}}
            ]
        }]
    )

    # Extract JSON from response
    content = response.choices[0].message.content
    start = content.find('{')
    end = content.rfind('}') + 1

    try:
        return json.loads(content[start:end] if start >= 0 else content)
    except:
        return {"severity": "Caution", "allergens_detected": [], "warnings": "Analysis failed"}

if __name__ == "__main__":
    # Hard-coded test values
    image_path = "test_product_3.jpg"
    allergens = ["nuts", "dairy"]

    result = detect_allergens(image_path, allergens)
    print(json.dumps(result, indent=2))