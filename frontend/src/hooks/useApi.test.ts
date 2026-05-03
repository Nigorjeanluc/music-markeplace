import { renderHook, waitFor } from '@testing-library/react'
import { describe, it, expect, vi, beforeEach } from 'vitest'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import React from 'react'
import {
  useArtists,
  useArtist,
  useCreateArtist,
  useAlbums,
  useCreateAlbum,
} from './useApi'
import { artistsApi, albumsApi } from '../api/client'
import type { ArtistResponse } from '../api/client'

// Mock the API
vi.mock('../api/client', () => ({
  artistsApi: {
    list: vi.fn(),
    get: vi.fn(),
    create: vi.fn(),
    update: vi.fn(),
    delete: vi.fn(),
  },
  albumsApi: {
    list: vi.fn(),
    get: vi.fn(),
    create: vi.fn(),
    update: vi.fn(),
    delete: vi.fn(),
  },
  purchasesApi: {
    purchase: vi.fn(),
    library: vi.fn(),
  },
  ratingsApi: {
    rate: vi.fn(),
    update: vi.fn(),
    myRatings: vi.fn(),
    albumRatings: vi.fn(),
  },
  genresApi: {
    list: vi.fn(),
    get: vi.fn(),
    create: vi.fn(),
    update: vi.fn(),
    delete: vi.fn(),
  },
  tracksApi: {
    list: vi.fn(),
    get: vi.fn(),
    create: vi.fn(),
    update: vi.fn(),
    delete: vi.fn(),
  },
  playlistsApi: {
    list: vi.fn(),
    get: vi.fn(),
    create: vi.fn(),
    update: vi.fn(),
    delete: vi.fn(),
    addTrack: vi.fn(),
  },
  uploadApi: {
    uploadImage: vi.fn(),
  },
}))

const createWrapper = () => {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: { retry: false },
      mutations: { retry: false },
    },
  })
  return ({ children }: { children: React.ReactNode }) =>
    React.createElement(QueryClientProvider, { client: queryClient }, children)
}

