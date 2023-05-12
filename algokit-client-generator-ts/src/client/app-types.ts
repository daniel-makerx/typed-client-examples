import { GeneratorContext } from './generator-context'
import { DecIndent, DecIndentAndCloseBlock, DocumentParts, IncIndent, inline, NewLine } from '../output/writer'
import * as algokit from '@algorandfoundation/algokit-utils'
import { getEquivalentType } from './helpers/get-equivalent-type'
import { makeSafePropertyIdentifier, makeSafeVariableIdentifier } from '../util/sanitization'

export function* appTypes({ app, methodSignatureToUniqueName, name }: GeneratorContext): DocumentParts {
  yield `export type ${name} = {`
  yield IncIndent
  yield 'methods: '
  yield IncIndent
  for (const method of app.contract.methods) {
    const methodSig = algokit.getABIMethodSignature(method)
    const uniqueName = methodSignatureToUniqueName[methodSig]
    yield `& Record<'${methodSig}'${methodSig !== uniqueName ? ` | '${uniqueName}'` : ''}, {`
    yield IncIndent
    yield `argsObj: {`
    yield IncIndent
    for (const arg of method.args) {
      yield `${makeSafePropertyIdentifier(arg.name)}: ${getEquivalentType(arg.type, 'input')}`
    }
    yield DecIndentAndCloseBlock
    yield* inline(
      `argsTuple: [`,
      method.args.map((t) => `${makeSafeVariableIdentifier(t.name)}: ${getEquivalentType(t.type, 'input')}`).join(', '),
      ']',
    )
    yield `returns: ${getEquivalentType(method.returns.type ?? 'void', 'output')}`

    yield DecIndent
    yield '}>'
  }
  yield DecIndentAndCloseBlock
  yield `export type MethodArgs<TSignature extends keyof ${name}['methods']> = ${name}['methods'][TSignature]['argsObj' | 'argsTuple']`
  yield `export type MethodReturn<TSignature extends keyof ${name}['methods']> = ${name}['methods'][TSignature]['returns']`
  yield `type MapperArgs<TSignature extends keyof ${name}['methods']> = TSignature extends any ? [signature: TSignature, args: MethodArgs<TSignature>, params: AppClientCallCoreParams & CoreAppCallArgs ] : never`
  yield NewLine
}
