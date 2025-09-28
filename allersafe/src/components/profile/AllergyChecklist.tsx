'use client'

import { useState, useEffect } from 'react'

interface Restriction {
  id: string
  name: string
  category: 'allergy' | 'dietary' | 'lifestyle'
  icon?: string
}

const restrictions: Restriction[] = [
  // FDA Top 9 Major Allergens (ordered by prevalence)
  { id: 'milk', name: 'Milk', category: 'allergy', icon: '🥛' }, // Most common - affects 2-3% of children
  { id: 'peanut', name: 'Peanuts', category: 'allergy', icon: '🥜' }, // 2nd most common - affects 2% of children
  { id: 'tree-nuts', name: 'Tree Nuts', category: 'allergy', icon: '🌰' }, // 3rd - affects 1% of population
  { id: 'eggs', name: 'Eggs', category: 'allergy', icon: '🥚' }, // 4th - affects 1-2% of young children
  { id: 'shellfish', name: 'Crustacean Shellfish', category: 'allergy', icon: '🦐' }, // Most common adult allergy - 2% of adults
  { id: 'wheat', name: 'Wheat', category: 'allergy', icon: '🌾' }, // 6th - affects 0.5-1% of children
  { id: 'soy', name: 'Soybeans', category: 'allergy', icon: '🫘' }, // 7th - affects 0.4% of children
  { id: 'fish', name: 'Fish', category: 'allergy', icon: '🐟' }, // 8th - affects 0.4% of adults
  { id: 'sesame', name: 'Sesame', category: 'allergy', icon: '🌱' }, // 9th - affects 0.1-0.2% of population

  // Fruit Allergies
  { id: 'strawberry', name: 'Strawberry', category: 'allergy', icon: '🍓' },
  { id: 'citrus', name: 'Citrus', category: 'allergy', icon: '🍊' },
  { id: 'kiwi', name: 'Kiwi', category: 'allergy', icon: '🥝' },
  { id: 'banana', name: 'Banana', category: 'allergy', icon: '🍌' },
  { id: 'apple', name: 'Apple', category: 'allergy', icon: '🍎' },
  { id: 'peach', name: 'Peach', category: 'allergy', icon: '🍑' },
  { id: 'melon', name: 'Melon', category: 'allergy', icon: '🍈' },
  { id: 'pineapple', name: 'Pineapple', category: 'allergy', icon: '🍍' },
  { id: 'mango', name: 'Mango', category: 'allergy', icon: '🥭' },
  { id: 'avocado', name: 'Avocado', category: 'allergy', icon: '🥑' },

  // Medical/Health Conditions
  { id: 'gluten-free', name: 'Gluten-Free', category: 'dietary', icon: '🚫' },
  { id: 'lactose-intolerant', name: 'Lactose Intolerant', category: 'dietary', icon: '🥛' },
  { id: 'diabetic', name: 'Diabetic', category: 'dietary', icon: '💉' },
  { id: 'keto', name: 'Keto', category: 'dietary', icon: '🥑' },
  { id: 'paleo', name: 'Paleo', category: 'dietary', icon: '🥩' },

  // Lifestyle Choices
  { id: 'vegan', name: 'Vegan', category: 'lifestyle', icon: '🌱' },
  { id: 'vegetarian', name: 'Vegetarian', category: 'lifestyle', icon: '🥗' },
  { id: 'pescatarian', name: 'Pescatarian', category: 'lifestyle', icon: '🐠' },
  { id: 'halal', name: 'Halal', category: 'lifestyle', icon: '☪️' },
  { id: 'kosher', name: 'Kosher', category: 'lifestyle', icon: '✡️' },
]