describe('useApi hooks', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  describe('useArtists', () => {
    it('fetches artists successfully', async () => {
      const mockArtists = [
        {
          id: '1',
          real_name: 'Test Artist',
          performing_name: 'Test Performer',
          date_of_birth: '1990-01-01',
          photo_url: null,
          created_at: '2023-01-01T00:00:00Z',
          album_count: 2,
        },
      ]
      const mockResponse = { items: mockArtists, total: 2, page: 1, page_size: 10, total_pages: 1 }

      vi.mocked(artistsApi.list).mockResolvedValue(mockResponse)

      const { result } = renderHook(() => useArtists(), { wrapper: createWrapper() })

      expect(result.current.isLoading).toBe(true)

      await waitFor(() => {
        expect(result.current.isSuccess).toBe(true)
      })

      expect(result.current.data).toEqual(mockResponse)
      expect(artistsApi.list).toHaveBeenCalledWith(undefined)
    })

    it('fetches artists with search parameter', async () => {
      const mockArtists: ArtistResponse[] = []
      const mockResponse = { items: mockArtists, total: 0, page: 1, page_size: 10, total_pages: 0 }
      vi.mocked(artistsApi.list).mockResolvedValue(mockResponse)

      const { result } = renderHook(() => useArtists({ search: 'test' }), { wrapper: createWrapper() })

      await waitFor(() => {
        expect(result.current.isSuccess).toBe(true)
      })

      expect(artistsApi.list).toHaveBeenCalledWith({ search: 'test' })
    })
  })

  describe('useArtist', () => {
    it('fetches single artist', async () => {
      const mockArtist = {
        id: '1',
        real_name: 'Test Artist',
        performing_name: 'Test Performer',
        date_of_birth: '1990-01-01',
        photo_url: null,
        created_at: '2023-01-01T00:00:00Z',
        album_count: 2,
      }

      vi.mocked(artistsApi.get).mockResolvedValue(mockArtist)

      const { result } = renderHook(() => useArtist('1'), { wrapper: createWrapper() })

      await waitFor(() => {
        expect(result.current.isSuccess).toBe(true)
      })

      expect(result.current.data).toEqual(mockArtist)
      expect(artistsApi.get).toHaveBeenCalledWith('1')
    })

    it('does not fetch when id is empty', () => {
      const { result } = renderHook(() => useArtist(''), { wrapper: createWrapper() })

      expect(result.current.isFetching).toBe(false)
      expect(artistsApi.get).not.toHaveBeenCalled()
    })
  })

  describe('useCreateArtist', () => {
    it('creates artist successfully', async () => {
      const mockArtist = {
        id: '1',
        real_name: 'New Artist',
        performing_name: 'New Performer',
        date_of_birth: '1990-01-01',
        photo_url: null,
        created_at: '2023-01-01T00:00:00Z',
        album_count: 0,
      }

      vi.mocked(artistsApi.create).mockResolvedValue(mockArtist)

      const { result } = renderHook(() => useCreateArtist(), { wrapper: createWrapper() })

      result.current.mutate({
        real_name: 'New Artist',
        performing_name: 'New Performer',
        date_of_birth: '1990-01-01',
      })

      await waitFor(() => {
        expect(result.current.isSuccess).toBe(true)
      })

      expect(result.current.data).toEqual(mockArtist)
      expect(vi.mocked(artistsApi.create).mock.calls[0][0]).toEqual({
        real_name: 'New Artist',
        performing_name: 'New Performer',
        date_of_birth: '1990-01-01',
      })
    })
  })

  describe('useAlbums', () => {
    it('fetches albums successfully', async () => {
      const mockAlbums = [
        {
          id: '1',
          name: 'Test Album',
          price: 19.99,
          release_date: '2023-01-01',
          artist_id: '1',
          artist_name: 'Test Artist',
          rating: 4.5,
          genre_names: ['Rock'],
          cover_image_url: null,
          created_at: '2023-01-01T00:00:00Z',
          updated_at: '2023-01-01T00:00:00Z',
        },
      ]
      const mockResponse = { items: mockAlbums, total: 1, page: 1, page_size: 10, total_pages: 1 }

      vi.mocked(albumsApi.list).mockResolvedValue(mockResponse)

      const { result } = renderHook(() => useAlbums(), { wrapper: createWrapper() })

      await waitFor(() => {
        expect(result.current.isSuccess).toBe(true)
      })

      expect(result.current.data).toEqual(mockResponse)
      expect(albumsApi.list).toHaveBeenCalledWith(undefined)
    })
  })

  describe('useCreateAlbum', () => {
    it('creates album successfully', async () => {
      const mockAlbum = {
        id: '1',
        name: 'New Album',
        price: 19.99,
        release_date: '2023-01-01',
        artist_id: '1',
        artist_name: 'Test Artist',
        rating: null,
        genre_names: ['Rock'],
        cover_image_url: null,
        created_at: '2023-01-01T00:00:00Z',
        updated_at: '2023-01-01T00:00:00Z',
      }

      vi.mocked(albumsApi.create).mockResolvedValue(mockAlbum)

      const { result } = renderHook(() => useCreateAlbum(), { wrapper: createWrapper() })

      result.current.mutate({
        name: 'New Album',
        price: 19.99,
        artist_id: '1',
        genre_ids: ['genre-1'],
      })

      await waitFor(() => {
        expect(result.current.isSuccess).toBe(true)
      })

      expect(result.current.data).toEqual(mockAlbum)
      expect(vi.mocked(albumsApi.create).mock.calls[0][0]).toEqual({
        name: 'New Album',
        price: 19.99,
        artist_id: '1',
        genre_ids: ['genre-1'],
      })
    })
  })
})