'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { AllergyChecklist } from '@/components/profile/AllergyChecklist'
import { markProfileCompleted } from '@/lib/profileChecker'

export default function ProfilePage() {
  const router = useRouter()
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [isSaving, setIsSaving] = useState(false)
  const [validationError, setValidationError] = useState('')
  const [showSuccessMessage, setShowSuccessMessage] = useState(false)

  useEffect(() => {
    const savedProfile = localStorage.getItem('userProfile')
    if (savedProfile) {
      const profile = JSON.parse(savedProfile)
      setName(profile.name || '')
      setEmail(profile.email || '')
    }
  }, [])

  const handleSaveProfile = () => {
    // Validation: require name and email
    if (!name.trim()) {
      setValidationError('Please enter your name')
      return
    }
    if (!email.trim()) {
      setValidationError('Please enter your email')
      return
    }
    // Basic email validation
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    if (!emailRegex.test(email)) {
      setValidationError('Please enter a valid email address')
      return
    }

    // Clear any previous errors
    setValidationError('')
    setIsSaving(true)

    // Save user profile
    const profile = {
      name,
      email,
      updatedAt: new Date().toISOString(),
    }
    localStorage.setItem('userProfile', JSON.stringify(profile))

    // Save dietary restrictions (call function from AllergyChecklist)
    if ((window as any).saveDietaryRestrictions) {
      (window as any).saveDietaryRestrictions()
    }

    // Mark profile as completed for this session
    markProfileCompleted()

    setTimeout(() => {
      setIsSaving(false)
      setShowSuccessMessage(true)

      // Auto-hide success message and redirect after 2 seconds
      setTimeout(() => {
        setShowSuccessMessage(false)
        router.push('/')
      }, 2000)
    }, 1000)
  }

  const isFormValid = name.trim() !== '' && email.trim() !== ''

  return (
    <div className="min-h-screen bg-gray-50 pb-24 overflow-y-auto">
      <div className="bg-white shadow-sm">
        <div className="px-4 py-6">
          <h1 className="text-3xl font-bold text-gray-900">Profile</h1>
          <p className="text-gray-600 mt-1 text-base tracking-wide">Manage your dietary preferences</p>
        </div>
      </div>

      <div className="px-4 py-6">
        <div className="bg-white rounded-lg shadow-sm p-6 mb-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Personal Information</h2>

          <div className="space-y-4">
            <div>
              <label htmlFor="name" className="block text-base font-medium text-gray-700 mb-1">
                Name
              </label>
              <input
                type="text"
                id="name"
                value={name}
                onChange={(e) => setName(e.target.value)}
                className="w-full px-3 py-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-teal-500 focus:border-transparent text-base"
                placeholder="Enter your name"
              />
            </div>

            <div>
              <label htmlFor="email" className="block text-base font-medium text-gray-700 mb-1">
                Email
              </label>
              <input
                type="email"
                id="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full px-3 py-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-teal-500 focus:border-transparent text-base"
                placeholder="Enter your email"
              />
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-sm p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Dietary Restrictions</h2>
          <AllergyChecklist />
        </div>

        {/* Validation error message */}
        {validationError && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-4">
            <div className="flex items-start">
              <svg className="w-5 h-5 text-red-600 mt-0.5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <p className="text-red-800 text-base">{validationError}</p>
            </div>
          </div>
        )}

        {/* Success message */}
        {showSuccessMessage && (
          <div className="bg-green-50 border border-green-200 rounded-lg p-4">
            <div className="flex items-start">
              <svg className="w-5 h-5 text-green-600 mt-0.5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <p className="text-green-800 text-base font-medium">Profile saved successfully! Redirecting...</p>
            </div>
          </div>
        )}

        {/* Single save button for entire profile */}
        <button
          onClick={handleSaveProfile}
          disabled={isSaving || !isFormValid}
          className="w-full bg-teal-600 text-white py-3 px-4 rounded-md hover:bg-teal-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed text-base font-medium"
        >
          {isSaving ? 'Saving...' : 'Save Profile'}
        </button>
      </div>
    </div>
  )
}