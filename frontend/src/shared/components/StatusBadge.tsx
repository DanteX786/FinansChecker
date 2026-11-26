import type { Status } from '../types/transaction'
import { STATUS_LABELS } from '../utils/labels'

// El estado siempre se muestra con color y texto, nunca solo con color
export function StatusBadge({ status }: { status: Status }) {
  return (
    <span className={`badge badge--${status}`}>
      <span className="badge__dot" aria-hidden="true" />
      {STATUS_LABELS[status]}
    </span>
  )
}
