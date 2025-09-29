#!/usr/bin/env python3
"""Ultra-simple allergen detection using GPT-4o with search"""

import sys
import json
import base64
import litellm
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

    # Load prompt from file
    with open("allergen_prompt.md", "r") as f:
        prompt_template = f.read()
    
    prompt = prompt_template.format(allergens=', '.join(allergens))

    # Single API call
    response = litellm.completion(
        model="gpt-5",  # Using GPT-5 model
        messages=[{
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"}}
            ]
        }]
        # Note: GPT-5 only supports temperature=1 (default)
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
    image_path = "test_product.jpg"
    allergens = ["nuts", "dairy", "gluten"]

    result = detect_allergens(image_path, allergens)
    print(json.dumps(result, indent=2))