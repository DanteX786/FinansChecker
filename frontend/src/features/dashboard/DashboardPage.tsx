import { Link } from 'react-router-dom'
import { Icon } from '../../shared/components/Icon'
import { PageHeader } from '../../shared/components/PageHeader'
import { RequestStatus } from '../../shared/components/RequestStatus'
import { formatCompactCurrency, formatCurrency, formatNumber } from '../../shared/utils/format'
import { DailyChart } from './components/DailyChart'
import { KpiCard } from './components/KpiCard'
import { RecentAlerts } from './components/RecentAlerts'
import { StatusChart } from './components/StatusChart'
import { useDashboard } from './hooks/useDashboard'

export function DashboardPage() {
  const { data, loading, connecting, error, reload } = useDashboard()

  return (
    <>
      <PageHeader
        title="Dashboard"
        description="Resumen de la actividad y del riesgo detectado por la IA"
        actions={
          <Link to="/simulator" className="btn btn--primary">
            <Icon name="play" size={16} />
            Simular transacción
          </Link>
        }
      />
      <RequestStatus loading={loading} connecting={connecting} error={error} onRetry={reload}>
        {data && (
          <div className="stack">
            <section className="kpi-grid" aria-label="Indicadores">
              <KpiCard label="Total de transacciones" value={formatNumber(data.stats.total_transactions)} />
              <KpiCard
                label="Monto total"
                value={formatCompactCurrency(data.stats.total_amount)}
                detail={formatCurrency(data.stats.total_amount)}
              />
              <KpiCard
                label="Sospechosas"
                value={`${data.stats.suspicious_percentage.toString().replace('.', ',')}%`}
                detail={`${formatNumber(data.stats.suspicious_count)} transacciones`}
                tone="suspicious"
              />
              <KpiCard
                label="En revisión"
                value={formatNumber(data.stats.review_count)}
                detail={`${formatNumber(data.stats.alert_count)} alertas en total`}
                tone="review"
              />
            </section>
            <section className="chart-grid">
              <DailyChart data={data.stats.by_day} />
              <StatusChart stats={data.stats} />
            </section>
            <RecentAlerts alerts={data.alerts} />
          </div>
        )}
      </RequestStatus>
    </>
  )
}
