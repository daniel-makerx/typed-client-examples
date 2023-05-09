import { DecIndent, DecIndentAndCloseBlock, DocumentParts, IncIndent, indent, inline, NewLine } from '../output/writer'
import { AlgoAppSpec, ContractMethod } from '../schema/application'
import {
  isSafeVariableIdentifier,
  makeSafeMethodIdentifier,
  makeSafePropertyIdentifier,
  makeSafeTypeIdentifier,
  makeSafeVariableIdentifier,
} from '../sanitization'

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
  yield* deployTypes(app)

  // Write a call factory
  yield* callFactory(app)
  yield NewLine
  // Write a client
  yield* client(app)
}
function* deployTypes(app: AlgoAppSpec): DocumentParts {
  const name = makeSafeTypeIdentifier(app.contract.name)
  yield `export type ${name}CreateArgs = BareCallArgs`
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

function* client(app: AlgoAppSpec): DocumentParts {
  yield `export class ${makeSafeTypeIdentifier(app.contract.name)}Client {`
  yield IncIndent
  yield 'public readonly appClient: ApplicationClient'
  yield NewLine
  yield `constructor(appDetails: AppDetails, algod: Algodv2) {`
  yield IncIndent
  yield 'this.appClient = algokit.getAppClient({'
  yield* indent('...appDetails,', 'app: APP_SPEC')
  yield '}, algod)'
  yield DecIndent
  yield '}'
  yield NewLine
  yield* genericCallMethod()
  yield* clientCallMethods(app)
  yield* deployMethods(app)
  yield DecIndentAndCloseBlock
}

function* deployMethods(app: AlgoAppSpec): DocumentParts {
  const name = makeSafeTypeIdentifier(app.contract.name)
  yield `public deploy(args?: ${name}DeployArgs, params?: AppClientDeployCoreParams) {`
  yield IncIndent
  yield `return this.appClient.deploy({ ...args, ...params, })`
  yield DecIndentAndCloseBlock
  yield NewLine

  yield `public create(args?: ${name}CreateArgs, params?: AppClientCallCoreParams & AppClientCompilationParams & CoreAppCallArgs) {`
  yield IncIndent
  yield `return this.appClient.create({ ...args, ...params, })`
  yield DecIndentAndCloseBlock
  yield NewLine
  yield `public update(args?: ${name}UpdateArgs, params?: AppClientCallCoreParams & AppClientCompilationParams & CoreAppCallArgs) {`
  yield IncIndent
  yield `return this.appClient.update({ ...args, ...params, })`
  yield DecIndentAndCloseBlock
  yield NewLine
  yield `public delete(args?: ${name}DeleteArgs, params?: AppClientCallCoreParams & AppClientCompilationParams & CoreAppCallArgs) {`
  yield IncIndent
  yield `return this.appClient.delete({ ...args, ...params, })`
  yield DecIndentAndCloseBlock
  yield NewLine
}

function* genericCallMethod(): DocumentParts {
  yield 'public async call<TReturn>(params: CallRequest<TReturn, any>): Promise<AppCallTransactionResultOfType<TReturn>> {'
  yield IncIndent
  yield `const result = await this.appClient.call(params)`
  yield `if(result.return?.decodeError) {`
  yield* indent(`throw result.return.decodeError`)
  yield '}'
  yield 'const returnValue = result.return?.returnValue as TReturn'
  yield 'return { ...result, return: returnValue }'
  yield DecIndentAndCloseBlock
  yield NewLine
}

function* clientCallMethods(app: AlgoAppSpec): DocumentParts {
  for (const method of app.contract.methods) {
    yield `public ${makeSafeMethodIdentifier(method.name)}(args: ${makeSafeTypeIdentifier(
      method.name,
    )}Args, params?: AppClientCallCoreParams & AppClientCompilationParams) {`
    yield IncIndent
    yield `return this.call(${makeSafeTypeIdentifier(app.contract.name)}CallFactory.${makeSafeMethodIdentifier(method.name)}(args, params))`
    yield DecIndent
    yield '}'
    yield NewLine
  }
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
  yield* inline(
    `export type ${safeIdentifier}ArgsTuple = [`,
    args.map((t) => `${makeSafeVariableIdentifier(t.name)}: ${t.type}`).join(','),
    ']',
  )
  yield `export type ${safeIdentifier}Args = ${safeIdentifier}ArgsObj | ${safeIdentifier}ArgsTuple`
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
  )}Args, params: AppClientCallCoreParams & AppClientCompilationParams = {}): CallRequest<${
    method.returns?.type ?? 'void'
  }, ${makeSafeTypeIdentifier(method.name)}Args>  {`
  yield IncIndent
  yield `return {`
  yield IncIndent
  yield `method: '${method.name}(${method.args.map((a) => a.type).join(',')})${method.returns?.type ?? ''}',`
  yield `methodArgs: Array.isArray(args) ? args : [${method.args
    .map((a) => (isSafeVariableIdentifier(a.name) ? `args.${a.name}` : `args['${makeSafePropertyIdentifier(a.name)}']`))
    .join(',')}],`
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

  yield `export type BareCallArgs = Omit<RawAppCallArgs, keyof CoreAppCallArgs>`
}

function* imports(): DocumentParts {
  yield `import * as algokit from '@algorandfoundation/algokit-utils'
import {
  AppCallTransactionResultOfType,
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
