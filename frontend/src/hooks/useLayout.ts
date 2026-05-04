import { useState, useEffect, useCallback } from 'react'
import { useAuth } from '../context/AuthContext'

interface LayoutState {
  sidebarOpen: boolean
  mobileOpen: boolean
  toggleSidebar: () => void
  toggleMobileSidebar: () => void
  closeMobileSidebar: () => void
  logout: () => void
}

export function useLayout(): LayoutState {
  const { logout: authLogout } = useAuth()
  const [sidebarOpen, setSidebarOpen] = useState(true)
  const [mobileOpen, setMobileOpen] = useState(false)

  const toggleSidebar = useCallback(() => {
    const newState = !sidebarOpen
    setSidebarOpen(newState)
    // Dispatch event for backward compatibility
    window.dispatchEvent(new CustomEvent('toggle-sidebar', { detail: { open: newState } }))
  }, [sidebarOpen])

  const toggleMobileSidebar = useCallback(() => {
    const newState = !mobileOpen
    setMobileOpen(newState)
    // Dispatch event for backward compatibility
    window.dispatchEvent(new CustomEvent('toggle-mobile-sidebar', { detail: { open: newState } }))
  }, [mobileOpen])

  const closeMobileSidebar = useCallback(() => {
    setMobileOpen(false)
    window.dispatchEvent(new CustomEvent('toggle-mobile-sidebar', { detail: { open: false } }))
  }, [])

  const logout = useCallback(() => {
    // Clear tokens
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    // Use auth context logout
    authLogout()
    // Redirect to login
    window.location.href = '/login'
  }, [authLogout])

  // Listen for external toggle events and keyboard navigation
  useEffect(() => {
    const handleSidebarToggle = (event: CustomEvent) => {
      setSidebarOpen(event.detail.open)
    }

    const handleMobileToggle = (event: CustomEvent) => {
      setMobileOpen(event.detail.open)
    }

    const handleKeyDown = (event: KeyboardEvent) => {
      // Close mobile sidebar on Escape key
      if (event.key === 'Escape' && mobileOpen) {
        setMobileOpen(false)
        window.dispatchEvent(new CustomEvent('toggle-mobile-sidebar', { detail: { open: false } }))
      }
    }

    window.addEventListener('toggle-sidebar', handleSidebarToggle as EventListener)
    window.addEventListener('toggle-mobile-sidebar', handleMobileToggle as EventListener)
    window.addEventListener('keydown', handleKeyDown)
    
    return () => {
      window.removeEventListener('toggle-sidebar', handleSidebarToggle as EventListener)
      window.removeEventListener('toggle-mobile-sidebar', handleMobileToggle as EventListener)
      window.removeEventListener('keydown', handleKeyDown)
    }
  }, [mobileOpen])

  return {
    sidebarOpen,
    mobileOpen,
    toggleSidebar,
    toggleMobileSidebar,
    closeMobileSidebar,
    logout
  }
}
