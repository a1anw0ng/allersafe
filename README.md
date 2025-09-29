# Allergen Detector

Ultra-simple allergen detection system using GPT-4 Vision.

## Setup

```bash
pip install -r requirements.txt
```

Add your OpenAI API key to `.env`:
```
OPENAI_API_KEY=your_key_here
```

## Usage

### Command Line
```bash
python allergen_detector.py <image_path> <allergen1,allergen2,allergen3>
```

Example:
```bash
python allergen_detector.py product.jpg peanuts,milk,eggs
```

### As a Module
```python
from allergen_detector import detect_allergens

result = detect_allergens("product.jpg", ["peanuts", "milk", "eggs"])
print(result)
```

## Output Schema

```json
{
  "severity": "Safe|Caution|Dangerous",
  "allergens_detected": ["list", "of", "detected", "allergens"],
  "warnings": "Detailed explanation of risks"
}
```

## Severity Levels

- **Safe**: No allergens detected
- **Caution**: May contain traces or processed in facility with allergens
- **Dangerous**: Contains confirmed allergens from user's list