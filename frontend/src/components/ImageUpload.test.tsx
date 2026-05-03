import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, it, expect, vi, beforeEach } from 'vitest'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { ImageUpload } from '../pages/ManagementPage'
import { useUploadImage } from '../hooks/useApi'

// Mock the upload hook
vi.mock('../hooks/useApi', () => ({
  useUploadImage: vi.fn(),
}))

const createWrapper = () => {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: { retry: false },
      mutations: { retry: false },
    },
  })
  return ({ children }: { children: React.ReactNode }) => (
    <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
  )
}

describe('ImageUpload', () => {
  const mockOnUploaded = vi.fn()
  const mockMutateAsync = vi.fn()

  beforeEach(() => {
    vi.clearAllMocks()
    vi.mocked(useUploadImage).mockReturnValue({
      mutateAsync: mockMutateAsync,
      isPending: false,
      isError: false,
    } as any)
  })

  it('renders with label and placeholder', () => {
    render(
      <ImageUpload
        label="Test Image"
        folder="test"
        onUploaded={mockOnUploaded}
      />,
      { wrapper: createWrapper() }
    )

    expect(screen.getByText('Test Image')).toBeInTheDocument()
    expect(screen.getByText('Drop image or click to select')).toBeInTheDocument()
    expect(screen.getByLabelText('Upload image file')).toBeInTheDocument()
  })

  it('shows current image when currentUrl is provided', () => {
    render(
      <ImageUpload
        label="Test Image"
        folder="test"
        currentUrl="https://example.com/image.jpg"
        onUploaded={mockOnUploaded}
      />,
      { wrapper: createWrapper() }
    )

    const img = screen.getByAltText('preview')
    expect(img).toBeInTheDocument()
    expect(img).toHaveAttribute('src', 'https://example.com/image.jpg')
  })

  it('handles file selection via input', async () => {
    const user = userEvent.setup()
    const mockFile = new File(['test'], 'test.jpg', { type: 'image/jpeg' })
    mockMutateAsync.mockResolvedValue({ url: 'https://example.com/uploaded.jpg' })

    render(
      <ImageUpload
        label="Test Image"
        folder="test"
        onUploaded={mockOnUploaded}
      />,
      { wrapper: createWrapper() }
    )

    const input = screen.getByLabelText('Upload image file')
    await user.upload(input, mockFile)

    await waitFor(() => {
      expect(mockMutateAsync).toHaveBeenCalledWith({
        file: mockFile,
        folder: 'test',
      })
      expect(mockOnUploaded).toHaveBeenCalledWith('https://example.com/uploaded.jpg')
    })
  })

  it('handles drag and drop', async () => {
    const mockFile = new File(['test'], 'test.jpg', { type: 'image/jpeg' })
    mockMutateAsync.mockResolvedValue({ url: 'https://example.com/uploaded.jpg' })

    render(
      <ImageUpload
        label="Test Image"
        folder="test"
        onUploaded={mockOnUploaded}
      />,
      { wrapper: createWrapper() }
    )

    const dropZone = screen.getByText('Drop image or click to select').closest('div')

    // Simulate drag over
    fireEvent.dragOver(dropZone!, {
      dataTransfer: {
        files: [mockFile],
      },
    })

    // Simulate drop
    fireEvent.drop(dropZone!, {
      dataTransfer: {
        files: [mockFile],
      },
    })

    await waitFor(() => {
      expect(mockMutateAsync).toHaveBeenCalledWith({
        file: mockFile,
        folder: 'test',
      })
      expect(mockOnUploaded).toHaveBeenCalledWith('https://example.com/uploaded.jpg')
    })
  })

  it('shows preview when file is selected', async () => {
    const user = userEvent.setup()
    const mockFile = new File(['test'], 'test.jpg', { type: 'image/jpeg' })
    mockMutateAsync.mockResolvedValue({ url: 'https://example.com/uploaded.jpg' })

    // Mock URL.createObjectURL
    vi.stubGlobal('URL', { ...globalThis.URL, createObjectURL: vi.fn(() => 'blob:test-url') })

    render(
      <ImageUpload
        label="Test Image"
        folder="test"
        onUploaded={mockOnUploaded}
      />,
      { wrapper: createWrapper() }
    )

    const input = screen.getByLabelText('Upload image file')
    await user.upload(input, mockFile)

    await waitFor(() => {
      const img = screen.getByAltText('preview')
      expect(img).toHaveAttribute('src', 'blob:test-url')
    })
  })

  it('shows loading state during upload', () => {
    vi.mocked(useUploadImage).mockReturnValue({
      mutateAsync: mockMutateAsync,
      isPending: true,
      isError: false,
    } as any)

    render(
      <ImageUpload
        label="Test Image"
        folder="test"
        onUploaded={mockOnUploaded}
      />,
      { wrapper: createWrapper() }
    )

    expect(screen.getByText('Uploading...')).toBeInTheDocument()
    expect(screen.getByText('⏳')).toBeInTheDocument()
  })

  it('shows error state when upload fails', () => {
    vi.mocked(useUploadImage).mockReturnValue({
      mutateAsync: mockMutateAsync,
      isPending: false,
      isError: true,
    } as any)

    render(
      <ImageUpload
        label="Test Image"
        folder="test"
        onUploaded={mockOnUploaded}
      />,
      { wrapper: createWrapper() }
    )

    expect(screen.getByText('Upload failed — check S3 config')).toBeInTheDocument()
  })

  it('reverts preview on upload failure', async () => {
    const user = userEvent.setup()
    const mockFile = new File(['test'], 'test.jpg', { type: 'image/jpeg' })
    mockMutateAsync.mockRejectedValue(new Error('Upload failed'))

    vi.stubGlobal('URL', { ...globalThis.URL, createObjectURL: vi.fn(() => 'blob:test-url') })

    render(
      <ImageUpload
        label="Test Image"
        folder="test"
        currentUrl="https://example.com/current.jpg"
        onUploaded={mockOnUploaded}
      />,
      { wrapper: createWrapper() }
    )

    const input = screen.getByLabelText('Upload image file')
    await user.upload(input, mockFile)

    // Should revert to current URL on error
    await waitFor(() => {
      expect(screen.getByAltText('preview')).toHaveAttribute('src', 'https://example.com/current.jpg')
    })
  })

  it('ignores non-image files', async () => {
    const user = userEvent.setup()
    const mockFile = new File(['test'], 'test.txt', { type: 'text/plain' })

    render(
      <ImageUpload
        label="Test Image"
        folder="test"
        onUploaded={mockOnUploaded}
      />,
      { wrapper: createWrapper() }
    )

    const input = screen.getByLabelText('Upload image file')
    await user.upload(input, mockFile)

    expect(mockMutateAsync).not.toHaveBeenCalled()
    expect(mockOnUploaded).not.toHaveBeenCalled()
  })
})