export function AllergyChecklist() {
  const [selected, setSelected] = useState<Set<string>>(new Set())
  const [customAllergies, setCustomAllergies] = useState<string[]>([])
  const [newAllergy, setNewAllergy] = useState('')
  const [isSaving, setIsSaving] = useState(false)

  useEffect(() => {
    const saved = localStorage.getItem('dietaryRestrictions')
    if (saved) {
      const parsed = JSON.parse(saved)
      // Filter out any empty strings or invalid values
      const validRestrictions = parsed.filter((r: string) => r && r.trim() !== '')
      setSelected(new Set(validRestrictions))
    }

    const savedCustom = localStorage.getItem('customAllergies')
    if (savedCustom) {
      const parsed = JSON.parse(savedCustom)
      // Filter out any empty strings or invalid values
      const validCustom = parsed.filter((a: string) => a && a.trim() !== '')
      setCustomAllergies(validCustom)
    }
  }, [])

  const handleToggle = (id: string) => {
    const newSelected = new Set(selected)
    if (newSelected.has(id)) {
      newSelected.delete(id)
    } else {
      newSelected.add(id)
    }
    setSelected(newSelected)
  }

  const handleAddCustom = () => {
    if (newAllergy.trim() && !customAllergies.includes(newAllergy.trim())) {
      const updated = [...customAllergies, newAllergy.trim()]
      setCustomAllergies(updated)
      localStorage.setItem('customAllergies', JSON.stringify(updated))
      setNewAllergy('')
    }
  }

  const handleRemoveCustom = (allergy: string) => {
    const updated = customAllergies.filter(a => a !== allergy)
    setCustomAllergies(updated)
    localStorage.setItem('customAllergies', JSON.stringify(updated))
  }

  const handleSave = () => {
    setIsSaving(true)
    localStorage.setItem('dietaryRestrictions', JSON.stringify(Array.from(selected)))
    localStorage.setItem('customAllergies', JSON.stringify(customAllergies))
    setTimeout(() => {
      setIsSaving(false)
    }, 1000)
  }

  const fdaAllergens = restrictions.filter(r => r.category === 'allergy').slice(0, 9) // FDA Top 9
  const fruitAllergens = restrictions.filter(r => r.category === 'allergy').slice(9) // Fruit allergies
  const dietaryRestrictions = restrictions.filter(r => r.category === 'dietary')
  const lifestyleRestrictions = restrictions.filter(r => r.category === 'lifestyle')

  return (
    <div className="space-y-6">
      <div>
        <h3 className="text-base font-semibold text-gray-700 uppercase tracking-wider mb-3">
          Allergies
        </h3>
        <div className="grid grid-cols-2 gap-3">
          {fdaAllergens.map((restriction) => (
            <label
              key={restriction.id}
              className="flex items-center space-x-2 cursor-pointer"
            >
              <input
                type="checkbox"
                checked={selected.has(restriction.id)}
                onChange={() => handleToggle(restriction.id)}
                className="w-4 h-4 text-teal-600 border-gray-300 rounded focus:ring-teal-500"
              />
              <span className="text-base text-gray-700 flex items-center gap-1">
                <span>{restriction.icon}</span>
                <span>{restriction.name}</span>
              </span>
            </label>
          ))}
        </div>
      </div>

      <div>
        <h3 className="text-base font-semibold text-gray-700 uppercase tracking-wider mb-3">
          Fruit Allergies
        </h3>
        <div className="grid grid-cols-2 gap-3">
          {fruitAllergens.map((restriction) => (
            <label
              key={restriction.id}
              className="flex items-center space-x-2 cursor-pointer"
            >
              <input
                type="checkbox"
                checked={selected.has(restriction.id)}
                onChange={() => handleToggle(restriction.id)}
                className="w-4 h-4 text-teal-600 border-gray-300 rounded focus:ring-teal-500"
              />
              <span className="text-base text-gray-700 flex items-center gap-1">
                <span>{restriction.icon}</span>
                <span>{restriction.name}</span>
              </span>
            </label>
          ))}
        </div>
      </div>

      <div>
        <h3 className="text-base font-semibold text-gray-700 uppercase tracking-wider mb-3">
          Dietary Needs
        </h3>
        <div className="grid grid-cols-2 gap-3">
          {dietaryRestrictions.map((restriction) => (
            <label
              key={restriction.id}
              className="flex items-center space-x-2 cursor-pointer"
            >
              <input
                type="checkbox"
                checked={selected.has(restriction.id)}
                onChange={() => handleToggle(restriction.id)}
                className="w-4 h-4 text-teal-600 border-gray-300 rounded focus:ring-teal-500"
              />
              <span className="text-base text-gray-700 flex items-center gap-1">
                <span>{restriction.icon}</span>
                <span>{restriction.name}</span>
              </span>
            </label>
          ))}
        </div>
      </div>

      <div>
        <h3 className="text-base font-semibold text-gray-700 uppercase tracking-wider mb-3">
          Lifestyle
        </h3>
        <div className="grid grid-cols-2 gap-3">
          {lifestyleRestrictions.map((restriction) => (
            <label
              key={restriction.id}
              className="flex items-center space-x-2 cursor-pointer"
            >
              <input
                type="checkbox"
                checked={selected.has(restriction.id)}
                onChange={() => handleToggle(restriction.id)}
                className="w-4 h-4 text-teal-600 border-gray-300 rounded focus:ring-teal-500"
              />
              <span className="text-base text-gray-700 flex items-center gap-1">
                <span>{restriction.icon}</span>
                <span>{restriction.name}</span>
              </span>
            </label>
          ))}
        </div>
      </div>

      <div>
        <h3 className="text-base font-semibold text-gray-700 uppercase tracking-wider mb-3">
          Other Dietary Restriction
        </h3>
        <div className="space-y-3">
          <div className="flex gap-2">
            <input
              type="text"
              value={newAllergy}
              onChange={(e) => setNewAllergy(e.target.value)}
              onKeyPress={(e) => {
                if (e.key === 'Enter') {
                  handleAddCustom()
                }
              }}
              placeholder="Enter custom dietary restriction"
              className="flex-1 px-3 py-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-teal-500 focus:border-transparent text-base"
            />
            <button
              onClick={handleAddCustom}
              className="px-4 py-3 bg-teal-600 text-white rounded-md hover:bg-teal-700 transition-colors text-base"
            >
              Add
            </button>
          </div>
          {customAllergies.length > 0 && (
            <div className="flex flex-wrap gap-2">
              {customAllergies.map((allergy) => (
                <span
                  key={allergy}
                  className="inline-flex items-center gap-1 px-3 py-1 bg-red-100 text-red-700 rounded-full text-base"
                >
                  <span>❌</span>
                  <span>{allergy}</span>
                  <button
                    onClick={() => handleRemoveCustom(allergy)}
                    className="ml-1 hover:text-red-900"
                  >
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                    </svg>
                  </button>
                </span>
              ))}
            </div>
          )}
        </div>
      </div>

      <button
        onClick={handleSave}
        disabled={isSaving}
        className="w-full bg-teal-600 text-white py-3 px-4 rounded-md hover:bg-teal-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed text-base"
      >
        {isSaving ? 'Saving...' : 'Save Preferences'}
      </button>
    </div>
  )
}