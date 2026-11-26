import type { Status } from '../types/transaction'

interface RiskScoreProps {
  score: number
  status: Status
}

export function RiskScore({ score, status }: RiskScoreProps) {
  return (
    <div className={`risk risk--${status}`}>
      <div className="risk__value">
        <span className="risk__number">{score}</span>
        <span className="risk__max">/100</span>
      </div>
      <div
        className="risk__bar"
        role="meter"
        aria-label="Puntaje de riesgo"
        aria-valuemin={0}
        aria-valuemax={100}
        aria-valuenow={score}
      >
        <div className="risk__fill" style={{ width: `${Math.max(score, 2)}%` }} />
        <span className="risk__mark risk__mark--40" aria-hidden="true" />
        <span className="risk__mark risk__mark--70" aria-hidden="true" />
      </div>
      <div className="risk__scale" aria-hidden="true">
        <span>0</span>
        <span>40</span>
        <span>70</span>
        <span>100</span>
      </div>
    </div>
  )
}
