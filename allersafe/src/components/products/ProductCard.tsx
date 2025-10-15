'use client'

import { useState } from 'react'

interface ProductProps {
  product: {
    id: string
    name: string
    brand: string
    image: string
    price: string
    safetyRating: 'safe' | 'caution' | 'unsafe'
    allergenFree: string[]
    storeLinks: { store: string; url: string; price: string }[]
    reasoning?: string
  }
}

export function ProductCard({ product }: ProductProps) {
  const [showReasoning, setShowReasoning] = useState(false)
  const getSafetyColor = () => {
    switch (product.safetyRating) {
      case 'safe':
        return 'bg-green-50 text-green-600 border-green-200'
      case 'caution':
        return 'bg-yellow-100 text-yellow-800 border-yellow-200'
      case 'unsafe':
        return 'bg-red-100 text-red-800 border-red-200'
    }
  }

  const getSafetyIcon = () => {
    switch (product.safetyRating) {
      case 'safe':
        return (
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        )
      case 'caution':
        return (
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
          </svg>
        )
      case 'unsafe':
        return (
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        )
    }
  }

  return (
    <div className="bg-white rounded-lg shadow-sm overflow-hidden">
      <div className="p-4">
          <div className="flex items-start justify-between mb-2">
            <div>
              <h3 className="font-semibold text-gray-900">{product.name}</h3>
              <p className="text-sm text-gray-600">{product.brand}</p>
            </div>
            <div className={`px-2 py-1 rounded-full flex items-center gap-1 text-xs ${getSafetyColor()}`}>
              {getSafetyIcon()}
              <span className="capitalize">{product.safetyRating}</span>
            </div>
          </div>

          <div className="flex flex-wrap gap-1 mb-3">
            {product.allergenFree.map((allergen) => (
              <span
                key={allergen}
                className="px-2 py-1 bg-green-50 text-green-600 rounded text-xs capitalize"
              >
                {allergen.replace(/-/g, ' ')}
              </span>
            ))}
          </div>

          {/* Why This Alternative - Expandable Section */}
          {product.reasoning && (
            <div className="mb-3">
              <button
                onClick={() => setShowReasoning(!showReasoning)}
                className="text-gray-700 text-xs font-medium hover:text-gray-900 flex items-center gap-1"
              >
                Why this alternative?
                <svg className={`w-3 h-3 transition-transform ${showReasoning ? 'rotate-180' : ''}`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                </svg>
              </button>
              {showReasoning && (
                <div className="mt-2 text-xs text-gray-600 bg-gray-50 p-2 rounded">
                  {product.reasoning}
                </div>
              )}
            </div>
          )}

          <div className="flex items-center justify-between">
            <span className="text-lg font-semibold text-green-600">{product.price}</span>
            <div className="flex gap-2">
              {product.storeLinks.map((link) => (
                <a
                  key={link.store}
                  href={link.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="px-3 py-1 bg-gradient-to-br from-green-400 to-green-600 text-white rounded text-sm hover:from-green-500 hover:to-green-700 transition-all"
                >
                  {link.store}
                </a>
              ))}
            </div>
        </div>
      </div>
    </div>
  )
}