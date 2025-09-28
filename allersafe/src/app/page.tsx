'use client'

import { useRouter } from 'next/navigation'
import { TopTabs } from '@/components/navigation/TopTabs'
import { FloatingFoodIcons } from '@/components/ui/FloatingFoodIcons'
import { useState, useEffect } from 'react'

export default function Home() {
  const router = useRouter()
  const [activeMode, setActiveMode] = useState<'groceries' | 'restaurants'>('groceries')

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

  const handleScan = () => {
    const currentTab = localStorage.getItem('activeTab') || 'groceries'
    if (currentTab === 'groceries') {
      router.push('/groceries/scan')
    } else {
      router.push('/restaurants/scan')
    }
  }

  return (
    <div className="flex flex-col h-screen overflow-hidden">
      <TopTabs />
      <FloatingFoodIcons />
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

      <div className="mt-8 text-center">
        <p className="text-sm text-gray-500">
          {activeMode === 'groceries'
            ? 'Scan grocery items to find safe alternatives'
            : 'Scan meals to find safe restaurant options'}
        </p>
      </div>
    </div>
    </div>
  )
}