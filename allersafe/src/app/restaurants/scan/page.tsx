'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { CameraCapture } from '@/components/scan/CameraCapture'
import { getAllergyNames } from '@/lib/allergyProfile'

export default function RestaurantsScanPage() {
  const router = useRouter()
  const [isProcessing, setIsProcessing] = useState(false)

  const handleImageCapture = async (s3Url: string) => {
    setIsProcessing(true)

    // Get allergy profile data as array
    const allergyProfile = getAllergyNames()

    // Console log the data for backend processing
    console.log('=== RESTAURANT SCAN DATA ===')
    console.log({
      s3_image_url: s3Url,
      allergy_profile: allergyProfile
    })
    console.log('============================')

    // TODO: Send S3 URL and allergy profile to backend API for processing

    // Simulate processing time
    setTimeout(() => {
      router.push(`/restaurants/map?imageUrl=${encodeURIComponent(s3Url)}`)
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
            <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-emerald-700 mx-auto mb-4"></div>
            <p className="text-gray-800 text-lg">Identifying cuisine...</p>
            <p className="text-gray-500 text-sm mt-2">Finding safe restaurant alternatives</p>
          </div>
        </div>
      ) : (
        <CameraCapture
          onCapture={handleImageCapture}
          onCancel={handleCancel}
          mode="meal"
        />
      )}
    </div>
  )
}