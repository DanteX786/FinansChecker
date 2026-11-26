import { Link } from 'react-router-dom'
import { Icon } from '../../../shared/components/Icon'
import { StatusBadge } from '../../../shared/components/StatusBadge'
import type { Alert } from '../../../shared/types/transaction'
import { formatCurrency, formatDateTime } from '../../../shared/utils/format'
import { TYPE_LABELS } from '../../../shared/utils/labels'

export function AlertCard({ alert }: { alert: Alert }) {
  return (
    <li>
      <Link to={`/transactions/${alert.transaction_id}`} className={`card alert-card alert-card--${alert.level}`}>
        <div className="alert-card__top">
          <StatusBadge status={alert.level} />
          <span className={`score score--${alert.level}`}>{alert.risk_score}/100</span>
        </div>
        <p className="alert-card__title">
          {TYPE_LABELS[alert.type]} de {formatCurrency(alert.amount)}
        </p>
        <p className="alert-card__meta">
          {alert.user_name} · {formatDateTime(alert.created_at)}
        </p>
        <ul className="reasons reasons--compact">
          {alert.reasons.map((reason) => (
            <li key={reason}>{reason}</li>
          ))}
        </ul>
        <span className="alert-card__link">
          Ver detalle <Icon name="arrow" size={14} />
        </span>
      </Link>
    </li>
  )
}
