import { useRequest } from '../../../shared/hooks/useRequest'
import { getTransactionDetail } from '../services/transactionsService'

export function useTransactionDetail(id: string) {
  return useRequest(() => getTransactionDetail(id), [id])
}
