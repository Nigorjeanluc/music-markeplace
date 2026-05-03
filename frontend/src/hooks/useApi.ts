import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { artistsApi, albumsApi, purchasesApi, ratingsApi, genresApi, tracksApi, playlistsApi } from '../api/client'

// ── Artists ──────────────────────────────────────────────────────────────────

export const useArtists = (params?: { search?: string; page?: number; page_size?: number }) =>
  useQuery({
    queryKey: ['artists', params],
    queryFn: () => artistsApi.list(params),
  })

export const useArtist = (id: string) =>
  useQuery({
    queryKey: ['artists', id],
    queryFn: () => artistsApi.get(id),
    enabled: !!id,
  })

export const useCreateArtist = () => {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: artistsApi.create,
    onSuccess: () => qc.invalidateQueries({ queryKey: ['artists'] }),
  })
}

export const useUpdateArtist = () => {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: Parameters<typeof artistsApi.update>[1] }) =>
      artistsApi.update(id, data),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['artists'] }),
  })
}

export const useDeleteArtist = () => {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: artistsApi.delete,
    onSuccess: () => qc.invalidateQueries({ queryKey: ['artists'] }),
  })
}

// ── Albums ───────────────────────────────────────────────────────────────────

export const useAlbums = (params?: { search?: string; artist_id?: string; genre?: string; page?: number; page_size?: number }) =>
  useQuery({
    queryKey: ['albums', params],
    queryFn: () => albumsApi.list(params),
  })

export const useAlbum = (id: string) =>
  useQuery({
    queryKey: ['albums', id],
    queryFn: () => albumsApi.get(id),
    enabled: !!id,
  })

export const useCreateAlbum = () => {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: albumsApi.create,
    onSuccess: () => qc.invalidateQueries({ queryKey: ['albums'] }),
  })
}

export const useUpdateAlbum = () => {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: Parameters<typeof albumsApi.update>[1] }) =>
      albumsApi.update(id, data),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['albums'] }),
  })
}

export const useDeleteAlbum = () => {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: albumsApi.delete,
    onSuccess: () => qc.invalidateQueries({ queryKey: ['albums'] }),
  })
}

// ── Purchases ────────────────────────────────────────────────────────────────

export const useLibrary = (enabled: boolean, params?: { page?: number; page_size?: number }) =>
  useQuery({
    queryKey: ['library', params],
    queryFn: () => purchasesApi.library(params),
    enabled,
  })

export const usePurchase = () => {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: purchasesApi.purchase,
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['library'] })
      qc.invalidateQueries({ queryKey: ['albums'] })
    },
  })
}

// ── Ratings ──────────────────────────────────────────────────────────────────

export const useMyRatings = (enabled: boolean, params?: { page?: number; page_size?: number }) =>
  useQuery({
    queryKey: ['ratings', 'me', params],
    queryFn: () => ratingsApi.myRatings(params),
    enabled,
  })

export const useRateAlbum = () => {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: ({ album_id, rating }: { album_id: string; rating: number }) =>
      ratingsApi.rate(album_id, rating),
    onSuccess: (_data, vars) => {
      qc.invalidateQueries({ queryKey: ['ratings', 'me'] })
      qc.invalidateQueries({ queryKey: ['albums', vars.album_id] })
      qc.invalidateQueries({ queryKey: ['library'] })
    },
  })
}

// ── Ratings (update) ───────────────────────────────────────────────────────────

export const useUpdateRating = () => {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: ({ album_id, rating }: { album_id: string; rating: number }) =>
      ratingsApi.update(album_id, rating),
    onSuccess: (_data, vars) => {
      qc.invalidateQueries({ queryKey: ['ratings', 'me'] })
      qc.invalidateQueries({ queryKey: ['albums', vars.album_id] })
      qc.invalidateQueries({ queryKey: ['library'] })
    },
  })
}

export const useAlbumRatings = (album_id: string, params?: { page?: number; page_size?: number }) =>
  useQuery({
    queryKey: ['ratings', 'album', album_id, params],
    queryFn: () => ratingsApi.albumRatings(album_id, params),
    enabled: !!album_id,
  })

// ── Genres ───────────────────────────────────────────────────────────────────

export const useGenres = () =>
  useQuery({ queryKey: ['genres'], queryFn: genresApi.list })

export const useCreateGenre = () => {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: genresApi.create,
    onSuccess: () => qc.invalidateQueries({ queryKey: ['genres'] }),
  })
}

export const useUpdateGenre = () => {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: { name?: string; description?: string } }) =>
      genresApi.update(id, data),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['genres'] }),
  })
}

export const useDeleteGenre = () => {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: genresApi.delete,
    onSuccess: () => qc.invalidateQueries({ queryKey: ['genres'] }),
  })
}

// ── Tracks ───────────────────────────────────────────────────────────────────

export const useTracks = (params?: { album_id?: string; search?: string; page?: number; page_size?: number }) =>
  useQuery({
    queryKey: ['tracks', params],
    queryFn: () => tracksApi.list(params),
  })

export const useAlbumTracks = (album_id: string) =>
  useQuery({
    queryKey: ['tracks', { album_id }],
    queryFn: () => tracksApi.list({ album_id }),
    enabled: !!album_id,
  })

export const useCreateTrack = () => {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: tracksApi.create,
    onSuccess: () => qc.invalidateQueries({ queryKey: ['tracks'] }),
  })
}

export const useUpdateTrack = () => {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: Parameters<typeof tracksApi.update>[1] }) =>
      tracksApi.update(id, data),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['tracks'] }),
  })
}

export const useDeleteTrack = () => {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: tracksApi.delete,
    onSuccess: () => qc.invalidateQueries({ queryKey: ['tracks'] }),
  })
}

// ── Playlists ─────────────────────────────────────────────────────────────────

export const usePlaylists = (enabled: boolean) =>
  useQuery({
    queryKey: ['playlists'],
    queryFn: playlistsApi.list,
    enabled,
  })

export const usePlaylist = (id: string) =>
  useQuery({
    queryKey: ['playlists', id],
    queryFn: () => playlistsApi.get(id),
    enabled: !!id,
  })

export const useCreatePlaylist = () => {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: playlistsApi.create,
    onSuccess: () => qc.invalidateQueries({ queryKey: ['playlists'] }),
  })
}

export const useUpdatePlaylist = () => {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: { name: string } }) =>
      playlistsApi.update(id, data),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['playlists'] }),
  })
}

export const useDeletePlaylist = () => {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: playlistsApi.delete,
    onSuccess: () => qc.invalidateQueries({ queryKey: ['playlists'] }),
  })
}

export const useAddTrackToPlaylist = () => {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: ({ playlist_id, track_id }: { playlist_id: string; track_id: string }) =>
      playlistsApi.addTrack(playlist_id, track_id),
    onSuccess: (_data, vars) => qc.invalidateQueries({ queryKey: ['playlists', vars.playlist_id] }),
  })
}

export const useRemoveTrackFromPlaylist = () => {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: ({ playlist_id, track_id }: { playlist_id: string; track_id: string }) =>
      playlistsApi.removeTrack(playlist_id, track_id),
    onSuccess: (_data, vars) => qc.invalidateQueries({ queryKey: ['playlists', vars.playlist_id] }),
  })
}
