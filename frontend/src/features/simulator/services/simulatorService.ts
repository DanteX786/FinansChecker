import { apiClient } from '../../../shared/api/apiClient'
import type { EvaluationResult, SimUser, TransactionPayload } from '../types'

export async function getUsers(): Promise<SimUser[]> {
  const { data } = await apiClient.get<SimUser[]>('/users')
  return data
}

export async function simulateTransaction(payload: TransactionPayload): Promise<EvaluationResult> {
  const { data } = await apiClient.post<EvaluationResult>('/transactions', payload)
  return data
}
