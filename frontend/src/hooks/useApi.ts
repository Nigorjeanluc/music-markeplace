import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { artistsApi, albumsApi, purchasesApi, ratingsApi, genresApi } from '../api/client'

// ── Artists ──────────────────────────────────────────────────────────────────

export const useArtists = (search?: string) =>
  useQuery({
    queryKey: ['artists', search],
    queryFn: () => artistsApi.list({ search }),
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

export const useAlbums = (params?: { search?: string; artist_id?: string; genre?: string }) =>
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

export const useLibrary = (enabled: boolean) =>
  useQuery({
    queryKey: ['library'],
    queryFn: purchasesApi.library,
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

export const useMyRatings = (enabled: boolean) =>
  useQuery({
    queryKey: ['ratings', 'me'],
    queryFn: ratingsApi.myRatings,
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

export const useDeleteGenre = () => {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: genresApi.delete,
    onSuccess: () => qc.invalidateQueries({ queryKey: ['genres'] }),
  })
}
