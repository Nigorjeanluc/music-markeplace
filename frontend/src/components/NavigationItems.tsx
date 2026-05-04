import { NavLink } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

const navItems = [
  { to: '/', label: 'Marketplace', icon: '◎', 'aria-label': 'Navigate to Marketplace' },
  { to: '/library', label: 'Library', icon: '▦', authRequired: true, hideForAdmin: true, 'aria-label': 'Navigate to Library' },
  { to: '/playlists', label: 'Playlists', icon: '♫', authRequired: true, hideForAdmin: true, 'aria-label': 'Navigate to Playlists' },
  { to: '/artists', label: 'Artists', icon: '👤', 'aria-label': 'Navigate to Artists' },
  { to: '/management', label: 'Management', icon: '⊞', adminOnly: true, 'aria-label': 'Navigate to Management' },
]

interface NavigationItemsProps {
  onItemClick?: () => void
  className?: string
}

export default function NavigationItems({ onItemClick, className = '' }: NavigationItemsProps) {
  const { user } = useAuth()
  const isAdmin = user?.is_admin ?? false

  return (
    <nav className={`flex-1 px-2 overflow-y-auto ${className}`}>
      {navItems.map(({ to, label, icon, adminOnly, authRequired, hideForAdmin, 'aria-label': ariaLabel }) => {
        if (adminOnly && !isAdmin) return null
        if (hideForAdmin && isAdmin) return null
        if (authRequired && !user) return null
        
        return (
          <NavLink
            key={to}
            to={to}
            end={to === '/'}
            onClick={onItemClick}
            className={({ isActive }) =>
              `flex items-center gap-3 px-3 py-2.5 rounded text-sm mb-0.5 transition-colors focus:outline-none focus:ring-2 focus:ring-[#00e5ff] focus:ring-offset-2 focus:ring-offset-[#0d0e14] ${
                isActive
                  ? 'bg-[#1a1b24] text-[#00e5ff] border-l-2 border-[#00e5ff]'
                  : 'text-[#8a8b9a] hover:text-white hover:bg-[#1a1b24]'
              }`
            }
            aria-label={ariaLabel}
          >
            <span className="text-base w-5 text-center" aria-hidden="true">{icon}</span>
            <span className="font-medium">{label}</span>
          </NavLink>
        )
      })}
    </nav>
  )
}
