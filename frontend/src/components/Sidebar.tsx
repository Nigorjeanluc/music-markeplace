import { NavLink } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import Logo from './Logo'

const navItems = [
  { to: '/', label: 'Marketplace', icon: '◎' },
  { to: '/library', label: 'Library', icon: '▦' },
  { to: '/artists', label: 'Artists', icon: '👤' },
  { to: '/management', label: 'Management', icon: '⊞', adminOnly: true },
  { to: '/settings', label: 'Settings', icon: '⚙' },
]

export default function Sidebar() {
  const { user } = useAuth()
  const isAdmin = user?.is_admin ?? false

  return (
    <aside className="fixed top-0 left-0 h-screen w-[200px] bg-[#0d0e14] border-r border-[#2a2b38] flex flex-col z-40">
      <div className="px-5 pt-5 pb-4 border-b border-[#2a2b38] mb-2">
        <Logo />
        <p className="text-[10px] tracking-[0.2em] text-[#4a4b5a] uppercase mt-3">Navigation</p>
        <p className="text-[10px] text-[#00e5ff] mt-0.5">Cyber-Noir Interface</p>
      </div>

      <nav className="flex-1 px-2">
        {navItems.map(({ to, label, icon, adminOnly }) => {
          if (adminOnly && !isAdmin) return null
          return (
            <NavLink
              key={to}
              to={to}
              end={to === '/'}
              className={({ isActive }) =>
                `flex items-center gap-3 px-3 py-2.5 rounded text-sm mb-0.5 transition-colors ${
                  isActive
                    ? 'bg-[#1a1b24] text-[#00e5ff] border-l-2 border-[#00e5ff]'
                    : 'text-[#8a8b9a] hover:text-white hover:bg-[#1a1b24]'
                }`
              }
            >
              <span className="text-base w-5 text-center">{icon}</span>
              {label}
            </NavLink>
          )
        })}
      </nav>

      {user && (
        <div className="p-4">
          <button className="w-full border border-[#2a2b38] text-white text-xs py-2.5 px-4 rounded hover:border-[#00e5ff] hover:text-[#00e5ff] transition-colors">
            {user.is_admin ? '+ Upload Track' : 'Upload Track'}
          </button>
        </div>
      )}
    </aside>
  )
}
