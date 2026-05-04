/* eslint-disable react-hooks/rules-of-hooks */
import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useQueryClient } from '@tanstack/react-query'
import { useAuth } from '../context/AuthContext'
import {
  usePlaylists, usePlaylist, useCreatePlaylist,
  useUpdatePlaylist, useDeletePlaylist, useRemoveTrackFromPlaylist,
  useAlbumTracks, useAlbums,
} from '../hooks/useApi'
import { useToast } from '../context/ToastContext'
import { playlistsApi } from '../api/client'
import type { PlaylistResponse, TrackInPlaylist } from '../api/client'

// ── Create form ───────────────────────────────────────────────────────────────

function CreatePlaylistForm() {
  const [name, setName] = useState('')
  const create = useCreatePlaylist()
  const { toast } = useToast()

  const submit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!name.trim()) return
    try {
      await create.mutateAsync({ name: name.trim(), track_ids: [] })
      setName('')
      toast('Playlist created', 'success')
    } catch {
      toast('Failed to create playlist')
    }
  }

  return (
    <form onSubmit={submit} className="flex gap-2">
      <input
        value={name}
        onChange={e => setName(e.target.value)}
        placeholder="New playlist name..."
        className="flex-1 bg-[#0d0e14] border border-[#2a2b38] rounded px-3 py-2 text-white text-sm placeholder-[#4a4b5a] outline-none focus:border-[#00e5ff] transition-colors"
      />
      <button
        type="submit"
        disabled={create.isPending || !name.trim()}
        className="bg-[#aa3bff] text-white px-4 py-2 rounded text-sm font-bold hover:bg-[#9030e0] transition-colors disabled:opacity-50"
      >
        {create.isPending ? '...' : '+ Create'}
      </button>
    </form>
  )
}

// ── Rename inline form ────────────────────────────────────────────────────────

function RenameForm({ playlist, onDone }: { playlist: PlaylistResponse; onDone: () => void }) {
  const [name, setName] = useState(playlist.name)
  const update = useUpdatePlaylist()
  const { toast } = useToast()

  const submit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!name.trim() || name.trim() === playlist.name) { onDone(); return }
    try {
      await update.mutateAsync({ id: playlist.id, data: { name: name.trim() } })
      toast('Playlist renamed', 'success')
      onDone()
    } catch {
      toast('Failed to rename playlist')
      onDone()
    }
  }

  return (
    <form onSubmit={submit} className="flex gap-1 flex-1" onClick={e => e.stopPropagation()}>
      <input
        autoFocus
        value={name}
        onChange={e => setName(e.target.value)}
        className="flex-1 bg-[#0d0e14] border border-[#aa3bff] rounded px-2 py-0.5 text-white text-sm outline-none min-w-0"
      />
      <button type="submit" className="text-[#00e5ff] text-xs px-1.5 hover:text-white flex-shrink-0">✓</button>
      <button type="button" onClick={onDone} className="text-[#4a4b5a] text-xs px-1 hover:text-white flex-shrink-0">✕</button>
    </form>
  )
}

// ── Add tracks panel ──────────────────────────────────────────────────────────

function AddTracksPanel({
  playlistId,
  existingTracks,
}: {
  playlistId: string
  existingTracks: TrackInPlaylist[]
}) {
  const { data: albumsData } = useAlbums({ page_size: 1000 })
  const albums = albumsData?.items ?? []
  const [selectedAlbum, setSelectedAlbum] = useState('')
  const { data: tracksData } = useAlbumTracks(selectedAlbum)
  const tracks = tracksData?.items ?? []
  const { toast } = useToast()
  const qc = useQueryClient()
  const existingIds = new Set(existingTracks.map(t => t.id))
  const [adding, setAdding] = useState<string | null>(null)

  const add = async (trackId: string, trackName: string) => {
    setAdding(trackId)
    try {
      await playlistsApi.addTrack(playlistId, trackId)
      qc.invalidateQueries({ queryKey: ['playlists', playlistId] })
      toast(`"${trackName}" added to playlist`, 'success')
    } catch (e: unknown) {
      const msg = (e as { response?: { data?: { detail?: string } } })?.response?.data?.detail
      toast(msg ?? 'Failed to add track')
    } finally {
      setAdding(null)
    }
  }

  return (
    <div className="bg-[#0d0e14] border border-[#2a2b38] rounded-lg p-4 mb-4">
      <p className="text-[10px] tracking-widest text-[#4a4b5a] uppercase mb-3">Add Tracks</p>
      <select
        value={selectedAlbum}
        onChange={e => setSelectedAlbum(e.target.value)}
        className="w-full bg-[#12131a] border border-[#2a2b38] rounded px-3 py-2 text-white text-sm outline-none focus:border-[#00e5ff] transition-colors mb-3"
      >
        <option value="">Select album to browse tracks...</option>
        {albums?.map(a => (
          <option key={a.id} value={a.id}>{a.name} — {a.artist_name}</option>
        ))}
      </select>

      {selectedAlbum && tracks?.length === 0 && (
        <p className="text-[#4a4b5a] text-xs text-center py-2">No tracks in this album.</p>
      )}

      {tracks && tracks.length > 0 && (
        <div className="space-y-1 max-h-52 overflow-y-auto pr-1">
          {tracks.map(t => {
            const already = existingIds.has(t.id)
            return (
              <div key={t.id} className="flex items-center gap-3 py-1.5 border-b border-[#1a1b24] last:border-0">
                <span className="text-white text-sm flex-1 truncate">{t.name}</span>
                <span className="text-[#4a4b5a] text-xs flex-shrink-0">{new Date(t.date).getFullYear()}</span>
                <button
                  disabled={already || adding === t.id}
                  onClick={() => add(t.id, t.name)}
                  className={`text-xs px-2 py-0.5 rounded border flex-shrink-0 transition-colors ${
                    already
                      ? 'border-[#2a2b38] text-[#4a4b5a] cursor-default'
                      : 'border-[#00e5ff] text-[#00e5ff] hover:bg-[#00e5ff]/10'
                  }`}
                >
                  {already ? '✓' : adding === t.id ? '...' : '+'}
                </button>
              </div>
            )
          })}
        </div>
      )}
    </div>
  )
}

