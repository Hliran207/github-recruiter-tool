import './Badge.css'

type BadgeTone =
  | 'gray'
  | 'blue'
  | 'green'
  | 'amber'
  | 'rose'
  | 'slate'

type BadgeProps = {
  label: string
  tone: BadgeTone
}

export function Badge({ label, tone }: BadgeProps) {
  return <span className={`badge badge-${tone}`}>{label}</span>
}