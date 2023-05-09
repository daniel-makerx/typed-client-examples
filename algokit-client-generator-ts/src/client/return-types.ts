import { AlgoAppSpec } from '../schema/application'
import { DecIndent, DecIndentAndCloseBlock, DocumentParts, IncIndent } from '../output/writer'
import { makeSafeTypeIdentifier } from '../util/sanitization'
import { getEquivalentType } from './helpers/get-equivalent-type'
import * as algokit from '@algorandfoundation/algokit-utils'

export function* returnTypes(app: AlgoAppSpec): DocumentParts {
  const appName = makeSafeTypeIdentifier(app.contract.name)
  yield `export type ${appName}ReturnTypes = {`
  yield IncIndent
  for (const method of app.contract.methods) {
    yield `'${algokit.getABIMethodSignature(method)}': ${getEquivalentType(method.returns.type ?? 'void')}`
    yield `'${method.name}': ${getEquivalentType(method.returns.type ?? 'void')}`
  }
  yield DecIndentAndCloseBlock
  yield `export type ${appName}ReturnTypeFor<TSignatureOrMethod> = TSignatureOrMethod extends keyof ${appName}ReturnTypes`
  yield IncIndent
  yield `? ${appName}ReturnTypes[TSignatureOrMethod]`
  yield `: undefined`
  yield DecIndent
}
