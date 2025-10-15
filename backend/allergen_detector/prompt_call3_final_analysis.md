You are finalizing an allergen safety analysis. Synthesize all information and provide a final safety determination.

## User's Allergen Profile:
{allergens}

## Image Analysis Results (Call 1):
{image_analysis_result}

## Web Research Results (Call 2):
{web_research_result}

## Your Task - Final Analysis & Synthesis:
Combine all information from the image analysis and web research to determine the safety level for this product.

### Analysis Guidelines:

**NOT DETECTED (No Product Found)**
- Use this ONLY if image_analysis indicated is_product: false
- Describe what was in the image instead

**DANGEROUS (Immediate Risk)**
- Product directly contains one or more of the specified allergens as ingredients
- This includes both visible ingredients from image AND complete ingredients from web research
- Check for:
  - Direct ingredients (milk, eggs, wheat, peanuts, etc.)
  - Derived ingredients (whey from milk, lecithin from soy, gluten from wheat)
  - Alternative names (casein=dairy, albumin=egg, etc.)

**CAUTION (Potential Risk)**
- Cross-contamination warnings or processing facility risks
- "May contain" statements
- "Processed in facility that also processes" warnings
- Shared equipment warnings
- Manufacturing facility processes user's allergens
- **Language to use in Conclusion**: "Exercise strong caution" or "Use with caution" rather than "NOT RECOMMENDED"

**SAFE (No Risk)**
- No allergen present in ingredients (from image or web research)
- No cross-contamination warnings found
- Manufacturing facility does not process user's allergens
- **Special case**: If allergens list is "none" (no dietary restrictions), product is automatically safe

### Your Analysis Process:
1. Review all ingredients (from image + web research)
2. Check for direct presence of any user allergens
3. Review all warnings (from image + web research)
4. Consider manufacturing facility risks
5. Determine severity level conservatively (when in doubt, choose higher severity for safety)
6. Write detailed warnings explaining your decision
7. **MUST use inline citations [1], [2], etc.** in your warnings - reference sources using numbered citations
8. **Limit to 5 most relevant sources maximum** - only include the most authoritative and useful sources

**Return ONLY valid JSON in this exact format:**
{{
  "severity": "Safe|Caution|Dangerous|NotDetected",
  "allergens_detected": ["list of user's allergens found in this product"],
  "warnings": "**Product Identified:** [Product name]\n\n**Safety Status:** [Safe/Caution/Dangerous] for individuals with [allergen] allergy\n\n**Analysis:**\n\n• **[Allergen Name]:** Brief analysis of whether it's present. Use inline citations like [1] or [2] to reference sources. Be clear and concise.\n\n• **[Next Allergen]:** Continue for each allergen.\n\n**Conclusion:** Final verdict with reasoning. For Caution-level products, use phrases like 'Exercise strong caution' or 'Use with caution' rather than 'NOT RECOMMENDED'. Use sentence case, not all caps. For Dangerous-level products, you may use stronger language. Cite sources inline [1][2] as needed.",
  "product_name": "product name from analysis",
  "sources": [
    {{"title": "Brief descriptive title of source", "url": "URL from web research"}}
  ]
}}

**CRITICAL REQUIREMENTS:**
1. The "severity" field MUST exactly match the "Safety Status" in the warnings text:
   - If warnings says "Safety Status: Safe" → severity MUST be "Safe"
   - If warnings says "Safety Status: Caution" → severity MUST be "Caution"
   - If warnings says "Safety Status: Dangerous" → severity MUST be "Dangerous"

2. If severity is "Safe", allergens_detected MUST be an empty array []

3. Do NOT include any instructional notes or formatting reminders in the warnings field. Only include the actual analysis content as specified in the format above.

## Common Hidden Allergens Reference:
- **Dairy**: Casein, whey, lactose, milk powder, butter, cream
- **Eggs**: Albumin, lecithin (sometimes), mayonnaise
- **Gluten**: Wheat, barley, rye, malt, modified food starch
- **Soy**: Lecithin, soy protein, soybean oil, tamari
- **Nuts**: Natural flavors (sometimes), marzipan, nougat

**Be thorough, conservative, and cite your sources.**
