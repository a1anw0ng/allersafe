# AllerSafe - Food Allergy Safety App

AllerSafe helps people with dietary restrictions and allergies find safe food alternatives by scanning products and meals.

## Features

- **Product Scanner**: Scan grocery items to find safe alternatives
- **Restaurant Finder**: Scan meals to discover safe dining options
- **Personalized Profiles**: Save your dietary restrictions and allergies
- **Shopping Links**: Direct links to purchase alternatives online
- **Map Integration**: Find nearby restaurants that accommodate your needs
- **Safety Ratings**: Clear indicators for safe, caution, and unsafe options

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

3. Set up environment variables:
```bash
cp .env.example .env.local
```

4. Fill in your API keys in `.env.local`:
   - OpenAI API Key (for image recognition)
   - Google Maps API Key (for restaurant locations)
   - Google Places API Key (for restaurant data)

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

## Security Notice

⚠️ **IMPORTANT**: The OpenAI API key in the parent directory's `.env` file is exposed and should be regenerated immediately. Never commit API keys to version control.

## Technologies Used

- **Next.js 14**: React framework with App Router
- **TypeScript**: Type-safe development
- **Tailwind CSS**: Utility-first CSS framework
- **Zustand**: Lightweight state management
- **PWA Ready**: Mobile-optimized responsive design

## Features Roadmap

- [ ] Real API integration for product identification
- [ ] User authentication with NextAuth.js
- [ ] Database integration for user data
- [ ] Real-time restaurant data from Google Places
- [ ] Barcode scanning capability
- [ ] Social features (share safe products/restaurants)
- [ ] Offline mode with cached data
- [ ] Push notifications for nearby safe options

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a pull request

## License

This project is licensed under the MIT License.