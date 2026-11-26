import { Bar, BarChart, CartesianGrid, Legend, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'
import { formatShortDay } from '../../../shared/utils/format'
import { STATUS_COLORS, STATUS_LABELS } from '../../../shared/utils/labels'
import type { DayCount } from '../types'

export function DailyChart({ data }: { data: DayCount[] }) {
  const rows = data.map((d) => ({ ...d, label: formatShortDay(d.day) }))

  return (
    <article className="card chart-card">
      <h2 className="card__title">Transacciones por día</h2>
      <p className="card__subtitle">Últimos 14 días</p>
      <div className="chart">
        <ResponsiveContainer width="100%" height={280}>
          <BarChart data={rows} margin={{ top: 8, right: 8, left: -16, bottom: 0 }}>
            <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e2e8f0" />
            <XAxis dataKey="label" tickLine={false} axisLine={false} fontSize={12} interval="preserveStartEnd" />
            <YAxis allowDecimals={false} tickLine={false} axisLine={false} fontSize={12} />
            <Tooltip cursor={{ fill: 'rgba(148, 163, 184, 0.12)' }} />
            <Legend iconType="circle" wrapperStyle={{ fontSize: 13 }} />
            <Bar dataKey="approved" name={STATUS_LABELS.approved} stackId="s" fill={STATUS_COLORS.approved} />
            <Bar dataKey="review" name={STATUS_LABELS.review} stackId="s" fill={STATUS_COLORS.review} />
            <Bar
              dataKey="suspicious"
              name={STATUS_LABELS.suspicious}
              stackId="s"
              fill={STATUS_COLORS.suspicious}
              radius={[4, 4, 0, 0]}
            />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </article>
  )
}
