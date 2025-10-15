'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { CameraCapture } from '@/components/scan/CameraCapture'
import { getAllergyNames } from '@/lib/allergyProfile'
import { hasCompletedProfile } from '@/lib/profileChecker'

export default function GroceriesScanPage() {
  const router = useRouter()
  const [isProcessing, setIsProcessing] = useState(false)
  const [currentPhase, setCurrentPhase] = useState(0)
  const [phaseMessage, setPhaseMessage] = useState('Preparing analysis...')
  const [totalPhases, setTotalPhases] = useState(8)

  // Safety check: redirect to profile if not completed
  useEffect(() => {
    if (!hasCompletedProfile()) {
      router.replace('/profile')
    }
  }, [])

  const handleImageCapture = async (s3Url: string) => {
    setIsProcessing(true)
    setCurrentPhase(0)
    setPhaseMessage('Preparing analysis...')

    try {
      // Get allergy profile data as array
      const allergyProfile = getAllergyNames()

      // Console log the data for backend processing
      console.log('=== GROCERY SCAN DATA (SSE) ===')
      console.log({
        s3_image_url: s3Url,
        allergy_profile: allergyProfile
      })
      console.log('===============================')

      // Use SSE endpoint for real-time phase updates
      const response = await fetch('http://localhost:8000/api/analyze-product-stream', {
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
        throw new Error('Failed to start analysis')
      }

      // Read SSE stream
      const reader = response.body?.getReader()
      const decoder = new TextDecoder()

      let result: any = null
      let buffer = '' // Accumulate data across chunk boundaries

      if (reader) {
        while (true) {
          const { done, value } = await reader.read()

          if (done) break

          // Decode the chunk and add to buffer
          buffer += decoder.decode(value, { stream: true })

          // SSE format: "data: {json}\n\n" - messages end with double newline
          // Split on double newline to get complete messages
          const messages = buffer.split('\n\n')

          // Last element might be incomplete, keep it in buffer
          buffer = messages.pop() || ''

          // Process complete messages
          for (const message of messages) {
            const lines = message.split('\n')

            for (const line of lines) {
              if (line.startsWith('data: ')) {
                const jsonData = line.substring(6) // Remove "data: " prefix

                try {
                  const event = JSON.parse(jsonData)

                  if (event.type === 'phase') {
                    // Update phase progress
                    setCurrentPhase(event.phase)
                    setPhaseMessage(event.message)
                    setTotalPhases(event.total)
                    console.log(`Phase ${event.phase}/${event.total}: ${event.message}`)
                  } else if (event.type === 'result') {
                    // Store final result
                    result = event.data
                    console.log('=== ANALYSIS COMPLETE ===')
                    console.log(result)
                    console.log('========================')
                  } else if (event.type === 'error') {
                    throw new Error(event.message)
                  }
                } catch (parseError) {
                  console.error('Parse error:', parseError, 'for data:', jsonData)
                }
              }
            }
          }
        }

        // Process any remaining data in buffer
        if (buffer.trim()) {
          const lines = buffer.split('\n')
          for (const line of lines) {
            if (line.startsWith('data: ')) {
              const jsonData = line.substring(6)
              try {
                const event = JSON.parse(jsonData)
                if (event.type === 'result') {
                  result = event.data
                  console.log('=== ANALYSIS COMPLETE (from buffer) ===')
                  console.log(result)
                }
              } catch (parseError) {
                console.error('Final buffer parse error:', parseError)
              }
            }
          }
        }
      }

      if (!result) {
        throw new Error('No result received from analysis')
      }

      const detectResult = result.allergen_analysis
      const alternativesData = result.alternatives || []

      // Check if no product was detected
      const noProductDetected =
        detectResult.error === 'no_product_detected' ||
        detectResult.severity === 'NotDetected' ||
        (detectResult.warnings && (
          detectResult.warnings.toLowerCase().includes('does not contain any product') ||
          detectResult.warnings.toLowerCase().includes('no product packaging') ||
          detectResult.warnings.toLowerCase().includes('no allergen analysis can be performed')
        ))

      if (noProductDetected) {
        router.push('/groceries/not-detected')
        return
      }

      // Store alternatives and sources in sessionStorage (too large for URL params)
      sessionStorage.setItem('alternativesData', JSON.stringify(alternativesData))
      sessionStorage.setItem('allergenSources', JSON.stringify(detectResult.sources || []))

      // Navigate to alternatives page with detection results
      const params = new URLSearchParams({
        imageUrl: s3Url,
        severity: detectResult.severity || 'Safe',
        allergensDetected: JSON.stringify(detectResult.allergens_detected || []),
        warnings: detectResult.warnings || ''
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
        <div className="flex items-center justify-center h-full px-6">
          <div className="text-center max-w-md w-full">
            {/* Spinner */}
            <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-green-500 mx-auto mb-6"></div>

            {/* Phase Title */}
            <p className="text-gray-800 text-xl font-semibold mb-2">Analyzing Product</p>

            {/* Current Phase Message */}
            <p className="text-green-600 text-base font-medium mb-4">{phaseMessage}</p>

            {/* Progress Bar */}
            <div className="w-full bg-gray-200 rounded-full h-2.5 mb-2">
              <div
                className="bg-green-500 h-2.5 rounded-full transition-all duration-500 ease-out"
                style={{ width: `${(currentPhase / totalPhases) * 100}%` }}
              ></div>
            </div>

            {/* Phase Counter */}
            <p className="text-gray-500 text-sm">
              Phase {currentPhase} of {totalPhases}
            </p>

            {/* Phase Details (optional) */}
            <div className="mt-6 text-left">
              <p className="text-gray-600 text-xs mb-2">What we're doing:</p>
              <ul className="text-gray-500 text-xs space-y-1">
                <li className={currentPhase >= 1 ? 'text-green-600 font-medium' : ''}>
                  {currentPhase > 3 ? '✓' : currentPhase >= 1 ? '•' : '○'} Analyzing ingredients
                </li>
                <li className={currentPhase >= 4 ? 'text-green-600 font-medium' : ''}>
                  {currentPhase > 5 ? '✓' : currentPhase >= 4 ? '•' : '○'} Finding safe alternatives
                </li>
                <li className={currentPhase >= 6 ? 'text-green-600 font-medium' : ''}>
                  {currentPhase > 7 ? '✓' : currentPhase >= 6 ? '•' : '○'} Verifying safety
                </li>
                <li className={currentPhase >= 8 ? 'text-green-600 font-medium' : ''}>
                  {currentPhase >= 8 ? '✓' : '○'} Finalizing results
                </li>
              </ul>
            </div>
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