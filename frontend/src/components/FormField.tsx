import { useField } from 'formik'
import type { InputHTMLAttributes, SelectHTMLAttributes } from 'react'

const inputCls = 'w-full bg-[#0d0e14] border rounded px-3 py-2 text-white text-sm outline-none transition-colors placeholder-[#4a4b5a]'
const labelCls = 'block text-[10px] tracking-widest text-[#8a8b9a] uppercase mb-1'
const errorCls = 'text-red-400 text-xs mt-1'

interface FieldProps extends InputHTMLAttributes<HTMLInputElement> {
  name: string
  label: string
  prefix?: string
}

export function FormField({ name, label, prefix, ...props }: FieldProps) {
  const [field, meta] = useField(name)
  const hasError = meta.touched && meta.error
  return (
    <div>
      <label className={labelCls}>{label}</label>
      <div className={`flex items-center bg-[#0d0e14] border rounded gap-2 px-3 py-2 transition-colors ${hasError ? 'border-red-500' : 'border-[#2a2b38] focus-within:border-[#00e5ff]'}`}>
        {prefix && <span className="text-[#4a4b5a] text-sm flex-shrink-0">{prefix}</span>}
        <input {...field} {...props} className="bg-transparent text-white text-sm outline-none w-full placeholder-[#4a4b5a]" />
      </div>
      {hasError && <p className={errorCls}>{meta.error}</p>}
    </div>
  )
}

interface SelectFieldProps extends SelectHTMLAttributes<HTMLSelectElement> {
  name: string
  label: string
  children: React.ReactNode
}

export function SelectField({ name, label, children, ...props }: SelectFieldProps) {
  const [field, meta] = useField(name)
  const hasError = meta.touched && meta.error
  return (
    <div>
      <label className={labelCls}>{label}</label>
      <select
        {...field}
        {...props}
        className={`${inputCls} ${hasError ? 'border-red-500' : 'border-[#2a2b38] focus:border-[#00e5ff]'}`}
      >
        {children}
      </select>
      {hasError && <p className={errorCls}>{meta.error}</p>}
    </div>
  )
}
