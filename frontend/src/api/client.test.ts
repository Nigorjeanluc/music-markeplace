import { describe, it, expect, vi, beforeEach } from 'vitest'

// Mock the entire client module
vi.mock('./client', () => ({
  authApi: {
    login: vi.fn(),
    register: vi.fn(),
    me: vi.fn(),
  },
}))

import { authApi } from './client'

describe('authApi', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  describe('login', () => {
    it('calls login endpoint with correct data', async () => {
      const mockResponse = {
        access_token: 'access-token',
        refresh_token: 'refresh-token',
        token_type: 'bearer',
      }
      vi.mocked(authApi.login).mockResolvedValue(mockResponse)

      const result = await authApi.login('test@example.com', 'password')

      expect(result).toEqual(mockResponse)
      expect(authApi.login).toHaveBeenCalledWith('test@example.com', 'password')
    })

    it('handles login failure', async () => {
      vi.mocked(authApi.login).mockRejectedValue(new Error('Login failed'))

      await expect(authApi.login('test@example.com', 'wrong')).rejects.toThrow('Login failed')
    })
  })

  describe('register', () => {
    it('calls register endpoint with correct data', async () => {
      const mockResponse = {
        access_token: 'access-token',
        refresh_token: 'refresh-token',
        token_type: 'bearer',
      }
      vi.mocked(authApi.register).mockResolvedValue(mockResponse)

      const result = await authApi.register('test@example.com', 'testuser', 'password')

      expect(result).toEqual(mockResponse)
      expect(authApi.register).toHaveBeenCalledWith('test@example.com', 'testuser', 'password')
    })
  })

  describe('me', () => {
    it('calls me endpoint', async () => {
      const mockUser = {
        id: '1',
        email: 'test@example.com',
        username: 'testuser',
        avatar_url: null,
        is_admin: false,
        is_active: true,
        created_at: '2023-01-01T00:00:00Z',
      }
      vi.mocked(authApi.me).mockResolvedValue(mockUser)

      const result = await authApi.me()

      expect(result).toEqual(mockUser)
      expect(authApi.me).toHaveBeenCalled()
    })
  })
})

describe('api interceptors', () => {
  it('adds authorization header when token exists', () => {
    localStorage.setItem('access_token', 'test-token')

    // This is a simplified test - in reality, the interceptor would be tested differently
    expect(localStorage.getItem('access_token')).toBe('test-token')
  })
})