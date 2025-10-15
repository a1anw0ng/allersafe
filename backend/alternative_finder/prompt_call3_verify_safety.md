Use the web search tool to verify allergen safety for each candidate product.

**IMPORTANT: This phase USES WEB SEARCH. Conduct thorough allergen safety research for each product.**

## Allergen Constraints:
{allergen_constraints}

## Candidate Products:
{candidates}

## Your Task - Verify Allergen Safety:
For each candidate product, use web search to thoroughly research allergen safety.

### Safety Verification Steps:

**For EACH candidate product, research:**

1. **Complete Ingredient List**:
   - Search for the official ingredient list
   - Check manufacturer website, Amazon, Walmart product pages
   - Look for the most recent/accurate ingredient information
   - Identify any of the user's allergens in ingredients

2. **Allergen Warnings**:
   - Search for "Contains:" statements
   - Search for "May contain:" warnings
   - Look for facility warnings ("Processed in facility that...")
   - Search for cross-contamination advisories

3. **Manufacturing Information**:
   - Research the manufacturer
   - Find what other products they make
   - Search for facility allergen information
   - Look for dedicated allergen-free facilities if applicable

4. **Allergen Certifications**:
   - Search for certifications (Certified Gluten-Free, Vegan, etc.)
   - Look for third-party allergen testing
   - Check for allergen-free brand status

5. **Safety Determination**:
   - **SAFE**: No user allergens in ingredients, no cross-contamination warnings, facility doesn't process user allergens
   - **CAUTION**: "May contain" user allergens, shared facility warnings, unclear labeling
   - **DANGEROUS**: Contains user allergens as ingredients (exclude from results)
   - **UNKNOWN**: Cannot verify safety (treat as CAUTION)

**Search Query Examples per Product:**
- "[product name] ingredients"
- "[product name] allergen information"
- "[manufacturer] facility allergen warnings"
- "[product name] contains [allergen]"
- "[manufacturer] [allergen] free"

**Return ONLY valid JSON in this exact format:**
{{
  "safety_results": [
    {{
      "product_name": "Product name",
      "safety_status": "Safe|Caution|Dangerous|Unknown",
      "ingredients_found": ["ingredient1", "ingredient2", ...] or "not_found",
      "allergen_warnings": ["warning1", "warning2", ...] or [],
      "contains_user_allergens": ["allergen1", "allergen2", ...] or [],
      "cross_contamination_risk": "none|low|medium|high",
      "certifications": ["cert1", "cert2", ...] or [],
      "safety_explanation": "Why this safety status was assigned",
      "sources": [
        {{"title": "source", "url": "URL", "info": "what was verified"}}
      ]
    }}
  ],
  "excluded_products": [
    {{"product_name": "Product name", "reason": "Contains [allergen]"}}
  ]
}}

**Important**:
- Search thoroughly for EACH product
- Exclude any products marked as "Dangerous" (contain user allergens)
- Be conservative: when in doubt, mark as "Caution" not "Safe"
- Cite all sources used for verification
- If user has NO allergens, all products are "Safe" (skip detailed allergen checks)
