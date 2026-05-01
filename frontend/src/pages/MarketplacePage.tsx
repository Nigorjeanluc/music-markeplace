import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { useAlbums, useArtists } from '../hooks/useApi'

const ALBUM_COLORS = ['#1a0a2e', '#0a1a2e', '#0a2e1a', '#1a1a0a', '#2e0a1a', '#0a0a2e']
const MATCH_SCORES = [92, 98, 84, 95, 88, 91]

function StarRating({ value }: { value: number }) {
  return (
    <div className="flex gap-0.5">
      {[1, 2, 3, 4, 5].map(i => (
        <span key={i} className={i <= Math.round(value) ? 'text-[#00e5ff]' : 'text-[#2a2b38]'}>★</span>
      ))}
    </div>
  )
}

function AlbumSkeleton() {
  return (
    <div className="bg-[#12131a] border border-[#2a2b38] rounded-lg overflow-hidden animate-pulse">
      <div className="h-44 bg-[#1a1b24]" />
      <div className="p-3 space-y-2">
        <div className="h-3 bg-[#1a1b24] rounded w-3/4" />
        <div className="h-3 bg-[#1a1b24] rounded w-1/2" />
      </div>
    </div>
  )
}

export default function MarketplacePage() {
  const { user } = useAuth()
  const navigate = useNavigate()
  const [search, setSearch] = useState('')
  const [submitted, setSubmitted] = useState('')

  const { data: albums, isLoading: albumsLoading, isError: albumsError } = useAlbums(submitted ? { search: submitted } : undefined)
  const { data: artists, isLoading: artistsLoading } = useArtists()

  const trendingAlbums = albums?.slice(0, 4) ?? []
  const spotlightArtists = artists?.slice(0, 3) ?? []

  return (
    <div>
      {/* Hero */}
      <div
        className="relative h-72 flex items-end overflow-hidden"
        style={{ background: 'linear-gradient(135deg, #0d1a2e 0%, #1a0a2e 50%, #0d0e14 100%)' }}
      >
        <div className="absolute inset-0 opacity-20"
          style={{ backgroundImage: 'repeating-linear-gradient(0deg, transparent, transparent 40px, #00e5ff11 40px, #00e5ff11 41px), repeating-linear-gradient(90deg, transparent, transparent 40px, #00e5ff11 40px, #00e5ff11 41px)' }} />
        <div className="relative px-8 pb-8 w-full">
          <h1 className="text-5xl font-bold text-[#00e5ff] mb-3" style={{ textShadow: '0 0 40px #00e5ff66' }}>
            Discover the Void
          </h1>
          <p className="text-[#8a8b9a] text-sm max-w-sm mb-6">
            Curating the finest cyber-beats and atmospheric noir sounds from across the digital sprawl.
          </p>
          <form className="flex gap-0" onSubmit={e => { e.preventDefault(); setSubmitted(search) }}>
            <div className="flex items-center bg-[#0d0e14]/80 border border-[#2a2b38] rounded-l px-4 py-2.5 gap-2 w-80">
              <span className="text-[#4a4b5a]">🔍</span>
              <input
                value={search}
                onChange={e => setSearch(e.target.value)}
                placeholder="Search artists, albums, or genres..."
                className="bg-transparent text-sm text-white placeholder-[#4a4b5a] outline-none w-full"
              />
            </div>
            <button type="submit" className="bg-[#00e5ff] text-[#0d0e14] px-5 py-2.5 text-sm font-semibold rounded-r hover:bg-[#00b8cc] transition-colors">
              Search
            </button>
          </form>
        </div>
      </div>

      <div className="px-8 py-8">
        {/* Trending Albums */}
        <div className="flex items-center justify-between mb-5">
          <div>
            <h2 className="text-white text-2xl font-semibold">{submitted ? `Results for "${submitted}"` : 'Trending Albums'}</h2>
            <div className="h-0.5 w-8 bg-[#00e5ff] mt-1" />
          </div>
          <div className="flex items-center gap-4">
            {submitted && (
              <button onClick={() => { setSearch(''); setSubmitted('') }} className="text-[#4a4b5a] text-xs hover:text-white transition-colors">
                Clear ✕
              </button>
            )}
            {!submitted && (
              <button onClick={() => navigate('/')} className="text-[#00e5ff] text-xs tracking-widest uppercase hover:text-white transition-colors">
                View All →
              </button>
            )}
          </div>
        </div>

        {albumsError && (
          <div className="bg-red-900/20 border border-red-500/30 rounded-lg p-4 mb-6 text-red-400 text-sm">
            Failed to load albums. Make sure the backend is running.
          </div>
        )}

        <div className="grid grid-cols-4 gap-4 mb-10">
          {albumsLoading
            ? Array.from({ length: 4 }).map((_, i) => <AlbumSkeleton key={i} />)
            : trendingAlbums.length === 0
              ? <p className="col-span-4 text-[#4a4b5a] text-sm py-8 text-center">No albums found.</p>
              : trendingAlbums.map((album, i) => (
                <div
                  key={album.id}
                  onClick={() => navigate(`/albums/${album.id}`)}
                  className="bg-[#12131a] border border-[#2a2b38] rounded-lg overflow-hidden cursor-pointer hover:border-[#00e5ff]/40 transition-colors group"
                >
                  <div
                    className="h-44 flex items-center justify-center text-4xl relative"
                    style={{ background: `radial-gradient(circle, ${ALBUM_COLORS[i % ALBUM_COLORS.length]} 0%, #0d0e14 100%)` }}
                  >
                    🎵
                  </div>
                  <div className="p-3">
                    <div className="flex items-start justify-between gap-1 mb-1">
                      <span className="text-white text-sm font-medium truncate">{album.name}</span>
                      <span className="text-[#00e5ff] text-xs font-bold whitespace-nowrap">${album.price}</span>
                    </div>
                    <p className="text-[#4a4b5a] text-xs mb-2">by {album.artist_name}</p>
                    <div className="flex items-center justify-between">
                      {album.rating != null ? <StarRating value={album.rating} /> : <span className="text-[#2a2b38] text-sm">★★★★★</span>}
                      <span className="text-[#8a8b9a] text-[10px] tracking-wider">{MATCH_SCORES[i % MATCH_SCORES.length]}% MATCH</span>
                    </div>
                  </div>
                </div>
              ))
          }
        </div>

        {/* Spotlight Artists */}
        {!submitted && (
          <>
            <div className="mb-5">
              <h2 className="text-white text-2xl font-semibold">Spotlight Artists</h2>
              <div className="h-0.5 w-8 bg-[#aa3bff] mt-1" />
            </div>
            <div className="grid grid-cols-3 gap-4">
              {artistsLoading
                ? Array.from({ length: 3 }).map((_, i) => (
                  <div key={i} className="bg-[#12131a] border border-[#2a2b38] rounded-lg p-4 animate-pulse h-28" />
                ))
                : spotlightArtists.map(artist => (
                  <div
                    key={artist.id}
                    onClick={() => navigate(`/artists/${artist.id}`)}
                    className="bg-[#12131a] border border-[#2a2b38] rounded-lg p-4 cursor-pointer hover:border-[#aa3bff]/40 transition-colors"
                  >
                    <div className="flex items-start justify-between mb-3">
                      <div className="flex items-center gap-3">
                        <div className="w-10 h-10 rounded-full bg-[#1a1b24] border border-[#2a2b38] flex items-center justify-center text-lg">🎤</div>
                        <div>
                          <p className="text-white text-sm font-medium">{artist.performing_name}</p>
                          <p className="text-[#4a4b5a] text-xs">{artist.real_name}</p>
                        </div>
                      </div>
                      {user && <button className="text-[#4a4b5a] hover:text-white">⋯</button>}
                    </div>
                    <div className="flex items-center gap-2">
                      <span className="border border-[#2a2b38] text-[#8a8b9a] text-[10px] px-2 py-0.5 rounded tracking-wider">
                        {artist.album_count} ALBUMS
                      </span>
                    </div>
                  </div>
                ))
              }
            </div>
          </>
        )}
      </div>
    </div>
  )
}
