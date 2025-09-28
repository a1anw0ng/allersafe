'use client'

interface ScanButtonProps {
  onClick: () => void
}

export function ScanButton({ onClick }: ScanButtonProps) {
  return (
    <button
      onClick={onClick}
      className="relative group"
      aria-label="Scan"
    >
      <div className="w-32 h-32 bg-gradient-to-br from-primary-500 to-primary-600 rounded-full flex items-center justify-center shadow-lg transform transition-transform group-hover:scale-105 group-active:scale-95">
        <div className="w-28 h-28 bg-white rounded-full flex items-center justify-center">
          <svg
            className="w-16 h-16 text-primary-600"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z"
            />
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M15 13a3 3 0 11-6 0 3 3 0 016 0z"
            />
          </svg>
        </div>
      </div>
      <div className="absolute inset-0 w-32 h-32 bg-primary-500 rounded-full animate-ping opacity-20"></div>
    </button>
  )
}