'use client'

import { useRouter } from 'next/navigation'
import { useState, useEffect } from 'react'
import { RestaurantCard } from '@/components/restaurants/RestaurantCard'
import { MapView } from '@/components/restaurants/MapView'

interface Restaurant {
  id: string
  name: string
  cuisine: string
  distance: string
  rating: number
  priceLevel: string
  safetyFeatures: string[]
  address: string
  coordinates: { lat: number; lng: number }
  allergenInfo: string
}

const mockRestaurants: Restaurant[] = [
  {
    id: '1',
    name: 'Green Garden Bistro',
    cuisine: 'Italian',
    distance: '0.5 mi',
    rating: 4.8,
    priceLevel: '$$',
    safetyFeatures: ['Allergen Menu', 'Gluten-Free Options', 'Vegan Friendly'],
    address: '123 Main St, City, State',
    coordinates: { lat: 40.7128, lng: -74.0060 },
    allergenInfo: 'Dedicated gluten-free kitchen area',
  },
  {
    id: '2',
    name: 'Safe Eats Kitchen',
    cuisine: 'American',
    distance: '0.8 mi',
    rating: 4.6,
    priceLevel: '$',
    safetyFeatures: ['Certified Allergy-Friendly', 'Custom Orders'],
    address: '456 Oak Ave, City, State',
    coordinates: { lat: 40.7260, lng: -74.0110 },
    allergenInfo: 'All allergens clearly marked on menu',
  },
  {
    id: '3',
    name: 'Pure Food Co.',
    cuisine: 'Mediterranean',
    distance: '1.2 mi',
    rating: 4.9,
    priceLevel: '$$$',
    safetyFeatures: ['100% Nut-Free', 'Dairy Alternatives', 'Organic'],
    address: '789 Elm St, City, State',
    coordinates: { lat: 40.7350, lng: -74.0020 },
    allergenInfo: 'Completely nut-free facility',
  },
]

export default function RestaurantsMapPage() {
  const router = useRouter()
  const [viewMode, setViewMode] = useState<'list' | 'map'>('list')
  const [filteredRestaurants, setFilteredRestaurants] = useState<Restaurant[]>(mockRestaurants)

  useEffect(() => {
    const saved = localStorage.getItem('dietaryRestrictions')
    if (saved) {
      const restrictions = JSON.parse(saved)

      const filtered = mockRestaurants.filter(restaurant => {
        if (restrictions.includes('peanut') || restrictions.includes('tree-nuts')) {
          return restaurant.safetyFeatures.some(feature =>
            feature.includes('Nut-Free') || feature.includes('Allergen')
          )
        }
        return true
      })
      setFilteredRestaurants(filtered)
    }
  }, [])

  return (
    <div className="min-h-screen bg-gray-50 pb-20">
      <div className="bg-white shadow-sm sticky top-0 z-10">
        <div className="px-4 py-4 flex items-center justify-between">
          <div className="flex items-center">
            <button
              onClick={() => router.back()}
              className="mr-4"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
              </svg>
            </button>
            <h1 className="text-xl font-bold">Safe Restaurants</h1>
          </div>

          <div className="flex bg-gray-100 rounded-lg p-1">
            <button
              onClick={() => setViewMode('list')}
              className={`px-3 py-1 rounded ${
                viewMode === 'list' ? 'bg-white shadow-sm' : ''
              }`}
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 10h16M4 14h16M4 18h16" />
              </svg>
            </button>
            <button
              onClick={() => setViewMode('map')}
              className={`px-3 py-1 rounded ${
                viewMode === 'map' ? 'bg-white shadow-sm' : ''
              }`}
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
            </button>
          </div>
        </div>
      </div>

      {viewMode === 'list' ? (
        <div className="px-4 py-6">
          <div className="mb-4">
            <h2 className="text-lg font-semibold text-gray-900 mb-1">
              {filteredRestaurants.length} Safe Options Found
            </h2>
            <p className="text-sm text-gray-600">
              Restaurants that accommodate your dietary restrictions
            </p>
          </div>

          <div className="space-y-4">
            {filteredRestaurants.map((restaurant) => (
              <RestaurantCard key={restaurant.id} restaurant={restaurant} />
            ))}
          </div>

          {filteredRestaurants.length === 0 && (
            <div className="text-center py-12">
              <svg className="w-16 h-16 text-gray-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <p className="text-gray-500">No restaurants found matching your restrictions</p>
            </div>
          )}
        </div>
      ) : (
        <MapView restaurants={filteredRestaurants} />
      )}
    </div>
  )
}