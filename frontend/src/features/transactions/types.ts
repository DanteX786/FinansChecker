import type { Transaction } from '../../shared/types/transaction'

export interface TransactionDetail {
  transaction: Transaction
  user_city: string
  reasons: string[]
}
