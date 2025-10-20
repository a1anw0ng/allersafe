# Alternative Product Finder

Find safe alternative products for people with food allergies using Gemini 2.5 Flash with web search integration.

## How It Works

This module implements **Phases 4-8** of the AllerSafe pipeline:

**Phase 4**: Product Categorization
- Determines product type and category
- Example: "snack", "dairy product", "beverage"

**Phase 5**: General Category Search
- Searches for alternatives in the same category
- Uses web search for real-time product information

**Phase 6**: Brand-Specific Search
- Finds alternatives from specific allergy-friendly brands
- Targets companies known for allergen-free products

**Phase 7**: Store Availability Search
- Finds where to purchase alternatives
- Includes pricing and availability information

**Phase 8**: Final Ranking & Validation
- Sorts alternatives by safety and relevance
- Filters out duplicates and validates safety claims
- Returns top 5 alternatives

## Integration

This module is called by `product_analyzer.py` as part of the full 8-phase pipeline:

```python
from alternative_finder.alternative_finder import find_alternatives

alternatives = await find_alternatives(
    product_name="Reese's Peanut Butter Cups",
    allergens_to_avoid=["peanuts", "dairy"],
    product_category="snack"
)
```

## Output Schema

```json
[
  {
    "alternative_name": "SunButter Cups",
    "company": "SunButter",
    "purchase_links": [
      "https://www.amazon.com/sunbutter-cups",
      "https://www.target.com/sunbutter-cups"
    ],
    "price": "$6.99 USD",
    "warning_level": "Safe",
    "tags": ["peanut-free", "dairy-free", "gluten-free"],
    "reasoning": "Made with sunflower seed butter instead of peanut butter. Produced in a dedicated allergen-free facility."
  }
]
```

## Warning Levels

- **Safe**: No allergens detected, no cross-contamination risks
- **Caution**: May contain traces or processed in shared facilities with allergens
- **Dangerous**: Contains allergens from user's avoid list (filtered out)

## Key Features

- **5-Phase Processing**: Comprehensive search across categories, brands, and stores
- **Web Search Integration**: Real-time product information via Gemini grounding
- **Safety Validation**: Filters out products with user's allergens
- **Purchase Links**: Direct links to buy products online
- **Pricing Information**: Current prices from verified sources
- **Source Citations**: Every alternative includes supporting web sources
- **Duplicate Filtering**: Removes redundant products across phases
- **Safety-First Ranking**: Prioritizes "Safe" alternatives over "Caution"

## AI Model

- **Model**: Gemini 2.5 Flash via OpenRouter
- **Model ID**: `openrouter/google/gemini-2.5-flash-preview-09-2025`
- **Web Search**: Enabled via Vertex AI grounding
- **Temperature**: 0.7 for balanced creativity and accuracy