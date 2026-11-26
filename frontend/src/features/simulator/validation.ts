import type { FieldErrors, SimulatorValues, TransactionPayload } from './types'

export const MIN_AMOUNT = 1
export const MAX_AMOUNT = 50_000_000

export const CITIES = [
  'Bogotá', 'Medellín', 'Cali', 'Barranquilla', 'Cartagena',
  'Bucaramanga', 'Pereira', 'Manizales', 'Santa Marta', 'Cúcuta',
]

// Validación del formulario antes de enviarlo, la del backend es la que manda
export function validate(values: SimulatorValues): FieldErrors {
  const errors: FieldErrors = {}
  const amount = Number(values.amount)

  if (!values.userId) errors.userId = 'Selecciona un usuario'
  if (!values.amount || Number.isNaN(amount) || amount < MIN_AMOUNT || amount > MAX_AMOUNT) {
    errors.amount = 'El monto debe estar entre $1 y $50.000.000'
  }
  if (!/^\d{6,20}$/.test(values.destinationAccount.trim())) {
    errors.destinationAccount = 'La cuenta destino debe tener entre 6 y 20 dígitos'
  }
  if (!values.city.trim()) errors.city = 'Selecciona una ciudad'
  if (values.createdAt && new Date(values.createdAt).getTime() > Date.now() + 5 * 60 * 1000) {
    errors.createdAt = 'La fecha no puede estar en el futuro'
  }
  return errors
}

export function toPayload(values: SimulatorValues): TransactionPayload {
  return {
    user_id: Number(values.userId),
    type: values.type,
    amount: Number(values.amount),
    destination_account: values.destinationAccount.trim(),
    city: values.city,
    channel: values.channel,
    ...(values.createdAt ? { created_at: `${values.createdAt}:00` } : {}),
  }
}

// Los nombres de campo del backend se traducen a los del formulario
const API_FIELDS: Record<string, keyof SimulatorValues> = {
  user_id: 'userId',
  type: 'type',
  amount: 'amount',
  destination_account: 'destinationAccount',
  city: 'city',
  channel: 'channel',
  created_at: 'createdAt',
}

export function fromApiErrors(errors: Record<string, string>): FieldErrors {
  const result: FieldErrors = {}
  for (const [field, message] of Object.entries(errors)) {
    const key = API_FIELDS[field]
    if (key) result[key] = message
  }
  return result
}
