import { Link, useParams } from 'react-router-dom'
import { Icon } from '../../shared/components/Icon'
import { PageHeader } from '../../shared/components/PageHeader'
import { RequestStatus } from '../../shared/components/RequestStatus'
import { RiskScore } from '../../shared/components/RiskScore'
import { StatusBadge } from '../../shared/components/StatusBadge'
import { formatCurrency, formatDateTime } from '../../shared/utils/format'
import { CHANNEL_LABELS, TYPE_LABELS } from '../../shared/utils/labels'
import { useTransactionDetail } from './hooks/useTransactionDetail'

export function TransactionDetailPage() {
  const { id = '' } = useParams()
  const { data, loading, connecting, error, reload } = useTransactionDetail(id)

  return (
    <>
      <Link to="/transactions" className="back-link">
        <Icon name="back" size={16} />
        Volver a transacciones
      </Link>
      <PageHeader title={`Transacción #${id}`} description="Resultado del análisis de riesgo" />
      <RequestStatus loading={loading} connecting={connecting} error={error} onRetry={reload}>
        {data && (
          <div className="detail-grid">
            <article className="card">
              <div className="card__header">
                <h2 className="card__title">Puntaje de riesgo</h2>
                <StatusBadge status={data.transaction.status} />
              </div>
              <RiskScore score={data.transaction.risk_score} status={data.transaction.status} />
              <h3 className="section-title">Motivos</h3>
              {data.reasons.length > 0 ? (
                <ul className="reasons">
                  {data.reasons.map((reason) => (
                    <li key={reason}>{reason}</li>
                  ))}
                </ul>
              ) : (
                <p className="empty empty--left">Sin señales de riesgo, la transacción fue aprobada</p>
              )}
            </article>
            <article className="card">
              <h2 className="card__title">Datos de la transacción</h2>
              <dl className="info-list">
                <div>
                  <dt>Usuario</dt>
                  <dd>{data.transaction.user_name}</dd>
                </div>
                <div>
                  <dt>Ciudad habitual</dt>
                  <dd>{data.user_city}</dd>
                </div>
                <div>
                  <dt>Tipo</dt>
                  <dd>{TYPE_LABELS[data.transaction.type]}</dd>
                </div>
                <div>
                  <dt>Monto</dt>
                  <dd>{formatCurrency(data.transaction.amount)}</dd>
                </div>
                <div>
                  <dt>Cuenta destino</dt>
                  <dd className="mono">{data.transaction.destination_account}</dd>
                </div>
                <div>
                  <dt>Ciudad</dt>
                  <dd>{data.transaction.city}</dd>
                </div>
                <div>
                  <dt>Canal</dt>
                  <dd>{CHANNEL_LABELS[data.transaction.channel]}</dd>
                </div>
                <div>
                  <dt>Fecha y hora</dt>
                  <dd>{formatDateTime(data.transaction.created_at)}</dd>
                </div>
              </dl>
            </article>
          </div>
        )}
      </RequestStatus>
    </>
  )
}
