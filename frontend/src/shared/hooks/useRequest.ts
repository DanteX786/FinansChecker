import { useCallback, useEffect, useRef, useState } from 'react'
import { toApiError, type ApiError } from '../api/apiError'

// El backend gratuito de Render puede tardar hasta un minuto en despertar,
// por eso los errores de conexión se reintentan antes de mostrar el error
const RETRY_DELAYS_MS = [3000, 6000, 10000, 15000, 20000]

export interface RequestState<T> {
  data: T | null
  loading: boolean
  connecting: boolean
  error: ApiError | null
  reload: () => void
}

export function useRequest<T>(fetcher: () => Promise<T>, deps: unknown[] = []): RequestState<T> {
  const [data, setData] = useState<T | null>(null)
  const [loading, setLoading] = useState(true)
  const [connecting, setConnecting] = useState(false)
  const [error, setError] = useState<ApiError | null>(null)
  const [attempt, setAttempt] = useState(0)
  const fetcherRef = useRef(fetcher)
  fetcherRef.current = fetcher

  useEffect(() => {
    let cancelled = false
    let timer: ReturnType<typeof setTimeout> | undefined

    const run = async (retry: number) => {
      try {
        const result = await fetcherRef.current()
        if (cancelled) return
        setData(result)
        setError(null)
        setConnecting(false)
        setLoading(false)
      } catch (err) {
        if (cancelled) return
        const apiError = toApiError(err)
        if (apiError.isConnectionError && retry < RETRY_DELAYS_MS.length) {
          setConnecting(true)
          timer = setTimeout(() => run(retry + 1), RETRY_DELAYS_MS[retry])
          return
        }
        setError(apiError)
        setConnecting(false)
        setLoading(false)
      }
    }

    setLoading(true)
    setError(null)
    run(0)
    return () => {
      cancelled = true
      if (timer) clearTimeout(timer)
    }
  }, [...deps, attempt])

  const reload = useCallback(() => setAttempt((n) => n + 1), [])

  return { data, loading, connecting, error, reload }
}
