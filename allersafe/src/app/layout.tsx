import type { Metadata } from 'next'
import { Playfair_Display } from 'next/font/google'
import './globals.css'
import { BottomNav } from '@/components/navigation/BottomNav'

const playfair = Playfair_Display({
  subsets: ['latin']
})

export const metadata: Metadata = {
  title: 'AllerSafe',
  description: 'Find safe food alternatives for your dietary restrictions and allergies',
  manifest: '/manifest.json',
  viewport: {
    width: 'device-width',
    initialScale: 1,
    maximumScale: 1,
    userScalable: false,
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={`${playfair.className} min-h-screen bg-gray-50`}>
        <div className="flex flex-col min-h-screen">
          <main className="flex-1">
            {children}
          </main>
          <BottomNav />
        </div>
      </body>
    </html>
  )
}