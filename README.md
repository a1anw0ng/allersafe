# AllerSafe - Allergen Detection & Alternative Finder

AI-powered food allergy safety system with real-time product analysis and safe alternative recommendations.

## Important Note

⚠️ **This project only works with food products that have their brand labeling and packaging visible.** The ideal setting would be seeing a product at a grocery store and taking a photo of it with the packaging clearly shown. The AI analyzes ingredient lists, nutrition labels, and allergen warnings printed on the packaging.

## System Architecture

**Frontend**: Next.js 16 (TypeScript, Tailwind CSS, Zustand)
**Backend**: FastAPI with streaming support (Python)
**AI Model**: Anthropic Claude Haiku 4.5 via AWS Bedrock (`us.anthropic.claude-haiku-4-5-20251001-v1:0`)
**Web Search**: Tavily API (used by RAG pattern on 4 of 8 phases)
**Image Storage**: AWS S3

### Retrieval-Augmented Generation (RAG)

Four of the eight phases need up-to-date, verifiable web information — real ingredient lists, real product availability, real prices. Bedrock has no built-in web search, so the backend implements the classic RAG pattern for those phases:

1. **Retrieve** — Python calls Tavily with a phase-specific query.
2. **Augment** — retrieved snippets are injected into the prompt as a "Web search results" block, with URLs preserved.
3. **Generate** — Claude reasons over the augmented prompt and returns JSON that cites the injected sources.

The other four phases (image analysis, allergen synthesis, categorization, final ranking) are pure LLM reasoning with no retrieval — the model already has everything it needs from prior-phase output.

### 8-Phase Analysis Pipeline

**Allergen Detection (Phases 1-3):**
1. Visual analysis with ingredient extraction (Claude vision, no retrieval)
2. Web verification of product details (**RAG** — Tavily + Claude)
3. Final allergen assessment with severity rating (Claude reasoning)

**Alternative Finding (Phases 4-8):**
4. Product categorization (Claude reasoning)
5. General category alternatives search (**RAG** — Tavily + Claude)
6. Brand-specific safety verification (**RAG** — Tavily + Claude, one query per candidate)
7. Store availability & pricing (**RAG** — Tavily + Claude, one query per candidate)
8. Final alternatives ranking (Claude reasoning)

## Project Structure

```
AllergyDetector/
├── allersafe/              # Next.js frontend application
│   ├── src/
│   │   ├── app/           # App router pages
│   │   ├── components/    # React components
│   │   └── store/         # Zustand state management
│   └── README.md
├── backend/               # FastAPI backend service
│   ├── main.py           # API endpoints
│   ├── allergen_detector/ # Phases 1-3
│   ├── alternative_finder/ # Phases 4-8
│   ├── utils.py           # Shared helpers (Tavily wrapper, source cleaning)
│   ├── evaluation/        # Testing & metrics
│   └── README.md
└── README.md             # This file
```

## Quick Start

### Backend Setup

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Configure environment (.env file)
TAVILY_API_KEY=your_tavily_key
AWS_ACCESS_KEY_ID=your_aws_key
AWS_SECRET_ACCESS_KEY=your_aws_secret
AWS_REGION=us-east-2
AWS_S3_BUCKET_NAME=your_bucket_name

# Run with Docker
docker-compose up --build

# Or run locally
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**IAM requirements** — the AWS credentials must have:
- **S3**: read/write access to `AWS_S3_BUCKET_NAME` (for uploaded product images).
- **Bedrock**: `bedrock:InvokeModel` and `bedrock:InvokeModelWithResponseStream` on Claude Haiku 4.5. The `AmazonBedrockFullAccess` managed policy covers this.
- **Region**: Bedrock model access must be enabled for `us-east-2` (matches `AWS_REGION`). The `us.` prefix in the model ID is a cross-region inference profile, required for Haiku 4.5.

### Frontend Setup

```bash
cd allersafe

# Install dependencies
npm install

# Configure environment (.env.local)
NEXT_PUBLIC_API_URL=http://localhost:8000

# Run development server
npm run dev
```

## Key Features

- **Real-time Streaming Analysis**: Server-sent events for live progress updates
- **Multi-phase RAG Verification**: Tavily-backed web search on ingredient facts, brand safety claims, and store availability
- **Safe Alternatives**: AI-powered recommendations with search-URL-based purchase links (guaranteed to resolve, unlike hallucinated product URLs)
- **Source Citations**: Every allergen and alternative claim is backed by a real Tavily-retrieved URL
- **Comprehensive Testing**: Built-in evaluation framework with metrics and per-model pricing

## API Endpoints

- `POST /api/analyze-product-stream` - Full analysis with SSE streaming
- `POST /api/analyze-product` - Full analysis (non-streaming)
- `POST /api/detect-allergens` - Allergen detection only (phases 1-3)
- `POST /api/find-alternatives` - Alternative finding only (phases 4-8)
- `GET /health` - Health check

## Severity Levels

- **Safe**: No allergens detected, product is safe to consume
- **Caution**: May contain traces or processed in shared facilities
- **Dangerous**: Contains confirmed allergens from user's list
- **NotDetected**: No product visible or image unclear

## Documentation

- [System Architecture](./docs/architecture.md) — full data flow, phase breakdown, design decisions
- [Backend API Documentation](./backend/README.md)
- [Frontend Documentation](./allersafe/README.md)
- [Evaluation System](./backend/evaluation/README.md)
- [Alternative Finder Details](./backend/alternative_finder/README.md)

## Deployment

- **Frontend**: Vercel (auto-deploys on push to `main`)
- **Backend**: Railway (Docker-based build via `backend/Dockerfile`, binds to Railway's `$PORT`)

See individual README files for host-specific instructions.
