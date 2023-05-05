import { DecIndent, DocumentParts, IncIndent, indent, inline, NewLine } from '../output/writer'
import { AlgoAppSpec, ContractMethod } from '../schema/application'
import { isSafeVariableIdentifier, makeSafeMethodIdentifier, makeSafePropertyIdentifier, makeSafeTypeIdentifier } from '../sanitization'

export function* generateClient(app: AlgoAppSpec): DocumentParts {
  yield* imports()
  yield* inline('export const APP_SPEC: AppSpec = ', JSON.stringify(app, undefined, 2))
  yield NewLine

  yield* utilityTypes()
  yield NewLine

  for (const method of app.contract.methods) {
    yield* argTypes(method)
  }
  yield NewLine

  // Write a call factory
  yield* callFactory(app)
  yield NewLine
  // Write a client
  yield* client(app)
}

function* client(app: AlgoAppSpec): DocumentParts {
  yield `export class ${makeSafeTypeIdentifier(app.contract.name)}Client {`
  yield IncIndent
  yield 'public readonly appClient: ApplicationClient'

  yield `constructor(appDetails: AppDetails, algod: Algodv2) {`
  yield IncIndent
  yield 'this.appClient = algokit.getAppClient({'
  yield* indent('...appDetails,', 'app: APP_SPEC')
  yield '}, algod)'
  yield DecIndent
  yield '}'
  yield NewLine
  yield 'public async call<TReturn>(params: CallRequest<TReturn, any>): Promise<CallResult<TReturn>> {'
  yield IncIndent
  yield `const result = await this.appClient.call(params)`
  yield `if(result.return?.decodeError) {`
  yield* indent(`throw result.return.decodeError`)
  yield '}'
  yield 'const returnValue = result.return?.returnValue as TReturn'
  yield 'return { ...result, return: returnValue }'
  yield DecIndent
  yield '}'

  for (const method of app.contract.methods) {
    yield `public ${makeSafeMethodIdentifier(method.name)}(args: ${makeSafeTypeIdentifier(
      method.name,
    )}ArgsObj, params?: AppClientCallCoreParams & AppClientCompilationParams) {`
    yield IncIndent
    yield `return this.call(${makeSafeTypeIdentifier(app.contract.name)}CallFactory.${makeSafeMethodIdentifier(method.name)}(args, params))`
    yield DecIndent
    yield '}'
  }

  yield DecIndent
  yield '}'
}

function* argTypes({ name, args }: ContractMethod): DocumentParts {
  const safeIdentifier = makeSafeTypeIdentifier(name)
  yield `export type ${safeIdentifier}ArgsObj = {`
  yield IncIndent
  for (const arg of args) {
    yield `'${makeSafePropertyIdentifier(arg.name)}': ${arg.type}`
  }
  yield DecIndent
  yield '}'
  yield* inline(`export type ${safeIdentifier}ArgsTuple = [`, args.map((t) => t.type).join(','), ']')
}

function* callFactory(app: AlgoAppSpec): DocumentParts {
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
  )}ArgsObj, params?: AppClientCallCoreParams & AppClientCompilationParams = {}): CallRequest<${
    method.returns?.type ?? 'void'
  }, ${makeSafeTypeIdentifier(method.name)}ArgsTuple>  {`
  yield IncIndent
  yield `return {`
  yield IncIndent
  yield `method: '${method.name}(${method.args.map((a) => a.type).join(',')})${method.returns?.type ?? ''}',`
  yield `methodArgs: [${method.args
    .map((a) => (isSafeVariableIdentifier(a.name) ? `args.${a.name}` : `args['${makeSafePropertyIdentifier(a.name)}']`))
    .join(',')}], `
  yield '...params,'
  yield DecIndent
  yield '}'
  yield DecIndent
  yield '}'
}

function* utilityTypes(): DocumentParts {
  yield 'export type CallRequest<TReturn, TArgs = undefined> = {'
  yield IncIndent
  yield 'method: string'
  yield 'methodArgs: TArgs'

  yield DecIndent
  yield '} & AppClientCallCoreParams & CoreAppCallArgs'
  yield 'export type CallResult<TReturn> = {'
  yield IncIndent
  yield 'return: TReturn'
  yield DecIndent
  yield `} & Omit<AppCallTransactionResult, 'return'>`
}

function* imports(): DocumentParts {
  yield `import * as algokit from '@algorandfoundation/algokit-utils'
import {
  AppCallTransactionResult,
  CoreAppCallArgs,
  RawAppCallArgs,
  TealTemplateParams,
} from '@algorandfoundation/algokit-utils/types/app'
import {
  AppClientCallArgs,
  AppClientCallCoreParams,
  AppClientCallParams,
  AppClientCompilationParams,
  AppClientDeployCoreParams,
  AppDetails,
  AppSpecAppDetails,
  ApplicationClient,
} from '@algorandfoundation/algokit-utils/types/app-client'
import { AppSpec } from '@algorandfoundation/algokit-utils/types/app-spec'
import { Algodv2 } from 'algosdk'`
}
