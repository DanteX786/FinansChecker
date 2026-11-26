import { PageHeader } from '../../shared/components/PageHeader'
import { RequestStatus } from '../../shared/components/RequestStatus'
import { SimulationResult } from './components/SimulationResult'
import { SimulatorForm } from './components/SimulatorForm'
import { useSimulator } from './hooks/useSimulator'

export function SimulatorPage() {
  const { users, submitting, result, fieldErrors, submitError, submit, reset } = useSimulator()

  return (
    <>
      <PageHeader
        title="Simulador"
        description="Crea una transacción de prueba y mira cómo la evalúa el motor de riesgo"
      />
      <RequestStatus loading={users.loading} connecting={users.connecting} error={users.error} onRetry={users.reload}>
        <div className="simulator-grid">
          <SimulatorForm
            users={users.data ?? []}
            submitting={submitting}
            fieldErrors={fieldErrors}
            submitError={submitError}
            onSubmit={submit}
          />
          <SimulationResult result={result} onReset={reset} />
        </div>
      </RequestStatus>
    </>
  )
}
