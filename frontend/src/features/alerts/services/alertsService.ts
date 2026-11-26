import { apiClient } from '../../../shared/api/apiClient'
import type { Alert } from '../../../shared/types/transaction'

export async function getAlerts(): Promise<Alert[]> {
  const { data } = await apiClient.get<Alert[]>('/alerts', { params: { limit: 100 } })
  return data
}
