Analyze the product in this image and find ALTERNATIVE products{allergen_context}

**FIRST**: Verify that the image contains a food or consumer product package with visible labels, ingredients, or product information. If the image shows a person, animal, scenery, or anything other than a product package, return an empty array:
```json
[]
```

**ONLY IF A PRODUCT IS DETECTED**: Continue with the task below.

## Your Task:
1. Identify the product shown in the image
2. Search online for 5 alternative products{safety_requirement}
3. Prioritize completely SAFE products over those with CAUTION warnings
4. Include purchase links with current prices

## Required Output Format:
Return ONLY a valid JSON array with up to 5 alternative products:

```json
[
  {{
    "alternative_name": "specific product name with brand",
    "company": "manufacturer name",
    "price": "~$X.XX for [size/unit]",
    "warning_level": "Safe or Caution",
    "tags": ["allergen-free", "dietary tags", "max 3 tags"]
  }}
]
```

**Price Format Examples (use ~ for approximate):**
- "~$4.99 for 12 oz box"
- "~$6.49/lb"
- "~$8.99 for 16 oz jar"
- "~$3.99 for 8-pack"
- "~$5.29/gallon"

## Warning Level Guidelines:

{warning_guidelines}

## Search Instructions:

1. **Identify Product Category**: Determine what type of product this is (snack, beverage, meal, etc.)

2. **Search for Alternatives**: Find:
   {search_criteria}
   - Popular brands for this product type
   - Typical price ranges from major retailers (Amazon, Walmart, Target, Whole Foods)

3. **Verify Safety**: For each alternative:
   {verification_steps}
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
- Include real, purchasable products with estimated prices
- Include full product name with brand (e.g., "Oatly Oat Milk Original" not just "Oat Milk")
- **Price format MUST include size/unit with ~ symbol** (e.g., "~$4.99 for 12 oz box" or "~$6.49/lb", NOT just "$4.99")
- Keep tags concise (2-3 words each)
- Focus on widely available alternatives that can be purchased online

