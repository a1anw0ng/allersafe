'use client'

import { usePathname } from 'next/navigation'
import Link from 'next/link'
import { useState, useEffect } from 'react'

export function BottomNav() {
  const pathname = usePathname()
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

  const isActive = (path: string) => {
    if (path === '/') {
      return pathname === '/' || pathname === '/groceries' || pathname === '/restaurants'
    }
    return pathname?.startsWith(path)
  }

  const getHomeColor = () => {
    if (!isActive('/')) return 'text-gray-500'
    return activeMode === 'groceries' ? 'text-green-500' : 'text-emerald-800'
  }

  const getHomeBg = () => {
    if (!isActive('/')) return ''
    return activeMode === 'groceries' ? 'bg-green-50' : 'bg-emerald-900/10'
  }

  return (
    <div className="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 safe-area-inset-bottom z-50">
      <div className="flex">
        <Link
          href="/"
          className={`flex-1 flex flex-col items-center py-5 px-3 transition-colors ${getHomeColor()} ${getHomeBg()}`}
        >
          <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
          </svg>
          <span className="text-xs mt-1 font-medium">Home</span>
        </Link>

        <Link
          href="/profile"
          className={`flex-1 flex flex-col items-center py-5 px-3 transition-colors ${
            isActive('/profile') ? 'text-teal-600 bg-teal-50' : 'text-gray-500'
          }`}
        >
          <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
          </svg>
          <span className="text-xs mt-1 font-medium">Profile</span>
        </Link>
      </div>
    </div>
  )
}