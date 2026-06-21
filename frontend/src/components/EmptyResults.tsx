import './EmptyResults.css'

type EmptyResultsProps = {
  username: string
}

export function EmptyResults({ username }: EmptyResultsProps) {
  return (
    <div className="empty-results">
      <h2 className="empty-results-title">No repositories to analyze</h2>
      <p className="empty-results-text">
        <strong>{username}</strong> has no qualifying public repositories in this
        view.
      </p>
      <p className="empty-results-hint">
        Forks are excluded by design. The user may only have private repos, or none
        in the most recently updated set we fetch.
      </p>
    </div>
  )
}