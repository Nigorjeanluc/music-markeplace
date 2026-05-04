import { createContext, useContext, useState, useCallback, type ReactNode } from 'react'

type ToastType = 'success' | 'error' | 'info'

interface Toast {
  id: number
  message: string
  type: ToastType
}

interface ToastCtx {
  toast: (message: string, type?: ToastType) => void
}

const ToastContext = createContext<ToastCtx>({ toast: () => {} })

let _id = 0

export function ToastProvider({ children }: { children: ReactNode }) {
  const [toasts, setToasts] = useState<Toast[]>([])

  const toast = useCallback((message: string, type: ToastType = 'error') => {
    const id = ++_id
    setToasts(prev => [...prev, { id, message, type }])
    setTimeout(() => setToasts(prev => prev.filter(t => t.id !== id)), 4000)
  }, [])

  const dismiss = (id: number) => setToasts(prev => prev.filter(t => t.id !== id))

  return (
    <ToastContext.Provider value={{ toast }}>
      {children}
      <div className="fixed bottom-5 right-5 z-[100] flex flex-col gap-2 max-w-sm w-full pointer-events-none">
        {toasts.map(t => (
          <div
            key={t.id}
            className={`pointer-events-auto flex items-start gap-3 px-4 py-3 rounded-lg border text-sm shadow-lg animate-fade-in
              ${t.type === 'error' ? 'bg-[#1a0a0a] border-red-500/40 text-red-400' : ''}
              ${t.type === 'success' ? 'bg-[#0a1a0a] border-[#00e5ff]/40 text-[#00e5ff]' : ''}
              ${t.type === 'info' ? 'bg-[#12131a] border-[#2a2b38] text-[#8a8b9a]' : ''}
            `}
          >
            <span className="flex-shrink-0 mt-0.5">
              {t.type === 'error' && '✕'}
              {t.type === 'success' && '✓'}
              {t.type === 'info' && 'ℹ'}
            </span>
            <span className="flex-1 leading-snug">{t.message}</span>
            <button
              onClick={() => dismiss(t.id)}
              className="flex-shrink-0 text-current opacity-50 hover:opacity-100 transition-opacity leading-none"
            >
              ✕
            </button>
          </div>
        ))}
      </div>
    </ToastContext.Provider>
  )
}

export const useToast = () => useContext(ToastContext)
