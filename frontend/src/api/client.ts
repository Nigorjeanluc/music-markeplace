import axios from 'axios'

export const api = axios.create({
  baseURL: (import.meta.env.VITE_API_URL ?? 'http://localhost:8000') + '/api/v1',
})

// Inject token on every request
api.interceptors.request.use(cfg => {
  const token = localStorage.getItem('access_token')
  if (token) cfg.headers.Authorization = `Bearer ${token}`
  return cfg
})

// Refresh token on 401
let isRefreshing = false
let queue: Array<(token: string) => void> = []

api.interceptors.response.use(
  r => r,
  async error => {
    const original = error.config
    if (error.response?.status === 401 && !original._retry) {
      original._retry = true
      const refresh = localStorage.getItem('refresh_token')
      if (!refresh) return Promise.reject(error)
      if (isRefreshing) {
        return new Promise(resolve => {
          queue.push((token: string) => {
            original.headers.Authorization = `Bearer ${token}`
            resolve(api(original))
          })
        })
      }
      isRefreshing = true
      try {
        const { data } = await axios.post(
          (import.meta.env.VITE_API_URL ?? 'http://localhost:8000') + '/api/v1/auth/refresh',
          { refresh_token: refresh }
        )
        localStorage.setItem('access_token', data.access_token)
        localStorage.setItem('refresh_token', data.refresh_token)
        api.defaults.headers.common.Authorization = `Bearer ${data.access_token}`
        queue.forEach(cb => cb(data.access_token))
        queue = []
        original.headers.Authorization = `Bearer ${data.access_token}`
        return api(original)
      } catch {
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        window.location.href = '/login'
        return Promise.reject(error)
      } finally {
        isRefreshing = false
      }
    }
    return Promise.reject(error)
  }
)

// ── Pagination ──────────────────────────────────────────────────────────────

export interface PaginatedResponse<T> {
  items: T[]
  total: number
  page: number
  page_size: number
  total_pages: number
}

// ── Types ────────────────────────────────────────────────────────────────────

export interface TokenResponse {
  access_token: string
  refresh_token: string
  token_type: string
}

export interface UserResponse {
  id: string
  email: string
  username: string
  avatar_url: string | null
  is_admin: boolean
  is_active: boolean
  created_at: string
}

export interface ArtistResponse {
  id: string
  real_name: string
  performing_name: string
  date_of_birth: string
  photo_url: string | null
  created_at: string
  album_count: number
}

export interface AlbumResponse {
  id: string
  name: string
  price: number
  release_date: string | null
  artist_id: string
  artist_name: string
  rating: number | null
  genre_names: string[]
  cover_image_url: string | null
  created_at: string
  updated_at: string
}

export interface PurchaseResponse {
  id: string
  album_id: string
  album_name: string
  artist_name: string
  purchase_date: string
  amount_paid: number
  user_rating?: number | null
  avg_rating?: number | null
}

export interface RatingResponse {
  album_id: string
  album_name: string
  user_rating: number
  avg_rating: number | null
  created_at: string
}

export interface GenreResponse {
  id: string
  name: string
  description: string | null
  created_at: string
  updated_at: string
}

export interface TrackResponse {
  id: string
  name: string
  date: string
  album_id: string
  created_at: string
}

export interface TrackInPlaylist {
  id: string
  name: string
  date: string
  album_name: string
  artist_name: string
}

export interface PlaylistResponse {
  id: string
  name: string
  created_at: string
  track_count: number
}

export interface PlaylistDetailResponse extends PlaylistResponse {
  tracks: TrackInPlaylist[]
}

// ── Auth ─────────────────────────────────────────────────────────────────────

export const authApi = {
  login: (email: string, password: string) =>
    api.post<TokenResponse>('/auth/login', { email, password }).then(r => r.data),
  register: (email: string, username: string, password: string) =>
    api.post<TokenResponse>('/auth/register', { email, username, password }).then(r => r.data),
  refresh: (refresh_token: string) =>
    api.post<TokenResponse>('/auth/refresh', { refresh_token }).then(r => r.data),
  me: () => api.get<UserResponse>('/auth/me').then(r => r.data),
}

// ── Artists ──────────────────────────────────────────────────────────────────

export const artistsApi = {
  list: (params?: { search?: string; page?: number; page_size?: number }) =>
    api.get<PaginatedResponse<ArtistResponse>>('/artists/', { params }).then(r => r.data),
  get: (id: string) => api.get<ArtistResponse>(`/artists/${id}`).then(r => r.data),
  create: (data: { real_name: string; performing_name: string; date_of_birth: string }) =>
    api.post<ArtistResponse>('/artists/', data).then(r => r.data),
  update: (id: string, data: Partial<{ real_name: string; performing_name: string; date_of_birth: string }>) =>
    api.put<ArtistResponse>(`/artists/${id}`, data).then(r => r.data),
  delete: (id: string) => api.delete(`/artists/${id}`),
}

