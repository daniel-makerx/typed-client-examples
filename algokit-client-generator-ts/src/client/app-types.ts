import { GeneratorContext } from './generator-context'
import { DecIndentAndCloseBlock, DocumentParts, IncIndent, inline, NewLine } from '../output/writer'
import * as algokit from '@algorandfoundation/algokit-utils'
import { getEquivalentType } from './helpers/get-equivalent-type'
import { makeSafePropertyIdentifier, makeSafeVariableIdentifier } from '../util/sanitization'

export function* appTypes({ app, callConfig, name }: GeneratorContext): DocumentParts {
  yield `export type ${name} = {`
  yield IncIndent
  yield 'methods: {'
  yield IncIndent
  for (const method of app.contract.methods) {
    yield `'${algokit.getABIMethodSignature(method)}': {`
    yield IncIndent
    yield `argsObj: {`
    yield IncIndent
    for (const arg of method.args) {
      yield `${makeSafePropertyIdentifier(arg.name)}: ${getEquivalentType(arg.type)}`
    }
    yield DecIndentAndCloseBlock
    yield* inline(
      `argsTuple: [`,
      method.args.map((t) => `${makeSafeVariableIdentifier(t.name)}: ${getEquivalentType(t.type)}`).join(', '),
      ']',
    )
    yield `returns: ${getEquivalentType(method.returns.type ?? 'void')}`

    yield DecIndentAndCloseBlock
  }
  yield DecIndentAndCloseBlock
  yield DecIndentAndCloseBlock
  yield `export type MethodArgs<TSignature extends keyof ${name}['methods']> = ${name}['methods'][TSignature]['argsObj' | 'argsTuple']`
  yield `export type MethodReturn<TSignature extends keyof ${name}['methods']> = ${name}['methods'][TSignature]['returns']`
  yield `type MapperArgs<TSignature extends keyof ${name}['methods']> = TSignature extends any ? [signature: TSignature, args: MethodArgs<TSignature>, params: AppClientCallCoreParams & CoreAppCallArgs ] : never`
  yield NewLine
}
