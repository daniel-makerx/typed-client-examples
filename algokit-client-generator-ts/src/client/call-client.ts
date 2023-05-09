import { AlgoAppSpec, Hint } from '../schema/application'
import { DecIndent, DecIndentAndCloseBlock, DocumentParts, IncIndent, indent, inline, NewLine } from '../output/writer'
import { makeSafeMethodIdentifier, makeSafeTypeIdentifier } from '../util/sanitization'
import * as algokit from '@algorandfoundation/algokit-utils'
import { extractMethodNameFromSignature } from './helpers/extract-method-name-from-signature'
import { getCreateMethods } from './helpers/get-create-methods'

export function* callClient(app: AlgoAppSpec): DocumentParts {
  const name = makeSafeTypeIdentifier(app.contract.name)

  yield `/** A client to make calls to the ${app.contract.name} smart contract */`
  yield `export class ${makeSafeTypeIdentifier(app.contract.name)}Client {`
  yield IncIndent
  yield '/** The underlying `ApplicationClient` for when you want to have more flexibility */'
  yield 'public readonly appClient: ApplicationClient'
  yield NewLine
  yield '/**'
  yield ` * Creates a new instance of \`${makeSafeTypeIdentifier(app.contract.name)}Client\``
  yield ' * @param appDetails The details to identify the app to deploy'
  yield ' * @param algod An algod client instance'
  yield ' */'
  yield `constructor(appDetails: AppDetails, algod: Algodv2) {`
  yield IncIndent
  yield 'this.appClient = algokit.getAppClient({'
  yield* indent('...appDetails,', 'app: APP_SPEC')
  yield '}, algod)'
  yield DecIndent
  yield '}'
  yield NewLine

  yield* inline(
    `public async mapReturnValue<TSignatureOrMethod extends string>`,
    `(resultPromise: Promise<AppCallTransactionResult> | AppCallTransactionResult): `,
    `Promise<AppCallTransactionResultOfType<${name}ReturnTypeFor<TSignatureOrMethod>>> {`,
  )
  yield IncIndent
  yield `const result = await resultPromise`
  yield `if(result.return?.decodeError) {`
  yield* indent(`throw result.return.decodeError`)
  yield `}`
  yield `const returnValue = result.return?.returnValue as ${name}ReturnTypeFor<TSignatureOrMethod>`
  yield `return { ...result, return: returnValue }`
  yield DecIndentAndCloseBlock
  yield NewLine

  yield `public call<TSignature extends string>(params: CallRequest<TSignature, any>) {`
  yield IncIndent
  yield `return this.mapReturnValue<TSignature>(this.appClient.call(params))`
  yield DecIndentAndCloseBlock
  yield NewLine

  yield* deployMethods(app)
  yield* clientCallMethods(app)
  yield DecIndentAndCloseBlock
}

