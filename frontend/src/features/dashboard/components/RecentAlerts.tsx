import { Link } from 'react-router-dom'
import { Icon } from '../../../shared/components/Icon'
import { StatusBadge } from '../../../shared/components/StatusBadge'
import type { Alert } from '../../../shared/types/transaction'
import { formatCurrency, formatDateTime } from '../../../shared/utils/format'

export function RecentAlerts({ alerts }: { alerts: Alert[] }) {
  return (
    <article className="card">
      <div className="card__header">
        <div>
          <h2 className="card__title">Últimas alertas</h2>
          <p className="card__subtitle">Transacciones en revisión o sospechosas</p>
        </div>
        <Link to="/alerts" className="link">
          Ver todas
        </Link>
      </div>
      {alerts.length === 0 ? (
        <p className="empty">No hay alertas por ahora</p>
      ) : (
        <ul className="mini-list">
          {alerts.map((alert) => (
            <li key={alert.id}>
              <Link to={`/transactions/${alert.transaction_id}`} className="mini-list__item">
                <div className="mini-list__main">
                  <span className="mini-list__title">{alert.user_name}</span>
                  <span className="mini-list__meta">
                    {formatCurrency(alert.amount)} · {formatDateTime(alert.created_at)}
                  </span>
                  <span className="mini-list__reason">{alert.reasons[0]}</span>
                </div>
                <StatusBadge status={alert.level} />
                <Icon name="arrow" size={16} />
              </Link>
            </li>
          ))}
        </ul>
      )}
    </article>
  )
}
