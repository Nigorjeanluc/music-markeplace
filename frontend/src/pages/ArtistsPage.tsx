import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useArtists } from '../hooks/useApi'

export default function ArtistsPage() {
  const navigate = useNavigate()
  const [search, setSearch] = useState('')
  const [submitted, setSubmitted] = useState('')
  const { data: artists, isLoading, isError } = useArtists(submitted || undefined)

  return (
    <div className="px-8 py-8">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-white text-2xl font-semibold">Artists</h1>
          <div className="h-0.5 w-8 bg-[#aa3bff] mt-1" />
        </div>
        <form className="flex items-center bg-[#12131a] border border-[#2a2b38] rounded px-3 py-2 gap-2 w-64"
          onSubmit={e => { e.preventDefault(); setSubmitted(search) }}>
          <span className="text-[#4a4b5a]">🔍</span>
          <input
            value={search}
            onChange={e => { setSearch(e.target.value); if (!e.target.value) setSubmitted('') }}
            placeholder="Search artists..."
            className="bg-transparent text-sm text-white placeholder-[#4a4b5a] outline-none w-full"
          />
        </form>
      </div>

      {isError && (
        <div className="bg-red-900/20 border border-red-500/30 rounded-lg p-4 mb-6 text-red-400 text-sm">
          Failed to load artists.
        </div>
      )}

      {isLoading ? (
        <div className="grid grid-cols-3 gap-4">
          {Array.from({ length: 6 }).map((_, i) => (
            <div key={i} className="bg-[#12131a] border border-[#2a2b38] rounded-lg p-5 animate-pulse h-36" />
          ))}
        </div>
      ) : artists?.length === 0 ? (
        <p className="text-[#4a4b5a] text-sm text-center py-16">No artists found.</p>
      ) : (
        <div className="grid grid-cols-3 gap-4">
          {artists?.map(artist => (
            <div
              key={artist.id}
              onClick={() => navigate(`/artists/${artist.id}`)}
              className="bg-[#12131a] border border-[#2a2b38] rounded-lg p-5 cursor-pointer hover:border-[#aa3bff]/40 transition-colors"
            >
              <div className="flex items-center gap-4 mb-4">
                <div className="w-14 h-14 rounded-full bg-[#1a1b24] border border-[#2a2b38] flex items-center justify-center text-2xl overflow-hidden">
                  {artist.photo_url
                    ? <img src={artist.photo_url} alt={artist.performing_name} className="w-full h-full object-cover" />
                    : '🎤'
                  }
                </div>
                <div>
                  <p className="text-white font-semibold">{artist.performing_name}</p>
                  <p className="text-[#4a4b5a] text-xs">{artist.real_name}</p>
                  <p className="text-[#8a8b9a] text-xs mt-0.5">{new Date(artist.date_of_birth).getFullYear()}</p>
                </div>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-[#4a4b5a] text-xs">{artist.album_count} albums</span>
                <span className="border border-[#2a2b38] text-[#8a8b9a] text-[10px] px-2 py-0.5 rounded tracking-wider">
                  ARTIST
                </span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
