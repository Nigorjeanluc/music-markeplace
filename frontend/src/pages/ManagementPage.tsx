import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Formik, Form } from 'formik'
import * as Yup from 'yup'
import { useAuth } from '../context/AuthContext'
import {
  useArtists, useAlbums, useCreateArtist, useUpdateArtist, useDeleteArtist,
  useCreateAlbum, useUpdateAlbum, useDeleteAlbum, useGenres,
  useCreateGenre, useUpdateGenre, useDeleteGenre,
  useTracks, useCreateTrack, useUpdateTrack, useDeleteTrack,
} from '../hooks/useApi'
import type { ArtistResponse, AlbumResponse, GenreResponse, TrackResponse } from '../api/client'
import { FormField, SelectField } from '../components/FormField'

const artistSchema = Yup.object({
  real_name: Yup.string().min(2, 'Min 2 chars').required('Required'),
  performing_name: Yup.string().min(2, 'Min 2 chars').required('Required'),
  date_of_birth: Yup.string().required('Required'),
})

const albumSchema = Yup.object({
  name: Yup.string().min(1, 'Required').required('Required'),
  price: Yup.number().typeError('Must be a number').min(0, 'Must be ≥ 0').required('Required'),
  artist_id: Yup.string().required('Select an artist'),
  release_date: Yup.string(),
  genre_ids: Yup.array().of(Yup.string()),
})

function Modal({ title, onClose, children }: { title: string; onClose: () => void; children: React.ReactNode }) {
  return (
    <div className="fixed inset-0 bg-black/70 flex items-center justify-center z-50 p-4">
      <div className="bg-[#12131a] border border-[#2a2b38] rounded-xl w-full max-w-md">
        <div className="flex items-center justify-between px-6 py-4 border-b border-[#2a2b38]">
          <h2 className="text-white font-semibold text-sm tracking-wide">{title}</h2>
          <button onClick={onClose} className="text-[#4a4b5a] hover:text-white text-lg leading-none">✕</button>
        </div>
        <div className="px-6 py-5">{children}</div>
      </div>
    </div>
  )
}

function ArtistModal({ artist, onClose }: { artist?: ArtistResponse; onClose: () => void }) {
  const createArtist = useCreateArtist()
  const updateArtist = useUpdateArtist()
  const [apiError, setApiError] = useState('')

  return (
    <Modal title={artist ? 'Edit Artist' : 'New Artist'} onClose={onClose}>
      <Formik
        initialValues={{
          real_name: artist?.real_name ?? '',
          performing_name: artist?.performing_name ?? '',
          date_of_birth: artist?.date_of_birth ?? '',
        }}
        validationSchema={artistSchema}
        onSubmit={async (values, { setSubmitting }) => {
          setApiError('')
          try {
            if (artist) {
              await updateArtist.mutateAsync({ id: artist.id, data: values })
            } else {
              await createArtist.mutateAsync(values)
            }
            onClose()
          } catch (e: unknown) {
            setApiError((e as { response?: { data?: { detail?: string } } })?.response?.data?.detail ?? 'Something went wrong')
          } finally {
            setSubmitting(false)
          }
        }}
      >
        {({ isSubmitting }) => (
          <Form className="space-y-4">
            <FormField name="real_name" label="Real Name" placeholder="Elena Vance-Kurayami" />
            <FormField name="performing_name" label="Performing Name" placeholder="NEON_VALKYRIE" />
            <FormField name="date_of_birth" label="Date of Birth" type="date" />
            {apiError && <p className="text-red-400 text-xs">{apiError}</p>}
            <div className="flex gap-3 pt-2">
              <button type="button" onClick={onClose} className="flex-1 border border-[#2a2b38] text-[#8a8b9a] py-2.5 rounded text-sm hover:border-white hover:text-white transition-colors">Cancel</button>
              <button type="submit" disabled={isSubmitting} className="flex-1 bg-[#00e5ff] text-[#0d0e14] py-2.5 rounded text-sm font-bold tracking-wide hover:bg-[#00b8cc] transition-colors disabled:opacity-50">
                {isSubmitting ? 'Saving...' : artist ? 'Update' : 'Create'}
              </button>
            </div>
          </Form>
        )}
      </Formik>
    </Modal>
  )
}

