import { NavLink, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

interface TopbarProps {
  searchPlaceholder?: string
}

export default function Topbar({ searchPlaceholder = 'Search the void...' }: TopbarProps) {
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <header className="fixed top-0 left-[200px] right-0 h-14 bg-[#0d0e14] border-b border-[#2a2b38] flex items-center px-6 gap-6 z-30">
      <nav className="flex gap-6 text-sm">
        {[
          { to: '/', label: 'Marketplace' },
          { to: '/library', label: 'Library', authRequired: true },
          { to: '/artists', label: 'Artists' },
          ...(user?.is_admin ? [{ to: '/management', label: 'Management' }] : []),
        ].map(({ to, label, authRequired }) => {
          if (authRequired && !user) return null
          return (
            <NavLink
              key={to}
              to={to}
              end={to === '/'}
              className={({ isActive }) =>
                `transition-colors ${isActive ? 'text-[#00e5ff] border-b border-[#00e5ff] pb-0.5' : 'text-[#8a8b9a] hover:text-white'}`
              }
            >
              {label}
            </NavLink>
          )
        })}
      </nav>

      <div className="ml-auto flex items-center gap-3">
        <div className="flex items-center bg-[#12131a] border border-[#2a2b38] rounded px-3 py-1.5 gap-2 w-52">
          <span className="text-[#4a4b5a] text-sm">🔍</span>
          <input
            className="bg-transparent text-sm text-white placeholder-[#4a4b5a] outline-none w-full"
            placeholder={searchPlaceholder}
          />
        </div>
        <button className="text-[#8a8b9a] hover:text-white text-lg">🔔</button>
        {user ? (
          <button
            onClick={handleLogout}
            className="w-8 h-8 rounded-full bg-[#1a1b24] border border-[#2a2b38] text-xs text-[#00e5ff] hover:border-[#00e5ff] transition-colors flex items-center justify-center"
            title={`${user.username} (${user.is_admin ? 'admin' : 'user'}) — click to logout`}
          >
            {user.username[0]}
          </button>
        ) : (
          <button
            onClick={() => navigate('/login')}
            className="w-8 h-8 rounded-full bg-[#1a1b24] border border-[#2a2b38] text-[#8a8b9a] hover:text-white flex items-center justify-center"
          >
            👤
          </button>
        )}
      </div>
    </header>
  )
}
