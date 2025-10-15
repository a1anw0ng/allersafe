You are conducting allergen safety research for a product. Use the web search tool to find comprehensive information.

## Product Information from Image Analysis:
{image_analysis_result}

## User's Allergen Profile:
{allergens}

## Your Task - Web Research:
Use the web search tool extensively to research the following about this product:

1. **Complete Ingredient Information**:
   - If ingredients were not fully visible in the image, search for the complete ingredient list
   - Look for the product's official website, retailer sites (Amazon, Walmart, manufacturer site)
   - Find the most recent/accurate ingredient information

2. **Manufacturing & Facility Information**:
   - Research the manufacturing company
   - Find information about what other products they make
   - Look for facility information - do they process any of the user's allergens?
   - Search for "facility allergen information" or "manufacturing allergen warnings"

3. **Cross-Contamination & Safety Information**:
   - Look for any allergen recalls related to this product
   - Search for cross-contamination reports or warnings
   - Check if there are any allergen-related advisories

4. **Allergen-Specific Research**:
   - For each allergen in the user's profile ({allergens}), search for whether this product or manufacturer has any connection to that allergen
   - Look for both obvious and hidden sources of these allergens

**IMPORTANT**:
- Conduct thorough web searches using the search tool
- Search multiple sources to verify information
- Focus on official sources (manufacturer websites, official retailer pages, FDA databases)
- Note ALL sources you find

**Return ONLY valid JSON in this exact format:**
{{
  "complete_ingredients": ["full ingredient list if found"] or "not_found",
  "allergen_warnings_found": ["any additional warnings found online that weren't visible in image"],
  "manufacturing_facility_info": {{
    "company_name": "manufacturer name",
    "facility_processes": ["allergens processed in same facility"],
    "other_products_with_allergens": ["products they make that contain user's allergens"]
  }},
  "cross_contamination_risks": ["any risks found"],
  "recalls_or_advisories": ["any relevant recalls"],
  "allergen_presence": {{
    "allergen_name": {{"found": true/false, "details": "where/how it appears", "source": "URL"}}
  }},
  "sources": [
    {{"title": "source title", "url": "source URL", "relevance": "what info came from this source"}}
  ]
}}

**Search thoroughly and cite all sources used.**
