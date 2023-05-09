import { ContractMethod } from '../schema/application'
import { DecIndent, DocumentParts, IncIndent, inline } from '../output/writer'
import { makeSafePropertyIdentifier, makeSafeTypeIdentifier, makeSafeVariableIdentifier } from '../util/sanitization'
import { getEquivalentType } from './helpers/get-equivalent-type'

export function* argTypes({ name, args }: ContractMethod): DocumentParts {
  const safeIdentifier = makeSafeTypeIdentifier(name)
  yield `export type ${safeIdentifier}ArgsObj = {`
  yield IncIndent
  for (const arg of args) {
    yield `${makeSafePropertyIdentifier(arg.name)}: ${getEquivalentType(arg.type)}`
  }
  yield DecIndent
  yield '}'
  yield* inline(
    `export type ${safeIdentifier}ArgsTuple = [`,
    args.map((t) => `${makeSafeVariableIdentifier(t.name)}: ${getEquivalentType(t.type)}`).join(', '),
    ']',
  )
  yield `export type ${safeIdentifier}Args = ${safeIdentifier}ArgsObj | ${safeIdentifier}ArgsTuple`
}
