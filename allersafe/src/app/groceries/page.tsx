'use client'

import { useRouter } from 'next/navigation'
import { ScanButton } from '@/components/scan/ScanButton'

export default function GroceriesPage() {
  const router = useRouter()

  const handleScan = () => {
    router.push('/groceries/scan')
  }

  return (
    <div className="min-h-screen bg-gray-50 pb-20">
      <div className="flex flex-col items-center justify-center min-h-[calc(100vh-200px)] px-4">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-3">Grocery Scanner</h1>
          <p className="text-gray-600 text-sm tracking-wide">Scan products to find safe alternatives</p>
        </div>

        <ScanButton onClick={handleScan} />

        <div className="mt-8 text-center max-w-sm">
          <p className="text-sm text-gray-500 mb-4">
            Take a photo of any grocery product to instantly find alternatives that match your dietary restrictions
          </p>

          <div className="flex flex-wrap justify-center gap-2 mt-4">
            <span className="px-3 py-1 bg-primary-100 text-primary-700 rounded-full text-xs">
              Instant Results
            </span>
            <span className="px-3 py-1 bg-primary-100 text-primary-700 rounded-full text-xs">
              Shop Links
            </span>
            <span className="px-3 py-1 bg-primary-100 text-primary-700 rounded-full text-xs">
              Price Compare
            </span>
          </div>
        </div>
      </div>
    </div>
  )
}