import { Link } from 'react-router-dom'
import { RiskScore } from '../../../shared/components/RiskScore'
import { StatusBadge } from '../../../shared/components/StatusBadge'
import { formatCurrency, formatDateTime } from '../../../shared/utils/format'
import { TYPE_LABELS } from '../../../shared/utils/labels'
import type { EvaluationResult } from '../types'

const HEADLINES = {
  approved: 'Transacción aprobada',
  review: 'Transacción en revisión',
  suspicious: 'Transacción sospechosa',
}

export function SimulationResult({ result, onReset }: { result: EvaluationResult | null; onReset: () => void }) {
  if (!result) {
    return (
      <article className="card result result--empty">
        <h2 className="card__title">Resultado</h2>
        <p className="muted">
          Llena el formulario y presiona "Simular transacción". La IA calculará el puntaje de riesgo y te dirá por qué.
        </p>
        <ul className="legend-steps">
          <li>
            <span className="badge badge--approved">0 a 39</span> Aprobada
          </li>
          <li>
            <span className="badge badge--review">40 a 69</span> En revisión
          </li>
          <li>
            <span className="badge badge--suspicious">70 a 100</span> Sospechosa
          </li>
        </ul>
      </article>
    )
  }

  const { transaction, reasons, alert_created } = result
  return (
    <article className={`card result result--${transaction.status}`} aria-live="polite">
      <div className="card__header">
        <h2 className="card__title">{HEADLINES[transaction.status]}</h2>
        <StatusBadge status={transaction.status} />
      </div>
      <RiskScore score={transaction.risk_score} status={transaction.status} />
      <p className="result__summary">
        {TYPE_LABELS[transaction.type]} de {formatCurrency(transaction.amount)} · {transaction.user_name} ·{' '}
        {formatDateTime(transaction.created_at)}
      </p>
      <h3 className="section-title">Motivos</h3>
      {reasons.length > 0 ? (
        <ul className="reasons">
          {reasons.map((reason) => (
            <li key={reason}>{reason}</li>
          ))}
        </ul>
      ) : (
        <p className="empty empty--left">Sin señales de riesgo</p>
      )}
      {alert_created && <p className="result__alert">Se creó una alerta para esta transacción</p>}
      <div className="result__actions">
        <Link to={`/transactions/${transaction.id}`} className="btn btn--secondary">
          Ver detalle
        </Link>
        <button type="button" className="btn btn--ghost" onClick={onReset}>
          Limpiar resultado
        </button>
      </div>
    </article>
  )
}
