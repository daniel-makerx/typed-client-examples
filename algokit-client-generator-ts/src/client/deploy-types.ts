import { DecIndent, DecIndentAndCloseBlock, DocumentParts, IncIndent, NewLine } from '../output/writer'
import { AlgoAppSpec } from '../schema/application'
import { makeSafeTypeIdentifier } from '../util/sanitization'
import { extractMethodNameFromSignature } from './helpers/extract-method-name-from-signature'
import { BARE_CALL, getCreateOnComplete } from './helpers/get-call-config-summary'
import { GeneratorContext } from './generator-context'

export function* deployTypes({ app, callConfig }: GeneratorContext): DocumentParts {
  const name = makeSafeTypeIdentifier(app.contract.name)

  if (callConfig.createMethods.length > 0) {
    yield `export type ${name}CreateArgs =`
    yield IncIndent
    for (const method of callConfig.createMethods) {
      if (method === BARE_CALL) {
        yield `| BareCallArgs ${getCreateOnComplete(app, method)}`
      } else {
        const methodName = extractMethodNameFromSignature(method)
        yield `| ({ method: '${methodName}' } & ${makeSafeTypeIdentifier(methodName)}ArgsObj) ${getCreateOnComplete(app, method)}`
      }
    }
    yield DecIndent
  }
  if (callConfig.updateMethods.length > 0) {
    yield `export type ${name}UpdateArgs =`
    yield IncIndent
    for (const method of callConfig.updateMethods) {
      if (method === BARE_CALL) {
        yield `| BareCallArgs`
      } else {
        const methodName = extractMethodNameFromSignature(method)
        yield `| ({ method: '${methodName}' } & ${makeSafeTypeIdentifier(methodName)}ArgsObj)`
      }
    }
    yield DecIndent
  }

  if (callConfig.deleteMethods.length > 0) {
    yield `export type ${name}DeleteArgs =`
    yield IncIndent
    for (const method of callConfig.deleteMethods) {
      if (method === BARE_CALL) {
        yield `| BareCallArgs`
      } else {
        const methodName = extractMethodNameFromSignature(method)
        yield `| ({ method: '${methodName}' } & ${makeSafeTypeIdentifier(methodName)}ArgsObj)`
      }
    }
    yield DecIndent
  }

  if (callConfig.optInMethods.length > 0) {
    yield `export type ${name}OptInArgs =`
    yield IncIndent
    for (const method of callConfig.optInMethods) {
      if (method === BARE_CALL) {
        yield `| BareCallArgs`
      } else {
        const methodName = extractMethodNameFromSignature(method)
        yield `| ({ method: '${methodName}' } & ${makeSafeTypeIdentifier(methodName)}ArgsObj)`
      }
    }
    yield DecIndent
  }
  if (callConfig.closeOutMethods.length > 0) {
    yield `export type ${name}CloseOutArgs =`
    yield IncIndent
    for (const method of callConfig.closeOutMethods) {
      if (method === BARE_CALL) {
        yield `| BareCallArgs`
      } else {
        const methodName = extractMethodNameFromSignature(method)
        yield `| ({ method: '${methodName}' } & ${makeSafeTypeIdentifier(methodName)}ArgsObj)`
      }
    }
    yield DecIndent
  }

  yield `export type ${name}DeployArgs = {`
  yield IncIndent
  yield `deployTimeParams?: TealTemplateParams`
  if (callConfig.createMethods.length) yield `createArgs?: ${name}CreateArgs & CoreAppCallArgs`
  if (callConfig.updateMethods.length) yield `updateArgs?: ${name}UpdateArgs & CoreAppCallArgs`
  if (callConfig.deleteMethods.length) yield `deleteArgs?: ${name}DeleteArgs & CoreAppCallArgs`
  yield DecIndentAndCloseBlock
  yield NewLine
}
