'use client'

import { useState, useRef, useEffect } from 'react'

interface CameraCaptureProps {
  onCapture: (imageData: string) => void
  onCancel: () => void
  mode: 'product' | 'meal'
}

export function CameraCapture({ onCapture, onCancel, mode }: CameraCaptureProps) {
  const [imageUrl, setImageUrl] = useState<string | null>(null)
  const fileInputRef = useRef<HTMLInputElement>(null)
  const videoRef = useRef<HTMLVideoElement>(null)
  const [hasCamera, setHasCamera] = useState(false)
  const [stream, setStream] = useState<MediaStream | null>(null)

  useEffect(() => {
    if (typeof navigator !== 'undefined' && navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
      navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' } })
        .then((mediaStream) => {
          setHasCamera(true)
          setStream(mediaStream)
          if (videoRef.current) {
            videoRef.current.srcObject = mediaStream
          }
        })
        .catch((err) => {
          console.log('Camera not available:', err)
          setHasCamera(false)
        })
    }

    return () => {
      if (stream) {
        stream.getTracks().forEach(track => track.stop())
      }
    }
  }, [])

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (file) {
      const reader = new FileReader()
      reader.onload = (event) => {
        const imageData = event.target?.result as string
        setImageUrl(imageData)
      }
      reader.readAsDataURL(file)
    }
  }

  const captureImage = () => {
    if (videoRef.current) {
      const canvas = document.createElement('canvas')
      canvas.width = videoRef.current.videoWidth
      canvas.height = videoRef.current.videoHeight
      const ctx = canvas.getContext('2d')
      if (ctx) {
        ctx.drawImage(videoRef.current, 0, 0)
        const imageData = canvas.toDataURL('image/jpeg')
        setImageUrl(imageData)
      }
    }
  }

  const handleConfirm = () => {
    if (imageUrl) {
      if (stream) {
        stream.getTracks().forEach(track => track.stop())
      }
      onCapture(imageUrl)
    }
  }

  const handleRetake = () => {
    setImageUrl(null)
  }

  return (
    <div className={`fixed inset-0 flex flex-col h-screen max-h-screen ${
      imageUrl ? 'bg-gray-50' : ''
    }`}>
      <div className={`absolute top-0 left-0 right-0 z-20 p-4 ${
        imageUrl ? 'bg-gray-50' : ''
      }`}>
        <button
          onClick={onCancel}
          className={`p-2 rounded-full ${
            imageUrl ? 'text-gray-700 bg-gray-100' : 'text-white bg-black/20 backdrop-blur-sm'
          }`}
        >
          <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
        <div className="text-center mt-2">
          <h2 className={`text-2xl font-bold mb-1 ${
            imageUrl ? 'text-gray-800' : 'text-white drop-shadow-lg'
          }`}>
            {mode === 'product' ? 'Groceries' : 'Restaurants'}
          </h2>
          <p className={`text-sm ${
            imageUrl ? 'text-gray-600' : 'text-white drop-shadow-lg'
          }`}>
            {imageUrl
              ? 'Review your photo'
              : mode === 'product' ? 'Scan Product Barcode or Label' : 'Capture Your Meal'
            }
          </p>
        </div>
      </div>

      <div className="absolute inset-0">
        {imageUrl ? (
          <div className="absolute top-24 bottom-32 left-4 right-4 flex items-center justify-center">
            <div className="relative w-full h-full overflow-hidden flex items-center justify-center">
              <img
                src={imageUrl}
                alt="Captured"
                className="max-w-full max-h-full object-contain"
              />
            </div>
          </div>
        ) : hasCamera ? (
          <video
            ref={videoRef}
            autoPlay
            playsInline
            className="absolute inset-0 w-full h-full object-cover"
          />
        ) : (
          <div className="flex flex-col items-center justify-center text-white p-4 h-full">
            <svg className="w-16 h-16 mb-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" />
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 13a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
            <p className="text-gray-400 mb-4">Camera not available</p>
            <button
              onClick={() => fileInputRef.current?.click()}
              className="bg-primary-600 text-white px-6 py-3 rounded-full"
            >
              Choose Photo
            </button>
          </div>
        )}
      </div>

      {!imageUrl && hasCamera && (
        <div className="absolute top-24 bottom-56 left-0 right-0 flex items-center justify-center pointer-events-none z-10">
          <div className="w-64 h-64 border-2 border-white opacity-70 rounded-lg relative">
            <div className="absolute top-0 left-0 w-8 h-8 border-t-4 border-l-4 border-white"></div>
            <div className="absolute top-0 right-0 w-8 h-8 border-t-4 border-r-4 border-white"></div>
            <div className="absolute bottom-0 left-0 w-8 h-8 border-b-4 border-l-4 border-white"></div>
            <div className="absolute bottom-0 right-0 w-8 h-8 border-b-4 border-r-4 border-white"></div>
          </div>
        </div>
      )}

      <div className={`absolute bottom-0 left-0 right-0 z-20 p-6 pb-24 flex justify-center gap-4 ${
        imageUrl ? 'bg-gray-50' : ''
      }`}>
        {imageUrl ? (
          <>
            <button
              onClick={handleRetake}
              className="bg-gray-600 text-white px-6 py-3 rounded-full flex-shrink-0 shadow-md"
            >
              Retake
            </button>
            <button
              onClick={handleConfirm}
              className={`text-white px-6 py-3 rounded-full flex-shrink-0 shadow-md ${
                mode === 'product'
                  ? 'bg-gradient-to-br from-green-400 to-green-600'
                  : 'bg-gradient-to-br from-emerald-700 to-emerald-900'
              }`}
            >
              Use Photo
            </button>
          </>
        ) : (
          <div className="flex flex-col items-center gap-4">
            {hasCamera && (
              <button
                onClick={captureImage}
                className="w-20 h-20 bg-white rounded-full flex items-center justify-center flex-shrink-0 shadow-xl"
              >
                <div className={`w-16 h-16 rounded-full ${
                  mode === 'product'
                    ? 'bg-gradient-to-br from-green-400 to-green-600'
                    : 'bg-gradient-to-br from-emerald-700 to-emerald-900'
                }`}></div>
              </button>
            )}
            <button
              onClick={() => fileInputRef.current?.click()}
              className={`text-white px-8 py-3 rounded-full flex-shrink-0 shadow-lg font-medium ${
                mode === 'product'
                  ? 'bg-gradient-to-br from-green-400 to-green-600'
                  : 'bg-gradient-to-br from-emerald-700 to-emerald-900'
              }`}
            >
              Upload Photo
            </button>
          </div>
        )}
      </div>

      <input
        ref={fileInputRef}
        type="file"
        accept="image/*"
        onChange={handleFileChange}
        className="hidden"
      />
    </div>
  )
}