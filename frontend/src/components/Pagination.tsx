interface PaginationProps {
  page: number
  totalPages: number
  onPageChange: (page: number) => void
  className?: string
}

export default function Pagination({ page, totalPages, onPageChange, className = '' }: PaginationProps) {
  if (totalPages <= 1) return null

  const getVisiblePages = () => {
    const delta = 2
    const pages: (number | string)[] = []

    for (let i = 1; i <= totalPages; i++) {
      if (
        i === 1 ||
        i === totalPages ||
        (i >= page - delta && i <= page + delta)
      ) {
        pages.push(i)
      } else if (pages[pages.length - 1] !== '...') {
        pages.push('...')
      }
    }

    return pages
  }

  return (
    <div className={`flex items-center justify-center gap-1 ${className}`}>
      <button
        onClick={() => onPageChange(page - 1)}
        disabled={page <= 1}
        className="px-3 py-1.5 text-xs border border-[#2a2b38] rounded text-[#8a8b9a] hover:border-[#4a4b5a] hover:text-white disabled:opacity-30 disabled:cursor-not-allowed transition-colors"
      >
        ← Prev
      </button>

      {getVisiblePages().map((p, i) => (
        typeof p === 'string' ? (
          <span key={`ellipsis-${i}`} className="px-2 text-[#4a4b5a] text-xs">...</span>
        ) : (
          <button
            key={p}
            onClick={() => onPageChange(p)}
            className={`w-8 h-8 text-xs rounded transition-colors ${
              p === page
                ? 'bg-[#00e5ff] text-[#0d0e14] font-bold'
                : 'border border-[#2a2b38] text-[#8a8b9a] hover:border-[#4a4b5a] hover:text-white'
            }`}
          >
            {p}
          </button>
        )
      ))}

      <button
        onClick={() => onPageChange(page + 1)}
        disabled={page >= totalPages}
        className="px-3 py-1.5 text-xs border border-[#2a2b38] rounded text-[#8a8b9a] hover:border-[#4a4b5a] hover:text-white disabled:opacity-30 disabled:cursor-not-allowed transition-colors"
      >
        Next →
      </button>

      <span className="ml-4 text-[#4a4b5a] text-xs">
        Page {page} of {totalPages}
      </span>
    </div>
  )
}
