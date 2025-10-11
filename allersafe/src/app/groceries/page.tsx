'use client'

import { useEffect } from 'react'
import { useRouter } from 'next/navigation'

export default function GroceriesPage() {
  const router = useRouter()

  useEffect(() => {
    // Set the active tab to groceries and redirect to home
    localStorage.setItem('activeTab', 'groceries')
    router.replace('/')
  }, [router])

  return null
}