'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { CameraCapture } from '@/components/scan/CameraCapture'
import { getAllergyNames } from '@/lib/allergyProfile'

export default function GroceriesScanPage() {
  const router = useRouter()
  const [isProcessing, setIsProcessing] = useState(false)

  const handleImageCapture = async (s3Url: string) => {
    setIsProcessing(true)

    try {
      // Get allergy profile data as array
      const allergyProfile = getAllergyNames()

      // Console log the data for backend processing
      console.log('=== GROCERY SCAN DATA ===')
      console.log({
        s3_image_url: s3Url,
        allergy_profile: allergyProfile
      })
      console.log('========================')

      // Call backend API to detect allergens
      const response = await fetch('http://localhost:8000/api/detect-allergens', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          s3_image_url: s3Url,
          allergens: allergyProfile
        })
      })

      if (!response.ok) {
        throw new Error('Failed to analyze product')
      }

      const result = await response.json()
      console.log('=== BACKEND RESPONSE ===')
      console.log(result)
      console.log('========================')

      // Navigate to alternatives page with results
      const params = new URLSearchParams({
        imageUrl: s3Url,
        severity: result.severity || 'Safe',
        allergensDetected: JSON.stringify(result.allergens_detected || []),
        warnings: result.warnings || ''
      })

      router.push(`/groceries/alternatives?${params.toString()}`)
    } catch (error) {
      console.error('Error analyzing product:', error)
      // Navigate to alternatives page with error state
      router.push(`/groceries/alternatives?error=true`)
    }
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