// ── Albums ───────────────────────────────────────────────────────────────────

export const albumsApi = {
  list: (params?: { search?: string; artist_id?: string; genre?: string; page?: number; page_size?: number }) =>
    api.get<PaginatedResponse<AlbumResponse>>('/albums/', { params }).then(r => r.data),
  get: (id: string) => api.get<AlbumResponse>(`/albums/${id}`).then(r => r.data),
  create: (data: { name: string; price: number; artist_id: string; genre_ids: string[]; release_date?: string }) =>
    api.post<AlbumResponse>('/albums/', data).then(r => r.data),
  update: (id: string, data: Partial<{ name: string; price: number; genre_ids: string[]; release_date: string }>) =>
    api.put<AlbumResponse>(`/albums/${id}`, data).then(r => r.data),
  delete: (id: string) => api.delete(`/albums/${id}`),
}

// ── Purchases ────────────────────────────────────────────────────────────────

export const purchasesApi = {
  purchase: (album_id: string) =>
    api.post<PurchaseResponse>('/purchases/', { album_id }).then(r => r.data),
  library: (params?: { page?: number; page_size?: number }) =>
    api.get<PaginatedResponse<PurchaseResponse>>('/purchases/me/library', { params }).then(r => r.data),
}

// ── Ratings ──────────────────────────────────────────────────────────────────

export const ratingsApi = {
  rate: (album_id: string, rating: number) =>
    api.post<RatingResponse>('/ratings/', { album_id, rating }).then(r => r.data),
  update: (album_id: string, rating: number) =>
    api.put<RatingResponse>(`/ratings/${album_id}`, { rating }).then(r => r.data),
  myRatings: (params?: { page?: number; page_size?: number }) =>
    api.get<PaginatedResponse<RatingResponse>>('/ratings/me', { params }).then(r => r.data),
  albumRatings: (album_id: string, params?: { page?: number; page_size?: number }) =>
    api.get<PaginatedResponse<RatingResponse>>(`/ratings/album/${album_id}`, { params }).then(r => r.data),
}

// ── Genres ───────────────────────────────────────────────────────────────────

export const genresApi = {
  list: () => api.get<GenreResponse[]>('/genres/').then(r => r.data),
  get: (id: string) => api.get<GenreResponse>(`/genres/${id}`).then(r => r.data),
  create: (data: { name: string; description?: string }) =>
    api.post<GenreResponse>('/genres/', data).then(r => r.data),
  update: (id: string, data: { name?: string; description?: string }) =>
    api.put<GenreResponse>(`/genres/${id}`, data).then(r => r.data),
  delete: (id: string) => api.delete(`/genres/${id}`),
}

// ── Tracks ───────────────────────────────────────────────────────────────────

export const tracksApi = {
  list: (params?: { album_id?: string; search?: string; page?: number; page_size?: number }) =>
    api.get<PaginatedResponse<TrackResponse>>('/tracks/', { params }).then(r => r.data),
  get: (id: string) => api.get<TrackResponse>(`/tracks/${id}`).then(r => r.data),
  create: (data: { name: string; date: string; album_id: string }) =>
    api.post<TrackResponse>('/tracks/', data).then(r => r.data),
  update: (id: string, data: { name?: string; date?: string; album_id?: string }) =>
    api.put<TrackResponse>(`/tracks/${id}`, data).then(r => r.data),
  delete: (id: string) => api.delete(`/tracks/${id}`),
}

// ── Playlists ─────────────────────────────────────────────────────────────────

export const playlistsApi = {
  list: () => api.get<PlaylistResponse[]>('/playlists/').then(r => r.data),
  get: (id: string) => api.get<PlaylistDetailResponse>(`/playlists/${id}`).then(r => r.data),
  create: (data: { name: string; track_ids?: string[] }) =>
    api.post<PlaylistDetailResponse>('/playlists/', data).then(r => r.data),
  update: (id: string, data: { name: string }) =>
    api.put<PlaylistResponse>(`/playlists/${id}`, data).then(r => r.data),
  delete: (id: string) => api.delete(`/playlists/${id}`),
  addTrack: (playlist_id: string, track_id: string) =>
    api.post(`/playlists/${playlist_id}/tracks`, { track_id }),
  removeTrack: (playlist_id: string, track_id: string) =>
    api.delete(`/playlists/${playlist_id}/tracks/${track_id}`),
}

// ── Upload ────────────────────────────────────────────────────────────────────

export const uploadApi = {
  image: (file: File, folder = 'images') => {
    const form = new FormData()
    form.append('file', file)
    form.append('folder', folder)
    return api.post<{ url: string }>('/upload/', form, {
      headers: { 'Content-Type': 'multipart/form-data' },
    }).then(r => r.data)
  },
}