function* deployMethods(app: AlgoAppSpec): DocumentParts {
  const name = makeSafeTypeIdentifier(app.contract.name)

  const createMethods = getCreateMethods(app)

  if (createMethods?.length) {
    yield `private mapCreateArgs(args: ${name}CreateArgs & CoreAppCallArgs): AppClientCallArgs {`
    yield IncIndent
    yield `switch (args.method) {`
    yield IncIndent
    for (const [methodSignature] of createMethods) {
      const methodName = extractMethodNameFromSignature(methodSignature)
      yield `case '${methodName}':`
      yield* indent(`return ${makeSafeTypeIdentifier(app.contract.name)}CallFactory.${makeSafeMethodIdentifier(methodName)}(args)`)
    }
    yield `default:`
    yield* indent(`return args`)
    yield DecIndentAndCloseBlock
    yield DecIndentAndCloseBlock
    yield NewLine
  }
  yield `/**`
  yield ` * Idempotently deploys the ${app.contract.name} smart contract.`
  yield ` * @param params The arguments for the contract calls and any additional parameters for the call`
  yield ` * @returns The deployment result`
  yield ` */`
  yield `public deploy(params: ${name}DeployArgs & AppClientDeployCoreParams = {}) {`
  yield IncIndent
  if (createMethods?.length) {
    yield `return this.appClient.deploy({ ...params, createArgs: params.createArgs && this.mapCreateArgs(params.createArgs)})`
  } else {
    yield `return this.appClient.deploy({ ...params, })`
  }
  yield DecIndentAndCloseBlock
  yield NewLine

  yield `/**`
  yield ` * Creates a new instance of the ${app.contract.name} smart contract.`
  yield ` * @param args The arguments for the contract call`
  yield ` * @param params Any additional parameters for the call`
  yield ` * @returns The creation result`
  yield ` */`
  yield `public create<TMethod extends string>(args: { method?: TMethod } & ${name}CreateArgs = {}, params?: AppClientCallCoreParams & AppClientCompilationParams & CoreAppCallArgs) {`
  yield IncIndent
  if (createMethods?.length) {
    yield `return this.mapReturnValue<TMethod>(this.appClient.create({ ...this.mapCreateArgs(args), ...params, }))`
  } else {
    yield `return this.appClient.create({ ...args, ...params, })`
  }
  yield DecIndentAndCloseBlock
  yield NewLine

  yield `/**`
  yield ` * Updates an existing instance of the ${app.contract.name} smart contract.`
  yield ` * @param args The arguments for the contract call`
  yield ` * @param params Any additional parameters for the call`
  yield ` * @returns The update result`
  yield ` */`
  yield `public update(args: ${name}UpdateArgs = {}, params?: AppClientCallCoreParams & AppClientCompilationParams & CoreAppCallArgs) {`
  yield IncIndent
  yield `return this.appClient.update({ ...args, ...params, })`
  yield DecIndentAndCloseBlock
  yield NewLine

  yield `/**`
  yield ` * Deletes an existing instance of the ${app.contract.name} smart contract.`
  yield ` * @param args The arguments for the contract call`
  yield ` * @param params Any additional parameters for the call`
  yield ` * @returns The deletion result`
  yield ` */`
  yield `public delete(args: ${name}DeleteArgs = {}, params?: AppClientCallCoreParams & AppClientCompilationParams & CoreAppCallArgs) {`
  yield IncIndent
  yield `return this.appClient.delete({ ...args, ...params, })`
  yield DecIndentAndCloseBlock
  yield NewLine
}

function getMethodHint(hints: undefined | AlgoAppSpec['hints'], methodName: string): Hint | undefined {
  return hints && Object.entries(hints).find(([methodSignature]) => extractMethodNameFromSignature(methodSignature) === methodName)?.[1]
}

function* clientCallMethods(app: AlgoAppSpec): DocumentParts {
  for (const method of app.contract.methods) {
    const methodHint = getMethodHint(app.hints, method.name)
    // Skip create only methods as they will be covered by the deploy methods
    if (methodHint?.call_config?.no_op === 'CREATE') continue
    yield `/**`
    if (method.desc) {
      yield ` * ${method.desc}`
      yield ` *`
    }
    yield ` * Calls the ${algokit.getABIMethodSignature(method)} ABI method.`
    yield ` *`
    yield ` * @param args The arguments for the ABI method`
    yield ` * @param params Any additional parameters for the call`
    yield ` * @returns The result of the call`
    yield ` */`
    yield `public ${makeSafeMethodIdentifier(method.name)}(args: ${makeSafeTypeIdentifier(
      method.name,
    )}Args, params?: AppClientCallCoreParams & CoreAppCallArgs) {`
    yield IncIndent
    yield `return this.call(${makeSafeTypeIdentifier(app.contract.name)}CallFactory.${makeSafeMethodIdentifier(method.name)}(args, params))`
    yield DecIndent
    yield '}'
    yield NewLine
  }
}
