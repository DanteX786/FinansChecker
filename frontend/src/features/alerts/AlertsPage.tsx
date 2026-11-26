import { PageHeader } from '../../shared/components/PageHeader'
import { RequestStatus } from '../../shared/components/RequestStatus'
import { AlertCard } from './components/AlertCard'
import { useAlerts } from './hooks/useAlerts'

export function AlertsPage() {
  const { data, loading, connecting, error, reload } = useAlerts()

  return (
    <>
      <PageHeader
        title="Alertas"
        description="Transacciones en revisión o sospechosas, con los motivos que detectó el motor de riesgo"
      />
      <RequestStatus loading={loading} connecting={connecting} error={error} onRetry={reload}>
        {data && data.length === 0 && <p className="card empty">No hay alertas por ahora</p>}
        {data && data.length > 0 && (
          <ul className="alert-grid">
            {data.map((alert) => (
              <AlertCard key={alert.id} alert={alert} />
            ))}
          </ul>
        )}
      </RequestStatus>
    </>
  )
}
