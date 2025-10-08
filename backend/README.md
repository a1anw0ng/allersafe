# AllerSafe Backend API

FastAPI-based backend service for food allergy detection and safe alternative finder.

## Features

- 🔍 **Allergen Detection**: Analyze product images for specific allergens using AI
- 🐳 **Dockerized**: Easy deployment with Docker and Docker Compose
- 🚀 **FastAPI**: High-performance async API
- ☁️ **S3 Integration**: Direct image download from AWS S3
- 📝 **Auto-documentation**: Interactive API docs at `/docs`

## Quick Start

### Using Docker Compose (Recommended)

1. **Ensure `.env` file exists** with required variables:
   ```env
   GEMINI_API_KEY=your_gemini_api_key
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

### POST `/api/detect-allergens`

Detect allergens in a product image from S3.

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
  "severity": "Safe|Caution|Dangerous",
  "allergens_detected": ["Milk"],
  "warnings": "Detailed explanation of the analysis"
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
| `GEMINI_API_KEY` | Google Gemini API key for AI analysis | Yes |
| `AWS_ACCESS_KEY_ID` | AWS access key for S3 | Yes |
| `AWS_SECRET_ACCESS_KEY` | AWS secret key for S3 | Yes |
| `AWS_REGION` | AWS region (e.g., us-east-2) | Yes |
| `AWS_S3_BUCKET_NAME` | S3 bucket name | Yes |

## Project Structure

```
backend/
├── main.py                      # FastAPI application
├── requirements.txt             # Python dependencies
├── Dockerfile                   # Docker image definition
├── docker-compose.yml          # Docker Compose configuration
├── .dockerignore               # Docker build exclusions
├── .env                        # Environment variables (not in git)
├── allergen_detector/
│   ├── allergen_detector.py    # Allergen detection logic
│   └── allergen_prompt.md      # AI prompt template
└── alternative_finder/
    ├── alternative_finder.py   # Alternative product finder
    └── alternative_prompt.md   # AI prompt template
```

## Testing the API

### Using curl

```bash
# Health check
curl http://localhost:8000/health

# Detect allergens
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

response = requests.post(
    "http://localhost:8000/api/detect-allergens",
    json={
        "s3_image_url": "https://allersafe.s3.us-east-2.amazonaws.com/uploads/product-123.jpg",
        "allergens": ["Milk", "Peanuts", "Eggs"]
    }
)

print(response.json())
```

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
