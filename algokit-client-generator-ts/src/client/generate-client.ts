import { DocumentParts } from '../output/writer'
import { AlgoAppSpec } from '../schema/application'

export function* generateClient(app: AlgoAppSpec): DocumentParts {
  yield '// Testing 123'

  // Write a call factory

  // Write a client
}
