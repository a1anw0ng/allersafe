Synthesize all research and select the top 5 alternative products.

## All Research Results:

### Category Analysis:
{category_analysis}

### Candidate Products:
{candidates}

### Safety Verification:
{safety_verification}

### Pricing & Links:
{pricing_info}

## Your Task - Final Selection & Synthesis:
Combine all information and select the top 5 alternative products.

### Selection Criteria:

1. **Prioritize Safety**:
   - SAFE products come first
   - CAUTION products only if insufficient Safe options
   - Never include DANGEROUS products

2. **Consider Quality Indicators**:
   - Products with certifications
   - Well-known allergen-free brands
   - Products with complete safety information
   - Good availability and pricing

3. **Ensure Diversity**:
   - Try to include variety of brands
   - Different price points if possible
   - Mix of widely available and specialty options

4. **Limit to 5 Products**:
   - Select top 5 alternatives only
   - Rank by safety first, then quality/availability

### Output Format Requirements:

**Generate tags (2-3 per product):**
- Allergen-specific: "peanut-free", "dairy-free", "gluten-free", "nut-free"
- Dietary: "vegan", "kosher", "halal", "organic", "non-GMO"
- Category: "high-protein", "low-sugar", "whole-grain", "certified-allergen-free"

**Warning level mapping:**
- "Safe" → product passed all safety checks
- "Caution" → has cross-contamination warnings or uncertainty

**Return ONLY valid JSON array with exactly this format:**
[
  {{
    "alternative_name": "Full product name with brand and variant",
    "company": "Manufacturer name",
    "image_url": "https://direct-image-url.com/product.jpg",
    "purchase_links": [
      "https://www.amazon.com/...",
      "https://www.walmart.com/..."
    ],
    "price": "~$X.XX for [size/unit]",
    "warning_level": "Safe|Caution",
    "tags": ["tag1", "tag2", "tag3"],
    "reasoning": "Brief explanation (2-3 sentences) of why this alternative was chosen. Include: allergen safety status, certifications, how it compares to the original product, and any special features that make it a good replacement."
  }}
]

**Important Requirements:**
- Return exactly 5 alternatives (or fewer if less than 5 safe options exist)
- List SAFE products before CAUTION products
- Each alternative must have complete information (name, company, image, links, price, tags, reasoning)
- Price MUST include size/unit with ~ symbol (e.g., "~$4.99 for 12 oz box")
- **Reasoning**: Based on safety verification data, explain why this is a good alternative. Reference allergen-free status, certifications from the safety verification phase, and key benefits compared to the original product
- **Image URL**: Provide a direct product image URL from your web research. Must be a real, working image URL (jpg, png, webp). If no image found, use empty string "".
- **Purchase links**: Use direct retailer URLs from pricing phase. If URLs are unavailable or invalid, use:
  - Amazon: https://www.amazon.com/s?k=[URL-encoded-product-name]
  - Walmart: https://www.walmart.com/search?q=[URL-encoded-product-name]
- DO NOT include redirect URLs or vertexaisearch URLs
- Tags must be concise (2-3 words max each)
- Include only products that were verified in previous phases
- If user has no allergens, all products are "Safe"

**Edge Cases:**
- If no alternatives found: return empty array []
- If less than 5 safe options: return what's available (prefer Safe over Caution)
- If exact pricing unavailable: provide a typical price range based on product category (e.g., "~$4-7 for 10 oz box"). Never use "Price varies" or "See retailer".
