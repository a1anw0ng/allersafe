'use client'

import { useRouter } from 'next/navigation'
import { ProductCard } from '@/components/products/ProductCard'
import { useState, useEffect } from 'react'

interface Alternative {
  id: string
  name: string
  brand: string
  image: string
  price: string
  safetyRating: 'safe' | 'caution' | 'unsafe'
  allergenFree: string[]
  storeLinks: { store: string; url: string; price: string }[]
}

const mockAlternatives: Alternative[] = [
  {
    id: '1',
    name: 'Sunflower Seed Butter',
    brand: 'SunButter',
    image: '/api/placeholder/200/200',
    price: '$5.99',
    safetyRating: 'safe',
    allergenFree: ['Peanut-Free', 'Tree Nut-Free', 'Gluten-Free'],
    storeLinks: [
      { store: 'Amazon', url: '#', price: '$5.99' },
      { store: 'Walmart', url: '#', price: '$5.49' },
    ],
  },
  {
    id: '2',
    name: 'Almond Butter',
    brand: 'Justin\'s',
    image: '/api/placeholder/200/200',
    price: '$8.99',
    safetyRating: 'caution',
    allergenFree: ['Peanut-Free', 'Gluten-Free'],
    storeLinks: [
      { store: 'Amazon', url: '#', price: '$8.99' },
      { store: 'Target', url: '#', price: '$9.49' },
    ],
  },
  {
    id: '3',
    name: 'Soy Butter',
    brand: 'WowButter',
    image: '/api/placeholder/200/200',
    price: '$4.99',
    safetyRating: 'safe',
    allergenFree: ['Peanut-Free', 'Tree Nut-Free', 'Dairy-Free'],
    storeLinks: [
      { store: 'Amazon', url: '#', price: '$4.99' },
      { store: 'Whole Foods', url: '#', price: '$5.49' },
    ],
  },
]

export default function AlternativesPage() {
  const router = useRouter()
  const [restrictions, setRestrictions] = useState<string[]>([])
  const [filteredAlternatives, setFilteredAlternatives] = useState<Alternative[]>(
    mockAlternatives.filter(alt => alt.safetyRating === 'safe')
  )

  useEffect(() => {
    const saved = localStorage.getItem('dietaryRestrictions')
    if (saved) {
      const restrictions = JSON.parse(saved)
      setRestrictions(restrictions)
    }

    const filtered = mockAlternatives.filter(alt => {
      return alt.safetyRating === 'safe'
    })
    setFilteredAlternatives(filtered)
  }, [])

  return (
    <div className="min-h-screen bg-gray-50 pb-20">
      <div className="bg-white shadow-sm sticky top-0 z-10">
        <div className="px-4 py-4 flex items-center">
          <button
            onClick={() => router.back()}
            className="mr-4"
          >
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
            </svg>
          </button>
          <h1 className="text-xl font-bold">Safe Alternatives</h1>
        </div>
      </div>

      <div className="px-4 py-6">
        <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
          <div className="flex items-start">
            <svg className="w-5 h-5 text-red-600 mt-0.5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
            <div>
              <p className="text-red-800 font-medium">Contains: Peanuts</p>
              <p className="text-red-700 text-sm mt-1">This product contains allergens from your profile</p>
            </div>
          </div>
        </div>

        <div className="mb-4">
          <h2 className="text-lg font-semibold text-gray-900 mb-2">
            {filteredAlternatives.length} Safe Alternative{filteredAlternatives.length !== 1 ? 's' : ''} Found
          </h2>
          <p className="text-sm text-gray-600">
            100% safe based on your dietary restrictions
          </p>
        </div>

        <div className="space-y-4">
          {filteredAlternatives.map((alternative) => (
            <ProductCard key={alternative.id} product={alternative} />
          ))}
        </div>

        {filteredAlternatives.length === 0 && (
          <div className="text-center py-12">
            <svg className="w-16 h-16 text-gray-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <p className="text-gray-500">No alternatives found matching your restrictions</p>
          </div>
        )}
      </div>
    </div>
  )
}