import { create } from 'zustand'
import { persist, createJSONStorage } from 'zustand/middleware'

export interface DietaryRestriction {
  id: string
  name: string
  category: 'allergy' | 'dietary' | 'lifestyle'
  icon?: string
}

export interface UserProfile {
  name: string
  email: string
  restrictions: string[]
  updatedAt?: string
}

export interface ScanHistory {
  id: string
  type: 'product' | 'meal'
  image?: string
  timestamp: Date
  result?: any
}

interface StoreState {
  userProfile: UserProfile | null
  scanHistory: ScanHistory[]
  activeTab: 'groceries' | 'restaurants'

  setUserProfile: (profile: UserProfile) => void
  updateRestrictions: (restrictions: string[]) => void
  addScanToHistory: (scan: ScanHistory) => void
  clearScanHistory: () => void
  setActiveTab: (tab: 'groceries' | 'restaurants') => void
  resetStore: () => void
}

const initialState = {
  userProfile: null,
  scanHistory: [],
  activeTab: 'groceries' as const,
}

export const useStore = create<StoreState>()(
  persist(
    (set) => ({
      ...initialState,

      setUserProfile: (profile) =>
        set(() => ({
          userProfile: {
            ...profile,
            updatedAt: new Date().toISOString(),
          },
        })),

      updateRestrictions: (restrictions) =>
        set((state) => ({
          userProfile: state.userProfile
            ? {
                ...state.userProfile,
                restrictions,
                updatedAt: new Date().toISOString(),
              }
            : {
                name: '',
                email: '',
                restrictions,
                updatedAt: new Date().toISOString(),
              },
        })),

      addScanToHistory: (scan) =>
        set((state) => ({
          scanHistory: [scan, ...state.scanHistory].slice(0, 20),
        })),

      clearScanHistory: () =>
        set(() => ({
          scanHistory: [],
        })),

      setActiveTab: (tab) =>
        set(() => ({
          activeTab: tab,
        })),

      resetStore: () =>
        set(() => initialState),
    }),
    {
      name: 'allersafe-storage',
      storage: createJSONStorage(() => localStorage),
      partialize: (state) => ({
        userProfile: state.userProfile,
        scanHistory: state.scanHistory,
      }),
    }
  )
)