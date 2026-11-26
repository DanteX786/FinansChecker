import { useRequest } from '../../../shared/hooks/useRequest'
import type { Status } from '../../../shared/types/transaction'
import { getTransactions } from '../services/transactionsService'

export function useTransactions(status: Status | null) {
  return useRequest(() => getTransactions(status), [status])
}
