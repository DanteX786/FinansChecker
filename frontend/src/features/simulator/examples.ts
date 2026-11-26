import type { SimUser, SimulatorValues } from './types'

const pad = (n: number) => String(n).padStart(2, '0')

function toInputValue(date: Date): string {
  return `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())}T${pad(date.getHours())}:${pad(date.getMinutes())}`
}

function lastOccurrence(hour: number): Date {
  const date = new Date()
  date.setHours(hour, 0, 0, 0)
  if (date.getTime() > Date.now()) date.setDate(date.getDate() - 1)
  return date
}

function randomAccount(): string {
  return Array.from({ length: 10 }, () => Math.floor(Math.random() * 10)).join('')
}

const roundThousands = (value: number) => Math.max(1000, Math.round(value / 1000) * 1000)

// Ejemplo de CP-01: monto habitual, cuenta conocida, en su ciudad y en horario normal
export function normalExample(user: SimUser): SimulatorValues {
  const hour = new Date().getHours()
  const daytime = hour >= 7 && hour < 22
  return {
    userId: String(user.id),
    type: 'transfer',
    amount: String(roundThousands(user.average_amount)),
    destinationAccount: user.usual_destination ?? randomAccount(),
    city: user.city,
    channel: 'app',
    createdAt: daytime ? '' : toInputValue(lastOccurrence(10)),
  }
}

// Ejemplo de CP-02: monto 8 veces mayor al promedio, a las 3:00 a. m., a una cuenta nueva
export function suspiciousExample(user: SimUser): SimulatorValues {
  return {
    userId: String(user.id),
    type: 'transfer',
    amount: String(roundThousands(user.average_amount * 8)),
    destinationAccount: randomAccount(),
    city: user.city,
    channel: 'app',
    createdAt: toInputValue(lastOccurrence(3)),
  }
}
