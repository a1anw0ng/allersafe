# AllerSafe - Allergen Detection & Alternative Finder

AI-powered food allergy safety system with real-time product analysis and safe alternative recommendations.

## Important Note

⚠️ **This project only works with food products that have their brand labeling and packaging visible.** The ideal setting would be seeing a product at a grocery store and taking a photo of it with the packaging clearly shown. The AI analyzes ingredient lists, nutrition labels, and allergen warnings printed on the packaging.

## System Architecture

**Frontend**: Next.js 14 (TypeScript, Tailwind CSS, Zustand)
**Backend**: FastAPI with streaming support (Python)
**AI Model**: Gemini 2.5 Flash via OpenRouter with web search
**Storage**: AWS S3 for image handling

### 8-Phase Analysis Pipeline

**Allergen Detection (Phases 1-3):**
1. Visual analysis with ingredient extraction
2. Web verification of product details
3. Final allergen assessment with severity rating

**Alternative Finding (Phases 4-8):**
4. Product categorization
5. General category alternatives search
6. Brand-specific alternatives search
7. Store availability search
8. Final alternatives ranking

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
OPENROUTER_API_KEY=your_openrouter_key
AWS_ACCESS_KEY_ID=your_aws_key
AWS_SECRET_ACCESS_KEY=your_aws_secret
AWS_REGION=us-east-2
AWS_S3_BUCKET_NAME=your_bucket_name

# Run with Docker
docker-compose up --build

# Or run locally
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

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
- **Multi-phase Verification**: Web search integration for accurate allergen detection
- **Safe Alternatives**: AI-powered recommendations with purchase links
- **Source Citations**: Every analysis includes verifiable web sources
- **Comprehensive Testing**: Built-in evaluation framework with metrics

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

- [Backend API Documentation](./backend/README.md)
- [Frontend Documentation](./allersafe/README.md)
- [Evaluation System](./backend/evaluation/README.md)
- [Alternative Finder Details](./backend/alternative_finder/README.md)

## Deployment

Both frontend and backend include Docker configurations and deployment configs for Railway/Render.

See individual README files for deployment instructions.