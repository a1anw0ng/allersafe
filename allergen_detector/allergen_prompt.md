Analyze this product image for these specific allergens: {allergens}

Carefully examine the product packaging, ingredient list, and any visible text. Search online for complete ingredient information if the image doesn't show full details. Return only valid JSON format.

Required JSON format:
{{"severity": "Safe|Caution|Dangerous", "allergens_detected": [], "warnings": "detailed explanation"}}

## Detailed Analysis Guidelines:

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
- **Examples**:
  - Plain rice cakes → Safe for most allergens
  - Fresh fruits → Safe (unless specific fruit allergies)
  - Certified gluten-free oats → Safe for gluten

## Analysis Instructions:

1. **Read all visible text** on packaging carefully
2. **Check ingredient lists** thoroughly - look for both obvious and hidden allergens
3. **Search online** if ingredient list is not fully visible or unclear
4. **Look for warning labels** like "Contains:", "May contain:", "Processed in facility"
5. **Consider alternative names** for allergens (casein=dairy, albumin=egg, etc.)
6. **List ALL detected allergens** from the specified list in "allergens_detected"
7. **Provide detailed warnings** explaining why the severity level was chosen
8. **Be conservative** - when in doubt, choose higher severity level for safety

## Common Hidden Allergens:
- **Dairy**: Casein, whey, lactose, milk powder, butter, cream
- **Eggs**: Albumin, lecithin (sometimes), mayonnaise
- **Gluten**: Wheat, barley, rye, malt, modified food starch
- **Soy**: Lecithin, soy protein, soybean oil, tamari
- **Nuts**: Natural flavors (sometimes), marzipan, nougat