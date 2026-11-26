import { Cell, Pie, PieChart, ResponsiveContainer, Tooltip } from 'recharts'
import type { Status } from '../../../shared/types/transaction'
import { formatNumber } from '../../../shared/utils/format'
import { STATUS_COLORS, STATUS_LABELS } from '../../../shared/utils/labels'
import type { Stats } from '../types'

export function StatusChart({ stats }: { stats: Stats }) {
  const data: { status: Status; value: number }[] = [
    { status: 'approved', value: stats.approved_count },
    { status: 'review', value: stats.review_count },
    { status: 'suspicious', value: stats.suspicious_count },
  ]
  const total = stats.total_transactions || 1

  return (
    <article className="card chart-card">
      <h2 className="card__title">Por estado</h2>
      <p className="card__subtitle">Todas las transacciones</p>
      <div className="donut">
        <ResponsiveContainer width="100%" height={200}>
          <PieChart>
            <Pie
              data={data.map((d) => ({ ...d, name: STATUS_LABELS[d.status] }))}
              dataKey="value"
              nameKey="name"
              innerRadius={58}
              outerRadius={88}
              paddingAngle={2}
              startAngle={90}
              endAngle={-270}
              stroke="none"
            >
              {data.map((d) => (
                <Cell key={d.status} fill={STATUS_COLORS[d.status]} />
              ))}
            </Pie>
            <Tooltip />
          </PieChart>
        </ResponsiveContainer>
      </div>
      <ul className="legend">
        {data.map((d) => (
          <li key={d.status}>
            <span className="legend__dot" style={{ background: STATUS_COLORS[d.status] }} aria-hidden="true" />
            <span className="legend__label">{STATUS_LABELS[d.status]}</span>
            <span className="legend__value">{formatNumber(d.value)}</span>
            <span className="legend__pct">{((d.value * 100) / total).toFixed(1).replace('.', ',')}%</span>
          </li>
        ))}
      </ul>
    </article>
  )
}
