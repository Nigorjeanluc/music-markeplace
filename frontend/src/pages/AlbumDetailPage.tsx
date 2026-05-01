import { useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { useAlbum, usePurchase, useRateAlbum, useLibrary } from '../hooks/useApi'

function StarRating({ value, locked, onRate }: { value: number; locked: boolean; onRate?: (v: number) => void }) {
  return (
    <div className="flex gap-1">
      {[1, 2, 3, 4, 5].map(i => (
        <button
          key={i}
          disabled={locked}
          onClick={() => onRate?.(i)}
          className={`text-xl transition-colors ${locked ? 'cursor-not-allowed' : 'cursor-pointer hover:text-[#00e5ff]'} ${i <= value ? 'text-[#00e5ff]' : 'text-[#2a2b38]'}`}
        >
          ★
        </button>
      ))}
    </div>
  )
}

export default function AlbumDetailPage() {
  const { id } = useParams<{ id: string }>()
  const { user } = useAuth()
  const navigate = useNavigate()
  const [playing, setPlaying] = useState(false)

  const { data: album, isLoading, isError } = useAlbum(id!)
  const { data: library } = useLibrary(!!user)
  const purchase = usePurchase()
  const rateAlbum = useRateAlbum()

  const purchased = library?.some(p => p.album_id === id) ?? false
  const myPurchase = library?.find(p => p.album_id === id)
  const userRating = myPurchase?.user_rating ?? 0
  const canRate = purchased && !!user

  const handlePurchase = () => {
    if (!user) { navigate('/login'); return }
    purchase.mutate(id!)
  }

  const handleRate = (v: number) => {
    rateAlbum.mutate({ album_id: id!, rating: v })
  }

  if (isLoading) {
    return (
      <div className="px-8 py-6 animate-pulse">
        <div className="h-4 bg-[#1a1b24] rounded w-32 mb-6" />
        <div className="grid grid-cols-2 gap-8">
          <div className="aspect-square bg-[#1a1b24] rounded-lg" />
          <div className="space-y-4">
            <div className="h-8 bg-[#1a1b24] rounded w-3/4" />
            <div className="h-4 bg-[#1a1b24] rounded w-1/2" />
          </div>
        </div>
      </div>
    )
  }

  if (isError || !album) {
    return (
      <div className="flex flex-col items-center justify-center h-[60vh] gap-4">
        <p className="text-[#8a8b9a]">Album not found.</p>
        <button onClick={() => navigate('/')} className="text-[#00e5ff] text-sm hover:underline">← Back to Marketplace</button>
      </div>
    )
  }

  return (
    <div className="px-8 py-6">
      <button
        onClick={() => navigate(-1)}
        className="flex items-center gap-2 text-[#8a8b9a] text-xs tracking-widest uppercase hover:text-white transition-colors mb-6"
      >
        ← Return to Marketplace
      </button>

      <div className="grid grid-cols-2 gap-8">
        {/* Left: Cover + Player */}
        <div>
          <div
            className="rounded-lg overflow-hidden mb-4 aspect-square flex items-center justify-center text-8xl"
            style={{ background: 'radial-gradient(circle, #0a1a2e 0%, #0d0e14 100%)' }}
          >
            🎵
          </div>
          <div className="bg-[#12131a] border border-[#2a2b38] rounded-lg p-4">
            <p className="text-[10px] tracking-widest text-[#00e5ff] uppercase mb-1">Previewing Track</p>
            <div className="flex items-center justify-between mb-3">
              <span className="text-white font-medium">{album.name}</span>
              <div className="flex items-center gap-3">
                <button className="text-[#8a8b9a] hover:text-white text-lg">⏮</button>
                <button
                  onClick={() => setPlaying(!playing)}
                  className="w-9 h-9 rounded-full border border-[#00e5ff] text-[#00e5ff] flex items-center justify-center hover:bg-[#00e5ff]/10 transition-colors"
                >
                  {playing ? '⏸' : '▶'}
                </button>
                <button className="text-[#8a8b9a] hover:text-white text-lg">⏭</button>
              </div>
            </div>
            <div className="h-1 bg-[#1a1b24] rounded-full">
              <div className="h-1 bg-[#00e5ff] rounded-full w-1/3" />
            </div>
          </div>
        </div>

        {/* Right: Info + Purchase */}
        <div>
          <div className="flex gap-2 mb-4">
            <span className="border border-[#2a2b38] text-[#8a8b9a] text-xs px-3 py-1 rounded tracking-wider">LOSSLESS</span>
            <span className="border border-[#2a2b38] text-[#8a8b9a] text-xs px-3 py-1 rounded tracking-wider">EXCLUSIVE</span>
            {album.genre_names.map(g => (
              <span key={g} className="border border-[#2a2b38] text-[#8a8b9a] text-xs px-3 py-1 rounded tracking-wider">{g}</span>
            ))}
          </div>

          <h1 className="text-white text-5xl font-black tracking-tight mb-4 uppercase" style={{ textShadow: '0 0 30px #00e5ff44' }}>
            {album.name}
          </h1>

          <div className="flex items-center gap-3 mb-6">
            <div className="w-9 h-9 rounded-full bg-[#1a1b24] border border-[#2a2b38] flex items-center justify-center">🎤</div>
            <div>
              <p className="text-[10px] tracking-widest text-[#4a4b5a] uppercase">Produced By</p>
              <p className="text-white font-semibold">{album.artist_name}</p>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-3 mb-6">
            <div className="bg-[#12131a] border border-[#2a2b38] rounded-lg p-4">
              <p className="text-[10px] tracking-widest text-[#4a4b5a] uppercase mb-2">Price</p>
              <div className="flex items-baseline gap-2">
                <span className="text-white text-3xl font-bold">{album.price.toFixed(2)}</span>
                <span className="text-[#4a4b5a] text-sm">USD</span>
              </div>
            </div>
            <div className="bg-[#12131a] border border-[#2a2b38] rounded-lg p-4">
              <p className="text-[10px] tracking-widest text-[#4a4b5a] uppercase mb-2">Rating</p>
              <div className="flex items-center gap-2">
                <span className="text-white text-3xl font-bold">{album.rating != null ? album.rating.toFixed(1) : '—'}</span>
                {album.rating != null && <span className="text-[#00e5ff]">★</span>}
              </div>
            </div>
          </div>

          {purchase.isError && (
            <p className="text-red-400 text-xs mb-3 text-center">
              {(purchase.error as { response?: { data?: { detail?: string } } })?.response?.data?.detail ?? 'Purchase failed'}
            </p>
          )}

          {!purchased ? (
            <>
              <button
                onClick={handlePurchase}
                disabled={purchase.isPending}
                className="w-full bg-[#00e5ff]/10 border border-[#00e5ff] text-[#00e5ff] py-4 rounded-lg text-sm tracking-widest uppercase font-semibold hover:bg-[#00e5ff]/20 transition-colors mb-3 flex items-center justify-center gap-2 disabled:opacity-50"
              >
                {purchase.isPending ? 'Processing...' : '🛒 Purchase Album'}
              </button>
              <p className="text-[#4a4b5a] text-xs text-center italic">
                "Secure your access to high-fidelity audio streams and digital ownership."
              </p>
            </>
          ) : (
            <div className="bg-[#00e5ff]/5 border border-[#00e5ff]/30 rounded-lg p-4 mb-3 text-center">
              <p className="text-[#00e5ff] text-sm font-semibold">✓ Album Purchased</p>
              <p className="text-[#4a4b5a] text-xs mt-1">Now in your library</p>
            </div>
          )}

          {/* Post-purchase rating */}
          <div className={`bg-[#12131a] border border-[#2a2b38] rounded-lg p-5 mt-4 ${!canRate ? 'opacity-50' : ''}`}>
            <p className="text-[10px] tracking-widest text-[#4a4b5a] uppercase mb-3">Post-Purchase Rating</p>
            <p className="text-[10px] tracking-widest text-[#4a4b5a] uppercase mb-2">Your Score</p>
            <div className="flex items-center gap-3">
              <StarRating value={userRating} locked={!canRate} onRate={canRate ? handleRate : undefined} />
              {!canRate && (
                <div className="flex items-center gap-2 text-[#4a4b5a] text-xs">
                  <span>🔒</span>
                  {!user ? (
                    <button onClick={() => navigate('/login')} className="text-[#00e5ff] hover:underline">Login to rate</button>
                  ) : (
                    'Purchase to Unlock Rating'
                  )}
                </div>
              )}
              {rateAlbum.isPending && <span className="text-[#4a4b5a] text-xs">Saving...</span>}
            </div>
          </div>

          {/* Metadata */}
          <div className="grid grid-cols-2 gap-3 mt-4 text-xs text-[#8a8b9a]">
            {album.release_date && (
              <div className="flex items-center gap-2">
                <span className="text-[#4a4b5a]">🕐</span>
                Released: {new Date(album.release_date).toLocaleDateString()}
              </div>
            )}
            <div className="flex items-center gap-2">
              <span className="text-[#4a4b5a]">🎵</span>
              Genres: {album.genre_names.join(', ') || 'N/A'}
            </div>
            <div className="flex items-center gap-2">
              <span className="text-[#4a4b5a]">📊</span>
              BPM: 128
            </div>
            <div className="flex items-center gap-2">
              <span className="text-[#4a4b5a]">🎹</span>
              Key: C Minor
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
