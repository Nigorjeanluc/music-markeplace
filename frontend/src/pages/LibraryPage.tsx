import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { useLibrary, useRateAlbum } from '../hooks/useApi'
import type { PurchaseResponse } from '../api/client'
import Pagination from '../components/Pagination'

const RARITY_MAP: Record<number, { label: string; cls: string }> = {
  5: { label: 'LEGENDARY', cls: 'border-[#aa3bff] text-[#aa3bff]' },
  4: { label: 'ULTRA-RARE', cls: 'border-[#00e5ff] text-[#00e5ff]' },
  3: { label: 'RARE', cls: 'border-[#f59e0b] text-[#f59e0b]' },
  2: { label: 'UNCOMMON', cls: 'border-[#8a8b9a] text-[#8a8b9a]' },
  1: { label: 'COMMON', cls: 'border-[#4a4b5a] text-[#4a4b5a]' },
}
const ALBUM_COLORS = ['#0a1a2e', '#1a0a1a', '#0a1a1a', '#0d1a0a', '#1a0a2e', '#0a0a2e']

function getRarity(p: PurchaseResponse) {
  const r = p.avg_rating ?? 0
  if (r >= 4.5) return RARITY_MAP[5]
  if (r >= 3.5) return RARITY_MAP[4]
  if (r >= 2.5) return RARITY_MAP[3]
  if (r >= 1.5) return RARITY_MAP[2]
  return RARITY_MAP[1]
}

function StarRating({ value, onRate }: { value: number; onRate?: (v: number) => void }) {
  return (
    <div className="flex gap-1">
      {[1, 2, 3, 4, 5].map(i => (
        <button
          key={i}
          onClick={() => onRate?.(i)}
          className={`text-lg transition-colors ${onRate ? 'cursor-pointer hover:text-[#00e5ff]' : 'cursor-default'} ${i <= value ? 'text-[#00e5ff]' : 'text-[#2a2b38]'}`}
        >
          ★
        </button>
      ))}
    </div>
  )
}

