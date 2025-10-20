# AllerSafe - Food Allergy Safety App

AllerSafe helps people with dietary restrictions and allergies find safe food alternatives by scanning products and meals.

## Important Note

⚠️ **This app only works with food products that have their brand labeling and packaging visible.** The ideal use case is photographing packaged products at a grocery store where the ingredient list, nutrition label, and allergen warnings are clearly visible. The AI analyzes this packaging information to detect allergens accurately.

## Features

### Currently Implemented
- **Product Scanner**: Scan grocery items to detect allergens in real-time
- **Alternative Finder**: Get AI-powered safe alternative recommendations
- **Streaming Analysis**: Live progress updates during 8-phase analysis
- **Safety Ratings**: Clear severity indicators (Safe/Caution/Dangerous)
- **Shopping Links**: Direct purchase links for alternative products
- **Source Citations**: Web sources for all allergen and alternative information
- **Personalized Profiles**: Save dietary restrictions and allergen list

### In Development
- **Restaurant Finder**: Scan meals to discover safe dining options
- **Map Integration**: Find nearby restaurants that accommodate your needs
- **Offline Mode**: Cached product database for offline scanning

## Getting Started

### Prerequisites

- Node.js 18+ installed
- npm or yarn package manager

### Installation

1. Clone the repository:
```bash
cd allersafe
```

2. Install dependencies:
```bash
npm install
```

3. Set up environment variables in `.env.local`:
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_AWS_S3_BUCKET_NAME=your_bucket_name
NEXT_PUBLIC_AWS_REGION=us-east-2
```

**Note**: The frontend connects to the FastAPI backend for all AI processing. No direct AI API keys are needed in the frontend.

### Running the Development Server

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) to view the app.

## Project Structure

```
src/
├── app/                  # Next.js app router pages
│   ├── groceries/       # Grocery scanning flow
│   ├── restaurants/     # Restaurant finding flow
│   └── profile/         # User profile management
├── components/          # React components
│   ├── navigation/      # Navigation components
│   ├── scan/           # Camera and scanning components
│   ├── products/       # Product display components
│   └── restaurants/    # Restaurant display components
├── store/              # Zustand state management
└── types/              # TypeScript type definitions
```

## Technologies Used

- **Next.js 14**: React framework with App Router
- **TypeScript**: Type-safe development
- **Tailwind CSS**: Utility-first CSS framework
- **Zustand**: Lightweight state management
- **Sharp**: Image optimization and processing
- **Server-Sent Events (SSE)**: Real-time streaming from backend
- **AWS S3**: Image upload and storage
- **PWA Ready**: Mobile-optimized responsive design

## Backend Integration

The frontend communicates with the FastAPI backend at `NEXT_PUBLIC_API_URL`:

**Primary Endpoint**: `POST /api/analyze-product-stream`
- Streams real-time analysis progress using Server-Sent Events
- Returns phase-by-phase updates during 8-phase pipeline
- Includes allergen detection results and alternative recommendations

**Image Upload Flow**:
1. User captures/uploads image
2. Frontend uploads to AWS S3
3. S3 URL sent to backend for analysis
4. Backend downloads from S3 and processes with AI
5. Results streamed back to frontend

## Features Roadmap

- [x] Real API integration with FastAPI backend
- [x] Product allergen detection with AI
- [x] Safe alternative recommendations
- [x] AWS S3 image storage
- [x] Real-time streaming analysis
- [ ] User authentication with NextAuth.js
- [ ] Database integration for user history
- [ ] Restaurant finder with location data
- [ ] Barcode scanning capability
- [ ] Social features (share safe products)
- [ ] Offline mode with cached products
- [ ] Push notifications for alerts

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a pull request

## License

This project is licensed under the MIT License.