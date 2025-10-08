/**
 * Utility functions for managing allergy profile data
 */

interface Restriction {
  id: string
  name: string
  category: 'allergy' | 'dietary' | 'lifestyle'
}

// Same restrictions list from AllergyChecklist component
const restrictions: Restriction[] = [
  // FDA Top 9 Major Allergens
  { id: 'milk', name: 'Milk', category: 'allergy' },
  { id: 'peanut', name: 'Peanuts', category: 'allergy' },
  { id: 'tree-nuts', name: 'Tree Nuts', category: 'allergy' },
  { id: 'eggs', name: 'Eggs', category: 'allergy' },
  { id: 'shellfish', name: 'Crustacean Shellfish', category: 'allergy' },
  { id: 'wheat', name: 'Wheat', category: 'allergy' },
  { id: 'soy', name: 'Soybeans', category: 'allergy' },
  { id: 'fish', name: 'Fish', category: 'allergy' },
  { id: 'sesame', name: 'Sesame', category: 'allergy' },

  // Fruit Allergies
  { id: 'strawberry', name: 'Strawberry', category: 'allergy' },
  { id: 'citrus', name: 'Citrus', category: 'allergy' },
  { id: 'kiwi', name: 'Kiwi', category: 'allergy' },
  { id: 'banana', name: 'Banana', category: 'allergy' },
  { id: 'apple', name: 'Apple', category: 'allergy' },
  { id: 'peach', name: 'Peach', category: 'allergy' },
  { id: 'melon', name: 'Melon', category: 'allergy' },
  { id: 'pineapple', name: 'Pineapple', category: 'allergy' },
  { id: 'mango', name: 'Mango', category: 'allergy' },
  { id: 'avocado', name: 'Avocado', category: 'allergy' },

  // Medical/Health Conditions
  { id: 'gluten-free', name: 'Gluten-Free', category: 'dietary' },
  { id: 'lactose-intolerant', name: 'Lactose Intolerant', category: 'dietary' },
  { id: 'diabetic', name: 'Diabetic', category: 'dietary' },
  { id: 'keto', name: 'Keto', category: 'dietary' },
  { id: 'paleo', name: 'Paleo', category: 'dietary' },

  // Lifestyle Choices
  { id: 'vegan', name: 'Vegan', category: 'lifestyle' },
  { id: 'vegetarian', name: 'Vegetarian', category: 'lifestyle' },
  { id: 'pescatarian', name: 'Pescatarian', category: 'lifestyle' },
  { id: 'halal', name: 'Halal', category: 'lifestyle' },
  { id: 'kosher', name: 'Kosher', category: 'lifestyle' },
]

/**
 * Get allergy profile data from localStorage
 * @returns Object with selected restrictions and custom allergies
 */
export function getAllergyProfile() {
  if (typeof window === 'undefined') {
    return { restrictions: [], customAllergies: [] }
  }

  try {
    const restrictionsJson = localStorage.getItem('dietaryRestrictions')
    const customJson = localStorage.getItem('customAllergies')

    const selectedRestrictions = restrictionsJson ? JSON.parse(restrictionsJson) : []
    const customAllergies = customJson ? JSON.parse(customJson) : []

    return {
      restrictions: selectedRestrictions.filter((r: string) => r && r.trim() !== ''),
      customAllergies: customAllergies.filter((a: string) => a && a.trim() !== ''),
    }
  } catch (error) {
    console.error('Error reading allergy profile:', error)
    return { restrictions: [], customAllergies: [] }
  }
}

/**
 * Format allergy profile as a human-readable string
 * @returns Formatted string with all allergy information
 */
export function formatAllergyProfileString(): string {
  const { restrictions: selectedIds, customAllergies } = getAllergyProfile()

  if (selectedIds.length === 0 && customAllergies.length === 0) {
    return 'No dietary restrictions specified'
  }

  // Group restrictions by category
  const allergies: string[] = []
  const dietary: string[] = []
  const lifestyle: string[] = []

  selectedIds.forEach((id: string) => {
    const restriction = restrictions.find(r => r.id === id)
    if (restriction) {
      switch (restriction.category) {
        case 'allergy':
          allergies.push(restriction.name)
          break
        case 'dietary':
          dietary.push(restriction.name)
          break
        case 'lifestyle':
          lifestyle.push(restriction.name)
          break
      }
    }
  })

  // Build formatted string
  const parts: string[] = []

  if (allergies.length > 0) {
    parts.push(`Allergies: ${allergies.join(', ')}`)
  }

  if (dietary.length > 0) {
    parts.push(`Dietary: ${dietary.join(', ')}`)
  }

  if (lifestyle.length > 0) {
    parts.push(`Lifestyle: ${lifestyle.join(', ')}`)
  }

  if (customAllergies.length > 0) {
    parts.push(`Custom: ${customAllergies.join(', ')}`)
  }

  return parts.join('; ')
}

/**
 * Get allergy profile data as an array of names (for API calls)
 * @returns Array of all allergy/restriction names
 */
export function getAllergyNames(): string[] {
  const { restrictions: selectedIds, customAllergies } = getAllergyProfile()

  const names = selectedIds.map((id: string) => {
    const restriction = restrictions.find(r => r.id === id)
    return restriction ? restriction.name : null
  }).filter((name): name is string => name !== null)

  return [...names, ...customAllergies]
}
