# AllerSafe Backend API

FastAPI-based backend service for food allergy detection and safe alternative finder.

## Features

- 🔍 **8-Phase Analysis Pipeline**: Comprehensive allergen detection + alternative finding
- 🌐 **Web Search Integration**: Real-time verification via Gemini 2.5 Flash with grounding
- 📡 **Streaming Support**: Server-sent events for real-time progress updates
- 🐳 **Dockerized**: Easy deployment with Docker and Docker Compose
- 🚀 **FastAPI**: High-performance async API
- ☁️ **S3 Integration**: Direct image download from AWS S3
- 📝 **Auto-documentation**: Interactive API docs at `/docs`
- 🧪 **Evaluation Framework**: Built-in testing system with comprehensive metrics

## Quick Start

### Using Docker Compose (Recommended)

1. **Ensure `.env` file exists** with required variables:
   ```env
   OPENROUTER_API_KEY=your_openrouter_api_key
   AWS_ACCESS_KEY_ID=your_aws_access_key
   AWS_SECRET_ACCESS_KEY=your_aws_secret_key
   AWS_REGION=us-east-2
   AWS_S3_BUCKET_NAME=allersafe
   ```

2. **Build and run**:
   ```bash
   docker-compose up --build
   ```

3. **Access the API**:
   - API: http://localhost:8000
   - Interactive docs: http://localhost:8000/docs
   - Health check: http://localhost:8000/health

### Using Docker Only

```bash
# Build
docker build -t allersafe-backend .

# Run
docker run -p 8000:8000 --env-file .env allersafe-backend
```

### Local Development (without Docker)

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the server**:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

## API Endpoints

### POST `/api/analyze-product-stream` (Primary Endpoint)

Full 8-phase analysis with Server-Sent Events streaming for real-time progress updates.

**Request Body:**
```json
{
  "s3_image_url": "https://allersafe.s3.us-east-2.amazonaws.com/uploads/product-123.jpg",
  "allergens": ["Milk", "Peanuts", "Eggs"]
}
```

**Response:** SSE stream of JSON events
```json
{"phase": 1, "status": "Processing", "message": "Analyzing image..."}
{"phase": 3, "status": "Complete", "data": {...}}
{"phase": 8, "status": "Complete", "data": {"alternatives": [...]}}
```

### POST `/api/analyze-product`

Full 8-phase analysis without streaming (returns complete result).

**Request Body:** Same as above

**Response:**
```json
{
  "severity": "Safe|Caution|Dangerous|NotDetected",
  "allergens_detected": ["Milk"],
  "warnings": "Detailed explanation",
  "sources": [{"title": "...", "url": "..."}],
  "alternatives": [
    {
      "alternative_name": "Safe Product",
      "company": "Brand Name",
      "purchase_links": ["https://..."],
      "price": "$5.99 USD",
      "warning_level": "Safe",
      "tags": ["dairy-free", "nut-free"],
      "reasoning": "..."
    }
  ]
}
```

### POST `/api/detect-allergens`

Allergen detection only (Phases 1-3), no alternatives.

**Request Body:**
```json
{
  "s3_image_url": "https://allersafe.s3.us-east-2.amazonaws.com/uploads/product-123.jpg",
  "allergens": ["Milk", "Peanuts", "Eggs"]
}
```

**Response:**
```json
{
  "severity": "Safe|Caution|Dangerous|NotDetected",
  "allergens_detected": ["Milk"],
  "warnings": "Detailed explanation",
  "sources": [{"title": "Product Info", "url": "https://..."}]
}
```

### POST `/api/find-alternatives`

Alternative finding only (Phases 4-8), requires product info from detection.

**Request Body:**
```json
{
  "product_name": "Reese's Peanut Butter Cups",
  "allergens_to_avoid": ["peanuts", "dairy"],
  "product_category": "snack"
}
```

**Response:**
```json
{
  "alternatives": [
    {
      "alternative_name": "SunButter Cups",
      "company": "SunButter",
      "purchase_links": ["https://amazon.com/..."],
      "price": "$6.99 USD",
      "warning_level": "Safe",
      "tags": ["peanut-free", "dairy-free"],
      "reasoning": "Made with sunflower seed butter..."
    }
  ]
}
```

### GET `/health`

Health check endpoint for monitoring.

**Response:**
```json
{
  "status": "healthy",
  "service": "allersafe-backend"
}
```

## 8-Phase Pipeline Architecture

**Phases 1-3: Allergen Detection**
1. **Visual Analysis** - Extract ingredients from product image
2. **Web Verification** - Search for product information online
3. **Final Assessment** - Determine severity and allergen presence

