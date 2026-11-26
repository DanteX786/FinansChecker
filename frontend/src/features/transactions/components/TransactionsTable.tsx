import { useNavigate } from 'react-router-dom'
import { StatusBadge } from '../../../shared/components/StatusBadge'
import type { Transaction } from '../../../shared/types/transaction'
import { formatCurrency, formatDateTime } from '../../../shared/utils/format'
import { TYPE_LABELS } from '../../../shared/utils/labels'

export function TransactionsTable({ transactions }: { transactions: Transaction[] }) {
  const navigate = useNavigate()

  if (transactions.length === 0) {
    return <p className="empty">No hay transacciones con este filtro</p>
  }

  return (
    <div className="table-wrap">
      <table className="table">
        <thead>
          <tr>
            <th scope="col">Fecha</th>
            <th scope="col">Usuario</th>
            <th scope="col">Tipo</th>
            <th scope="col" className="num">
              Monto
            </th>
            <th scope="col" className="num">
              Puntaje
            </th>
            <th scope="col">Estado</th>
          </tr>
        </thead>
        <tbody>
          {transactions.map((tx) => {
            const open = () => navigate(`/transactions/${tx.id}`)
            return (
              <tr
                key={tx.id}
                className={`table__row table__row--${tx.status}`}
                tabIndex={0}
                aria-label={`Ver detalle de la transacción ${tx.id}`}
                onClick={open}
                onKeyDown={(e) => {
                  if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault()
                    open()
                  }
                }}
              >
                <td className="nowrap">{formatDateTime(tx.created_at)}</td>
                <td>{tx.user_name}</td>
                <td>{TYPE_LABELS[tx.type]}</td>
                <td className="num nowrap">{formatCurrency(tx.amount)}</td>
                <td className="num">
                  <span className={`score score--${tx.status}`}>{tx.risk_score}</span>
                </td>
                <td>
                  <StatusBadge status={tx.status} />
                </td>
              </tr>
            )
          })}
        </tbody>
      </table>
    </div>
  )
}
