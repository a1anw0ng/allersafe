# AllerSafe Backend API

FastAPI-based backend service for food allergy detection and safe alternative finder.

## Important Note

⚠️ **This system only works with food products that have their brand labeling and packaging visible.** The ideal use case is photographing packaged products at a grocery store where the ingredient list, nutrition label, and allergen warnings are clearly visible on the packaging. The AI requires this information to accurately detect allergens.

## Features

- 🔍 **8-Phase Analysis Pipeline**: allergen detection + alternative finding
- 🧠 **AI Model**: Anthropic Claude Haiku 4.5 via AWS Bedrock (cross-region inference profile `us.anthropic.claude-haiku-4-5-20251001-v1:0`)
- 🌐 **RAG Web Search**: Tavily API retrieves live sources; results are injected into Claude prompts on 4 of the 8 phases
- 📡 **Streaming Support**: Server-sent events for real-time progress updates
- 🐳 **Dockerized**: `backend/Dockerfile` binds uvicorn to Railway's `$PORT` for portable deploy
- 🚀 **FastAPI**: async request handling and SSE
- ☁️ **AWS S3**: image storage for uploaded product photos
- 📝 **Auto-documentation**: Interactive API docs at `/docs`
- 🧪 **Evaluation Framework**: built-in tests with per-model pricing (Gemini Flash, Claude Sonnet, Claude 3.5 Haiku, Claude Haiku 4.5)

## Architecture: Retrieval-Augmented Generation (RAG)

Bedrock has no built-in web search. To keep the "sources you can click on" feature that safety-critical allergen and alternative claims depend on, the backend implements the RAG pattern on the four phases that need live data:

```
Python (this backend)          Tavily API              AWS Bedrock
─────────────────────          ──────────              ───────────
build phase-specific query ──> web search  ──> results
                                                  │
inject results into prompt <──────────────────────┘
send augmented prompt ─────────────────────────────────> Claude Haiku 4.5
                                                              │
receive JSON answer + cited URLs <────────────────────────────┘
```

**RAG phases**: 2 (product verification), 5 (find candidates), 6 (verify safety per candidate), 7 (pricing per candidate).

**Non-RAG phases**: 1 (image analysis — Claude vision), 3 (allergen synthesis — reasoning), 4 (categorization — reasoning), 8 (final ranking — reasoning). These don't retrieve because the task is judgment, not fact-lookup.

**Tavily API call budget per full scan**: ~8 searches (1 for phase 2, 1 for phase 5, up to 3 for phase 6, up to 3 for phase 7). Tavily's free tier is 1,000 searches/month → ~125 full scans/month at no cost.

## Quick Start

### Using Docker Compose (Recommended)

1. **Ensure `.env` file exists** with required variables:
   ```env
   TAVILY_API_KEY=tvly-...
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
# Build (from repo root — Dockerfile expects backend/ as a subdirectory)
docker build -f backend/Dockerfile -t allersafe-backend .

# Run
docker run -p 8000:8000 --env-file backend/.env allersafe-backend
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

Note: `image_url` fields returned by Claude are stripped server-side, since the model cannot know real product image URLs and would otherwise hallucinate broken CDN links. `purchase_links` are similarly rewritten to guaranteed-resolvable Amazon/Walmart/Target search URLs.

### POST `/api/detect-allergens`

Allergen detection only (Phases 1-3), no alternatives. Same request/response shape as above but without `alternatives`.

### POST `/api/find-alternatives`

Alternative finding only (Phases 4-8), requires product info from detection.

### GET `/health`

Health check endpoint for monitoring.

```json
{
  "status": "healthy",
  "service": "allersafe-backend"
}
```

## 8-Phase Pipeline Detail

**Phases 1-3: Allergen Detection** (`allergen_detector/`)
1. **Visual Analysis** — Claude vision reads the packaging image, extracts product name, brand, and any visible ingredient/allergen text. No retrieval.
2. **Web Verification** — **RAG**: Tavily searches `"{product_name} ingredients allergens"`; results injected into prompt; Claude produces a verified ingredient list with cited sources.
3. **Final Assessment** — Claude synthesizes phases 1 and 2 into a `severity` (Safe / Caution / Dangerous / NotDetected), `allergens_detected` array, and warning explanation.

**Phases 4-8: Alternative Finding** (`alternative_finder/`)
4. **Categorization** — Claude reasons about product category, allergen constraints, and generates search terms for phase 5.
5. **Find Candidates** — **RAG**: Tavily searches using the LLM-generated terms; Claude proposes 5-10 candidate alternatives.
6. **Verify Safety** — **RAG**: For the top 3 candidates, Tavily fetches ingredient/allergen info per product; Claude flags any that contain the user's allergens as `Dangerous` (excluded from final).
7. **Pricing & Availability** — **RAG**: For safe candidates, Tavily fetches price/store info per product.
8. **Ranking** — Claude produces the final top-5 list with `warning_level`, `tags`, `reasoning`. `purchase_links` are then rewritten server-side to search URLs (never Claude-generated direct product URLs, which frequently 404).

## Docker Commands

```bash
docker-compose up -d              # Start in detached mode
docker-compose logs -f backend    # Tail logs
docker-compose down               # Stop
docker-compose up --build         # Rebuild after code changes
docker-compose down -v            # Remove volumes too
```

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `TAVILY_API_KEY` | Tavily API key for RAG web search on phases 2, 5, 6, 7 | Yes |
| `AWS_ACCESS_KEY_ID` | AWS access key. Used for both S3 (image storage) and Bedrock (LLM calls). | Yes |
| `AWS_SECRET_ACCESS_KEY` | AWS secret key. Same IAM user must have S3 + Bedrock permissions. | Yes |
| `AWS_REGION` | Must be `us-east-2` (matches Bedrock cross-region profile prefix `us.` and the S3 bucket region). | Yes |
| `AWS_S3_BUCKET_NAME` | S3 bucket name for product image uploads. | Yes |
| `PORT` | Optional. Falls back to 8000. On Railway, injected automatically. | No |

**IAM policy required on the AWS user** (managed policy `AmazonBedrockFullAccess` covers Bedrock; add S3 read/write for the bucket separately, or use `AmazonS3FullAccess` in dev):
- `bedrock:InvokeModel`, `bedrock:InvokeModelWithResponseStream`
- `s3:GetObject`, `s3:PutObject` on the bucket

## Project Structure

```
backend/
├── main.py                      # FastAPI app + endpoint handlers
├── product_analyzer.py          # 8-phase pipeline orchestrator
├── utils.py                     # tavily_search(), source cleaning helpers
├── requirements.txt             # Python dependencies (incl. litellm, tavily-python)
├── Dockerfile                   # Docker image; CMD binds uvicorn to $PORT
├── docker-compose.yml
├── railway.json                 # Railway build config (builder=DOCKERFILE)
├── .env                         # Environment variables (gitignored)
├── allergen_detector/
│   ├── allergen_detector.py    # Phases 1-3
│   └── prompt_call*.md          # Per-phase prompt templates
├── alternative_finder/
│   ├── alternative_finder.py   # Phases 4-8
│   ├── prompt_call*.md          # Per-phase prompt templates
│   └── README.md
└── evaluation/
    ├── run_evaluation.py       # Test runner
    ├── metrics.py              # Metrics + per-model pricing table
    ├── report_generator.py
    ├── test_cases.json
    ├── test_images/
    └── README.md
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
```

### Using Python

```python
import requests, sseclient

