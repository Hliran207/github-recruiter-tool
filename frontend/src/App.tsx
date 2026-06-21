import { useState } from 'react'
import type { CandidateAnalysisResponse } from './types/analysis'
import { normalizeGitHubUsername } from './utils/githubInput'
import { AnalyzeApiError, fetchCandidateAnalysis } from './api/analyze'
import { LoadingSkeleton } from './components/LoadingSkeleton'
import { ErrorMessage } from './components/ErrorMessage'
import { EmptyResults } from './components/EmptyResults'
import { RepoCard } from './components/RepoCard'
import './App.css'

type ErrorKind = 'validation' | 'not_found' | 'server' | 'network' | 'unknown'

function App() {
  const [usernameInput, setUsernameInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [errorKind, setErrorKind] = useState<ErrorKind | null>(null)
  const [analysisResult, setAnalysisResult] = useState<CandidateAnalysisResponse | null>(null)

  async function handleAnalyzeClick() {
    const trimmed = usernameInput.trim()

    if (!trimmed) {
      setErrorKind('validation')
      setError('Please enter a GitHub username or profile URL.')
      setAnalysisResult(null)
      return
    }

    let normalizedUsername: string

    try {
      normalizedUsername = normalizeGitHubUsername(trimmed)
    } catch {
      setErrorKind('validation')
      setError('Enter a valid GitHub username or profile URL.')
      setAnalysisResult(null)
      return
    }

    setError(null)
    setErrorKind(null)
    setAnalysisResult(null)
    setIsLoading(true)

    try {
      const data = await fetchCandidateAnalysis(normalizedUsername)
      setAnalysisResult(data)
    } catch (err) {
      if (err instanceof AnalyzeApiError) {
        setError(err.message)

        if (err.status === 404) {
          setErrorKind('not_found')
        } else if (err.status === 0) {
          setErrorKind('network')
        } else if (err.status === 400 || err.status === 502) {
          setErrorKind('server')
        } else {
          setErrorKind('unknown')
        }
      } else {
        setErrorKind('unknown')
        setError('Something went wrong. Please try again.')
      }

      setAnalysisResult(null)
    } finally {
      setIsLoading(false)
    }
  }

  function getErrorTitle(kind: ErrorKind): string {
    switch (kind) {
      case 'validation':
        return 'Invalid input'
      case 'not_found':
        return 'User not found'
      case 'network':
        return 'Connection problem'
      case 'server':
        return 'Server error'
      default:
        return 'Something went wrong'
    }
  }

  function getErrorHint(kind: ErrorKind): string | undefined {
    switch (kind) {
      case 'not_found':
        return 'Double-check spelling and make sure the profile is public.'
      case 'network':
        return 'Confirm the backend is running on port 8000 and try again.'
      case 'server':
        return 'This may be temporary. Wait a moment and retry.'
      default:
        return undefined
    }
  }

  const hasEmptyResults =
    analysisResult !== null && analysisResult.assessments.length === 0

  return (
    <div className="app">
      <header className="app-header">
        <h1>GitHub Recruiter Tool</h1>
        <p className="app-subtitle">
          Paste a candidate&apos;s GitHub username to review their public projects.
        </p>
      </header>

      <section className="search-section" aria-label="Analyze a GitHub profile">
        <form
          className="search-row"
          onSubmit={(event) => {
            event.preventDefault()
            void handleAnalyzeClick()
          }}
        >
          <input
            type="text"
            className="search-input"
            placeholder="username or https://github.com/username"
            aria-label="GitHub username or profile URL"
            value={usernameInput}
            onChange={(event) => setUsernameInput(event.target.value)}
            disabled={isLoading}
          />
          <button
            type="submit"
            className="analyze-button"
            disabled={isLoading}
          >
            {isLoading ? 'Analyzing…' : 'Analyze'}
          </button>
        </form>
      </section>

      <section className="results-section" aria-label="Assessment results">
        {error && errorKind && (
          <ErrorMessage
            title={getErrorTitle(errorKind)}
            message={error}
            hint={getErrorHint(errorKind)}
          />
        )}

        {!error && isLoading && <LoadingSkeleton />}

        {!error && !isLoading && hasEmptyResults && analysisResult && (
          <EmptyResults username={analysisResult.username} />
        )}

        {!error && !isLoading && analysisResult && !hasEmptyResults && (
          <div className="results-panel">
            <div className="results-summary">
              <p>
                Analysis for{' '}
                <a
                  href={analysisResult.profile_url}
                  target="_blank"
                  rel="noreferrer"
                  className="profile-link"
                >
                  {analysisResult.username}
                </a>{' '}
                — {analysisResult.repos_analyzed} repo
                {analysisResult.repos_analyzed === 1 ? '' : 's'}
                <span className="results-summary-meta">
                  {' '}
                  ({analysisResult.public_repos} public total on GitHub)
                </span>
              </p>
            </div>

            <div className="repo-card-list">
              {analysisResult.assessments.map((assessment) => (
                <RepoCard
                  key={assessment.repo_name}
                  assessment={assessment}
                  githubUsername={analysisResult.username}
                />
              ))}
            </div>
          </div>
        )}

        {!error && !isLoading && !analysisResult && (
          <div className="results-placeholder">
            <p>Results will appear here after you analyze a profile.</p>
          </div>
        )}
      </section>
    </div>
  )
}

export default App