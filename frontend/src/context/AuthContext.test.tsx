import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, it, expect, vi, beforeEach } from 'vitest'
import { AuthProvider, useAuth } from './AuthContext'
import { authApi } from '../api/client'

// Mock the API
vi.mock('../api/client', () => ({
  authApi: {
    login: vi.fn(),
    register: vi.fn(),
    me: vi.fn(),
  },
}))

const TestComponent = () => {
  const { user, token, login, register, logout, isAdmin } = useAuth()
  return (
    <div>
      <div data-testid="user">{user ? user.username : 'no-user'}</div>
      <div data-testid="token">{token || 'no-token'}</div>
      <div data-testid="is-admin">{isAdmin ? 'admin' : 'not-admin'}</div>
      <button onClick={() => login('test@example.com', 'password')}>Login</button>
      <button onClick={() => register('test@example.com', 'testuser', 'password')}>Register</button>
      <button onClick={logout}>Logout</button>
    </div>
  )
}

describe('AuthContext', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    localStorage.clear()
  })

  it('provides initial state', () => {
    render(
      <AuthProvider>
        <TestComponent />
      </AuthProvider>
    )

    expect(screen.getByTestId('user')).toHaveTextContent('no-user')
    expect(screen.getByTestId('token')).toHaveTextContent('no-token')
    expect(screen.getByTestId('is-admin')).toHaveTextContent('not-admin')
  })

  it('loads user on mount if token exists', async () => {
    const mockUser = {
      id: '1',
      email: 'test@example.com',
      username: 'testuser',
      avatar_url: null,
      is_admin: false,
      is_active: true,
      created_at: '2023-01-01T00:00:00Z',
    }

    localStorage.setItem('access_token', 'test-token')
    vi.mocked(authApi.me).mockResolvedValue(mockUser)

    render(
      <AuthProvider>
        <TestComponent />
      </AuthProvider>
    )

    await waitFor(() => {
      expect(screen.getByTestId('user')).toHaveTextContent('testuser')
      expect(screen.getByTestId('token')).toHaveTextContent('test-token')
      expect(screen.getByTestId('is-admin')).toHaveTextContent('not-admin')
    })

    expect(authApi.me).toHaveBeenCalled()
  })

  it('handles login successfully', async () => {
    const user = userEvent.setup()
    const mockTokens = {
      access_token: 'access-token',
      refresh_token: 'refresh-token',
      token_type: 'bearer',
    }
    const mockUser = {
      id: '1',
      email: 'test@example.com',
      username: 'testuser',
      avatar_url: null,
      is_admin: true,
      is_active: true,
      created_at: '2023-01-01T00:00:00Z',
    }

    vi.mocked(authApi.login).mockResolvedValue(mockTokens)
    vi.mocked(authApi.me).mockResolvedValue(mockUser)

    render(
      <AuthProvider>
        <TestComponent />
      </AuthProvider>
    )

    await user.click(screen.getByRole('button', { name: /login/i }))

    await waitFor(() => {
      expect(screen.getByTestId('user')).toHaveTextContent('testuser')
      expect(screen.getByTestId('token')).toHaveTextContent('access-token')
      expect(screen.getByTestId('is-admin')).toHaveTextContent('admin')
    })

    expect(authApi.login).toHaveBeenCalledWith('test@example.com', 'password')
    expect(authApi.me).toHaveBeenCalled()
    expect(localStorage.getItem('access_token')).toBe('access-token')
    expect(localStorage.getItem('refresh_token')).toBe('refresh-token')
  })

  it('handles register successfully', async () => {
    const user = userEvent.setup()
    const mockTokens = {
      access_token: 'access-token',
      refresh_token: 'refresh-token',
      token_type: 'bearer',
    }
    const mockUser = {
      id: '1',
      email: 'test@example.com',
      username: 'testuser',
      avatar_url: null,
      is_admin: false,
      is_active: true,
      created_at: '2023-01-01T00:00:00Z',
    }

    vi.mocked(authApi.register).mockResolvedValue(mockTokens)
    vi.mocked(authApi.me).mockResolvedValue(mockUser)

    render(
      <AuthProvider>
        <TestComponent />
      </AuthProvider>
    )

    await user.click(screen.getByRole('button', { name: /register/i }))

    await waitFor(() => {
      expect(screen.getByTestId('user')).toHaveTextContent('testuser')
      expect(screen.getByTestId('token')).toHaveTextContent('access-token')
    })

    expect(authApi.register).toHaveBeenCalledWith('test@example.com', 'testuser', 'password')
    expect(authApi.me).toHaveBeenCalled()
  })

  it('handles logout', async () => {
    const user = userEvent.setup()

    // Set up logged in state
    localStorage.setItem('access_token', 'test-token')
    localStorage.setItem('refresh_token', 'refresh-token')

    render(
      <AuthProvider>
        <TestComponent />
      </AuthProvider>
    )

    await user.click(screen.getByRole('button', { name: /logout/i }))

    expect(localStorage.getItem('access_token')).toBeNull()
    expect(localStorage.getItem('refresh_token')).toBeNull()
    expect(screen.getByTestId('user')).toHaveTextContent('no-user')
    expect(screen.getByTestId('token')).toHaveTextContent('no-token')
  })

  it('clears tokens on failed me call', async () => {
    localStorage.setItem('access_token', 'invalid-token')
    vi.mocked(authApi.me).mockRejectedValue(new Error('Invalid token'))

    render(
      <AuthProvider>
        <TestComponent />
      </AuthProvider>
    )

    await waitFor(() => {
      expect(localStorage.getItem('access_token')).toBeNull()
      expect(localStorage.getItem('refresh_token')).toBeNull()
    })
  })
})