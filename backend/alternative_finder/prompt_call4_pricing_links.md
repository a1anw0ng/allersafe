Use the web search tool to find current pricing and purchase links for safe products.

**IMPORTANT: This phase USES WEB SEARCH. Research current prices and availability.**

## Safe Products (excluding Dangerous):
{safe_products}

## Your Task - Research Pricing & Purchase Links:
For each safe product (Safe or Caution status), find current pricing and where to buy.

### Pricing Research Steps:

**For EACH safe product:**

1. **Search Major Retailers**:
   - Amazon - search for exact product name
   - Walmart - search for product
   - Target - search for product
   - Whole Foods / other specialty stores if relevant
   - Manufacturer website / direct purchase

2. **Find Current Prices**:
   - Look for current listed price
   - Note the package size/quantity
   - Find typical price range if varies
   - Use approximate prices with ~ symbol

3. **Verify Availability**:
   - Check if currently in stock
   - Note if product is regularly available
   - Identify primary retailers carrying this product

4. **Generate Purchase Links**:
   - **IMPORTANT**: Provide DIRECT product page URLs (e.g., https://www.amazon.com/dp/PRODUCTID)
   - DO NOT use redirect URLs or grounding API URLs
   - If direct URL not available, use retailer search URLs:
     - Amazon: https://www.amazon.com/s?k=[URL-encoded product name]
     - Walmart: https://www.walmart.com/search?q=[URL-encoded product name]
   - Manufacturer website if applicable

**Search Query Examples:**
- "[exact product name] price"
- "[exact product name] buy online"
- "[exact product name] Amazon"
- "[exact product name] Walmart"
- "[product name] [retailer] price"

**Price Format Examples:**
- "~$4.99 for 12 oz box"
- "~$6.49/lb"
- "~$8.99 for 16 oz jar"
- "~$3.99 for 8-pack"
- "~$12.99 for 32 oz bottle"

**Return ONLY valid JSON in this exact format:**
{{
  "pricing_results": [
    {{
      "product_name": "Exact product name",
      "price": "~$X.XX for [size/unit]",
      "price_range": "~$X.XX - $Y.YY" or null,
      "availability": "widely available|limited availability|specialty stores only",
      "purchase_links": [
        {{"retailer": "Amazon", "url": "direct product or search URL"}},
        {{"retailer": "Walmart", "url": "direct product or search URL"}},
        {{"retailer": "Target", "url": "direct product or search URL"}}
      ],
      "primary_retailers": ["Amazon", "Walmart", ...],
      "sources": [
        {{"title": "source", "url": "URL", "price_found": "$X.XX"}}
      ]
    }}
  ],
  "pricing_notes": "Any important notes about pricing, availability, or trends"
}}

**Important**:
- Search for ACTUAL current prices from real retailers
- Include package size in price (e.g., "for 12 oz" not just "$4.99")
- Use ~ symbol for approximate prices
- Provide direct links when possible, search URLs when direct link unavailable
- Focus on major online retailers (Amazon, Walmart, Target)
- Document all pricing sources
