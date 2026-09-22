Use the web search tool to find alternative products based on the search strategy.

**IMPORTANT: This phase USES WEB SEARCH. Conduct thorough online searches to find real products.**

## Category Analysis Results:
{category_analysis}

## Your Task - Find Alternative Product Candidates:
Use web search to find exactly 3 alternative products that best match the search criteria. Choose the 3 you have the highest confidence about — each one will be individually verified for allergen safety in the next phase, and all 3 will be shown to the user.

### Search Instructions:

1. **Search Using Defined Terms**:
   - Use the search terms from category analysis
   - Search for the specific product categories identified
   - Look for the suggested brands and other popular alternatives
   - Search for products with dietary certifications if specified

2. **Find Real Products**:
   - Search major retailers: Amazon, Walmart, Target, Whole Foods
   - Look for manufacturer websites
   - Find specialty allergen-free food sites if relevant
   - Identify exactly 3 specific product alternatives (with exact product names and brands) — pick the 3 you have highest confidence about

3. **Gather Basic Information**:
   - Full product name with brand (e.g., "Enjoy Life Soft Baked Cookies - Double Chocolate Brownie")
   - Manufacturer/company name
   - Product type and key features
   - Note where product information was found (URLs)

4. **Prioritize Allergen-Free Brands**:
   - Focus on brands known for allergen-free products
   - Look for certified allergen-free or dietary-specific brands
   - Search for products explicitly labeled as free from user's allergens

**Search Query Examples:**
- "[product category] [allergen]-free" (e.g., "chocolate chip cookies dairy-free")
- "[product category] allergen-free brands" (e.g., "cookies peanut-free brands")
- "[suggested brand] [product type]" (e.g., "Enjoy Life cookies")
- "best [allergen]-free [product category]" (e.g., "best gluten-free bread")

**Return ONLY valid JSON in this exact format:**
{{
  "candidates": [
    {{
      "product_name": "Full product name with brand and variant",
      "company": "Manufacturer name",
      "product_type": "Specific product type",
      "key_features": ["feature1", "feature2", ...],
      "found_at": ["URL1", "URL2", ...]
    }}
  ],
  "search_summary": "Brief summary of search approach and what was found",
  "sources_consulted": [
    {{"title": "source title", "url": "URL", "relevance": "what info came from here"}}
  ]
}}

**Important**:
- Must return exactly 3 candidate products
- Each product must be real and currently available — no hallucinated products
- Include full product names (brand + product name + variant if applicable)
- Document all sources for verification
- Pick the 3 you are most confident about; all 3 will be individually verified and shown to the user
