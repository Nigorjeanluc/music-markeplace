import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { useLibrary, useMyRatings, usePlaylists } from '../hooks/useApi'

export default function ProfilePage() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()
  const [tab, setTab] = useState<'overview' | 'ratings' | 'playlists'>('overview')

  const { data: libraryData } = useLibrary(!!user)
  const { data: ratingsData } = useMyRatings(!!user)
  const { data: playlists } = usePlaylists(!!user)
  const library = libraryData?.items ?? []
  const ratings = ratingsData?.items ?? []

  if (!user) {
    return (
      <div className="flex flex-col items-center justify-center h-[60vh] gap-4">
        <p className="text-[#8a8b9a]">You need to be logged in to view your profile.</p>
        <button onClick={() => navigate('/login')} className="border border-[#00e5ff] text-[#00e5ff] px-6 py-2 rounded text-sm hover:bg-[#00e5ff]/10 transition-colors">
          Login
        </button>
      </div>
    )
  }

  const totalSpent = library.reduce((s, p) => s + p.amount_paid, 0)
  const avgRating = ratings.length > 0
    ? ratings.reduce((s, r) => s + r.user_rating, 0) / ratings.length
    : null

  return (
    <div className="px-8 py-8 max-w-4xl">
      {/* Header */}
      <div className="flex items-center gap-6 mb-8">
        <div className="w-20 h-20 rounded-full bg-[#1a1b24] border-2 border-[#2a2b38] flex items-center justify-center text-3xl font-bold text-[#00e5ff]">
          {user.username[0].toUpperCase()}
        </div>
        <div className="flex-1">
          <h1 className="text-white text-2xl font-bold">{user.username}</h1>
          <p className="text-[#4a4b5a] text-sm mt-0.5">{user.email}</p>
          <div className="flex items-center gap-2 mt-2">
            <span className={`text-[10px] px-2 py-0.5 rounded border tracking-widest uppercase ${user.is_admin ? 'border-[#aa3bff] text-[#aa3bff]' : 'border-[#2a2b38] text-[#8a8b9a]'}`}>
              {user.is_admin ? 'Admin' : 'Member'}
            </span>
            <span className="text-[10px] text-[#4a4b5a]">
              Joined {new Date(user.created_at).toLocaleDateString('en-US', { year: 'numeric', month: 'long' })}
            </span>
          </div>
        </div>
        <button
          onClick={() => { logout(); navigate('/login') }}
          className="border border-[#2a2b38] text-[#8a8b9a] text-xs px-4 py-2 rounded hover:border-red-500/50 hover:text-red-400 transition-colors"
        >
          Logout
        </button>
      </div>

      {/* Stats row */}
      <div className="grid grid-cols-4 gap-4 mb-8">
        {[
          { label: 'Albums Owned', value: library.length, color: 'text-[#00e5ff]' },
          { label: 'Total Spent', value: `$${totalSpent.toFixed(2)}`, color: 'text-[#aa3bff]' },
          { label: 'Ratings Given', value: ratings.length, color: 'text-[#00e5ff]' },
          { label: 'Playlists', value: playlists?.length ?? 0, color: 'text-[#aa3bff]' },
        ].map(s => (
          <div key={s.label} className="bg-[#12131a] border border-[#2a2b38] rounded-lg p-4">
            <p className={`text-2xl font-bold ${s.color}`}>{s.value}</p>
            <p className="text-[#4a4b5a] text-xs tracking-widest uppercase mt-1">{s.label}</p>
          </div>
        ))}
      </div>

      {/* Tabs */}
      <div className="flex gap-1 mb-6 bg-[#12131a] border border-[#2a2b38] rounded-lg p-1 w-fit">
        {(['overview', 'ratings', 'playlists'] as const).map(t => (
          <button
            key={t}
            onClick={() => setTab(t)}
            className={`px-4 py-1.5 rounded text-xs tracking-widest uppercase transition-colors ${tab === t ? 'bg-[#1a1b24] text-[#00e5ff]' : 'text-[#4a4b5a] hover:text-white'}`}
          >
            {t}
          </button>
        ))}
      </div>

      {/* Overview tab */}
      {tab === 'overview' && (
        <div className="space-y-4">
          <div className="bg-[#12131a] border border-[#2a2b38] rounded-lg p-5">
            <p className="text-[10px] tracking-widest text-[#4a4b5a] uppercase mb-4">Account Details</p>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <p className="text-[10px] tracking-widest text-[#4a4b5a] uppercase mb-1">Username</p>
                <p className="text-white text-sm">{user.username}</p>
              </div>
              <div>
                <p className="text-[10px] tracking-widest text-[#4a4b5a] uppercase mb-1">Email</p>
                <p className="text-white text-sm">{user.email}</p>
              </div>
              <div>
                <p className="text-[10px] tracking-widest text-[#4a4b5a] uppercase mb-1">Role</p>
                <p className="text-white text-sm">{user.is_admin ? 'Administrator' : 'Member'}</p>
              </div>
              <div>
                <p className="text-[10px] tracking-widest text-[#4a4b5a] uppercase mb-1">Status</p>
                <div className="flex items-center gap-1.5">
                  <span className="w-1.5 h-1.5 rounded-full bg-[#00e5ff]" />
                  <p className="text-white text-sm">{user.is_active ? 'Active' : 'Inactive'}</p>
                </div>
              </div>
              {avgRating != null && (
                <div>
                  <p className="text-[10px] tracking-widest text-[#4a4b5a] uppercase mb-1">Avg Rating Given</p>
                  <p className="text-white text-sm">{avgRating.toFixed(1)} ★</p>
                </div>
              )}
            </div>
          </div>

          {/* Recent purchases */}
          {library.length > 0 && (
            <div className="bg-[#12131a] border border-[#2a2b38] rounded-lg p-5">
              <div className="flex items-center justify-between mb-4">
                <p className="text-[10px] tracking-widest text-[#4a4b5a] uppercase">Recent Purchases</p>
                <button onClick={() => navigate('/library')} className="text-[#00e5ff] text-xs hover:underline">View Library →</button>
              </div>
              <div className="space-y-2">
                {library.slice(0, 4).map(p => (
                  <div
                    key={p.id}
                    onClick={() => navigate(`/albums/${p.album_id}`)}
                    className="flex items-center justify-between py-2 border-b border-[#1a1b24] last:border-0 cursor-pointer hover:text-white transition-colors"
                  >
                    <div>
                      <p className="text-white text-sm">{p.album_name}</p>
                      <p className="text-[#4a4b5a] text-xs">{p.artist_name}</p>
                    </div>
                    <div className="text-right">
                      <p className="text-[#00e5ff] text-xs">${p.amount_paid.toFixed(2)}</p>
                      {p.user_rating && <p className="text-[#4a4b5a] text-xs">{'★'.repeat(p.user_rating)}</p>}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {/* Ratings tab */}
      {tab === 'ratings' && (
        <div className="bg-[#12131a] border border-[#2a2b38] rounded-lg overflow-hidden">
          {ratings.length === 0 ? (
            <div className="p-8 text-center">
              <p className="text-[#4a4b5a] text-sm">No ratings yet.</p>
              <button onClick={() => navigate('/')} className="text-[#00e5ff] text-xs mt-2 hover:underline">Browse albums →</button>
            </div>
          ) : (
            <>
              <div className="grid grid-cols-4 gap-4 px-5 py-3 border-b border-[#2a2b38] text-[10px] tracking-widest text-[#4a4b5a] uppercase">
                <span className="col-span-2">Album</span>
                <span>Your Rating</span>
                <span>Avg Rating</span>
              </div>
              {ratings.map(r => (
                <div key={r.album_id} className="grid grid-cols-4 gap-4 px-5 py-3 border-b border-[#2a2b38] last:border-0 items-center hover:bg-[#1a1b24] transition-colors">
                  <div className="col-span-2">
                    <p className="text-white text-sm">{r.album_name}</p>
                    <p className="text-[#4a4b5a] text-xs">{new Date(r.created_at).toLocaleDateString()}</p>
                  </div>
                  <p className="text-[#00e5ff] text-sm">{'★'.repeat(r.user_rating)}{'☆'.repeat(5 - r.user_rating)}</p>
                  <p className="text-[#8a8b9a] text-sm">{r.avg_rating != null ? `${r.avg_rating.toFixed(1)} ★` : '—'}</p>
                </div>
              ))}
            </>
          )}
        </div>
      )}

      {/* Playlists tab */}
      {tab === 'playlists' && (
        <div>
          <div className="flex items-center justify-between mb-4">
            <p className="text-[#4a4b5a] text-xs">{playlists?.length ?? 0} playlist{playlists?.length !== 1 ? 's' : ''}</p>
            <button onClick={() => navigate('/playlists')} className="text-[#00e5ff] text-xs hover:underline">Manage Playlists →</button>
          </div>
          {playlists?.length === 0 ? (
            <div className="bg-[#12131a] border border-[#2a2b38] rounded-lg p-8 text-center">
              <p className="text-[#4a4b5a] text-sm">No playlists yet.</p>
              <button onClick={() => navigate('/playlists')} className="text-[#00e5ff] text-xs mt-2 hover:underline">Create one →</button>
            </div>
          ) : (
            <div className="grid grid-cols-2 gap-3">
              {playlists?.map(pl => (
                <div
                  key={pl.id}
                  onClick={() => navigate('/playlists')}
                  className="bg-[#12131a] border border-[#2a2b38] rounded-lg p-4 cursor-pointer hover:border-[#aa3bff]/40 transition-colors"
                >
                  <p className="text-white text-sm font-medium truncate">{pl.name}</p>
                  <p className="text-[#4a4b5a] text-xs mt-1">{pl.track_count} track{pl.track_count !== 1 ? 's' : ''}</p>
                  <p className="text-[#4a4b5a] text-[10px] mt-1">{new Date(pl.created_at).toLocaleDateString()}</p>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  )
}
