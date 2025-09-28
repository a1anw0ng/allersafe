'use client'

import { useState, useEffect } from 'react'
import { usePathname } from 'next/navigation'
import Link from 'next/link'

export function TopTabs() {
  const pathname = usePathname()
  const [activeTab, setActiveTab] = useState<'groceries' | 'restaurants'>('groceries')

  useEffect(() => {
    const savedTab = localStorage.getItem('activeTab') as 'groceries' | 'restaurants' | null
    if (savedTab) {
      setActiveTab(savedTab)
    }
  }, [])

  return (
    <div className="bg-white border-b border-gray-200 sticky top-0 z-40 safe-area-inset-top">
      <div className="flex">
        <button
          className={`flex-1 py-5 px-4 text-center font-semibold text-lg transition-colors ${
            activeTab === 'groceries'
              ? 'text-green-600 border-b-3 border-green-500 bg-green-50'
              : 'text-gray-600 hover:text-gray-800 hover:bg-gray-50'
          }`}
          onClick={() => {
            setActiveTab('groceries')
            localStorage.setItem('activeTab', 'groceries')
            window.dispatchEvent(new Event('storage'))
          }}
        >
          <div className="flex items-center justify-center gap-2">
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" />
            </svg>
            <span>Groceries</span>
          </div>
        </button>

        <button
          className={`flex-1 py-5 px-4 text-center font-semibold text-lg transition-colors ${
            activeTab === 'restaurants'
              ? 'text-emerald-800 border-b-3 border-emerald-700 bg-emerald-900/10'
              : 'text-gray-600 hover:text-gray-800 hover:bg-gray-50'
          }`}
          onClick={() => {
            setActiveTab('restaurants')
            localStorage.setItem('activeTab', 'restaurants')
            window.dispatchEvent(new Event('storage'))
          }}
        >
          <div className="flex items-center justify-center gap-2">
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
            </svg>
            <span>Restaurants</span>
          </div>
        </button>
      </div>
    </div>
  )
}