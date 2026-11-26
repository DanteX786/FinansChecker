import { useRequest } from '../../../shared/hooks/useRequest'
import { getRecentAlerts, getStats } from '../services/dashboardService'

export function useDashboard() {
  return useRequest(async () => {
    const [stats, alerts] = await Promise.all([getStats(), getRecentAlerts()])
    return { stats, alerts }
  })
}