**Phases 4-8: Alternative Finding**
4. **Categorization** - Identify product category and type
5. **General Search** - Find alternatives in same category
6. **Brand Search** - Find specific brand alternatives
7. **Store Search** - Find where to buy alternatives
8. **Ranking** - Sort and filter best alternatives

## Docker Commands

```bash
# Build and start in detached mode
docker-compose up -d

# View logs
docker-compose logs -f backend

# Stop services
docker-compose down

# Rebuild after code changes
docker-compose up --build

# Remove everything (including volumes)
docker-compose down -v
```

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENROUTER_API_KEY` | OpenRouter API key for Gemini 2.5 Flash access | Yes |
| `AWS_ACCESS_KEY_ID` | AWS access key for S3 image storage | Yes |
| `AWS_SECRET_ACCESS_KEY` | AWS secret key for S3 image storage | Yes |
| `AWS_REGION` | AWS region (e.g., us-east-2) | Yes |
| `AWS_S3_BUCKET_NAME` | S3 bucket name for image uploads | Yes |

## Project Structure

```
backend/
├── main.py                      # FastAPI application with all endpoints
├── product_analyzer.py          # Full 8-phase pipeline orchestrator
├── utils.py                     # Shared utilities and source extraction
├── requirements.txt             # Python dependencies
├── Dockerfile                   # Docker image definition
├── docker-compose.yml          # Docker Compose configuration
├── .env                        # Environment variables (not in git)
├── allergen_detector/
│   ├── allergen_detector.py    # Phases 1-3: Allergen detection
│   └── allergen_prompt.md      # AI prompt templates
├── alternative_finder/
│   ├── alternative_finder.py   # Phases 4-8: Alternative finding
│   ├── alternative_prompt.md   # AI prompt templates
│   └── README.md               # Alternative finder documentation
└── evaluation/
    ├── run_evaluation.py       # Test runner
    ├── metrics.py              # Metrics calculation
    ├── report_generator.py     # Report generation
    ├── test_cases.json         # Test dataset
    ├── test_images/            # Test images
    └── README.md               # Evaluation documentation
```

## Testing the API

### Using curl

```bash
# Health check
curl http://localhost:8000/health

# Full analysis (non-streaming)
curl -X POST http://localhost:8000/api/analyze-product \
  -H "Content-Type: application/json" \
  -d '{
    "s3_image_url": "https://allersafe.s3.us-east-2.amazonaws.com/uploads/product-123.jpg",
    "allergens": ["Milk", "Peanuts"]
  }'

# Allergen detection only
curl -X POST http://localhost:8000/api/detect-allergens \
  -H "Content-Type: application/json" \
  -d '{
    "s3_image_url": "https://allersafe.s3.us-east-2.amazonaws.com/uploads/product-123.jpg",
    "allergens": ["Milk", "Peanuts"]
  }'
```

### Using Python

```python
import requests

# Full analysis
response = requests.post(
    "http://localhost:8000/api/analyze-product",
    json={
        "s3_image_url": "https://allersafe.s3.us-east-2.amazonaws.com/uploads/product-123.jpg",
        "allergens": ["Milk", "Peanuts", "Eggs"]
    }
)

print(response.json())

# Streaming analysis (SSE)
import sseclient

response = requests.post(
    "http://localhost:8000/api/analyze-product-stream",
    json={
        "s3_image_url": "https://allersafe.s3.us-east-2.amazonaws.com/uploads/product-123.jpg",
        "allergens": ["Milk", "Peanuts"]
    },
    stream=True
)

client = sseclient.SSEClient(response)
for event in client.events():
    print(event.data)
```

## Running Evaluation Tests

```bash
# Run all evaluation tests
python -m evaluation.run_evaluation --verbose

# Run specific test
python -m evaluation.run_evaluation --test-id 001

# Save results to file
python -m evaluation.run_evaluation --output results.json
```

See [evaluation/README.md](./evaluation/README.md) for detailed testing documentation.

## Production Deployment

1. **Update CORS settings** in `main.py`:
   ```python
   allow_origins=["https://yourdomain.com"]
   ```

2. **Remove development volumes** from `docker-compose.yml`

3. **Use production-grade secrets management** instead of `.env` files

4. **Set up reverse proxy** (nginx/traefik) for HTTPS

5. **Configure monitoring and logging**

## Troubleshooting

**Issue**: Container exits immediately
- Check logs: `docker-compose logs backend`
- Verify `.env` file exists and contains all required variables

**Issue**: S3 access denied
- Verify AWS credentials in `.env`
- Check IAM permissions for S3 bucket access

**Issue**: Port 8000 already in use
- Change port mapping in `docker-compose.yml`: `"8001:8000"`

## License

Proprietary - AllerSafe
