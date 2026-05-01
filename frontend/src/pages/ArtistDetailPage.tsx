import { useParams, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { useArtist, useAlbums } from '../hooks/useApi'

const ALBUM_COLORS = ['#0a1a2e', '#1a0a2e', '#0a2e1a', '#1a1a0a']

export default function ArtistDetailPage() {
  const { id } = useParams<{ id: string }>()
  const { user } = useAuth()
  const navigate = useNavigate()
  const { data: artist, isLoading, isError } = useArtist(id!)
  const { data: albums } = useAlbums({ artist_id: id })

  if (isLoading) {
    return (
      <div className="animate-pulse">
        <div className="h-72 bg-[#1a1b24]" />
        <div className="px-8 py-6 space-y-4">
          <div className="h-6 bg-[#1a1b24] rounded w-1/3" />
          <div className="h-4 bg-[#1a1b24] rounded w-2/3" />
        </div>
      </div>
    )
  }

  if (isError || !artist) {
    return (
      <div className="flex flex-col items-center justify-center h-[60vh] gap-4">
        <p className="text-[#8a8b9a]">Artist not found.</p>
        <button onClick={() => navigate('/artists')} className="text-[#00e5ff] text-sm hover:underline">← Back to Artists</button>
      </div>
    )
  }

  return (
    <div>
      {/* Hero */}
      <div className="relative h-72 flex items-end" style={{ background: 'linear-gradient(180deg, #1a0a2e 0%, #0d0e14 100%)' }}>
        <div className="absolute inset-0 opacity-10"
          style={{ backgroundImage: 'repeating-linear-gradient(45deg, #aa3bff11 0px, #aa3bff11 1px, transparent 1px, transparent 20px)' }} />
        <div className="relative px-8 pb-6 w-full flex items-end justify-between">
          <div>
            <p className="text-[10px] tracking-[0.3em] text-[#00e5ff] uppercase mb-2">Featured Producer</p>
            <h1 className="text-white text-3xl font-bold mb-2">{artist.performing_name}</h1>
            <p className="text-[#8a8b9a] text-sm">{artist.album_count} Albums · Born {new Date(artist.date_of_birth).getFullYear()}</p>
          </div>
          <div className="flex gap-3">
            <button className="bg-[#00e5ff] text-[#0d0e14] px-5 py-2.5 rounded text-sm font-semibold hover:bg-[#00b8cc] transition-colors">
              ▶ Follow
            </button>
            <button className="border border-[#2a2b38] text-white px-5 py-2.5 rounded text-sm hover:border-[#00e5ff] transition-colors">
              ↗ Share
            </button>
          </div>
        </div>
      </div>

      <div className="px-8 py-6 grid grid-cols-3 gap-6">
        {/* Left: Bio + Discography */}
        <div className="col-span-2 space-y-6">
          <div className="bg-[#12131a] border border-[#2a2b38] rounded-lg p-6">
            <div className="flex items-center gap-2 mb-5">
              <div className="w-6 h-0.5 bg-[#00e5ff]" />
              <span className="text-white text-sm font-medium">Bio</span>
            </div>
            <div className="grid grid-cols-2 gap-4 mb-4">
              <div>
                <p className="text-[10px] tracking-widest text-[#4a4b5a] uppercase mb-1">Legal Identity</p>
                <p className="text-white text-sm">{artist.real_name}</p>
              </div>
              <div>
                <p className="text-[10px] tracking-widest text-[#4a4b5a] uppercase mb-1">Date of Birth</p>
                <p className="text-white text-sm">{new Date(artist.date_of_birth).toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' })}</p>
              </div>
            </div>
            <p className="text-[#8a8b9a] text-sm leading-relaxed">
              {artist.performing_name} is a recording artist with {artist.album_count} album{artist.album_count !== 1 ? 's' : ''} in the catalog.
            </p>
          </div>

          {/* Discography */}
          <div>
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-white font-semibold">Discography</h2>
            </div>
            {!albums || albums.length === 0 ? (
              <p className="text-[#4a4b5a] text-sm">No albums yet.</p>
            ) : (
              <div className="grid grid-cols-2 gap-4">
                {albums.map((album, i) => (
                  <div key={album.id} className="bg-[#12131a] border border-[#2a2b38] rounded-lg overflow-hidden">
                    <div
                      className="h-40 flex items-center justify-center text-4xl"
                      style={{ background: `radial-gradient(circle, ${ALBUM_COLORS[i % ALBUM_COLORS.length]} 0%, #0d0e14 100%)` }}
                    >
                      🎵
                    </div>
                    <div className="p-4">
                      <div className="flex items-center justify-between mb-1">
                        <span className="text-white text-sm font-medium">{album.name}</span>
                        <span className="text-[#00e5ff] text-sm font-semibold">${album.price}</span>
                      </div>
                      <p className="text-[#4a4b5a] text-xs mb-3">
                        {album.release_date ? `Released ${new Date(album.release_date).getFullYear()}` : 'Unreleased'}
                        {album.genre_names.length > 0 && ` · ${album.genre_names.join(', ')}`}
                      </p>
                      <button
                        onClick={() => navigate(`/albums/${album.id}`)}
                        className="w-full border border-[#2a2b38] text-white text-xs py-2 rounded tracking-widest uppercase hover:border-[#00e5ff] hover:text-[#00e5ff] transition-colors"
                      >
                        View Details
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>

        {/* Right: Metrics + Events */}
        <div className="space-y-4">
          <div className="bg-[#12131a] border border-[#2a2b38] rounded-lg p-5">
            <p className="text-[10px] tracking-widest text-[#4a4b5a] uppercase mb-4">Real-Time Metrics</p>
            <div className="space-y-3 mb-4">
              <div>
                <div className="flex justify-between text-xs mb-1">
                  <span className="text-[#8a8b9a]">Signal Strength</span>
                  <span className="text-white">98.4%</span>
                </div>
                <div className="h-1 bg-[#1a1b24] rounded-full">
                  <div className="h-1 bg-[#00e5ff] rounded-full" style={{ width: '98.4%' }} />
                </div>
              </div>
              <div>
                <div className="flex justify-between text-xs mb-1">
                  <span className="text-[#8a8b9a]">Collector Density</span>
                  <span className="text-white">High</span>
                </div>
                <div className="h-1 bg-[#1a1b24] rounded-full">
                  <div className="h-1 bg-[#aa3bff] rounded-full" style={{ width: '75%' }} />
                </div>
              </div>
            </div>
            <div className="grid grid-cols-2 gap-3 pt-3 border-t border-[#2a2b38]">
              <div>
                <p className="text-[10px] tracking-widest text-[#4a4b5a] uppercase mb-1">Global Rank</p>
                <p className="text-white text-xl font-bold">#0{(artist.album_count % 9) + 1}</p>
              </div>
              <div>
                <p className="text-[10px] tracking-widest text-[#4a4b5a] uppercase mb-1">Albums</p>
                <p className="text-white text-xl font-bold">{artist.album_count}</p>
              </div>
            </div>
          </div>

          <div className="bg-[#12131a] border border-[#2a2b38] rounded-lg p-5">
            <p className="text-[10px] tracking-widest text-[#4a4b5a] uppercase mb-4">Upcoming Events</p>
            <div className="space-y-2">
              <div className="bg-[#1a1b24] rounded p-3">
                <p className="text-white text-xs font-medium">Void-Fest Virtual Mainstage</p>
                <p className="text-[#4a4b5a] text-[10px] mt-0.5">Oct 14 · 23:00 GMT</p>
              </div>
              <div className="bg-[#1a1b24] rounded p-3">
                <p className="text-white text-xs font-medium">Prism Protocol Release Party</p>
                <p className="text-[#4a4b5a] text-[10px] mt-0.5">Dec 02 · 20:00 GMT</p>
              </div>
            </div>
          </div>

          {!user && (
            <p className="text-[#4a4b5a] text-xs text-center">
              <button onClick={() => navigate('/login')} className="text-[#00e5ff] hover:underline">Login</button> to follow and get personalized recommendations
            </p>
          )}
        </div>
      </div>
    </div>
  )
}
