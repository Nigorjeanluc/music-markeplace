import { useState, useCallback } from 'react'
import { useUploadImage } from '../hooks/useApi'

interface ImageUploadProps {
  label: string
  folder?: string
  currentUrl?: string
  onUploaded?: (url: string) => void
}

export default function ImageUpload({ label, folder = 'general', currentUrl, onUploaded }: ImageUploadProps) {
  const upload = useUploadImage()
  const [preview, setPreview] = useState<string | null>(null)
  const [error, setError] = useState(false)

  const currentSrc = preview ?? currentUrl ?? null

  const processFile = useCallback((file: File) => {
    if (!file.type.startsWith('image/')) {
      setError(true)
      return
    }
    setError(false)
    const objectUrl = URL.createObjectURL(file)
    setPreview(objectUrl)
    upload.mutateAsync({ file, folder })
      .then((data: { url: string }) => {
        onUploaded?.(data.url)
      })
      .catch(() => {
        setError(true)
        setPreview(null)
      })
  }, [folder, upload, onUploaded])

  const handleInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (file) processFile(file)
  }

  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault()
    const file = e.dataTransfer.files?.[0]
    if (file) processFile(file)
  }

  return (
    <div className="space-y-2">
      <label className="block text-[10px] tracking-widest text-[#8a8b9a] uppercase">{label}</label>
      <div
        className={`border-2 border-dashed rounded-lg p-6 text-center cursor-pointer transition-colors ${
          error ? 'border-red-500 bg-red-900/20' : 'border-[#2a2b38] hover:border-[#00e5ff] bg-[#12131a]'
        }`}
        onDrop={handleDrop}
        onDragOver={e => e.preventDefault()}
        onClick={() => document.getElementById('image-upload-input')?.click()}
      >
        {currentSrc ? (
          <img src={currentSrc} alt="preview" className="max-h-32 mx-auto rounded" />
        ) : (
          <p className="text-[#4a4b5a] text-sm">Drop image or click to select</p>
        )}
        {upload.isPending && (
          <p className="text-[#00e5ff] text-xs mt-2">Uploading...</p>
        )}
        {error && (
          <p className="text-red-400 text-xs mt-2">Upload failed — check S3 config</p>
        )}
        <input
          id="image-upload-input"
          type="file"
          accept="image/*"
          className="hidden"
          onChange={handleInput}
          aria-label="Upload image file"
        />
      </div>
    </div>
  )
}
