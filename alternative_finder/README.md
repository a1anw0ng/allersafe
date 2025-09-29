# Alternative Product Finder

Find safe alternative products for people with food allergies using GPT-5 with web search.

## How It Works

1. **Input**: Product image + list of user's allergies
2. **Processing**: GPT-5 analyzes the product and searches for alternatives
3. **Output**: Up to 5 safe alternative products with purchase links

## Usage

```bash
python3 alternative_finder.py
```

Currently uses hard-coded test values:
- Image: `test_product.jpg`
- Allergens: `["nuts", "dairy", "gluten"]`

## Output Schema

```json
[
  {
    "alternative_name": "Product name",
    "company": "Manufacturer",
    "purchase_links": ["URL1", "URL2"],
    "price": "$X.XX USD",
    "warning_level": "Safe|Caution",
    "tags": ["allergen-free", "dietary-tag"]
  }
]
```

## Warning Levels

- **Safe**: No allergens, no cross-contamination risks
- **Caution**: May contain traces or processed in shared facilities

## Features

- Prioritizes completely safe products
- Includes real purchase links with current prices
- Returns maximum 5 alternatives
- Uses GPT-5's web search for real-time product information