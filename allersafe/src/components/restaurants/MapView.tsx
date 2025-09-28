'use client'

interface Restaurant {
  id: string
  name: string
  cuisine: string
  distance: string
  rating: number
  coordinates: { lat: number; lng: number }
  safetyFeatures: string[]
}

interface MapViewProps {
  restaurants: Restaurant[]
}

export function MapView({ restaurants }: MapViewProps) {
  return (
    <div className="relative h-[calc(100vh-120px)]">
      <div className="absolute inset-0 bg-gray-200">
        <div className="w-full h-full flex items-center justify-center">
          <div className="text-center">
            <svg className="w-16 h-16 text-gray-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7" />
            </svg>
            <p className="text-gray-600 mb-2">Interactive Map View</p>
            <p className="text-sm text-gray-500">Google Maps integration would go here</p>
          </div>
        </div>
      </div>

      <div className="absolute bottom-0 left-0 right-0 bg-white shadow-lg rounded-t-2xl p-4 max-h-[40%] overflow-y-auto">
        <div className="flex items-center justify-between mb-3">
          <h3 className="font-semibold text-gray-900">
            {restaurants.length} Restaurants Found
          </h3>
          <button className="text-primary-600 text-sm">Filter</button>
        </div>

        <div className="space-y-3">
          {restaurants.map((restaurant) => (
            <div
              key={restaurant.id}
              className="flex items-center justify-between py-2 border-b border-gray-100 last:border-0"
            >
              <div className="flex-1">
                <div className="flex items-center gap-2">
                  <div className="w-8 h-8 bg-primary-600 text-white rounded-full flex items-center justify-center text-xs font-medium">
                    {restaurant.name.charAt(0)}
                  </div>
                  <div>
                    <p className="font-medium text-gray-900 text-sm">{restaurant.name}</p>
                    <p className="text-xs text-gray-600">
                      {restaurant.cuisine} • {restaurant.distance} • ★ {restaurant.rating}
                    </p>
                  </div>
                </div>
              </div>
              <button className="text-primary-600 p-2">
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                </svg>
              </button>
            </div>
          ))}
        </div>
      </div>

      {restaurants.map((restaurant, index) => (
        <div
          key={restaurant.id}
          className="absolute"
          style={{
            top: `${20 + (index * 10)}%`,
            left: `${30 + (index * 15)}%`,
          }}
        >
          <div className="relative">
            <div className="bg-primary-600 text-white px-2 py-1 rounded-lg shadow-lg">
              <p className="text-xs font-medium">{restaurant.name}</p>
            </div>
            <div className="absolute bottom-0 left-1/2 transform -translate-x-1/2 translate-y-full">
              <div className="w-0 h-0 border-l-4 border-r-4 border-t-4 border-transparent border-t-primary-600"></div>
            </div>
          </div>
        </div>
      ))}
    </div>
  )
}