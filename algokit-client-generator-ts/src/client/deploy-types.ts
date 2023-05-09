import { AlgoAppSpec } from '../schema/application'
import { DecIndent, DecIndentAndCloseBlock, DocumentParts, IncIndent, NewLine } from '../output/writer'
import { makeSafeTypeIdentifier } from '../util/sanitization'
import { extractMethodNameFromSignature } from './helpers/extract-method-name-from-signature'
import { getCreateMethods } from './helpers/get-create-methods'

export function* deployTypes(app: AlgoAppSpec): DocumentParts {
  const name = makeSafeTypeIdentifier(app.contract.name)

  const createMethods = getCreateMethods(app)
  if (createMethods?.length) {
    // Multiple create methods
    yield `export type ${name}CreateArgs = BareCallArgs`
    yield IncIndent
    for (const [methodSignature] of createMethods) {
      const methodName = extractMethodNameFromSignature(methodSignature)
      yield `| ({ method: '${methodName}' } & ${makeSafeTypeIdentifier(methodName)}ArgsObj)`
    }

    yield DecIndent
  } else {
    // Only bare create
    yield `export type ${name}CreateArgs = BareCallArgs`
  }

  yield `export type ${name}UpdateArgs = BareCallArgs`
  yield `export type ${name}DeleteArgs = BareCallArgs`
  yield `export type ${name}DeployArgs = {`
  yield IncIndent
  yield `deployTimeParams?: TealTemplateParams`
  yield `createArgs?: ${name}CreateArgs & CoreAppCallArgs`
  yield `updateArgs?: ${name}UpdateArgs & CoreAppCallArgs`
  yield `deleteArgs?: ${name}DeleteArgs & CoreAppCallArgs`
  yield DecIndentAndCloseBlock
  yield NewLine
}
