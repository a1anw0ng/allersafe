'use client'

import { useRouter } from 'next/navigation'

interface ProfilePromptModalProps {
  isOpen: boolean
  onClose: () => void
}

export function ProfilePromptModal({ isOpen, onClose }: ProfilePromptModalProps) {
  const router = useRouter()

  if (!isOpen) return null

  const handleSetupProfile = () => {
    onClose()
    router.push('/profile')
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
      {/* Backdrop */}
      <div
        className="absolute inset-0 bg-black/50 backdrop-blur-sm"
        onClick={onClose}
      />

      {/* Modal */}
      <div className="relative bg-white rounded-2xl shadow-xl max-w-md w-full p-6 animate-in fade-in zoom-in duration-200">
        {/* Icon */}
        <div className="flex justify-center mb-4">
          <div className="bg-teal-100 rounded-full p-4">
            <svg className="w-12 h-12 text-teal-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
            </svg>
          </div>
        </div>

        {/* Content */}
        <div className="text-center mb-6">
          <h2 className="text-2xl font-bold text-gray-900 mb-2">
            Confirm Your Profile
          </h2>
          <p className="text-gray-600">
            Before scanning products, please confirm your dietary restrictions. This ensures we always have accurate, up-to-date information to find the safest alternatives for you.
          </p>
        </div>

        {/* Actions */}
        <div className="flex flex-col gap-3">
          <button
            onClick={handleSetupProfile}
            className="w-full bg-teal-600 text-white py-3 px-4 rounded-lg font-medium hover:bg-teal-700 transition-colors"
          >
            Confirm Profile
          </button>
        </div>
      </div>
    </div>
  )
}
