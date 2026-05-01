import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Formik, Form, useField } from 'formik'
import * as Yup from 'yup'
import { useAuth } from '../context/AuthContext'

// ── Inline field (styled for login page) ─────────────────────────────────────

function LoginField({
  name, label, type = 'text', placeholder, prefix,
}: {
  name: string; label: string; type?: string; placeholder: string; prefix: string
}) {
  const [field, meta] = useField(name)
  const hasError = meta.touched && meta.error
  return (
    <div>
      <label className="block text-[10px] tracking-[0.15em] text-[#8a8b9a] uppercase mb-2">{label}</label>
      <div className={`flex items-center bg-[#0d0e14] border rounded px-3 py-2.5 gap-2 transition-colors ${hasError ? 'border-red-500' : 'border-[#2a2b38] focus-within:border-[#00e5ff]'}`}>
        <span className="text-[#4a4b5a]">{prefix}</span>
        <input
          {...field}
          type={type}
          placeholder={placeholder}
          className="bg-transparent text-white text-sm placeholder-[#4a4b5a] outline-none w-full"
        />
      </div>
      {hasError && <p className="text-red-400 text-xs mt-1">{meta.error}</p>}
    </div>
  )
}

// ── Schemas ───────────────────────────────────────────────────────────────────

const loginSchema = Yup.object({
  email: Yup.string().email('Invalid email').required('Required'),
  password: Yup.string().min(4, 'Min 4 characters').required('Required'),
})

const registerSchema = Yup.object({
  email: Yup.string().email('Invalid email').required('Required'),
  username: Yup.string().min(3, 'Min 3 characters').max(30, 'Max 30 characters').required('Required'),
  password: Yup.string().min(6, 'Min 6 characters').required('Required'),
})

// ── Page ──────────────────────────────────────────────────────────────────────

export default function LoginPage() {
  const { login, register } = useAuth()
  const navigate = useNavigate()
  const [mode, setMode] = useState<'login' | 'register'>('login')
  const [apiError, setApiError] = useState('')

  const isLogin = mode === 'login'

  return (
    <div
      className="min-h-screen bg-[#0d0e14] flex flex-col"
      style={{ background: 'radial-gradient(ellipse at 20% 60%, #0d2a2a 0%, transparent 50%), radial-gradient(ellipse at 80% 40%, #1a0a2e 0%, transparent 50%), #0d0e14' }}
    >
      <header className="flex items-center justify-between px-8 py-5">
        <span className="font-black tracking-tight text-lg select-none">
          <span style={{ background: 'linear-gradient(135deg, #00e5ff 0%, #00b8cc 50%, #aa3bff 100%)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent', backgroundClip: 'text' }}>
            Music
          </span>
          <span className="text-white font-light tracking-widest text-sm ml-1 uppercase">Marketplace</span>
        </span>
        <nav className="flex gap-6 text-sm text-[#8a8b9a]">
          <a href="#" className="hover:text-white transition-colors">Support</a>
          <a href="#" className="hover:text-white transition-colors">Network Status</a>
        </nav>
      </header>

      <div className="flex-1 flex items-center justify-center px-4">
        <div className="w-full max-w-md bg-[#12131a] border border-[#2a2b38] rounded-xl p-8">
          <div className="text-center mb-8">
            <h1 className="text-white text-xl font-medium mb-2">Welcome Back</h1>
            <p className="text-[#8a8b9a] text-sm">Access the high-fidelity soundscape.</p>
          </div>

          <Formik
            key={mode}
            initialValues={isLogin
              ? { email: '', password: '' }
              : { email: '', username: '', password: '' }
            }
            validationSchema={isLogin ? loginSchema : registerSchema}
            onSubmit={async (values, { setSubmitting }) => {
              setApiError('')
              try {
                if (isLogin) {
                  await login(values.email, values.password)
                } else {
                  await register(values.email, (values as { username: string }).username, values.password)
                }
                navigate('/')
              } catch (e: unknown) {
                setApiError(
                  (e as { response?: { data?: { detail?: string } } })?.response?.data?.detail ?? 'Invalid credentials'
                )
              } finally {
                setSubmitting(false)
              }
            }}
          >
            {({ isSubmitting }) => (
              <Form className="space-y-5">
                <LoginField name="email" label="Identity Code" type="email" placeholder="user@sonicvoid.io" prefix="@" />

                {!isLogin && (
                  <LoginField name="username" label="Username" placeholder="your_handle" prefix="👤" />
                )}

                <LoginField name="password" label="Secure Key" type="password" placeholder="••••••••" prefix="🔒" />

                {isLogin && (
                  <div className="flex items-center justify-between text-sm">
                    <label className="flex items-center gap-2 text-[#8a8b9a] cursor-pointer">
                      <input type="checkbox" className="accent-[#00e5ff]" />
                      Remember node
                    </label>
                    <a href="#" className="text-[#aa3bff] hover:text-purple-300 transition-colors">Forgot Key?</a>
                  </div>
                )}

                {apiError && <p className="text-red-400 text-xs text-center">{apiError}</p>}

                <button
                  type="submit"
                  disabled={isSubmitting}
                  className="w-full border border-[#00e5ff] text-[#00e5ff] py-3 rounded text-sm tracking-[0.15em] uppercase hover:bg-[#00e5ff]/10 transition-colors disabled:opacity-50"
                >
                  {isSubmitting ? 'Processing...' : isLogin ? 'Enter Void →' : 'Register Identity →'}
                </button>

                <div className="flex items-center gap-3 text-[#4a4b5a] text-xs">
                  <div className="flex-1 h-px bg-[#2a2b38]" />OR<div className="flex-1 h-px bg-[#2a2b38]" />
                </div>

                <button
                  type="button"
                  onClick={() => { setMode(isLogin ? 'register' : 'login'); setApiError('') }}
                  className="w-full border border-[#aa3bff] text-[#aa3bff] py-3 rounded text-sm tracking-[0.15em] uppercase hover:bg-[#aa3bff]/10 transition-colors"
                >
                  {isLogin ? 'Register Identity 👤+' : '← Back to Login'}
                </button>
              </Form>
            )}
          </Formik>

          {isLogin && (
            <p className="text-[#4a4b5a] text-xs text-center mt-4">
              Seeded: <span className="text-[#00e5ff]">admin@musicmarket.com</span> / <span className="text-[#00e5ff]">john@musicmarket.com</span>
              {' '}— password: <span className="text-[#8a8b9a]">admin123 / password123</span>
            </p>
          )}
        </div>
      </div>

      <footer className="flex justify-center gap-8 py-4 text-[#4a4b5a] text-xs">
        <span>🛡 AES-256 Encrypted</span>
        <span>🛡 Sonic Protocol V.4</span>
      </footer>
    </div>
  )
}
