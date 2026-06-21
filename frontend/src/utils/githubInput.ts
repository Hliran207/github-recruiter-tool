export function normalizeGitHubUsername(raw: string): string {
    let value = raw.trim()
  
    if (!value) {
      throw new Error('Username cannot be empty')
    }
  
    if (value.startsWith('@')) {
      value = value.slice(1).trim()
    }
  
    if (value.toLowerCase().includes('github.com')) {
      if (!value.startsWith('http://') && !value.startsWith('https://')) {
        value = `https://${value}`
      }
  
      const url = new URL(value)
      const pathParts = url.pathname
        .split('/')
        .map((part) => part.trim())
        .filter(Boolean)
  
      if (pathParts.length === 0) {
        throw new Error('No username found in GitHub URL')
      }
  
      value = pathParts[0]
    }
  
    value = value.trim().replace(/^\/+|\/+$/g, '')
  
    if (!value) {
      throw new Error('Username cannot be empty')
    }
  
    return value.toLowerCase()
  }