import { useState } from 'react'
import { toApiError } from '../../../shared/api/apiError'
import { useRequest } from '../../../shared/hooks/useRequest'
import { getUsers, simulateTransaction } from '../services/simulatorService'
import type { EvaluationResult, FieldErrors, SimulatorValues } from '../types'
import { fromApiErrors, toPayload, validate } from '../validation'

export function useSimulator() {
  const users = useRequest(getUsers)
  const [submitting, setSubmitting] = useState(false)
  const [result, setResult] = useState<EvaluationResult | null>(null)
  const [fieldErrors, setFieldErrors] = useState<FieldErrors>({})
  const [submitError, setSubmitError] = useState<string | null>(null)

  const submit = async (values: SimulatorValues) => {
    setSubmitError(null)
    const errors = validate(values)
    setFieldErrors(errors)
    if (Object.keys(errors).length > 0) return

    setSubmitting(true)
    try {
      setResult(await simulateTransaction(toPayload(values)))
    } catch (err) {
      const apiError = toApiError(err)
      const mapped = fromApiErrors(apiError.fieldErrors)
      setFieldErrors(mapped)
      setSubmitError(apiError.message)
    } finally {
      setSubmitting(false)
    }
  }

  const reset = () => {
    setResult(null)
    setFieldErrors({})
    setSubmitError(null)
  }

  return { users, submitting, result, fieldErrors, submitError, submit, reset }
}
