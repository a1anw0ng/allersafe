'use client'

import { useState, useEffect } from 'react'

interface FoodIcon {
  id: string
  emoji: string
  restrictionId?: string
  top: number
  left: number
  animationDuration: number
  animationDelay: number
}

const allFoodIcons = [
  // Major allergens
  { id: 'peanut', emoji: '🥜', restrictionId: 'peanut' },
  { id: 'tree-nuts', emoji: '🌰', restrictionId: 'tree-nuts' },
  { id: 'milk', emoji: '🥛', restrictionId: 'milk' },
  { id: 'eggs', emoji: '🥚', restrictionId: 'eggs' },
  { id: 'soy', emoji: '🫘', restrictionId: 'soy' },
  { id: 'wheat', emoji: '🌾', restrictionId: 'wheat' },
  { id: 'shellfish', emoji: '🦐', restrictionId: 'shellfish' },
  { id: 'fish', emoji: '🐟', restrictionId: 'fish' },

  // Common foods with allergens
  { id: 'bread', emoji: '🍞', restrictionId: 'wheat' },
  { id: 'cheese', emoji: '🧀', restrictionId: 'milk' },
  { id: 'meat', emoji: '🥩', restrictionId: 'meat' },
  { id: 'chicken', emoji: '🍗', restrictionId: 'meat' },
  { id: 'pizza', emoji: '🍕', restrictionId: 'wheat' },
  { id: 'pasta', emoji: '🍝', restrictionId: 'wheat' },
  { id: 'sushi', emoji: '🍣', restrictionId: 'fish' },
  { id: 'shrimp', emoji: '🍤', restrictionId: 'shellfish' },

  // Fruits
  { id: 'strawberry', emoji: '🍓', restrictionId: 'strawberry' },
  { id: 'orange', emoji: '🍊', restrictionId: 'citrus' },
  { id: 'kiwi', emoji: '🥝', restrictionId: 'kiwi' },
  { id: 'banana', emoji: '🍌', restrictionId: 'banana' },
  { id: 'apple', emoji: '🍎', restrictionId: 'apple' },
  { id: 'peach', emoji: '🍑', restrictionId: 'peach' },
  { id: 'melon', emoji: '🍈', restrictionId: 'melon' },
  { id: 'pineapple', emoji: '🍍', restrictionId: 'pineapple' },
  { id: 'mango', emoji: '🥭', restrictionId: 'mango' },

  // Additional foods
  { id: 'avocado', emoji: '🥑', restrictionId: 'avocado' },
  { id: 'bacon', emoji: '🥓', restrictionId: 'meat' },
]

export function FloatingFoodIcons() {
  const [foodIcons, setFoodIcons] = useState<FoodIcon[]>([])
  const [restrictions, setRestrictions] = useState<Set<string>>(new Set())

  useEffect(() => {
    const saved = localStorage.getItem('dietaryRestrictions')
    if (saved) {
      setRestrictions(new Set(JSON.parse(saved)))
    }

    const handleStorageChange = () => {
      const saved = localStorage.getItem('dietaryRestrictions')
      if (saved) {
        setRestrictions(new Set(JSON.parse(saved)))
      }
    }

    window.addEventListener('storage', handleStorageChange)
    return () => window.removeEventListener('storage', handleStorageChange)
  }, [])

  useEffect(() => {
    const icons = allFoodIcons.map(food => ({
      ...food,
      top: Math.random() * 90,
      left: Math.random() * 90,
      animationDuration: 15 + Math.random() * 15,
      animationDelay: Math.random() * 5,
    }))
    setFoodIcons(icons)
  }, [])

  const isRestricted = (restrictionId?: string) => {
    if (!restrictionId) return false

    // Direct match
    if (restrictions.has(restrictionId)) return true

    // Lifestyle-based restrictions
    if (restrictions.has('vegan') && (restrictionId === 'meat' || restrictionId === 'dairy' || restrictionId === 'eggs' || restrictionId === 'fish' || restrictionId === 'shellfish')) return true
    if (restrictions.has('vegetarian') && (restrictionId === 'meat' || restrictionId === 'fish' || restrictionId === 'shellfish')) return true
    if (restrictions.has('pescatarian') && restrictionId === 'meat') return true

    // Medical conditions
    if (restrictions.has('lactose-intolerant') && restrictionId === 'dairy') return true
    if (restrictions.has('gluten-free') && restrictionId === 'wheat') return true

    // Religious restrictions
    if (restrictions.has('halal') && restrictionId === 'meat') return true // Not all meat, but flagging for awareness
    if (restrictions.has('kosher') && restrictionId === 'shellfish') return true

    return false
  }

  return (
    <div
      className="fixed inset-0 overflow-hidden z-0 pointer-events-none"
    >
      {foodIcons.map((food) => (
        <div
          key={food.id}
          id={`food-icon-${food.id}`}
          className="absolute floating-icon pointer-events-none"
          style={{
            top: `${food.top}%`,
            left: `${food.left}%`,
            animation: `float ${food.animationDuration}s ease-in-out ${food.animationDelay}s infinite`,
          }}
        >
          <div className="relative">
            <span className="text-7xl md:text-8xl opacity-10">
              {food.emoji}
            </span>
            {isRestricted(food.restrictionId) && (
              <div className="absolute inset-0 flex items-center justify-center">
                <svg
                  className="w-20 h-20 md:w-24 md:h-24 opacity-30"
                  viewBox="0 0 24 24"
                  fill="none"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <circle cx="12" cy="12" r="10" stroke="red" strokeWidth="2"/>
                  <line x1="6" y1="6" x2="18" y2="18" stroke="red" strokeWidth="2"/>
                </svg>
              </div>
            )}
          </div>
        </div>
      ))}

    </div>
  )
}