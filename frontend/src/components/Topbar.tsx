import { useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import Logo from './Logo'
import { useLayout } from '../hooks/useLayout'

export default function Topbar() {
  const { user } = useAuth()
  const navigate = useNavigate()
  const { sidebarOpen, mobileOpen, toggleSidebar, toggleMobileSidebar, logout } = useLayout()

  return (
    <header className="fixed top-0 left-0 right-0 h-14 bg-[#0d0e14] border-b border-[#2a2b38] flex items-center justify-between px-4 sm:px-6 z-50">
      {/* Left side: Logo and sidebar toggle */}
      <div className="flex items-center gap-4">
        {/* Desktop toggle button */}
        <button
          onClick={toggleSidebar}
          className="hidden lg:flex w-8 h-8 rounded bg-[#1a1b24] border border-[#2a2b38] text-[#8a8b9a] hover:text-white hover:border-[#4a4b5a] transition-colors items-center justify-center text-lg focus:outline-none focus:ring-2 focus:ring-[#00e5ff] focus:ring-offset-2 focus:ring-offset-[#0d0e14]"
          title={sidebarOpen ? 'Hide sidebar' : 'Show sidebar'}
          aria-label={sidebarOpen ? 'Hide navigation sidebar' : 'Show navigation sidebar'}
          aria-expanded={sidebarOpen}
          aria-controls="sidebar"
        >
          {sidebarOpen ? '✕' : '☰'}
        </button>
        {/* Mobile toggle button */}
        <button
          onClick={toggleMobileSidebar}
          className="lg:hidden w-8 h-8 rounded bg-[#1a1b24] border border-[#2a2b38] text-[#8a8b9a] hover:text-white hover:border-[#4a4b5a] transition-colors flex items-center justify-center text-lg focus:outline-none focus:ring-2 focus:ring-[#00e5ff] focus:ring-offset-2 focus:ring-offset-[#0d0e14]"
          title="Toggle mobile menu"
          aria-label={mobileOpen ? 'Close mobile menu' : 'Open mobile menu'}
          aria-expanded={mobileOpen}
          aria-controls="sidebar"
        >
          {mobileOpen ? '✕' : '☰'}
        </button>
        <Logo />
      </div>

      {/* Right side: User actions */}
      <div className="flex items-center gap-3">
        {user ? (
          <button
            onClick={logout}
            className="w-8 h-8 rounded-full bg-[#1a1b24] border border-[#2a2b38] text-xs text-[#00e5ff] hover:border-[#00e5ff] transition-colors flex items-center justify-center focus:outline-none focus:ring-2 focus:ring-[#00e5ff] focus:ring-offset-2 focus:ring-offset-[#0d0e14]"
            title={`${user.username} (${user.is_admin ? 'admin' : 'user'}) — click to logout`}
            aria-label={`User ${user.username} (${user.is_admin ? 'admin' : 'user'}) - click to logout`}
          >
            {user.username[0].toUpperCase()}
          </button>
        ) : (
          <button
            onClick={() => navigate('/login')}
            className="border border-[#2a2b38] text-[#8a8b9a] text-xs px-3 py-1.5 rounded hover:border-[#00e5ff] hover:text-[#00e5ff] transition-colors focus:outline-none focus:ring-2 focus:ring-[#00e5ff] focus:ring-offset-2 focus:ring-offset-[#0d0e14]"
            aria-label="Navigate to login page"
          >
            Login
          </button>
        )}
      </div>
    </header>
  )
}
