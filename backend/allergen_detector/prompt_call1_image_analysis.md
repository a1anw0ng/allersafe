Analyze this product image and extract all visible information.

{allergen_instruction}

**FIRST**: Verify that the image contains a food or consumer product package with visible labels, ingredients, or product information. If the image shows a person, animal, scenery, or anything other than a product package, return:
{{"is_product": false, "description": "[Briefly describe what you see in the image instead]"}}

**IF A PRODUCT IS DETECTED**: Extract the following information from what is visible in the image:

### Your Task - Image Analysis Only:
Carefully examine the product packaging visible in the image and extract:

1. **Product Identification**:
   - Product name (exact name as shown on package)
   - Brand name
   - Product type/category (e.g., snack, beverage, cereal)

2. **Visible Ingredients**:
   - List ALL ingredients that are clearly readable in the image
   - Note if ingredient list is partially visible, not visible, or fully visible

3. **Visible Allergen Warnings**:
   - Any "Contains:" statements
   - Any "May contain:" statements
   - Any facility warnings (e.g., "Processed in a facility that also processes...")
   - Allergen declarations or bolded allergen names in ingredient lists

4. **What Needs Research**:
   - Is the ingredient list incomplete or unclear?
   - Is the product name/brand known but ingredients not visible?
   - Are there any questions about the manufacturing process?

**Return ONLY valid JSON in this exact format:**
{{
  "is_product": true,
  "product_name": "exact product name",
  "brand": "brand name",
  "product_type": "product category",
  "visible_ingredients": ["ingredient1", "ingredient2", ...] or "not_visible" or "partially_visible",
  "visible_allergen_warnings": ["warning1", "warning2", ...] or [],
  "ingredient_list_status": "fully_visible|partially_visible|not_visible",
  "needs_research": true/false,
  "research_needed_for": ["complete ingredient list", "manufacturing facility info", "cross-contamination risks", ...]
}}

**Important**:
- Be precise and only report what you can actually see in the image
- Do not make assumptions about ingredients that are not visible
- Do not search the web - this is pure image analysis
- If text is blurry or unclear, mark it as "partially_visible" or "not_visible"