function AlbumModal({ album, onClose }: { album?: AlbumResponse; onClose: () => void }) {
  const createAlbum = useCreateAlbum()
  const updateAlbum = useUpdateAlbum()
  const { data: artists } = useArtists()
  const { data: genres } = useGenres()
  const [apiError, setApiError] = useState('')

  return (
    <Modal title={album ? 'Edit Album' : 'New Album'} onClose={onClose}>
      <Formik
        initialValues={{
          name: album?.name ?? '',
          price: album?.price?.toString() ?? '',
          artist_id: album?.artist_id ?? '',
          release_date: album?.release_date ?? '',
          genre_ids: [] as string[],
        }}
        validationSchema={albumSchema}
        onSubmit={async (values, { setSubmitting }) => {
          setApiError('')
          try {
            const price = parseFloat(values.price as unknown as string)
            const release_date = values.release_date || undefined
            if (album) {
              await updateAlbum.mutateAsync({ id: album.id, data: { name: values.name, price, genre_ids: values.genre_ids, release_date } })
            } else {
              await createAlbum.mutateAsync({ name: values.name, price, artist_id: values.artist_id, genre_ids: values.genre_ids, release_date })
            }
            onClose()
          } catch (e: unknown) {
            setApiError((e as { response?: { data?: { detail?: string } } })?.response?.data?.detail ?? 'Something went wrong')
          } finally {
            setSubmitting(false)
          }
        }}
      >
        {({ isSubmitting, values, setFieldValue }) => (
          <Form className="space-y-4">
            <FormField name="name" label="Album Name" placeholder="Prism Protocol" />
            <FormField name="price" label="Price (USD)" type="number" placeholder="19.99" />
            {!album && (
              <SelectField name="artist_id" label="Artist">
                <option value="">Select artist...</option>
                {artists?.map(a => <option key={a.id} value={a.id}>{a.performing_name}</option>)}
              </SelectField>
            )}
            <FormField name="release_date" label="Release Date (optional)" type="date" />
            {genres && genres.length > 0 && (
              <div>
                <label className="block text-[10px] tracking-widest text-[#8a8b9a] uppercase mb-2">Genres</label>
                <div className="flex flex-wrap gap-2">
                  {genres.map(g => {
                    const checked = values.genre_ids.includes(g.id)
                    return (
                      <button key={g.id} type="button"
                        onClick={() => setFieldValue('genre_ids', checked ? values.genre_ids.filter(id => id !== g.id) : [...values.genre_ids, g.id])}
                        className={`text-xs px-3 py-1 rounded border transition-colors ${checked ? 'border-[#00e5ff] text-[#00e5ff] bg-[#00e5ff]/10' : 'border-[#2a2b38] text-[#8a8b9a] hover:border-[#4a4b5a]'}`}
                      >
                        {g.name}
                      </button>
                    )
                  })}
                </div>
              </div>
            )}
            {apiError && <p className="text-red-400 text-xs">{apiError}</p>}
            <div className="flex gap-3 pt-2">
              <button type="button" onClick={onClose} className="flex-1 border border-[#2a2b38] text-[#8a8b9a] py-2.5 rounded text-sm hover:border-white hover:text-white transition-colors">Cancel</button>
              <button type="submit" disabled={isSubmitting} className="flex-1 bg-[#00e5ff] text-[#0d0e14] py-2.5 rounded text-sm font-bold tracking-wide hover:bg-[#00b8cc] transition-colors disabled:opacity-50">
                {isSubmitting ? 'Saving...' : album ? 'Update' : 'Create'}
              </button>
            </div>
          </Form>
        )}
      </Formik>
    </Modal>
  )
}

const GENRE_LABELS = ['SYNTHWAVE', 'GLITCH-HOP', 'AMBIENT', 'CYBER-NOIR', 'INDUSTRIAL', 'ELECTRONIC']
const STATUS_CYCLE = ['Verified', 'Verified', 'Pending', 'Verified', 'Pending', 'Verified']
const COLORS = ['#0a1a2e', '#1a0a2e', '#0a2e1a', '#1a1a0a', '#2e0a1a', '#0a0a2e']

const genreSchema = Yup.object({
  name: Yup.string().min(1, 'Required').required('Required'),
  description: Yup.string(),
})

const trackSchema = Yup.object({
  name: Yup.string().min(1, 'Required').required('Required'),
  date: Yup.string().required('Required'),
  album_id: Yup.string().required('Select an album'),
})

