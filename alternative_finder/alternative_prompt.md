Analyze the product in this image and find SAFE ALTERNATIVE products for someone with these allergies: {allergens}

## Your Task:
1. Identify the product shown in the image
2. Search online for 5 alternative products that are SAFE for someone with the listed allergies
3. Prioritize completely SAFE products over those with CAUTION warnings
4. Include purchase links with current prices

## Required Output Format:
Return ONLY a valid JSON array with up to 5 alternative products:

```json
[
  {{
    "alternative_name": "specific product name",
    "company": "manufacturer name",
    "purchase_links": ["direct URL to purchase", "second URL if available"],
    "price": "$X.XX USD",
    "warning_level": "Safe or Caution",
    "tags": ["allergen-free", "dietary tags", "max 3 tags"]
  }}
]
```

## Warning Level Guidelines:

### SAFE (No Risk) - PRIORITIZE THESE:
- Product contains NONE of the user's allergens
- No cross-contamination warnings
- No "may contain" statements for user's allergens
- No shared equipment warnings for user's allergens

### CAUTION (Potential Risk) - LIST AFTER SAFE OPTIONS:
- "May contain traces of" user's allergens
- "Processed in facility that also processes" user's allergens
- Manufactured on shared equipment with user's allergens
- Unclear labeling about allergen content

## Search Instructions:

1. **Identify Product Category**: Determine what type of product this is (snack, beverage, meal, etc.)

2. **Search for Alternatives**: Use web search to find:
   - Products in the same category that are free from user's allergens
   - Popular allergen-free brands for this product type
   - Current prices from major retailers (Amazon, Walmart, Target, Whole Foods)
   - Direct purchase links (not just brand websites)

3. **Verify Safety**: For each alternative:
   - Confirm it doesn't contain any of the user's allergens
   - Check for cross-contamination warnings
   - Verify current availability and pricing

4. **Generate Tags**: Create 2-3 word descriptive tags such as:
   - Allergen-specific: "peanut-free", "dairy-free", "gluten-free"
   - Dietary: "vegan", "kosher", "halal", "organic"
   - Category: "high-protein", "low-sugar", "whole-grain"

## Examples of Good Alternatives:

For someone allergic to **dairy** looking at milk:
- Oat milk (Oatly, Chobani)
- Soy milk (Silk)
- Almond milk (Blue Diamond) - unless nut allergy
- Coconut milk (So Delicious)
- Rice milk (Rice Dream)

For someone allergic to **gluten** looking at bread:
- Canyon Bakehouse Gluten-Free Bread
- Udi's Gluten Free Bread
- Schar Gluten-Free Artisan Bread
- Simple Kneads Gluten-Free Bread
- Little Northern Bakehouse Seeds & Grains Bread

## Important Requirements:

- Return EXACTLY 5 alternatives (or fewer if not enough safe options exist)
- List SAFE products first, then CAUTION products
- Include real, purchasable products with actual prices
- Provide working purchase links from major retailers
- All prices in USD
- Keep tags concise (2-3 words each)
- Focus on widely available alternatives that can be purchased online

