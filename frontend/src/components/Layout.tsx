import { Outlet } from 'react-router-dom'
import Sidebar from './Sidebar'
import Topbar from './Topbar'

export default function Layout() {
  return (
    <div className="min-h-screen bg-[#0d0e14]">
      <Sidebar />
      <Topbar />
      <main className="ml-[200px] pt-14">
        <Outlet />
      </main>
    </div>
  )
}
