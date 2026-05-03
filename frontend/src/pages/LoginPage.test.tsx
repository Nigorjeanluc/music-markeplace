import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, it, expect, vi, beforeEach } from 'vitest'
import { MemoryRouter } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import LoginPage from './LoginPage'
import { useAuth } from '../context/AuthContext'

// Mock the auth context
vi.mock('../context/AuthContext', () => ({
  useAuth: vi.fn(),
}))

const createWrapper = () => {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: { retry: false },
      mutations: { retry: false },
    },
  })
  return ({ children }: { children: React.ReactNode }) => (
    <QueryClientProvider client={queryClient}>
      <MemoryRouter>
        {children}
      </MemoryRouter>
    </QueryClientProvider>
  )
}

describe('LoginPage', () => {
  const mockLogin = vi.fn()
  const mockRegister = vi.fn()

  beforeEach(() => {
    vi.clearAllMocks()
    vi.mocked(useAuth).mockReturnValue({
      user: null,
      token: null,
      login: mockLogin,
      register: mockRegister,
      logout: vi.fn(),
      isAdmin: false,
    })
  })

  it('renders login form by default', () => {
    render(<LoginPage />, { wrapper: createWrapper() })

    expect(screen.getByText('Welcome Back')).toBeInTheDocument()
    expect(screen.getByText('Access the high-fidelity soundscape.')).toBeInTheDocument()
    expect(screen.getByPlaceholderText('user@sonicvoid.io')).toBeInTheDocument()
    expect(screen.getByPlaceholderText('••••••••')).toBeInTheDocument()
    expect(screen.getByRole('button', { name: /enter void/i })).toBeInTheDocument()
    expect(screen.getByText('Register Identity 👤+')).toBeInTheDocument()
  })

  it('shows seeded credentials hint', () => {
    render(<LoginPage />, { wrapper: createWrapper() })

    expect(screen.getByText(/seeded:/i)).toBeInTheDocument()
    expect(screen.getByText('admin@musicmarket.com')).toBeInTheDocument()
    expect(screen.getByText('john@musicmarket.com')).toBeInTheDocument()
  })

  it('switches to register mode', async () => {
    const user = userEvent.setup()
    render(<LoginPage />, { wrapper: createWrapper() })

    await user.click(screen.getByRole('button', { name: /register identity/i }))

    expect(screen.getByPlaceholderText('your_handle')).toBeInTheDocument()
    expect(screen.getByRole('button', { name: /register identity/i })).toBeInTheDocument()
    expect(screen.getByText('← Back to Login')).toBeInTheDocument()
  })

  it('validates login form', async () => {
    const user = userEvent.setup()
    render(<LoginPage />, { wrapper: createWrapper() })

    const submitButton = screen.getByRole('button', { name: /enter void/i })
    await user.click(submitButton)

    // Check for required field errors
    const requiredErrors = screen.getAllByText('Required')
    expect(requiredErrors).toHaveLength(2) // email and password
  })

  it('validates email format', async () => {
    const user = userEvent.setup()
    render(<LoginPage />, { wrapper: createWrapper() })

    const emailInput = screen.getByPlaceholderText('user@sonicvoid.io')
    await user.type(emailInput, 'invalid-email')

    const passwordInput = screen.getByPlaceholderText('••••••••')
    await user.type(passwordInput, 'password123')

    const submitButton = screen.getByRole('button', { name: /enter void/i })
    await user.click(submitButton)

    expect(screen.getByText('Invalid email')).toBeInTheDocument()
  })

  it('validates password minimum length', async () => {
    const user = userEvent.setup()
    render(<LoginPage />, { wrapper: createWrapper() })

    const emailInput = screen.getByPlaceholderText('user@sonicvoid.io')
    await user.type(emailInput, 'test@example.com')

    const passwordInput = screen.getByPlaceholderText('••••••••')
    await user.type(passwordInput, '123')

    const submitButton = screen.getByRole('button', { name: /enter void/i })
    await user.click(submitButton)

    expect(screen.getByText('Min 4 characters')).toBeInTheDocument()
  })

  it('calls login on valid form submission', async () => {
    const user = userEvent.setup()
    mockLogin.mockResolvedValue(undefined)

    render(<LoginPage />, { wrapper: createWrapper() })

    const emailInput = screen.getByPlaceholderText('user@sonicvoid.io')
    await user.type(emailInput, 'test@example.com')

    const passwordInput = screen.getByPlaceholderText('••••••••')
    await user.type(passwordInput, 'password123')

    const submitButton = screen.getByRole('button', { name: /enter void/i })
    await user.click(submitButton)

    await waitFor(() => {
      expect(mockLogin).toHaveBeenCalledWith('test@example.com', 'password123')
    })
  })

  it('shows API error on login failure', async () => {
    const user = userEvent.setup()
    mockLogin.mockRejectedValue({
      response: { data: { detail: 'Invalid credentials' } }
    })

    render(<LoginPage />, { wrapper: createWrapper() })

    const emailInput = screen.getByPlaceholderText('user@sonicvoid.io')
    await user.type(emailInput, 'test@example.com')

    const passwordInput = screen.getByPlaceholderText('••••••••')
    await user.type(passwordInput, 'wrongpassword')

    const submitButton = screen.getByRole('button', { name: /enter void/i })
    await user.click(submitButton)

    await waitFor(() => {
      const errorElements = screen.getAllByText('Invalid credentials')
      const visibleError = errorElements.find(el => !el.className.includes('hidden'))
      expect(visibleError?.closest('div')).toHaveClass('bg-red-900/20')
    })
  })

  it('validates register form', async () => {
    const user = userEvent.setup()

    render(<LoginPage />, { wrapper: createWrapper() })
    await user.click(screen.getByRole('button', { name: /register identity/i }))

    const submitButton = screen.getByRole('button', { name: /register identity/i })
    await user.click(submitButton)

    // Check for required field errors - should be 3: email, username, password
    const requiredErrors = screen.getAllByText('Required')
    expect(requiredErrors.length).toBeGreaterThanOrEqual(3)
  })

  it('validates username length', async () => {
    const user = userEvent.setup()

    render(<LoginPage />, { wrapper: createWrapper() })
    await user.click(screen.getByRole('button', { name: /register identity/i }))

    const usernameInput = screen.getByPlaceholderText('your_handle')
    await user.type(usernameInput, 'ab')

    const submitButton = screen.getByRole('button', { name: /register identity/i })
    await user.click(submitButton)

    expect(screen.getByText('Min 3 characters')).toBeInTheDocument()
  })

  it('calls register on valid form submission', async () => {
    const user = userEvent.setup()
    mockRegister.mockResolvedValue(undefined)

    render(<LoginPage />, { wrapper: createWrapper() })
    await user.click(screen.getByRole('button', { name: /register identity/i }))

    const emailInput = screen.getByPlaceholderText('user@sonicvoid.io')
    await user.type(emailInput, 'test@example.com')

    const usernameInput = screen.getByPlaceholderText('your_handle')
    await user.type(usernameInput, 'testuser')

    const passwordInput = screen.getByPlaceholderText('••••••••')
    await user.type(passwordInput, 'password123')

    const submitButton = screen.getByRole('button', { name: /register identity/i })
    await user.click(submitButton)

    await waitFor(() => {
      expect(mockRegister).toHaveBeenCalledWith('test@example.com', 'testuser', 'password123')
    })
  })

  it('shows loading state during submission', async () => {
    const user = userEvent.setup()
    mockLogin.mockImplementation(() => new Promise(resolve => setTimeout(resolve, 100)))

    render(<LoginPage />, { wrapper: createWrapper() })

    const emailInput = screen.getByPlaceholderText('user@sonicvoid.io')
    await user.type(emailInput, 'test@example.com')

    const passwordInput = screen.getByPlaceholderText('••••••••')
    await user.type(passwordInput, 'password123')

    const submitButton = screen.getByRole('button', { name: /enter void/i })
    await user.click(submitButton)

    expect(screen.getByText('Processing...')).toBeInTheDocument()
  })

  it('clears API error when switching modes', async () => {
    const user = userEvent.setup()
    mockLogin.mockRejectedValue({
      response: { data: { detail: 'Invalid credentials' } }
    })

    render(<LoginPage />, { wrapper: createWrapper() })

    // Trigger an error
    const emailInput = screen.getByPlaceholderText('user@sonicvoid.io')
    await user.type(emailInput, 'test@example.com')
    const passwordInput = screen.getByPlaceholderText('••••••••')
    await user.type(passwordInput, 'wrongpassword')
    const submitButton = screen.getByRole('button', { name: /enter void/i })
    await user.click(submitButton)

    await waitFor(() => {
      expect(screen.getAllByText('Invalid credentials').length).toBeGreaterThan(0)
    })

    // Switch to register mode
    await user.click(screen.getByText('Register Identity 👤+'))

    // Error should be cleared or hidden
    const visibleErrors = screen.queryAllByText('Invalid credentials').filter(
      el => !el.className.includes('hidden')
    )
    expect(visibleErrors.length).toBe(0)
  })
})