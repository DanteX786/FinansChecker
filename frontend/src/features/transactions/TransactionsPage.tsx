import { useState } from 'react'
import { PageHeader } from '../../shared/components/PageHeader'
import { RequestStatus } from '../../shared/components/RequestStatus'
import type { Status } from '../../shared/types/transaction'
import { StatusFilter } from './components/StatusFilter'
import { TransactionsTable } from './components/TransactionsTable'
import { useTransactions } from './hooks/useTransactions'

export function TransactionsPage() {
  const [status, setStatus] = useState<Status | null>(null)
  const { data, loading, connecting, error, reload } = useTransactions(status)

  return (
    <>
      <PageHeader title="Transacciones" description="De la más reciente a la más antigua, haz clic en una para ver su detalle" />
      <article className="card">
        <div className="card__header">
          <StatusFilter value={status} onChange={setStatus} />
          {data && <span className="muted">{data.length} resultados</span>}
        </div>
        <RequestStatus loading={loading} connecting={connecting} error={error} onRetry={reload}>
          {data && <TransactionsTable transactions={data} />}
        </RequestStatus>
      </article>
    </>
  )
}
