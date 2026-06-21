import axios, { AxiosError, isAxiosError } from 'axios'
import type { CandidateAnalysisResponse } from '../types/analysis'

export class AnalyzeApiError extends Error {
  status: number

  constructor(message: string, status: number) {
    super(message)
    this.name = 'AnalyzeApiError'
    this.status = status
  }
}

function mapErrorMessage(status: number, detail: unknown): string {
  if (status === 404) {
    return 'GitHub user not found. Check the username and try again.'
  }

  if (status === 400) {
    if (typeof detail === 'string') return detail
    return 'Invalid username. Please check your input.'
  }

  if (status === 502) {
    return 'GitHub is temporarily unavailable. Please try again later.'
  }

  return 'Something went wrong while analyzing this profile. Please try again.'
}

export async function fetchCandidateAnalysis(
  username: string,
): Promise<CandidateAnalysisResponse> {
  try {
    const response = await axios.get<CandidateAnalysisResponse>(
      `/api/analyze/${encodeURIComponent(username)}`,
    )
    return response.data
  } catch (error) {
    if (isAxiosError(error)) {
      const status = error.response?.status ?? 0
      const detail = error.response?.data?.detail

      throw new AnalyzeApiError(
        mapErrorMessage(status, detail),
        status,
      )
    }

    throw new AnalyzeApiError(
      'Could not reach the server. Is the backend running on port 8000?',
      0,
    )
  }
}