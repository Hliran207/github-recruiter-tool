export type ComplexityLevel = 'Beginner' | 'Intermediate' | 'Advanced'
export type DocumentationQuality = 'Poor' | 'Adequate' | 'Excellent'

export interface RepoAssessment {
  repo_name: string
  has_readme: boolean
  complexity_level: ComplexityLevel | null
  documentation_quality: DocumentationQuality | null
  estimated_experience_signal: string | null
  summary: string
  assessment_error: string | null
}

export interface CandidateAnalysisResponse {
  username: string
  profile_url: string
  public_repos: number
  repos_analyzed: number
  assessments: RepoAssessment[]
}