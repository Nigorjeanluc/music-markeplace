import { Outlet } from 'react-router-dom'
import Sidebar from './Sidebar'
import Topbar from './Topbar'

interface LayoutProps {
  searchPlaceholder?: string
}

export default function Layout({ searchPlaceholder }: LayoutProps) {
  return (
    <div className="min-h-screen bg-[#0d0e14]">
      <Sidebar />
      <Topbar searchPlaceholder={searchPlaceholder} />
      <main className="ml-[200px] pt-14">
        <Outlet />
      </main>
    </div>
  )
}
