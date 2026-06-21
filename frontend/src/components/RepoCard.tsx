import type { RepoAssessment } from '../types/analysis'
import { Badge } from './Badge'
import { complexityTone, documentationTone } from '../utils/badgeTones'
import './RepoCard.css'

type RepoCardProps = {
  assessment: RepoAssessment
  githubUsername: string
}

export function RepoCard({ assessment, githubUsername }: RepoCardProps) {
  const repoUrl = `https://github.com/${githubUsername}/${assessment.repo_name}`

  const isSkipped = !assessment.has_readme
  const isFailed = Boolean(assessment.assessment_error)
  const isAssessed =
    assessment.complexity_level !== null &&
    assessment.documentation_quality !== null

  return (
    <article className="repo-card">
      <header className="repo-card-header">
        <h3 className="repo-card-title">
          <a href={repoUrl} target="_blank" rel="noreferrer">
            {assessment.repo_name}
          </a>
        </h3>

        {isAssessed && (
          <div className="repo-card-badges">
            <Badge
              label={assessment.complexity_level!}
              tone={complexityTone(assessment.complexity_level!)}
            />
            <Badge
              label={`Docs: ${assessment.documentation_quality!}`}
              tone={documentationTone(assessment.documentation_quality!)}
            />
          </div>
        )}
      </header>

      {isSkipped && (
        <p className="repo-card-flag repo-card-flag-muted">
          No README — assessment skipped
        </p>
      )}

      {isFailed && (
        <p className="repo-card-flag repo-card-flag-error">
          Assessment failed: {assessment.assessment_error}
        </p>
      )}

      <p className="repo-card-summary">{assessment.summary}</p>

      {assessment.estimated_experience_signal && (
        <p className="repo-card-signal">
          <span className="repo-card-signal-label">Experience signal:</span>{' '}
          {assessment.estimated_experience_signal}
        </p>
      )}
    </article>
  )
}