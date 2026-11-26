const currency = new Intl.NumberFormat('es-CO', {
  style: 'currency',
  currency: 'COP',
  maximumFractionDigits: 0,
})

const compactCurrency = new Intl.NumberFormat('es-CO', {
  style: 'currency',
  currency: 'COP',
  notation: 'compact',
  maximumFractionDigits: 1,
})

const dateTime = new Intl.DateTimeFormat('es-CO', {
  day: '2-digit',
  month: 'short',
  year: 'numeric',
  hour: 'numeric',
  minute: '2-digit',
})

const shortDay = new Intl.DateTimeFormat('es-CO', { day: '2-digit', month: 'short' })

const number = new Intl.NumberFormat('es-CO')

export const formatCurrency = (value: number) => currency.format(value)

export const formatCompactCurrency = (value: number) => compactCurrency.format(value)

export const formatNumber = (value: number) => number.format(value)

// Las fechas llegan en hora de Colombia sin zona horaria y se muestran tal cual
export const formatDateTime = (iso: string) => dateTime.format(new Date(iso))

export const formatShortDay = (isoDay: string) => shortDay.format(new Date(`${isoDay}T12:00:00`))
