import './ErrorMessage.css'

type ErrorMessageProps = {
  title: string
  message: string
  hint?: string
}

export function ErrorMessage({ title, message, hint }: ErrorMessageProps) {
  return (
    <div className="error-message" role="alert">
      <h2 className="error-message-title">{title}</h2>
      <p className="error-message-text">{message}</p>
      {hint && <p className="error-message-hint">{hint}</p>}
    </div>
  )
}