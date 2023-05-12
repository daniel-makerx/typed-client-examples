import { DecIndent, DocumentParts, IncIndent, inline } from '../output/writer'
import { ContractMethod } from '../schema/application'
import { makeSafePropertyIdentifier, makeSafeTypeIdentifier, makeSafeVariableIdentifier } from '../util/sanitization'
import { getEquivalentType } from './helpers/get-equivalent-type'

export function* argTypes({ name, args }: ContractMethod): DocumentParts {
  const safeIdentifier = makeSafeTypeIdentifier(name)
  yield `export type ${safeIdentifier}ArgsObj = {`
  yield IncIndent
  for (const arg of args) {
    yield `${makeSafePropertyIdentifier(arg.name)}: ${getEquivalentType(arg.type, 'input')}`
  }
  yield DecIndent
  yield '}'
  yield* inline(
    `export type ${safeIdentifier}ArgsTuple = [`,
    args.map((t) => `${makeSafeVariableIdentifier(t.name)}: ${getEquivalentType(t.type, 'input')}`).join(', '),
    ']',
  )
  yield `export type ${safeIdentifier}Args = ${safeIdentifier}ArgsObj | ${safeIdentifier}ArgsTuple`
}
