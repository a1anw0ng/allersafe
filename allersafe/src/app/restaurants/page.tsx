'use client'

import { useRouter } from 'next/navigation'
import { ScanButton } from '@/components/scan/ScanButton'

export default function RestaurantsPage() {
  const router = useRouter()

  const handleScan = () => {
    router.push('/restaurants/scan')
  }

  return (
    <div className="min-h-screen bg-gray-50 pb-20">
      <div className="flex flex-col items-center justify-center min-h-[calc(100vh-200px)] px-4">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-3">Restaurant Finder</h1>
          <p className="text-gray-600 text-sm tracking-wide">Scan meals to find safe dining options</p>
        </div>

        <ScanButton onClick={handleScan} />

        <div className="mt-8 text-center max-w-sm">
          <p className="text-sm text-gray-500 mb-4">
            Take a photo of any meal to discover restaurants nearby that can accommodate your dietary restrictions
          </p>

          <div className="flex flex-wrap justify-center gap-2 mt-4">
            <span className="px-3 py-1 bg-primary-100 text-primary-700 rounded-full text-xs">
              Nearby Options
            </span>
            <span className="px-3 py-1 bg-primary-100 text-primary-700 rounded-full text-xs">
              Safety Verified
            </span>
            <span className="px-3 py-1 bg-primary-100 text-primary-700 rounded-full text-xs">
              Reviews & Ratings
            </span>
          </div>
        </div>
      </div>
    </div>
  )
}