export default function LibraryPage() {
  const { user } = useAuth()
  const navigate = useNavigate()
  const [page, setPage] = useState(1)
  const { data: libraryData, isLoading, isError } = useLibrary(!!user, { page, page_size: 12 })
  const rateAlbum = useRateAlbum()
  const library = libraryData?.items ?? []

  if (!user) {
    return (
      <div className="flex flex-col items-center justify-center h-[60vh] gap-4">
        <p className="text-[#8a8b9a] text-lg">Access restricted</p>
        <p className="text-[#4a4b5a] text-sm">You need to be logged in to view your library.</p>
        <button onClick={() => navigate('/login')} className="border border-[#00e5ff] text-[#00e5ff] px-6 py-2 rounded text-sm hover:bg-[#00e5ff]/10 transition-colors">
          Login
        </button>
      </div>
    )
  }

  const totalValue = library.reduce((s, p) => s + p.amount_paid, 0)
  const unrated = library.filter(p => !p.user_rating).length

  return (
    <div className="px-4 sm:px-8 pb-6 sm:pb-8">
      <h1 className="text-white text-2xl font-semibold mb-1">User Library</h1>
      <p className="text-[#8a8b9a] text-sm mb-6">
        Access your private vault of digital sonic assets. Every frequency owned, every echo collected.
      </p>

      {/* Stats */}
      <div className="grid grid-cols-3 gap-4 mb-8">
        <div className="bg-[#12131a] border border-[#2a2b38] rounded-lg p-5">
          <p className="text-[10px] tracking-widest text-[#00e5ff] uppercase mb-3">Collection Value</p>
          <div className="flex items-baseline gap-2 mb-3">
            <span className="text-white text-3xl font-bold">${totalValue.toFixed(2)}</span>
          </div>
          <div className="h-1 bg-[#1a1b24] rounded-full">
            <div className="h-1 bg-[#00e5ff] rounded-full" style={{ width: `${Math.min(100, (libraryData?.total ?? 0) * 10)}%` }} />
          </div>
        </div>
        <div className="bg-[#12131a] border border-[#2a2b38] rounded-lg p-5 flex items-start justify-between">
          <div>
            <p className="text-[10px] tracking-widest text-[#aa3bff] uppercase mb-3">Total Albums</p>
            <span className="text-white text-3xl font-bold">{libraryData?.total ?? library.length}</span>
          </div>
          <span className="text-[#2a2b38] text-3xl mt-1">🗄</span>
        </div>
        <div className="bg-[#12131a] border border-[#2a2b38] rounded-lg p-5 flex items-start justify-between">
          <div>
            <p className="text-[10px] tracking-widest text-[#00e5ff] uppercase mb-3">Unrated Clips</p>
            <span className="text-white text-3xl font-bold">{unrated}</span>
          </div>
          <span className="text-[#2a2b38] text-3xl mt-1">☆</span>
        </div>
      </div>

      {isError && (
        <div className="bg-red-900/20 border border-red-500/30 rounded-lg p-4 mb-6 text-red-400 text-sm">
          Failed to load library.
        </div>
      )}

      {isLoading ? (
        <div className="grid grid-cols-4 gap-4">
          {Array.from({ length: 4 }).map((_, i) => (
            <div key={i} className="bg-[#12131a] border border-[#2a2b38] rounded-lg overflow-hidden animate-pulse">
              <div className="h-44 bg-[#1a1b24]" />
              <div className="p-3 space-y-2">
                <div className="h-3 bg-[#1a1b24] rounded w-3/4" />
                <div className="h-3 bg-[#1a1b24] rounded w-1/2" />
              </div>
            </div>
          ))}
        </div>
      ) : library.length === 0 ? (
        <div className="text-center py-16">
          <p className="text-[#4a4b5a] text-lg mb-2">Your vault is empty</p>
          <p className="text-[#4a4b5a] text-sm mb-4">Browse the marketplace and purchase albums to fill your library.</p>
          <button onClick={() => navigate('/')} className="border border-[#00e5ff] text-[#00e5ff] px-6 py-2 rounded text-sm hover:bg-[#00e5ff]/10 transition-colors">
            Browse Marketplace
          </button>
        </div>
      ) : (
        <>
          <div className="grid grid-cols-4 gap-4">
            {library.map((purchase, i) => {
              const rarity = getRarity(purchase)
              return (
                <div key={purchase.id} className="bg-[#12131a] border border-[#2a2b38] rounded-lg overflow-hidden hover:border-[#00e5ff]/30 transition-colors">
                  <div
                    className="h-44 flex items-center justify-center text-4xl cursor-pointer"
                    style={{ background: `radial-gradient(circle, ${ALBUM_COLORS[i % ALBUM_COLORS.length]} 0%, #0d0e14 100%)` }}
                    onClick={() => navigate(`/albums/${purchase.album_id}`)}
                  >
                    🎵
                  </div>
                  <div className="p-3">
                    <div className="flex items-center gap-2 mb-0.5 flex-wrap">
                      <span className="text-white text-sm font-medium">{purchase.album_name}</span>
                      <span className={`border text-[9px] px-1.5 py-0.5 rounded tracking-wider ${rarity.cls}`}>{rarity.label}</span>
                    </div>
                    <p className="text-[#4a4b5a] text-xs mb-3">{purchase.artist_name}</p>
                    <p className={`text-[10px] tracking-widest uppercase mb-1 ${purchase.user_rating ? 'text-[#00e5ff]' : 'text-[#4a4b5a]'}`}>
                      {purchase.user_rating ? 'Your Rating' : 'Rate This Album'}
                    </p>
                    <StarRating
                      value={purchase.user_rating ?? 0}
                      onRate={v => rateAlbum.mutate({ album_id: purchase.album_id, rating: v })}
                    />
                  </div>
                </div>
              )
            })}
          </div>
          {libraryData && libraryData.total_pages > 1 && (
            <div className="mt-8">
              <Pagination
                page={libraryData.page}
                totalPages={libraryData.total_pages}
                onPageChange={setPage}
              />
            </div>
          )}
        </>
      )}
    </div>
  )
}
