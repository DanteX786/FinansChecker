import axios from 'axios'

export interface ApiError {
  message: string
  fieldErrors: Record<string, string>
  isConnectionError: boolean
}

interface ErrorBody {
  message?: string
  errors?: Record<string, string>
}

const CONNECTION_MESSAGE = 'No pudimos conectar con el servidor, intenta de nuevo'
const GENERIC_MESSAGE = 'No pudimos procesar la solicitud, intenta de nuevo'

// Convierte cualquier error en un mensaje entendible, nunca muestra detalles técnicos
export function toApiError(error: unknown): ApiError {
  if (axios.isAxiosError<ErrorBody>(error)) {
    if (!error.response) {
      return { message: CONNECTION_MESSAGE, fieldErrors: {}, isConnectionError: true }
    }
    const { status, data } = error.response
    const isConnectionError = status === 502 || status === 503 || status === 504
    return {
      message: data?.message ?? (isConnectionError ? CONNECTION_MESSAGE : GENERIC_MESSAGE),
      fieldErrors: data?.errors ?? {},
      isConnectionError,
    }
  }
  return { message: GENERIC_MESSAGE, fieldErrors: {}, isConnectionError: false }
}
