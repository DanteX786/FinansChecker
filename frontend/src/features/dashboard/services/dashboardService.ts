import { apiClient } from '../../../shared/api/apiClient'
import type { Alert } from '../../../shared/types/transaction'
import type { Stats } from '../types'

export async function getStats(): Promise<Stats> {
  const { data } = await apiClient.get<Stats>('/stats', { params: { days: 14 } })
  return data
}

export async function getRecentAlerts(): Promise<Alert[]> {
  const { data } = await apiClient.get<Alert[]>('/alerts', { params: { limit: 5 } })
  return data
}
