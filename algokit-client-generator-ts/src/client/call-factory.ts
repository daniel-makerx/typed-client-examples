import { ContractMethod } from '../schema/application'
import { DecIndent, DocumentParts, IncIndent } from '../output/writer'
import {
  isSafeVariableIdentifier,
  makeSafeMethodIdentifier,
  makeSafePropertyIdentifier,
  makeSafeTypeIdentifier,
} from '../util/sanitization'
import * as algokit from '@algorandfoundation/algokit-utils'
import { GeneratorContext } from './generator-context'

export function* callFactory({ app }: GeneratorContext): DocumentParts {
  yield `export abstract class ${makeSafeTypeIdentifier(app.contract.name)}CallFactory {`
  yield IncIndent
  for (const method of app.contract.methods) {
    yield* callFactoryMethod(method)
  }
  yield DecIndent
  yield '}'
}

function* callFactoryMethod(method: ContractMethod) {
  yield `static ${makeSafeMethodIdentifier(method.name)}(args: ${makeSafeTypeIdentifier(
    method.name,
  )}Args, params: AppClientCallCoreParams & CoreAppCallArgs = {}) {`
  yield IncIndent
  yield `return {`
  yield IncIndent
  yield `method: '${algokit.getABIMethodSignature(method)}' as const,`
  yield `methodArgs: Array.isArray(args) ? args : [${method.args
    .map((a) => (isSafeVariableIdentifier(a.name) ? `args.${a.name}` : `args['${makeSafePropertyIdentifier(a.name)}']`))
    .join(', ')}],`
  yield '...params,'
  yield DecIndent
  yield '}'
  yield DecIndent
  yield '}'
}
