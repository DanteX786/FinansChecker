import type { Status } from '../../../shared/types/transaction'
import { STATUS_LABELS } from '../../../shared/utils/labels'

const OPTIONS: { value: Status | null; label: string }[] = [
  { value: null, label: 'Todas' },
  { value: 'approved', label: STATUS_LABELS.approved },
  { value: 'review', label: STATUS_LABELS.review },
  { value: 'suspicious', label: STATUS_LABELS.suspicious },
]

interface StatusFilterProps {
  value: Status | null
  onChange: (value: Status | null) => void
}

export function StatusFilter({ value, onChange }: StatusFilterProps) {
  return (
    <div className="chips" role="group" aria-label="Filtrar por estado">
      {OPTIONS.map((option) => (
        <button
          key={option.label}
          type="button"
          className={`chip ${option.value ? `chip--${option.value}` : ''}`}
          aria-pressed={value === option.value}
          onClick={() => onChange(option.value)}
        >
          {option.label}
        </button>
      ))}
    </div>
  )
}
