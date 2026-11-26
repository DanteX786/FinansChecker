export interface DayCount {
  day: string
  approved: number
  review: number
  suspicious: number
}

export interface Stats {
  total_transactions: number
  total_amount: number
  approved_count: number
  review_count: number
  suspicious_count: number
  suspicious_percentage: number
  alert_count: number
  by_day: DayCount[]
}
