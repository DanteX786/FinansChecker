import type { Channel, Status, TransactionType } from '../types/transaction'

export const STATUS_LABELS: Record<Status, string> = {
  approved: 'Aprobada',
  review: 'En revisión',
  suspicious: 'Sospechosa',
}

export const TYPE_LABELS: Record<TransactionType, string> = {
  transfer: 'Transferencia',
  payment: 'Pago',
  withdrawal: 'Retiro',
  online_purchase: 'Compra en línea',
}

export const CHANNEL_LABELS: Record<Channel, string> = {
  app: 'App móvil',
  web: 'Web',
  atm: 'Cajero',
}

export const STATUS_COLORS: Record<Status, string> = {
  approved: '#16a34a',
  review: '#f59e0b',
  suspicious: '#dc2626',
}
