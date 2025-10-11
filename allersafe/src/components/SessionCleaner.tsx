'use client'

import { useEffect } from 'react'

/**
 * Component that cleans up stale profile data on app load
 * This ensures users always start with a fresh session
 */
export function SessionCleaner() {
  useEffect(() => {
    // Only run once on mount
    if (typeof window === 'undefined') return

    // Clear the old profile completion flag (from localStorage)
    // We now use sessionStorage for this instead
    localStorage.removeItem('profileCompleted')

    // Note: We keep userProfile, dietaryRestrictions, customAllergies
    // as defaults for the user, but they must confirm each session
  }, [])

  return null
}