# Streaming analysis (SSE)
response = requests.post(
    "http://localhost:8000/api/analyze-product-stream",
    json={
        "s3_image_url": "https://allersafe.s3.us-east-2.amazonaws.com/uploads/product-123.jpg",
        "allergens": ["Milk", "Peanuts"]
    },
    stream=True
)
for event in sseclient.SSEClient(response).events():
    print(event.data)
```

## Running Evaluation Tests

```bash
python -m evaluation.run_evaluation --verbose      # all tests
python -m evaluation.run_evaluation --test-id 001  # one test
python -m evaluation.run_evaluation --output results.json
```

See [evaluation/README.md](./evaluation/README.md) for details on the metrics framework.

## Production Deployment (Railway)

The backend is deployed on Railway using the Dockerfile builder:

- **Builder**: Dockerfile (set explicitly in `railway.json`; do not use Nixpacks/Railpack which will fail on the multi-project repo layout).
- **Root Directory**: `/` (repo root — the Dockerfile reaches into `backend/` via `COPY backend/...`).
- **Target Port** (Railway → Networking): must match the port uvicorn binds to. Since the Dockerfile CMD uses `${PORT:-8000}` and Railway injects `PORT=8080`, set Target Port to `8080`.
- **Env vars**: set `TAVILY_API_KEY`, `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_REGION`, `AWS_S3_BUCKET_NAME` in the Railway Variables tab.

## Troubleshooting

**`OpenrouterException: No cookie auth credentials found`** — the running container has the old pre-Bedrock code. Force a fresh deploy so Railway picks up the current commit.

**`AccessDeniedException: bedrock:InvokeModel not authorized`** — the IAM user is missing Bedrock permissions. Attach `AmazonBedrockFullAccess` (or a scoped policy with `bedrock:InvokeModel*`).

**`Invocation of model ID ... with on-demand throughput isn't supported`** — the model requires a cross-region inference profile. The model ID must start with `us.` (already set in code).

**`The image was specified using the image/jpeg media type, but the image appears to be a image/png image`** — Claude validates the declared MIME against the actual bytes. The backend sniffs magic bytes to pick the right type; if you're uploading an unusual format (HEIC, etc.) it will fall back to `image/jpeg` and fail. Convert to JPEG/PNG/WEBP client-side.

**`Tavily search failed: ModuleNotFoundError: No module named 'tavily'`** — `pip install -r requirements.txt` didn't include `tavily-python`. Rebuild the container.

**502 from Railway on all requests** — port mismatch. Uvicorn is listening on one port, Railway's proxy is routing to another. Match Target Port in the Networking settings to the port shown in `Uvicorn running on http://0.0.0.0:<port>` in the runtime logs.

**Container exits immediately** — check `docker-compose logs backend` (local) or `npx @railway/cli logs` (Railway). Usually a missing env var.

## License

Proprietary - AllerSafe
