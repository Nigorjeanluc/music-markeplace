import { useAuth } from '../context/AuthContext'

interface UserSectionProps {
  onLogout: () => void
  className?: string
}

export default function UserSection({ onLogout, className = '' }: UserSectionProps) {
  const { user } = useAuth()

  return (
    <div className={`p-4 border-t border-[#2a2b38] ${className}`}>
      {user ? (
        <div className="space-y-3">
          <div className="text-center">
            <div className="w-8 h-8 rounded-full bg-[#1a1b24] border border-[#2a2b38] text-xs text-[#8a8b9a] flex items-center justify-center mx-auto mb-2">
              {user.username[0].toUpperCase()}
            </div>
            <p className="text-[10px] tracking-widest text-[#4a4b5a] uppercase mb-1 truncate">{user.username}</p>
            <p className="text-[10px] text-[#00e5ff]">{user.is_admin ? 'Admin' : 'Member'}</p>
          </div>
          <button
            onClick={onLogout}
            className="w-full px-3 py-2 bg-[#1a1b24] border border-[#2a2b38] text-[#8a8b9a] text-xs rounded hover:bg-[#2a2b38] hover:text-white hover:border-[#4a4b5a] transition-colors focus:outline-none focus:ring-2 focus:ring-[#00e5ff] focus:ring-offset-2 focus:ring-offset-[#0d0e14]"
            aria-label="Logout from application"
          >
            Logout
          </button>
        </div>
      ) : (
        <div className="text-center">
          <div className="w-8 h-8 rounded-full bg-[#1a1b24] border border-[#2a2b38] text-[#4a4b9a] flex items-center justify-center mx-auto mb-2">
            ?
          </div>
          <p className="text-[10px] tracking-widest text-[#4a4b5a] uppercase">Not logged in</p>
        </div>
      )}
    </div>
  )
}
