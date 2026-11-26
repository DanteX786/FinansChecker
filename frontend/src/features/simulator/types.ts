import type { Channel, Transaction, TransactionType } from '../../shared/types/transaction'

export interface SimUser {
  id: number
  name: string
  city: string
  average_amount: number
  transaction_count: number
  usual_destination: string | null
}

export interface SimulatorValues {
  userId: string
  type: TransactionType
  amount: string
  destinationAccount: string
  city: string
  channel: Channel
  createdAt: string
}

export interface TransactionPayload {
  user_id: number
  type: TransactionType
  amount: number
  destination_account: string
  city: string
  channel: Channel
  created_at?: string
}

export interface EvaluationResult {
  transaction: Transaction
  reasons: string[]
  alert_created: boolean
}

export type FieldErrors = Partial<Record<keyof SimulatorValues, string>>
