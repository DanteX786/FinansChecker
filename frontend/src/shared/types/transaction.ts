export type Status = 'approved' | 'review' | 'suspicious'
export type TransactionType = 'transfer' | 'payment' | 'withdrawal' | 'online_purchase'
export type Channel = 'app' | 'web' | 'atm'

export interface Transaction {
  id: number
  user_id: number
  user_name: string
  type: TransactionType
  amount: number
  destination_account: string
  city: string
  channel: Channel
  created_at: string
  risk_score: number
  status: Status
}

export interface Alert {
  id: number
  transaction_id: number
  level: Exclude<Status, 'approved'>
  reasons: string[]
  created_at: string
  user_name: string
  amount: number
  type: TransactionType
  risk_score: number
}
