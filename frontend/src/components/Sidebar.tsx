import { useLayout } from '../hooks/useLayout'
import NavigationItems from './NavigationItems'
import UserSection from './UserSection'

export default function Sidebar() {
  const { sidebarOpen, mobileOpen, closeMobileSidebar, logout } = useLayout()

  return (
    <>
      {/* Mobile overlay */}
      {mobileOpen && (
        <div
          className="lg:hidden fixed inset-0 bg-black/60 z-20"
          onClick={closeMobileSidebar}
          aria-label="Close mobile sidebar"
        />
      )}

      <aside
        id="sidebar"
        className={`
        fixed top-0 left-0 h-screen w-[200px] bg-[#0d0e14] border-r border-[#2a2b38] flex flex-col z-30
        transform transition-transform duration-300 ease-in-out
        lg:translate-x-0
        ${sidebarOpen ? 'lg:translate-x-0' : 'lg:-translate-x-full'}
        ${mobileOpen ? 'translate-x-0' : '-translate-x-full'}
      `}
      aria-label="Main navigation sidebar"
      >
        <div className="px-5 pt-5 pb-4 border-b border-[#2a2b38] mb-2">
          <div className="flex justify-center">
            <span className="font-black text-lg text-[#00e5ff]" aria-hidden="true">M</span>
          </div>
          <p className="text-[10px] tracking-[0.2em] text-[#4a4b5a] uppercase mt-3">Navigation</p>
          <p className="text-[10px] text-[#00e5ff] mt-0.5">Cyber-Noir Interface</p>
        </div>

        <NavigationItems onItemClick={closeMobileSidebar} />
        <UserSection onLogout={logout} />
      </aside>
    </>
  )
}
