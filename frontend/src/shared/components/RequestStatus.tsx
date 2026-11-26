import type { ReactNode } from 'react'
import type { ApiError } from '../api/apiError'
import { Icon } from './Icon'

interface RequestStatusProps {
  loading: boolean
  connecting: boolean
  error: ApiError | null
  onRetry: () => void
  children: ReactNode
}

// Muestra carga, reconexión o error, así ninguna vista se queda en blanco
export function RequestStatus({ loading, connecting, error, onRetry, children }: RequestStatusProps) {
  if (error) {
    return (
      <div className="state state--error" role="alert">
        <p>{error.message}</p>
        <button type="button" className="btn btn--secondary" onClick={onRetry}>
          <Icon name="refresh" size={16} />
          Reintentar
        </button>
      </div>
    )
  }
  if (loading) {
    return (
      <div className="state" role="status">
        <span className="spinner" aria-hidden="true" />
        <p>{connecting ? 'Conectando con el servidor…' : 'Cargando…'}</p>
        {connecting && <p className="state__hint">El servidor puede tardar hasta un minuto en despertar</p>}
      </div>
    )
  }
  return <>{children}</>
}
