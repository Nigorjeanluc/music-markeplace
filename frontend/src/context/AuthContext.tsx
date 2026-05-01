import { createContext, useContext, useState, useEffect, type ReactNode } from 'react'
import { authApi, type UserResponse } from '../api/client'

interface AuthCtx {
  user: UserResponse | null
  token: string | null
  login: (email: string, password: string) => Promise<void>
  register: (email: string, username: string, password: string) => Promise<void>
  logout: () => void
  isAdmin: boolean
}

const AuthContext = createContext<AuthCtx>(null!)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<UserResponse | null>(null)
  const [token, setToken] = useState<string | null>(() => localStorage.getItem('access_token'))

  // On mount, if we have a token, fetch current user
  useEffect(() => {
    if (token && !user) {
      authApi.me().then(setUser).catch(() => {
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        setToken(null)
      })
    }
  }, [token]) // eslint-disable-line react-hooks/exhaustive-deps

  const storeTokens = (access: string, refresh: string) => {
    localStorage.setItem('access_token', access)
    localStorage.setItem('refresh_token', refresh)
    setToken(access)
  }

  const login = async (email: string, password: string) => {
    const tokens = await authApi.login(email, password)
    storeTokens(tokens.access_token, tokens.refresh_token)
    const me = await authApi.me()
    setUser(me)
  }

  const register = async (email: string, username: string, password: string) => {
    const tokens = await authApi.register(email, username, password)
    storeTokens(tokens.access_token, tokens.refresh_token)
    const me = await authApi.me()
    setUser(me)
  }

  const logout = () => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    setToken(null)
    setUser(null)
  }

  return (
    <AuthContext.Provider value={{ user, token, login, register, logout, isAdmin: user?.is_admin ?? false }}>
      {children}
    </AuthContext.Provider>
  )
}

export const useAuth = () => useContext(AuthContext)
