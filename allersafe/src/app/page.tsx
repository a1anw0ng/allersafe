'use client'

import { useRouter } from 'next/navigation'
import { FloatingFoodIcons } from '@/components/ui/FloatingFoodIcons'
import { ProfilePromptModal } from '@/components/ui/ProfilePromptModal'
import { hasCompletedProfile } from '@/lib/profileChecker'
import { useState, useEffect } from 'react'

export default function Home() {
  const router = useRouter()
  const [activeMode, setActiveMode] = useState<'groceries' | 'restaurants'>('groceries')
  const [showProfileModal, setShowProfileModal] = useState(false)

  useEffect(() => {
    const savedTab = localStorage.getItem('activeTab') as 'groceries' | 'restaurants' | null
    if (savedTab) {
      setActiveMode(savedTab)
    }

    const handleStorageChange = () => {
      const savedTab = localStorage.getItem('activeTab') as 'groceries' | 'restaurants' | null
      if (savedTab) {
        setActiveMode(savedTab)
      }
    }

    window.addEventListener('storage', handleStorageChange)
    return () => window.removeEventListener('storage', handleStorageChange)
  }, [])

  const handleTabChange = (mode: 'groceries' | 'restaurants') => {
    setActiveMode(mode)
    localStorage.setItem('activeTab', mode)
    window.dispatchEvent(new Event('storage'))
  }

  const handleScan = () => {
    // Check if user has completed their profile
    if (!hasCompletedProfile()) {
      setShowProfileModal(true)
      return
    }

    const currentTab = localStorage.getItem('activeTab') || 'groceries'
    if (currentTab === 'groceries') {
      router.push('/groceries/scan')
    } else {
      router.push('/restaurants/scan')
    }
  }

  return (
    <div className="flex flex-col h-screen overflow-hidden">
      {/* Integrated Tab Buttons */}
      <div className="bg-white border-b border-gray-200 sticky top-0 z-40 safe-area-inset-top">
        <div className="flex">
          <button
            className={`flex-1 py-5 px-4 text-center font-semibold text-lg transition-colors ${
              activeMode === 'groceries'
                ? 'text-green-600 border-b-3 border-green-500 bg-green-50'
                : 'text-gray-600 hover:text-gray-800 hover:bg-gray-50'
            }`}
            onClick={() => handleTabChange('groceries')}
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
              activeMode === 'restaurants'
                ? 'text-emerald-800 border-b-3 border-emerald-700 bg-emerald-900/10'
                : 'text-gray-600 hover:text-gray-800 hover:bg-gray-50'
            }`}
            onClick={() => handleTabChange('restaurants')}
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

      <FloatingFoodIcons />
      <ProfilePromptModal isOpen={showProfileModal} onClose={() => setShowProfileModal(false)} />
      <div className="flex-1 flex flex-col items-center justify-center px-4 relative z-10 pb-20">
        <div className="text-center mb-8">
          <h1 className="text-5xl font-bold text-gray-900 mb-3">AllerSafe</h1>
          <p className="text-gray-600 text-sm tracking-wide">Find safe food alternatives instantly</p>
        </div>

        <button
          onClick={handleScan}
          className={`${
            activeMode === 'groceries'
              ? 'bg-gradient-to-br from-green-400 to-green-600'
              : 'bg-gradient-to-br from-emerald-700 to-emerald-900'
          } text-white px-12 py-8 rounded-2xl shadow-lg transform transition-all hover:scale-105 active:scale-95 flex flex-col items-center gap-3`}
        >
          <svg
            className="w-16 h-16"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z"
            />
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M15 13a3 3 0 11-6 0 3 3 0 016 0z"
            />
          </svg>
          <span className="text-xl font-semibold">
            {activeMode === 'groceries' ? 'Groceries' : 'Restaurants'}
          </span>
        </button>

        <div className="mt-8 text-center max-w-sm">
          <p className="text-sm text-gray-500 mb-4">
            {activeMode === 'groceries'
              ? 'Take a photo of any grocery product to instantly find alternatives that match your dietary restrictions'
              : 'Take a photo of any meal to discover restaurants nearby that can accommodate your dietary restrictions'}
          </p>

          <div className="flex flex-wrap justify-center gap-2 mt-4">
            {activeMode === 'groceries' ? (
              <>
                <span className="px-3 py-1 bg-primary-100 text-primary-700 rounded-full text-xs">
                  Safe Alternatives
                </span>
                <span className="px-3 py-1 bg-primary-100 text-primary-700 rounded-full text-xs">
                  Shop Links
                </span>
                <span className="px-3 py-1 bg-primary-100 text-primary-700 rounded-full text-xs">
                  Price Compare
                </span>
              </>
            ) : (
              <>
                <span className="px-3 py-1 bg-primary-100 text-primary-700 rounded-full text-xs">
                  Nearby Options
                </span>
                <span className="px-3 py-1 bg-primary-100 text-primary-700 rounded-full text-xs">
                  Safety Verified
                </span>
                <span className="px-3 py-1 bg-primary-100 text-primary-700 rounded-full text-xs">
                  Reviews & Ratings
                </span>
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}