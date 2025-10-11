'use client'

import { useEffect } from 'react'
import { useRouter } from 'next/navigation'

export default function RestaurantsPage() {
  const router = useRouter()

  useEffect(() => {
    // Set the active tab to restaurants and redirect to home
    localStorage.setItem('activeTab', 'restaurants')
    router.replace('/')
  }, [router])

  return null
}