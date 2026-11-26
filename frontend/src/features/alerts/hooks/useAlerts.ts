import { useRequest } from '../../../shared/hooks/useRequest'
import { getAlerts } from '../services/alertsService'

export function useAlerts() {
  return useRequest(getAlerts)
}
