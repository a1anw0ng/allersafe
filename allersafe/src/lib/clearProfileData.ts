/**
 * Clear all profile-related data from localStorage
 * Use this to force users to re-enter their profile
 */
export function clearAllProfileData() {
  if (typeof window === 'undefined') return

  // Clear all profile-related keys
  localStorage.removeItem('userProfile')
  localStorage.removeItem('dietaryRestrictions')
  localStorage.removeItem('customAllergies')
  localStorage.removeItem('noDietaryRestrictions')
  localStorage.removeItem('profileCompleted')
}

/**
 * Clear only dietary restriction data (keep user info)
 */
export function clearDietaryData() {
  if (typeof window === 'undefined') return

  localStorage.removeItem('dietaryRestrictions')
  localStorage.removeItem('customAllergies')
  localStorage.removeItem('noDietaryRestrictions')
  localStorage.removeItem('profileCompleted')
}
