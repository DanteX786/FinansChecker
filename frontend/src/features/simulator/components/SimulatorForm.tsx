import { useState, type FormEvent } from 'react'
import type { Channel, TransactionType } from '../../../shared/types/transaction'
import { formatCurrency } from '../../../shared/utils/format'
import { CHANNEL_LABELS, TYPE_LABELS } from '../../../shared/utils/labels'
import { normalExample, suspiciousExample } from '../examples'
import type { FieldErrors, SimUser, SimulatorValues } from '../types'
import { CITIES } from '../validation'

const EMPTY: SimulatorValues = {
  userId: '',
  type: 'transfer',
  amount: '',
  destinationAccount: '',
  city: '',
  channel: 'app',
  createdAt: '',
}

interface SimulatorFormProps {
  users: SimUser[]
  submitting: boolean
  fieldErrors: FieldErrors
  submitError: string | null
  onSubmit: (values: SimulatorValues) => void
}

export function SimulatorForm({ users, submitting, fieldErrors, submitError, onSubmit }: SimulatorFormProps) {
  const [values, setValues] = useState<SimulatorValues>(EMPTY)
  const selectedUser = users.find((u) => String(u.id) === values.userId)

  const set = <K extends keyof SimulatorValues>(key: K, value: SimulatorValues[K]) =>
    setValues((prev) => ({ ...prev, [key]: value }))

  const selectUser = (userId: string) => {
    const user = users.find((u) => String(u.id) === userId)
    setValues((prev) => ({ ...prev, userId, city: user ? user.city : prev.city }))
  }

  const fillExample = (kind: 'normal' | 'suspicious') => {
    const user = selectedUser ?? users[0]
    if (!user) return
    setValues(kind === 'normal' ? normalExample(user) : suspiciousExample(user))
  }

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault()
    onSubmit(values)
  }

  const error = (key: keyof SimulatorValues) =>
    fieldErrors[key] ? (
      <p className="field__error" id={`${key}-error`}>
        {fieldErrors[key]}
      </p>
    ) : null

  const describedBy = (key: keyof SimulatorValues) => (fieldErrors[key] ? `${key}-error` : undefined)

  return (
    <form className="card form" onSubmit={handleSubmit} noValidate>
      <div className="card__header">
        <h2 className="card__title">Datos de la transacción</h2>
      </div>

      <div className="examples">
        <span className="muted">Ejemplos rápidos:</span>
        <button type="button" className="btn btn--ghost btn--sm" onClick={() => fillExample('normal')}>
          Transacción normal
        </button>
        <button type="button" className="btn btn--ghost btn--sm" onClick={() => fillExample('suspicious')}>
          Transacción sospechosa
        </button>
      </div>

      <div className="field">
        <label htmlFor="userId">Usuario</label>
        <select
          id="userId"
          value={values.userId}
          onChange={(e) => selectUser(e.target.value)}
          aria-invalid={Boolean(fieldErrors.userId)}
          aria-describedby={describedBy('userId')}
        >
          <option value="">Selecciona un usuario</option>
          {users.map((u) => (
            <option key={u.id} value={u.id}>
              {u.name} · {u.city}
            </option>
          ))}
        </select>
        {selectedUser && (
          <p className="field__hint">
            Promedio {formatCurrency(selectedUser.average_amount)} · {selectedUser.transaction_count} transacciones
            {selectedUser.usual_destination && <> · cuenta habitual {selectedUser.usual_destination}</>}
          </p>
        )}
        {error('userId')}
      </div>

      <div className="form__row">
        <div className="field">
          <label htmlFor="type">Tipo de transacción</label>
          <select id="type" value={values.type} onChange={(e) => set('type', e.target.value as TransactionType)}>
            {Object.entries(TYPE_LABELS).map(([value, label]) => (
              <option key={value} value={value}>
                {label}
              </option>
            ))}
          </select>
        </div>
        <div className="field">
          <label htmlFor="amount">Monto (COP)</label>
          <input
            id="amount"
            type="number"
            inputMode="numeric"
            min={1}
            max={50000000}
            step={100}
            placeholder="150000"
            value={values.amount}
            onChange={(e) => set('amount', e.target.value)}
            aria-invalid={Boolean(fieldErrors.amount)}
            aria-describedby={describedBy('amount')}
          />
          {error('amount')}
        </div>
      </div>

      <div className="form__row">
        <div className="field">
          <label htmlFor="destinationAccount">Cuenta destino</label>
          <input
            id="destinationAccount"
            type="text"
            inputMode="numeric"
            placeholder="10 dígitos"
            value={values.destinationAccount}
            onChange={(e) => set('destinationAccount', e.target.value)}
            aria-invalid={Boolean(fieldErrors.destinationAccount)}
            aria-describedby={describedBy('destinationAccount')}
          />
          {error('destinationAccount')}
        </div>
        <div className="field">
          <label htmlFor="city">Ciudad</label>
          <select
            id="city"
            value={values.city}
            onChange={(e) => set('city', e.target.value)}
            aria-invalid={Boolean(fieldErrors.city)}
            aria-describedby={describedBy('city')}
          >
            <option value="">Selecciona una ciudad</option>
            {CITIES.map((city) => (
              <option key={city} value={city}>
                {city}
              </option>
            ))}
          </select>
          {error('city')}
        </div>
      </div>

      <div className="form__row">
        <div className="field">
          <label htmlFor="channel">Canal</label>
          <select id="channel" value={values.channel} onChange={(e) => set('channel', e.target.value as Channel)}>
            {Object.entries(CHANNEL_LABELS).map(([value, label]) => (
              <option key={value} value={value}>
                {label}
              </option>
            ))}
          </select>
        </div>
        <div className="field">
          <label htmlFor="createdAt">Fecha y hora (opcional)</label>
          <input
            id="createdAt"
            type="datetime-local"
            value={values.createdAt}
            onChange={(e) => set('createdAt', e.target.value)}
            aria-invalid={Boolean(fieldErrors.createdAt)}
            aria-describedby={describedBy('createdAt') ?? 'createdAt-hint'}
          />
          {error('createdAt') ?? (
            <p className="field__hint" id="createdAt-hint">
              Si la dejas vacía se usa la hora actual
            </p>
          )}
        </div>
      </div>

      {submitError && (
        <p className="form__error" role="alert">
          {submitError}
        </p>
      )}

      <button type="submit" className="btn btn--primary btn--block" disabled={submitting}>
        {submitting ? 'Evaluando con IA…' : 'Simular transacción'}
      </button>
    </form>
  )
}
