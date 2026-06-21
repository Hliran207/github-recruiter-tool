import './LoadingSkeleton.css'

const SKELETON_CARD_COUNT = 3

export function LoadingSkeleton() {
  return (
    <div className="loading-skeleton" aria-live="polite" aria-busy="true">
      <p className="loading-skeleton-message">
        Analyzing repositories… this may take several seconds.
      </p>

      <div className="skeleton-card-list">
        {Array.from({ length: SKELETON_CARD_COUNT }).map((_, index) => (
          <div className="skeleton-card" key={index} aria-hidden="true">
            <div className="skeleton-line skeleton-line-title" />
            <div className="skeleton-badges">
              <div className="skeleton-pill" />
              <div className="skeleton-pill" />
            </div>
            <div className="skeleton-line skeleton-line-body" />
            <div className="skeleton-line skeleton-line-body short" />
          </div>
        ))}
      </div>
    </div>
  )
}