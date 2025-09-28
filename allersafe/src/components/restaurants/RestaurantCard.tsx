'use client'

interface RestaurantProps {
  restaurant: {
    id: string
    name: string
    cuisine: string
    distance: string
    rating: number
    priceLevel: string
    safetyFeatures: string[]
    address: string
    allergenInfo: string
  }
}

export function RestaurantCard({ restaurant }: RestaurantProps) {
  const renderStars = (rating: number) => {
    const stars = []
    const fullStars = Math.floor(rating)
    const hasHalfStar = rating % 1 >= 0.5

    for (let i = 0; i < fullStars; i++) {
      stars.push(
        <svg key={i} className="w-4 h-4 text-yellow-400 fill-current" viewBox="0 0 20 20">
          <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
        </svg>
      )
    }

    if (hasHalfStar) {
      stars.push(
        <svg key="half" className="w-4 h-4 text-yellow-400 fill-current" viewBox="0 0 20 20">
          <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
        </svg>
      )
    }

    return stars
  }

  return (
    <div className="bg-white rounded-lg shadow-sm overflow-hidden">
      <div className="p-4">
        <div className="flex justify-between items-start mb-2">
          <div>
            <h3 className="font-semibold text-gray-900 text-lg">{restaurant.name}</h3>
            <p className="text-sm text-gray-600">{restaurant.cuisine} • {restaurant.priceLevel}</p>
          </div>
          <div className="text-right">
            <p className="text-sm font-medium text-emerald-700">{restaurant.distance}</p>
            <div className="flex items-center mt-1">
              {renderStars(restaurant.rating)}
              <span className="text-xs text-gray-600 ml-1">{restaurant.rating}</span>
            </div>
          </div>
        </div>

        <div className="flex flex-wrap gap-1 mb-3">
          {restaurant.safetyFeatures.map((feature) => (
            <span
              key={feature}
              className="px-2 py-1 bg-emerald-50 text-emerald-700 rounded text-xs"
            >
              {feature}
            </span>
          ))}
        </div>

        <div className="bg-blue-50 border border-blue-200 rounded p-2 mb-3">
          <p className="text-xs text-blue-800">
            <span className="font-medium">Allergen Info:</span> {restaurant.allergenInfo}
          </p>
        </div>

        <div className="flex items-center justify-between text-sm">
          <p className="text-gray-600 flex items-center">
            <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
            {restaurant.address}
          </p>
        </div>

        <div className="flex gap-2 mt-3">
          <button className="flex-1 bg-gradient-to-br from-emerald-700 to-emerald-900 text-white py-2 px-4 rounded text-sm hover:from-emerald-800 hover:to-emerald-950 transition-all">
            Directions
          </button>
          <button className="flex-1 border border-emerald-700 text-emerald-700 py-2 px-4 rounded text-sm hover:bg-emerald-50 transition-colors">
            View Menu
          </button>
        </div>
      </div>
    </div>
  )
}