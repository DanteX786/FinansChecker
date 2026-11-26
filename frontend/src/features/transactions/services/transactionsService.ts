import { apiClient } from '../../../shared/api/apiClient'
import type { Status, Transaction } from '../../../shared/types/transaction'
import type { TransactionDetail } from '../types'

export async function getTransactions(status: Status | null): Promise<Transaction[]> {
  const { data } = await apiClient.get<Transaction[]>('/transactions', {
    params: { limit: 200, ...(status ? { status } : {}) },
  })
  return data
}

export async function getTransactionDetail(id: string): Promise<TransactionDetail> {
  const { data } = await apiClient.get<TransactionDetail>(`/transactions/${id}`)
  return data
}
