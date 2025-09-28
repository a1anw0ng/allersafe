'use client'

import { useState, useEffect } from 'react'
import { AllergyChecklist } from '@/components/profile/AllergyChecklist'

export default function ProfilePage() {
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [isSaving, setIsSaving] = useState(false)

  useEffect(() => {
    const savedProfile = localStorage.getItem('userProfile')
    if (savedProfile) {
      const profile = JSON.parse(savedProfile)
      setName(profile.name || '')
      setEmail(profile.email || '')
    }
  }, [])

  const handleSaveProfile = () => {
    setIsSaving(true)
    const profile = {
      name,
      email,
      updatedAt: new Date().toISOString(),
    }
    localStorage.setItem('userProfile', JSON.stringify(profile))
    setTimeout(() => {
      setIsSaving(false)
    }, 1000)
  }

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

            <button
              onClick={handleSaveProfile}
              disabled={isSaving}
              className="w-full bg-teal-600 text-white py-3 px-4 rounded-md hover:bg-teal-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed text-base"
            >
              {isSaving ? 'Saving...' : 'Save Profile'}
            </button>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-sm p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Dietary Restrictions</h2>
          <AllergyChecklist />
        </div>
      </div>
    </div>
  )
}