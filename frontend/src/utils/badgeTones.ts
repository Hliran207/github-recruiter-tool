import type {
    ComplexityLevel,
    DocumentationQuality,
  } from '../types/analysis'
  
  export function complexityTone(
    level: ComplexityLevel,
  ): 'gray' | 'blue' | 'green' {
    switch (level) {
      case 'Beginner':
        return 'gray'
      case 'Intermediate':
        return 'blue'
      case 'Advanced':
        return 'green'
    }
  }
  
  export function documentationTone(
    level: DocumentationQuality,
  ): 'rose' | 'amber' | 'green' {
    switch (level) {
      case 'Poor':
        return 'rose'
      case 'Adequate':
        return 'amber'
      case 'Excellent':
        return 'green'
    }
  }