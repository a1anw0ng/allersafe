Analyze the product and allergen detection results to define search criteria for finding safe alternatives.

## Allergen Detection Results:
{allergen_result}

## User's Allergen Profile:
{allergens}

## Your Task - Product Category Analysis:
Based on the allergen detection results, analyze the product and define what alternatives we should search for.

### Analysis Steps:

1. **Product Understanding**:
   - What type of product is this? (snack, beverage, meal, condiment, etc.)
   - What is the specific category? (e.g., "chocolate chip cookies", "oat milk", "peanut butter")
   - What are the key characteristics? (flavor profile, texture, use case)

2. **Allergen Considerations**:
   - Which allergens were detected in the original product?
   - Which allergens must be avoided in alternatives?
   - Are there any cross-contamination concerns?

3. **Alternative Search Strategy**:
   - What product categories should we search? (be specific)
   - What allergen-free brands are known for this product type?
   - What key terms should we use in searches?
   - What dietary certifications might be relevant? (vegan, gluten-free, etc.)

4. **Safety Requirements**:
   - What ingredients must be avoided?
   - What manufacturing warnings should we watch for?
   - What "may contain" statements are dealbreakers?

**Return ONLY valid JSON in this exact format:**
{{
  "original_product": {{
    "name": "product name from detection",
    "category": "specific product category",
    "type": "product type",
    "characteristics": ["key feature 1", "key feature 2", ...]
  }},
  "allergen_constraints": {{
    "must_avoid_ingredients": ["allergen1", "allergen2", ...],
    "must_avoid_warnings": ["may contain X", "shared facility with Y", ...],
    "acceptable_if": ["conditions that make Caution acceptable if no Safe options exist"]
  }},
  "search_strategy": {{
    "product_categories_to_search": ["category 1", "category 2", ...],
    "known_safe_brands": ["brand suggestions for this category"],
    "search_terms": ["search term 1", "search term 2", ...],
    "dietary_certifications": ["vegan", "certified gluten-free", ...]
  }},
  "priority_guidance": "Explanation of what makes a good alternative for this specific case"
}}

**Important**:
- Be specific about product category (not just "snack" but "chocolate chip cookies")
- Consider both direct allergen presence and cross-contamination
- Suggest realistic brands that are known for allergen-free products
- If user has no allergens, focus on similar products in same category
