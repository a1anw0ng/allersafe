{allergen_instruction}

**FIRST**: Verify that the image contains a food or consumer product package with visible labels, ingredients, or product information. If the image shows a person, animal, scenery, or anything other than a product package, return:
{{"severity": "NotDetected", "allergens_detected": [], "warnings": "No food product detected. [Briefly describe what you see in the image instead, e.g., 'Image shows a person in an indoor setting']"}}

**ONLY IF A PRODUCT IS DETECTED**: Perform a two-phase analysis:

### Phase 1: Image Analysis
Carefully examine the product packaging visible in the image:
- Read all visible product names, brands, and labels
- Analyze the ingredient list if visible
- Look for any allergen warnings or statements on the packaging
- Note any "Contains:", "May contain:", or facility warnings

### Phase 2: Deep Background Research (Using Web Tool)
Use the web search tool to conduct extensive research on the product:
- Search for complete ingredient information if not fully visible in the image
- Research the manufacturing company to identify:
  - Other products they manufacture that may contain allergens from the user's profile
  - Whether their processing facility also processes any of the user's allergens
  - Any cross-contamination risks or recalls related to allergens
- Look for allergen-related warnings or advisories for this specific product
- YOU MUST **directly cite any links or sources used** in your warnings response

**Important**: Return only valid JSON format with detailed warnings explaining your findings and citing sources.
- YOU MUST **directly cite any links or sources used** in your warnings response

Required JSON format:
{{"severity": "Safe|Caution|Dangerous|NotDetected", "allergens_detected": [], "warnings": "detailed explanation"}}

## Detailed Analysis Guidelines:

### NOT DETECTED (No Product Found)
Image does not contain a product package or food label:
- **People, animals, or scenery**: Image shows non-product subjects
- **No packaging visible**: No product labels, boxes, or containers visible
- **Unclear/blurry**: Cannot identify any product information
- **Examples**:
  - Selfies or photos of people
  - Pictures of pets or animals
  - Landscapes or random objects
  - Blank walls or surfaces

### DANGEROUS (Immediate Risk)
Product directly contains one or more of the specified allergens as ingredients:
- **Direct ingredients**: Allergen is explicitly listed in ingredients (milk, eggs, wheat, peanuts, etc.)
- **Derived ingredients**: Contains derivatives (whey from milk, lecithin from soy, gluten from wheat)
- **Alternative names**: Check for alternate names (casein=dairy, albumin=egg, etc.)
- **Examples**: 
  - Hot Cheetos → Dangerous for dairy (contains cheese powder)
  - Bread → Dangerous for gluten (contains wheat flour)
  - Snickers → Dangerous for nuts and dairy (contains peanuts and milk chocolate)

### CAUTION (Potential Risk)
Cross-contamination warnings or processing facility risks:
- **"May contain" statements**: Product processed in facility with allergens
- **"Processed in facility that also processes"** warnings
- **Shared equipment**: Manufacturing equipment used for multiple products
- **Cross-contamination risk**: Even trace amounts can trigger severe reactions
- **Examples**:
  - Sunflower seeds → Caution for tree nuts (facility also processes almonds)
  - Granola bars → Caution for peanuts ("may contain peanuts")
  - Chocolate → Caution for nuts (manufactured on shared equipment)

### SAFE (No Risk)
No allergen present and no cross-contamination warnings:
- **No direct allergens**: None of the specified allergens in ingredient list
- **No facility warnings**: No "may contain" or processing facility statements
- **Certified allergen-free**: Products specifically labeled as allergen-free
- **No dietary restrictions**: If allergens list is "none", product is automatically safe since user has no restrictions
- **Examples**:
  - Plain rice cakes → Safe for most allergens
  - Fresh fruits → Safe (unless specific fruit allergies)
  - Certified gluten-free oats → Safe for gluten
  - Any food product when allergens="none" → Safe (describe the product in warnings)

## Analysis Instructions:

1. **Read all visible text** on packaging carefully
2. **Check ingredient lists** thoroughly - look for both obvious and hidden allergens
3. **Search online** if ingredient list is not fully visible or unclear
4. **Look for warning labels** like "Contains:", "May contain:", "Processed in facility"
5. **Consider alternative names** for allergens (casein=dairy, albumin=egg, etc.)
6. **List ALL detected allergens** from the specified list in "allergens_detected"
7. **Provide detailed warnings** explaining why the severity level was chosen AND describe what you see in the image:
   - If NotDetected: Describe what's in the image (e.g., "No food product detected. Image shows a person sitting indoors")
   - If Safe/Caution/Dangerous: Identify the product and explain the allergen analysis (e.g., "Product identified as Lay's Classic Potato Chips. Safe - contains no allergens from your profile")
8. **Be conservative** - when in doubt, choose higher severity level for safety

## Common Hidden Allergens:
- **Dairy**: Casein, whey, lactose, milk powder, butter, cream
- **Eggs**: Albumin, lecithin (sometimes), mayonnaise
- **Gluten**: Wheat, barley, rye, malt, modified food starch
- **Soy**: Lecithin, soy protein, soybean oil, tamari
- **Nuts**: Natural flavors (sometimes), marzipan, nougat