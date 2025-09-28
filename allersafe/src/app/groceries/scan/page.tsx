'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { CameraCapture } from '@/components/scan/CameraCapture'

export default function GroceriesScanPage() {
  const router = useRouter()
  const [isProcessing, setIsProcessing] = useState(false)

  const handleImageCapture = async (imageData: string) => {
    setIsProcessing(true)

    setTimeout(() => {
      router.push(`/groceries/alternatives?product=${encodeURIComponent('sample-product')}`)
    }, 2000)
  }

  const handleCancel = () => {
    router.back()
  }

  return (
    <div className="fixed inset-0 bg-white">
      {isProcessing ? (
        <div className="flex items-center justify-center h-full">
          <div className="text-center">
            <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-green-500 mx-auto mb-4"></div>
            <p className="text-gray-800 text-lg">Analyzing product...</p>
            <p className="text-gray-500 text-sm mt-2">Checking ingredients and allergens</p>
          </div>
        </div>
      ) : (
        <CameraCapture
          onCapture={handleImageCapture}
          onCancel={handleCancel}
          mode="product"
        />
      )}
    </div>
  )
}