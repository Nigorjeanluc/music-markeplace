import { useParams, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { useArtist, useAlbums } from '../hooks/useApi'

const ALBUM_COLORS = ['#0a1a2e', '#1a0a2e', '#0a2e1a', '#1a1a0a']

export default function ArtistDetailPage() {
  const { id } = useParams<{ id: string }>()
  const { user } = useAuth()
  const navigate = useNavigate()
  const { data: artist, isLoading, isError } = useArtist(id!)
  const { data: albumsData } = useAlbums({ artist_id: id })
  const albums = albumsData?.items ?? []

  if (isLoading) {
    return (
      <div className="animate-pulse">
        <div className="h-48 sm:h-60 md:h-72 bg-[#1a1b24]" />
        <div className="px-8 pb-6 pt-2 space-y-4">
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

  // Derive real stats from discography
  const ratedAlbums = albums.filter(a => a.rating != null)
  const avgRating = ratedAlbums.length > 0
    ? ratedAlbums.reduce((s, a) => s + a.rating!, 0) / ratedAlbums.length
    : null
  const allGenres = [...new Set(albums.flatMap(a => a.genre_names))]
  const totalValue = albums.reduce((s, a) => s + a.price, 0)

  return (
    <div>
      {/* Hero */}
      <div
        className="relative h-72 flex items-end overflow-hidden"
        style={artist.photo_url
          ? { backgroundImage: `url(${artist.photo_url})`, backgroundSize: 'cover', backgroundPosition: 'center top' }
          : { background: 'linear-gradient(180deg, #1a0a2e 0%, #0d0e14 100%)' }
        }
      >
        {artist.photo_url && <div className="absolute inset-0 bg-gradient-to-t from-[#0d0e14] via-[#0d0e14]/60 to-transparent" />}
        {!artist.photo_url && (
          <div className="absolute inset-0 opacity-10"
            style={{ backgroundImage: 'repeating-linear-gradient(45deg, #aa3bff11 0px, #aa3bff11 1px, transparent 1px, transparent 20px)' }} />
        )}
        <div className="relative px-8 pb-6 w-full flex items-end justify-between">
          <div className="flex items-end gap-5">
            <div className="w-20 h-20 rounded-full bg-[#1a1b24] border-2 border-[#2a2b38] flex items-center justify-center text-3xl overflow-hidden flex-shrink-0">
              {artist.photo_url
                ? <img src={artist.photo_url} alt={artist.performing_name} className="w-full h-full object-cover" />
                : '🎤'
              }
            </div>
            <div>
              <p className="text-[10px] tracking-[0.3em] text-[#00e5ff] uppercase mb-1">Artist</p>
              <h1 className="text-white text-3xl font-bold mb-1">{artist.performing_name}</h1>
              <p className="text-[#8a8b9a] text-sm">
                {artist.album_count} {artist.album_count === 1 ? 'Album' : 'Albums'}
                {' · '}Born {new Date(artist.date_of_birth).getFullYear()}
              </p>
            </div>
          </div>
        </div>
      </div>

      <div className="px-8 pb-6 pt-2 grid grid-cols-3 gap-6">
        {/* Left: Bio + Discography */}
        <div className="col-span-2 space-y-6">
          <div className="bg-[#12131a] border border-[#2a2b38] rounded-lg p-6">
            <div className="flex items-center gap-2 mb-5">
              <div className="w-6 h-0.5 bg-[#00e5ff]" />
              <span className="text-white text-sm font-medium">Bio</span>
            </div>
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
              <div>
                <p className="text-[10px] tracking-widest text-[#4a4b5a] uppercase mb-1">Legal Identity</p>
                <p className="text-white text-sm">{artist.real_name}</p>
              </div>
              <div>
                <p className="text-[10px] tracking-widest text-[#4a4b5a] uppercase mb-1">Date of Birth</p>
                <p className="text-white text-sm">{new Date(artist.date_of_birth).toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' })}</p>
              </div>
              {allGenres.length > 0 && (
                <div className="col-span-2">
                  <p className="text-[10px] tracking-widest text-[#4a4b5a] uppercase mb-2">Genres</p>
                  <div className="flex flex-wrap gap-2">
                    {allGenres.map(g => (
                      <span key={g} className="border border-[#2a2b38] text-[#8a8b9a] text-[10px] px-2 py-0.5 rounded tracking-wider">{g}</span>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Discography */}
          <div>
            <h2 className="text-white font-semibold mb-4">Discography</h2>
            {!albumsData || albums.length === 0 ? (
              <p className="text-[#4a4b5a] text-sm">No albums yet.</p>
            ) : (
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
                {albums.map((album, i) => (
                  <div
                    key={album.id}
                    onClick={() => navigate(`/albums/${album.id}`)}
                    className="bg-[#12131a] border border-[#2a2b38] rounded-lg overflow-hidden cursor-pointer hover:border-[#00e5ff]/40 transition-colors"
                  >
                    <div
                      className="h-40 flex items-center justify-center text-4xl"
                      style={album.cover_image_url
                        ? { backgroundImage: `url(${album.cover_image_url})`, backgroundSize: 'cover', backgroundPosition: 'center' }
                        : { background: `radial-gradient(circle, ${ALBUM_COLORS[i % ALBUM_COLORS.length]} 0%, #0d0e14 100%)` }
                      }
                    >
                      {!album.cover_image_url && '🎵'}
                    </div>
                    <div className="p-4">
                      <div className="flex items-center justify-between mb-1">
                        <span className="text-white text-sm font-medium truncate">{album.name}</span>
                        <span className="text-[#00e5ff] text-sm font-semibold flex-shrink-0 ml-2">${album.price}</span>
                      </div>
                      <p className="text-[#4a4b5a] text-xs mb-1">
                        {album.release_date ? `Released ${new Date(album.release_date).getFullYear()}` : 'Unreleased'}
                        {album.genre_names.length > 0 && ` · ${album.genre_names.join(', ')}`}
                      </p>
                      {album.rating != null && (
                        <p className="text-[#00e5ff] text-xs">★ {album.rating.toFixed(1)}</p>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>

        {/* Right: Real stats */}
        <div className="space-y-4">
          <div className="bg-[#12131a] border border-[#2a2b38] rounded-lg p-5">
            <p className="text-[10px] tracking-widest text-[#4a4b5a] uppercase mb-4">Artist Stats</p>
            <div className="space-y-4">
              <div>
                <p className="text-[10px] tracking-widest text-[#4a4b5a] uppercase mb-1">Albums</p>
                <p className="text-white text-2xl font-bold">{artist.album_count}</p>
              </div>
              <div>
                <p className="text-[10px] tracking-widest text-[#4a4b5a] uppercase mb-1">Avg Rating</p>
                {avgRating != null ? (
                  <div className="flex items-center gap-2">
                    <p className="text-white text-2xl font-bold">{avgRating.toFixed(1)}</p>
                    <span className="text-[#00e5ff]">★</span>
                    <span className="text-[#4a4b5a] text-xs">({ratedAlbums.length} rated)</span>
                  </div>
                ) : (
                  <p className="text-[#4a4b5a] text-sm">No ratings yet</p>
                )}
              </div>
              {albumsData && albums.length > 0 && (
                <div>
                  <p className="text-[10px] tracking-widest text-[#4a4b5a] uppercase mb-1">Catalog Value</p>
                  <p className="text-white text-2xl font-bold">${totalValue.toFixed(2)}</p>
                </div>
              )}
              {albumsData && albums.length > 0 && (
                <div>
                  <p className="text-[10px] tracking-widest text-[#4a4b5a] uppercase mb-2">Rating Distribution</p>
                  <div className="h-1 bg-[#1a1b24] rounded-full">
                    <div
                      className="h-1 bg-[#00e5ff] rounded-full transition-all"
                      style={{ width: avgRating != null ? `${(avgRating / 5) * 100}%` : '0%' }}
                    />
                  </div>
                </div>
              )}
            </div>
          </div>

          {!user && (
            <p className="text-[#4a4b5a] text-xs text-center">
              <button onClick={() => navigate('/login')} className="text-[#00e5ff] hover:underline">Login</button> to purchase albums from this artist
            </p>
          )}
        </div>
      </div>
    </div>
  )
}
