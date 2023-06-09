import { DocumentParts, inline, NewLine } from '../output/writer'
import { AlgoAppSpec } from '../schema/application'
import { callFactory } from './call-factory'
import { callClient } from './call-client'
import { deployTypes } from './deploy-types'
import { utilityTypes } from './utility-types'
import { imports } from './imports'
import { createGeneratorContext } from './generator-context'
import { appTypes } from './app-types'

export function* generate(app: AlgoAppSpec): DocumentParts {
  const ctx = createGeneratorContext(app)
  yield `/* eslint-disable */`
  yield `/**`
  yield ` * This file was automatically generated by algokit-client-generator.`
  yield ` * DO NOT MODIFY IT BY HAND.`
  yield ` */`

  yield* imports()
  yield* inline('export const APP_SPEC: AppSpec = ', JSON.stringify(app, undefined, 2))
  yield NewLine

  yield* utilityTypes()
  yield NewLine
  yield* appTypes(ctx)
  //
  // yield NewLine
  yield* deployTypes(ctx)

  // Write a call factory
  yield* callFactory(ctx)
  yield NewLine
  // Write a client
  yield* callClient(ctx)
}
