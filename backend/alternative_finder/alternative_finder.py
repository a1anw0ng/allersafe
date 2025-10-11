#!/usr/bin/env python3
"""Find safe alternative products using GPT-5 with web search"""

import sys
import json
import base64
import litellm
import os
from typing import List, Dict
from urllib.parse import quote_plus
from dotenv import load_dotenv

load_dotenv()

def find_alternatives(image_path: str, allergens: List[str]) -> List[Dict]:
    """Find safe alternative products based on allergens

    Args:
        image_path: Path to product image
        allergens: List of allergens to avoid (can be empty for general alternatives)

    Returns:
        List of alternative products (max 5) with details
    """
    # Read and encode image
    with open(image_path, "rb") as f:
        image_b64 = base64.b64encode(f.read()).decode()

    # Load prompt from file (relative to this module's directory)
    module_dir = os.path.dirname(os.path.abspath(__file__))
    prompt_path = os.path.join(module_dir, "alternative_prompt.md")
    with open(prompt_path, "r") as f:
        prompt_template = f.read()

    # Format prompt based on whether allergens are provided
    if allergens and len(allergens) > 0:
        allergen_context = f" for someone with these allergies: {', '.join(allergens)}"
        safety_requirement = " that are SAFE for someone with the listed allergies"
        warning_guidelines = """### SAFE (No Risk) - PRIORITIZE THESE:
- Product contains NONE of the user's allergens
- No cross-contamination warnings
- No "may contain" statements for user's allergens
- No shared equipment warnings for user's allergens

### CAUTION (Potential Risk) - LIST AFTER SAFE OPTIONS:
- "May contain traces of" user's allergens
- "Processed in facility that also processes" user's allergens
- Manufactured on shared equipment with user's allergens
- Unclear labeling about allergen content"""
        search_criteria = "- Products in the same category that are free from user's allergens\n   - Popular allergen-free brands for this product type"
        verification_steps = "- Confirm it doesn't contain any of the user's allergens\n   - Check for cross-contamination warnings"
    else:
        allergen_context = " that are similar or healthier alternatives"
        safety_requirement = " in the same category"
        warning_guidelines = """### SAFE (No Allergen Restrictions):
- User has NO dietary restrictions or allergies
- ALL products are safe from an allergen perspective
- Mark ALL alternatives as "Safe" (do not use "Caution")
- Focus on finding similar, quality products in the same category"""
        search_criteria = "- Products in the same category (similar type/flavor profile)\n   - Popular well-reviewed brands"
        verification_steps = "- Verify it's a legitimate alternative\n   - Check general quality and reviews"

    prompt = prompt_template.format(
        allergen_context=allergen_context,
        safety_requirement=safety_requirement,
        warning_guidelines=warning_guidelines,
        search_criteria=search_criteria,
        verification_steps=verification_steps
    )

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

    # Extract JSON array from response
    content = response.choices[0].message.content

    # Find JSON array in response
    start = content.find('[')
    end = content.rfind(']') + 1

    try:
        if start >= 0 and end > 0:
            json_str = content[start:end]
            alternatives = json.loads(json_str)

            # Ensure we return a list
            if isinstance(alternatives, list):
                # Add purchase links based on product names
                for alt in alternatives:
                    product_name = alt.get('alternative_name', '')
                    if product_name:
                        # URL-encode product name for search queries
                        encoded_name = quote_plus(product_name)
                        alt['purchase_links'] = [
                            f"https://www.amazon.com/s?k={encoded_name}",
                            f"https://www.walmart.com/search?q={encoded_name}"
                        ]
                    else:
                        alt['purchase_links'] = []

                # Limit to 5 alternatives, prioritize Safe over Caution
                safe = [alt for alt in alternatives if alt.get('warning_level') == 'Safe']
                caution = [alt for alt in alternatives if alt.get('warning_level') == 'Caution']

                # Combine: safe products first, then caution
                sorted_alternatives = safe + caution
                return sorted_alternatives[:5]
            else:
                return [alternatives]  # Wrap single object in list
        else:
            # Try parsing as single object
            return [json.loads(content)]
    except Exception as e:
        # Log the error for debugging
        print(f"Error parsing alternatives response: {e}")
        print(f"Raw response content: {content}")

        # Return error response
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
    allergens = ["nuts", "dairy", "gluten"]

    alternatives = find_alternatives(image_path, allergens)
    print(json.dumps(alternatives, indent=2))