function GenreModal({ genre, onClose }: { genre?: GenreResponse; onClose: () => void }) {
  const createGenre = useCreateGenre()
  const updateGenre = useUpdateGenre()
  const [apiError, setApiError] = useState('')

  return (
    <Modal title={genre ? 'Edit Genre' : 'New Genre'} onClose={onClose}>
      <Formik
        initialValues={{ name: genre?.name ?? '', description: genre?.description ?? '' }}
        validationSchema={genreSchema}
        onSubmit={async (values, { setSubmitting }) => {
          setApiError('')
          try {
            if (genre) {
              await updateGenre.mutateAsync({ id: genre.id, data: values })
            } else {
              await createGenre.mutateAsync(values)
            }
            onClose()
          } catch (e: unknown) {
            setApiError((e as { response?: { data?: { detail?: string } } })?.response?.data?.detail ?? 'Something went wrong')
          } finally {
            setSubmitting(false)
          }
        }}
      >
        {({ isSubmitting }) => (
          <Form className="space-y-4">
            <FormField name="name" label="Genre Name" placeholder="Synthwave" />
            <FormField name="description" label="Description (optional)" placeholder="Electronic retro-futuristic sounds" />
            {apiError && <p className="text-red-400 text-xs">{apiError}</p>}
            <div className="flex gap-3 pt-2">
              <button type="button" onClick={onClose} className="flex-1 border border-[#2a2b38] text-[#8a8b9a] py-2.5 rounded text-sm hover:border-white hover:text-white transition-colors">Cancel</button>
              <button type="submit" disabled={isSubmitting} className="flex-1 bg-[#00e5ff] text-[#0d0e14] py-2.5 rounded text-sm font-bold tracking-wide hover:bg-[#00b8cc] transition-colors disabled:opacity-50">
                {isSubmitting ? 'Saving...' : genre ? 'Update' : 'Create'}
              </button>
            </div>
          </Form>
        )}
      </Formik>
    </Modal>
  )
}

function TrackModal({ track, onClose }: { track?: TrackResponse; onClose: () => void }) {
  const createTrack = useCreateTrack()
  const updateTrack = useUpdateTrack()
  const { data: albums } = useAlbums()
  const [apiError, setApiError] = useState('')

  return (
    <Modal title={track ? 'Edit Track' : 'New Track'} onClose={onClose}>
      <Formik
        initialValues={{
          name: track?.name ?? '',
          date: track?.date ?? '',
          album_id: track?.album_id ?? '',
        }}
        validationSchema={trackSchema}
        onSubmit={async (values, { setSubmitting }) => {
          setApiError('')
          try {
            if (track) {
              await updateTrack.mutateAsync({ id: track.id, data: values })
            } else {
              await createTrack.mutateAsync(values)
            }
            onClose()
          } catch (e: unknown) {
            setApiError((e as { response?: { data?: { detail?: string } } })?.response?.data?.detail ?? 'Something went wrong')
          } finally {
            setSubmitting(false)
          }
        }}
      >
        {({ isSubmitting }) => (
          <Form className="space-y-4">
            <FormField name="name" label="Track Name" placeholder="Neon Drift" />
            <FormField name="date" label="Release Date" type="date" />
            <SelectField name="album_id" label="Album">
              <option value="">Select album...</option>
              {albums?.map(a => <option key={a.id} value={a.id}>{a.name} — {a.artist_name}</option>)}
            </SelectField>
            {apiError && <p className="text-red-400 text-xs">{apiError}</p>}
            <div className="flex gap-3 pt-2">
              <button type="button" onClick={onClose} className="flex-1 border border-[#2a2b38] text-[#8a8b9a] py-2.5 rounded text-sm hover:border-white hover:text-white transition-colors">Cancel</button>
              <button type="submit" disabled={isSubmitting} className="flex-1 bg-[#00e5ff] text-[#0d0e14] py-2.5 rounded text-sm font-bold tracking-wide hover:bg-[#00b8cc] transition-colors disabled:opacity-50">
                {isSubmitting ? 'Saving...' : track ? 'Update' : 'Create'}
              </button>
            </div>
          </Form>
        )}
      </Formik>
    </Modal>
  )
}

