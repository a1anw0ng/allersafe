/**
 * Check if user has completed their allergy profile for this session
 * Resets on page refresh to ensure fresh data
 */
export function hasCompletedProfile(): boolean {
  if (typeof window === 'undefined') {
    return false
  }

  try {
    // Check if profile was completed THIS SESSION (stored in sessionStorage)
    const sessionCompleted = sessionStorage.getItem('profileCompletedThisSession')
    if (sessionCompleted === 'true') {
      return true
    }

    return false
  } catch (error) {
    console.error('Error checking profile completion:', error)
    return false
  }
}

/**
 * Mark profile as completed for this session only
 */
export function markProfileCompleted() {
  if (typeof window === 'undefined') return
  sessionStorage.setItem('profileCompletedThisSession', 'true')
}

/**
 * Check if user has name and email saved
 */
export function hasUserInfo(): boolean {
  if (typeof window === 'undefined') return false

  try {
    const userProfile = localStorage.getItem('userProfile')
    if (!userProfile) return false

    const profile = JSON.parse(userProfile)
    return !!(profile.name && profile.email)
  } catch {
    return false
  }
}
