import { DecIndent, DocumentParts, IncIndent } from '../output/writer'

export function* utilityTypes(): DocumentParts {
  yield 'export type CallRequest<TSignature extends string, TArgs = undefined> = {'
  yield IncIndent
  yield 'method: TSignature'
  yield 'methodArgs: TArgs'
  yield DecIndent
  yield '} & AppClientCallCoreParams & CoreAppCallArgs'

  yield `export type BareCallArgs = Omit<RawAppCallArgs, keyof CoreAppCallArgs>`
}