// ── Playlist detail panel ─────────────────────────────────────────────────────

function PlaylistDetail({ playlistId }: { playlistId: string }) {
  const { data: playlist } = usePlaylist(playlistId)
  const removeTrack = useRemoveTrackFromPlaylist()
  const { toast } = useToast()
  const [showAdd, setShowAdd] = useState(false)

  const handleRemove = async (trackId: string, trackName: string) => {
    try {
      await removeTrack.mutateAsync({ playlist_id: playlistId, track_id: trackId })
      toast(`"${trackName}" removed`, 'success')
    } catch {
      toast('Failed to remove track')
    }
  }

  if (!playlist) {
    return <div className="bg-[#12131a] border border-[#2a2b38] rounded-lg p-5 animate-pulse h-48" />
  }

  return (
    <div className="bg-[#12131a] border border-[#2a2b38] rounded-lg p-5">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h2 className="text-white font-semibold">{playlist.name}</h2>
          <p className="text-[#4a4b5a] text-xs mt-0.5">
            {playlist.track_count} track{playlist.track_count !== 1 ? 's' : ''}
            {' · '}Created {new Date(playlist.created_at).toLocaleDateString()}
          </p>
        </div>
        <button
          onClick={() => setShowAdd(v => !v)}
          className={`text-xs px-3 py-1.5 rounded border transition-colors ${showAdd ? 'border-[#4a4b5a] text-[#4a4b5a]' : 'border-[#00e5ff] text-[#00e5ff] hover:bg-[#00e5ff]/10'}`}
        >
          {showAdd ? '✕ Close' : '+ Add Tracks'}
        </button>
      </div>

      {showAdd && (
        <AddTracksPanel
          playlistId={playlistId}
          existingTracks={playlist.tracks}
        />
      )}

      {playlist.tracks.length === 0 ? (
        <p className="text-[#4a4b5a] text-sm text-center py-8">
          No tracks yet.{' '}
          <button onClick={() => setShowAdd(true)} className="text-[#00e5ff] hover:underline">Add some →</button>
        </p>
      ) : (
        <div className="space-y-0">
          {playlist.tracks.map((t, i) => (
            <div key={t.id} className="flex items-center gap-3 py-2.5 border-b border-[#1a1b24] last:border-0 group">
              <span className="text-[#4a4b5a] text-xs w-5 text-right flex-shrink-0">{i + 1}</span>
              <div className="flex-1 min-w-0">
                <p className="text-white text-sm truncate">{t.name}</p>
                <p className="text-[#4a4b5a] text-xs truncate">{t.artist_name} · {t.album_name}</p>
              </div>
              <span className="text-[#4a4b5a] text-xs flex-shrink-0">{new Date(t.date).getFullYear()}</span>
              <button
                onClick={() => handleRemove(t.id, t.name)}
                className="text-[#4a4b5a] hover:text-red-400 text-xs opacity-0 group-hover:opacity-100 transition-all flex-shrink-0 w-4"
                title="Remove from playlist"
              >
                ✕
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

// ── Main page ─────────────────────────────────────────────────────────────────

export default function PlaylistsPage() {
  const { user } = useAuth()
  const navigate = useNavigate()
  const { toast } = useToast()

  if (user?.is_admin) {
    return (
      <div className="flex flex-col items-center justify-center h-[60vh] gap-4">
        <p className="text-[#8a8b9a] text-lg">Access Denied</p>
        <p className="text-[#4a4b5a] text-sm">Playlists are only available to regular users.</p>
        <button
          onClick={() => navigate('/')}
          className="border border-[#2a2b38] text-white px-6 py-2 rounded text-sm hover:border-[#00e5ff] transition-colors"
        >
          Return to Marketplace
        </button>
      </div>
    )
  }

  const { data: playlists, isLoading } = usePlaylists(!!user)
  const deletePlaylist = useDeletePlaylist()

  const [activeId, setActiveId] = useState<string | null>(null)
  const [renaming, setRenaming] = useState<string | null>(null)

  if (!user) {
    return (
      <div className="flex flex-col items-center justify-center h-[60vh] gap-4">
        <p className="text-[#8a8b9a]">Login to manage your playlists.</p>
        <button
          onClick={() => navigate('/login')}
          className="border border-[#00e5ff] text-[#00e5ff] px-6 py-2 rounded text-sm hover:bg-[#00e5ff]/10 transition-colors"
        >
          Login
        </button>
      </div>
    )
  }

  const handleDelete = async (id: string, name: string, e: React.MouseEvent) => {
    e.stopPropagation()
    if (!confirm(`Delete playlist "${name}"?`)) return
    try {
      await deletePlaylist.mutateAsync(id)
      if (activeId === id) setActiveId(null)
      toast(`"${name}" deleted`, 'success')
    } catch {
      toast('Failed to delete playlist')
    }
  }

  return (
    <div className="px-4 sm:px-8 pb-6 sm:pb-8">
      <div className="mb-6">
        <h1 className="text-white text-2xl font-semibold">Playlists</h1>
        <div className="h-0.5 w-8 bg-[#aa3bff] mt-1" />
      </div>

      <div className="mb-6">
        <CreatePlaylistForm />
      </div>

      {isLoading ? (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {Array.from({ length: 3 }).map((_, i) => (
            <div key={i} className="bg-[#12131a] border border-[#2a2b38] rounded-lg h-20 animate-pulse" />
          ))}
        </div>
      ) : !playlists || playlists.length === 0 ? (
        <div className="text-center py-16">
          <p className="text-[#4a4b5a] text-sm">No playlists yet. Create one above.</p>
        </div>
      ) : (
        <div className="grid grid-cols-3 gap-6">
          {/* Left: playlist list */}
          <div className="space-y-2">
            <p className="text-[10px] tracking-widest text-[#4a4b5a] uppercase mb-3">
              {playlists.length} Playlist{playlists.length !== 1 ? 's' : ''}
            </p>
            {playlists.map(pl => (
              <div
                key={pl.id}
                onClick={() => { setActiveId(pl.id); setRenaming(null) }}
                className={`bg-[#12131a] border rounded-lg p-3 cursor-pointer transition-colors ${
                  activeId === pl.id ? 'border-[#aa3bff]/60 bg-[#1a1b24]' : 'border-[#2a2b38] hover:border-[#aa3bff]/30'
                }`}
              >
                <div className="flex items-center gap-2 min-w-0">
                  <span className="text-[#aa3bff] flex-shrink-0">♫</span>
                  {renaming === pl.id ? (
                    <RenameForm playlist={pl} onDone={() => setRenaming(null)} />
                  ) : (
                    <span className="text-white text-sm font-medium flex-1 truncate">{pl.name}</span>
                  )}
                </div>
                {renaming !== pl.id && (
                  <div className="flex items-center justify-between mt-1.5">
                    <span className="text-[#4a4b5a] text-xs">
                      {pl.track_count} track{pl.track_count !== 1 ? 's' : ''}
                    </span>
                    <div className="flex gap-2" onClick={e => e.stopPropagation()}>
                      <button
                        onClick={e => { e.stopPropagation(); setRenaming(pl.id) }}
                        className="text-[#4a4b5a] hover:text-white text-xs transition-colors"
                        title="Rename"
                      >✏</button>
                      <button
                        onClick={e => handleDelete(pl.id, pl.name, e)}
                        className="text-[#4a4b5a] hover:text-red-400 text-xs transition-colors"
                        title="Delete"
                      >🗑</button>
                    </div>
                  </div>
                )}
              </div>
            ))}
          </div>

          {/* Right: detail */}
          <div className="col-span-2">
            {activeId ? (
              <PlaylistDetail playlistId={activeId} />
            ) : (
              <div className="bg-[#12131a] border border-[#2a2b38] rounded-lg flex items-center justify-center min-h-[200px]">
                <p className="text-[#4a4b5a] text-sm">← Select a playlist</p>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  )
}