export default function ManagementPage() {
  const { user } = useAuth()
  const navigate = useNavigate()
  const { data: artists, isLoading: artistsLoading } = useArtists()
  const { data: albums, isLoading: albumsLoading } = useAlbums()
  const { data: genres, isLoading: genresLoading } = useGenres()
  const { data: tracks, isLoading: tracksLoading } = useTracks()
  const deleteArtist = useDeleteArtist()
  const deleteAlbum = useDeleteAlbum()
  const deleteGenre = useDeleteGenre()
  const deleteTrack = useDeleteTrack()

  const [artistModal, setArtistModal] = useState<{ open: boolean; artist?: ArtistResponse }>({ open: false })
  const [albumModal, setAlbumModal] = useState<{ open: boolean; album?: AlbumResponse }>({ open: false })
  const [genreModal, setGenreModal] = useState<{ open: boolean; genre?: GenreResponse }>({ open: false })
  const [trackModal, setTrackModal] = useState<{ open: boolean; track?: TrackResponse }>({ open: false })

  if (!user?.is_admin) {
    return (
      <div className="flex flex-col items-center justify-center h-[60vh] gap-4">
        <p className="text-[#8a8b9a] text-lg">Access Denied</p>
        <p className="text-[#4a4b5a] text-sm">This area requires administrator privileges.</p>
        <button onClick={() => navigate('/')} className="border border-[#2a2b38] text-white px-6 py-2 rounded text-sm hover:border-[#00e5ff] transition-colors">
          Return to Marketplace
        </button>
      </div>
    )
  }

  const stats = [
    { label: 'Total Artists', value: artistsLoading ? '…' : String(artists?.length ?? 0), change: '+12%', icon: '👤' },
    { label: 'Total Albums', value: albumsLoading ? '…' : String(albums?.length ?? 0), change: '+5.4%', icon: '◎' },
    { label: 'Total Genres', value: genresLoading ? '…' : String(genres?.length ?? 0), change: '', icon: '🎶' },
    { label: 'Total Tracks', value: tracksLoading ? '…' : String(tracks?.length ?? 0), change: '', icon: '📀' },
  ]

  return (
    <div className="px-8 py-8">
      {artistModal.open && <ArtistModal artist={artistModal.artist} onClose={() => setArtistModal({ open: false })} />}
      {albumModal.open && <AlbumModal album={albumModal.album} onClose={() => setAlbumModal({ open: false })} />}
      {genreModal.open && <GenreModal genre={genreModal.genre} onClose={() => setGenreModal({ open: false })} />}
      {trackModal.open && <TrackModal track={trackModal.track} onClose={() => setTrackModal({ open: false })} />}

      <h1 className="text-white text-4xl font-bold mb-2">Admin Management</h1>
      <p className="text-[#8a8b9a] text-sm mb-8 max-w-xl">
        System-level orchestration of the Music Marketplace ecosystem. Monitor performance metrics
        and execute database modifications via the secure administrative layer.
      </p>

      {/* Stats */}
      <div className="grid grid-cols-4 gap-4 mb-10">
        {stats.map(s => (
          <div key={s.label} className="bg-[#12131a] border border-[#2a2b38] rounded-lg p-5">
            <div className="flex items-start justify-between mb-3">
              <span className="text-2xl">{s.icon}</span>
              <span className="text-[#00e5ff] text-xs">{s.change}</span>
            </div>
            <p className="text-white text-3xl font-bold mb-1">{s.value}</p>
            <p className="text-[#4a4b5a] text-xs tracking-wider uppercase">{s.label}</p>
          </div>
        ))}
      </div>

      {/* Manage Artists */}
      <div className="mb-10">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h2 className="text-white text-2xl font-semibold">Manage Artists</h2>
            <p className="text-[#4a4b5a] text-xs mt-0.5">Registry of verified Music Marketplace creators</p>
          </div>
          <button
            onClick={() => setArtistModal({ open: true })}
            className="bg-[#00e5ff] text-[#0d0e14] px-4 py-2.5 rounded text-xs font-bold tracking-widest uppercase hover:bg-[#00b8cc] transition-colors"
          >
            ⊕ Add New Artist
          </button>
        </div>

        <div className="bg-[#12131a] border border-[#2a2b38] rounded-lg overflow-hidden">
          <div className="grid grid-cols-6 gap-4 px-5 py-3 border-b border-[#2a2b38] text-[10px] tracking-widest text-[#4a4b5a] uppercase">
            <span className="col-span-2">Artist Node</span>
            <span>Genre Class</span>
            <span>Inventory</span>
            <span>System Status</span>
            <span>Operations</span>
          </div>

          {artistsLoading ? (
            <div className="px-5 py-8 text-center text-[#4a4b5a] text-sm animate-pulse">Loading...</div>
          ) : artists?.length === 0 ? (
            <div className="px-5 py-8 text-center text-[#4a4b5a] text-sm">No artists yet. Add one above.</div>
          ) : (
            artists?.map((a, i) => (
              <div key={a.id} className="grid grid-cols-6 gap-4 px-5 py-4 border-b border-[#2a2b38] last:border-0 items-center hover:bg-[#1a1b24] transition-colors">
                <div className="col-span-2 flex items-center gap-3">
                  <div className="w-9 h-9 rounded-full bg-[#1a1b24] border border-[#2a2b38] flex items-center justify-center text-sm">🎤</div>
                  <div>
                    <p className="text-white text-sm">{a.performing_name}</p>
                    <p className="text-[#4a4b5a] text-xs">{a.real_name}</p>
                  </div>
                </div>
                <div>
                  <span className="border border-[#2a2b38] text-[#8a8b9a] text-[10px] px-2 py-0.5 rounded tracking-wider">
                    {GENRE_LABELS[i % GENRE_LABELS.length]}
                  </span>
                </div>
                <p className="text-[#8a8b9a] text-sm">{a.album_count} {a.album_count === 1 ? 'Album' : 'Albums'}</p>
                <div className="flex items-center gap-1.5">
                  <span className={`w-1.5 h-1.5 rounded-full ${STATUS_CYCLE[i % STATUS_CYCLE.length] === 'Verified' ? 'bg-[#00e5ff]' : 'bg-[#8a8b9a]'}`} />
                  <span className="text-[#8a8b9a] text-xs">{STATUS_CYCLE[i % STATUS_CYCLE.length]}</span>
                </div>
                <div className="flex gap-3">
                  <button onClick={() => setArtistModal({ open: true, artist: a })} className="text-[#4a4b5a] hover:text-white text-sm transition-colors" title="Edit">✏</button>
                  <button
                    onClick={() => { if (confirm(`Delete "${a.performing_name}"? This will also delete their albums.`)) deleteArtist.mutate(a.id) }}
                    className="text-[#4a4b5a] hover:text-red-400 text-sm transition-colors" title="Delete"
                  >🗑</button>
                </div>
              </div>
            ))
          )}
        </div>
      </div>

      {/* Manage Albums */}
      <div>
        <div className="flex items-center justify-between mb-4">
          <div>
            <h2 className="text-white text-2xl font-semibold">Manage Albums</h2>
            <p className="text-[#4a4b5a] text-xs mt-0.5">Global catalog of high-fidelity releases</p>
          </div>
          <button
            onClick={() => setAlbumModal({ open: true })}
            className="border border-[#00e5ff] text-[#00e5ff] px-4 py-2.5 rounded text-xs font-bold tracking-widest uppercase hover:bg-[#00e5ff]/10 transition-colors"
          >
            + Add New Album
          </button>
        </div>

        {albumsLoading ? (
          <div className="text-center text-[#4a4b5a] text-sm py-8 animate-pulse">Loading...</div>
        ) : albums?.length === 0 ? (
          <div className="text-center text-[#4a4b5a] text-sm py-8">No albums yet. Add one above.</div>
        ) : (
          <div className="grid grid-cols-2 gap-4">
            {albums?.map((album, i) => (
              <div key={album.id} className="bg-[#12131a] border border-[#2a2b38] rounded-lg p-4 flex items-center gap-4 hover:border-[#2a2b38]/80 transition-colors">
                <div
                  className="w-16 h-16 rounded flex items-center justify-center text-2xl flex-shrink-0"
                  style={{ background: `radial-gradient(circle, ${COLORS[i % COLORS.length]} 0%, #0d0e14 100%)` }}
                >
                  🎵
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-white font-medium truncate">{album.name}</p>
                  <p className="text-[#00e5ff] text-sm">{album.artist_name}</p>
                  <p className="text-[#4a4b5a] text-xs mt-1">
                    ${album.price}
                    {album.release_date && ` · ${new Date(album.release_date).getFullYear()}`}
                    {album.genre_names.length > 0 && ` · ${album.genre_names.join(', ')}`}
                    {album.rating != null && <span className="ml-2 text-[#00e5ff]">★ {album.rating.toFixed(1)}</span>}
                  </p>
                </div>
                <div className="flex gap-3 flex-shrink-0">
                  <button onClick={() => setAlbumModal({ open: true, album })} className="text-[#4a4b5a] hover:text-white text-sm transition-colors" title="Edit">✏</button>
                  <button
                    onClick={() => { if (confirm(`Delete "${album.name}"?`)) deleteAlbum.mutate(album.id) }}
                    className="text-[#4a4b5a] hover:text-red-400 text-sm transition-colors" title="Delete"
                  >🗑</button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Manage Genres */}
      <div className="mt-10">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h2 className="text-white text-2xl font-semibold">Manage Genres</h2>
            <p className="text-[#4a4b5a] text-xs mt-0.5">Music classification taxonomy</p>
          </div>
          <button
            onClick={() => setGenreModal({ open: true })}
            className="border border-[#aa3bff] text-[#aa3bff] px-4 py-2.5 rounded text-xs font-bold tracking-widest uppercase hover:bg-[#aa3bff]/10 transition-colors"
          >
            + Add Genre
          </button>
        </div>
        {genresLoading ? (
          <div className="text-center text-[#4a4b5a] text-sm py-8 animate-pulse">Loading...</div>
        ) : genres?.length === 0 ? (
          <div className="text-center text-[#4a4b5a] text-sm py-8">No genres yet.</div>
        ) : (
          <div className="flex flex-wrap gap-3">
            {genres?.map(g => (
              <div key={g.id} className="bg-[#12131a] border border-[#2a2b38] rounded-lg px-4 py-3 flex items-center gap-3">
                <div>
                  <p className="text-white text-sm font-medium">{g.name}</p>
                  {g.description && <p className="text-[#4a4b5a] text-xs mt-0.5">{g.description}</p>}
                </div>
                <div className="flex gap-2 ml-2">
                  <button onClick={() => setGenreModal({ open: true, genre: g })} className="text-[#4a4b5a] hover:text-white text-sm transition-colors">✏</button>
                  <button
                    onClick={() => { if (confirm(`Delete genre "${g.name}"?`)) deleteGenre.mutate(g.id) }}
                    className="text-[#4a4b5a] hover:text-red-400 text-sm transition-colors"
                  >🗑</button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Manage Tracks */}
      <div className="mt-10">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h2 className="text-white text-2xl font-semibold">Manage Tracks</h2>
            <p className="text-[#4a4b5a] text-xs mt-0.5">Individual audio assets in the catalog</p>
          </div>
          <button
            onClick={() => setTrackModal({ open: true })}
            className="border border-[#00e5ff] text-[#00e5ff] px-4 py-2.5 rounded text-xs font-bold tracking-widest uppercase hover:bg-[#00e5ff]/10 transition-colors"
          >
            + Add Track
          </button>
        </div>
        <div className="bg-[#12131a] border border-[#2a2b38] rounded-lg overflow-hidden">
          <div className="grid grid-cols-5 gap-4 px-5 py-3 border-b border-[#2a2b38] text-[10px] tracking-widest text-[#4a4b5a] uppercase">
            <span className="col-span-2">Track Name</span>
            <span>Album</span>
            <span>Date</span>
            <span>Operations</span>
          </div>
          {tracksLoading ? (
            <div className="px-5 py-8 text-center text-[#4a4b5a] text-sm animate-pulse">Loading...</div>
          ) : tracks?.length === 0 ? (
            <div className="px-5 py-8 text-center text-[#4a4b5a] text-sm">No tracks yet. Add one above.</div>
          ) : (
            tracks?.map(t => {
              const album = albums?.find(a => a.id === t.album_id)
              return (
                <div key={t.id} className="grid grid-cols-5 gap-4 px-5 py-3 border-b border-[#2a2b38] last:border-0 items-center hover:bg-[#1a1b24] transition-colors">
                  <div className="col-span-2 flex items-center gap-2">
                    <span className="text-[#4a4b5a] text-xs">🎵</span>
                    <span className="text-white text-sm truncate">{t.name}</span>
                  </div>
                  <p className="text-[#00e5ff] text-xs truncate">{album?.name ?? t.album_id.slice(0, 8) + '…'}</p>
                  <p className="text-[#8a8b9a] text-xs">{new Date(t.date).toLocaleDateString()}</p>
                  <div className="flex gap-3">
                    <button onClick={() => setTrackModal({ open: true, track: t })} className="text-[#4a4b5a] hover:text-white text-sm transition-colors">✏</button>
                    <button
                      onClick={() => { if (confirm(`Delete track "${t.name}"?`)) deleteTrack.mutate(t.id) }}
                      className="text-[#4a4b5a] hover:text-red-400 text-sm transition-colors"
                    >🗑</button>
                  </div>
                </div>
              )
            })
          )}
        </div>
      </div>
    </div>
  )
}
