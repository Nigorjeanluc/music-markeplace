import { Outlet } from 'react-router-dom'
import Sidebar from './Sidebar'
import Topbar from './Topbar'
import { useLayout } from '../hooks/useLayout'

export default function Layout() {
  const { sidebarOpen } = useLayout()

  return (
    <div className="min-h-screen bg-[#0d0e14">
      <Topbar />
      <div className={`relative transition-all duration-300 pt-14 ${sidebarOpen ? 'lg:ml-[200px]' : ''}`}>
        <Sidebar />
        <main className="relative">
          <Outlet />
        </main>
      </div>
    </div>
  )
}
