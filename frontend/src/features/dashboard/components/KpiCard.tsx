interface KpiCardProps {
  label: string
  value: string
  detail?: string
  tone?: 'default' | 'review' | 'suspicious'
}

export function KpiCard({ label, value, detail, tone = 'default' }: KpiCardProps) {
  return (
    <article className={`card kpi kpi--${tone}`}>
      <p className="kpi__label">{label}</p>
      <p className="kpi__value">{value}</p>
      {detail && <p className="kpi__detail">{detail}</p>}
    </article>
  )
}
