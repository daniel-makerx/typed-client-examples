import { DecIndent, DecIndentAndCloseBlock, DocumentParts, IncIndent, indent, inline, NewLine } from '../output/writer'
import * as algokit from '@algorandfoundation/algokit-utils'
import { notFalsy } from '../util/not-falsy'
import { makeSafeMethodIdentifier, makeSafeTypeIdentifier } from '../util/sanitization'
import { extractMethodNameFromSignature } from './helpers/extract-method-name-from-signature'
import { BARE_CALL } from './helpers/get-call-config-summary'
import { GeneratorContext } from './generator-context'

export function* callClient(ctx: GeneratorContext): DocumentParts {
  const { app, name } = ctx

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

  yield* methodArgMapper(ctx)
  yield* deployMethods(ctx)
  yield* optInMethod(ctx)
  yield* closeOutMethod(ctx)
  yield* clearState(ctx)
  yield* clientCallMethods(ctx)

  yield DecIndentAndCloseBlock
}

function* methodArgMapper({ app, callConfig, name }: GeneratorContext): DocumentParts {
  const mappableMethods = [
    ...callConfig.createMethods,
    ...callConfig.updateMethods,
    ...callConfig.deleteMethods,
    ...callConfig.optInMethods,
    ...callConfig.closeOutMethods,
  ].filter((m): m is string => m !== BARE_CALL)

  if (mappableMethods.length) {
    const args = [
      callConfig.createMethods.length && `${name}CreateArgs`,
      callConfig.updateMethods.length && `${name}UpdateArgs`,
      callConfig.deleteMethods.length && `${name}DeleteArgs`,
      callConfig.closeOutMethods.length && `${name}CloseOutArgs`,
      callConfig.optInMethods.length && `${name}OptInArgs`,
    ].filter(notFalsy)

    yield `private mapMethodArgs(args: ${args.join(' | ')}, params?: CoreAppCallArgs): AppClientCallArgs {`
    yield IncIndent
    yield `switch (args.method) {`
    yield IncIndent
    for (const methodSignature of mappableMethods) {
      const methodName = extractMethodNameFromSignature(methodSignature)
      yield `case '${methodName}':`
      yield* indent(`return ${makeSafeTypeIdentifier(app.contract.name)}CallFactory.${makeSafeMethodIdentifier(methodName)}(args, params)`)
    }
    yield `default:`
    yield* indent(`return args`)
    yield DecIndentAndCloseBlock
    yield DecIndentAndCloseBlock
    yield NewLine
  }
}

function* deployMethods({ app, callConfig, name }: GeneratorContext): DocumentParts {
  yield `/**`
  yield ` * Idempotently deploys the ${app.contract.name} smart contract.`
  yield ` * @param params The arguments for the contract calls and any additional parameters for the call`
  yield ` * @returns The deployment result`
  yield ` */`
  yield `public deploy(params: ${name}DeployArgs & AppClientDeployCoreParams = {}) {`
  yield IncIndent
  if (callConfig.createMethods.some((m) => m !== BARE_CALL)) {
    yield `const { boxes: create_boxes, lease: create_lease, onCompleteAction: createOnCompleteAction, ...createArgs } = params.createArgs ?? {}`
  } else {
    yield `const { onCompleteAction: createOnCompleteAction } = params.createArgs ?? {}`
  }
  if (callConfig.updateMethods.some((m) => m !== BARE_CALL))
    yield `const { boxes: update_boxes, lease: update_lease, ...updateArgs } = params.updateArgs ?? {}`
  if (callConfig.deleteMethods.some((m) => m !== BARE_CALL))
    yield `const { boxes: delete_boxes, lease: delete_lease, ...deleteArgs } = params.deleteArgs ?? {}`
  yield `return this.appClient.deploy({ `
  yield IncIndent
  yield `...params,`
  if (callConfig.createMethods.some((m) => m !== BARE_CALL))
    yield `createArgs: params.createArgs ? this.mapMethodArgs(createArgs, { boxes: create_boxes, lease: create_lease }) : undefined,`
  yield `createOnCompleteAction,`
  if (callConfig.updateMethods.some((m) => m !== BARE_CALL))
    yield `updateArgs: params.updateArgs ? this.mapMethodArgs(updateArgs, { boxes: update_boxes, lease: update_lease }) : undefined,`
  if (callConfig.deleteMethods.some((m) => m !== BARE_CALL))
    yield `deleteArgs: params.deleteArgs ? this.mapMethodArgs(deleteArgs, { boxes: delete_boxes, lease: delete_lease }) : undefined,`
  yield DecIndent
  yield `})`
  yield DecIndentAndCloseBlock
  yield NewLine
  if (callConfig.createMethods.length) {
    yield `/**`
    yield ` * Creates a new instance of the ${app.contract.name} smart contract.`
    yield ` * @param args The arguments for the contract call`
    yield ` * @param params Any additional parameters for the call`
    yield ` * @returns The creation result`
    yield ` */`
    yield `public create<TMethod extends string>(args: { method?: TMethod } & ${name}CreateArgs${
      callConfig.createMethods.some((m) => m === BARE_CALL) ? ' = {}' : ''
    }, params?: AppClientCallCoreParams & AppClientCompilationParams & CoreAppCallArgs) {`
    yield IncIndent
    yield `const onCompleteAction = args.onCompleteAction`
    if (callConfig.createMethods.some((m) => m !== BARE_CALL)) {
      yield `return this.mapReturnValue<TMethod>(this.appClient.create({ ...this.mapMethodArgs(args), ...params, ...{ onCompleteAction } }))`
    } else {
      yield `return this.appClient.create({ ...args, ...params, ...{ onCompleteAction } })`
    }
    yield DecIndentAndCloseBlock
    yield NewLine
  }
  if (callConfig.updateMethods.length) {
    yield `/**`
    yield ` * Updates an existing instance of the ${app.contract.name} smart contract.`
    yield ` * @param args The arguments for the contract call`
    yield ` * @param params Any additional parameters for the call`
    yield ` * @returns The update result`
    yield ` */`
    yield `public update<TMethod extends string>(args: { method?: TMethod } & ${name}UpdateArgs${
      callConfig.updateMethods.some((m) => m === BARE_CALL) ? ' = {}' : ''
    }, params?: AppClientCallCoreParams & AppClientCompilationParams & CoreAppCallArgs) {`
    yield IncIndent
    if (callConfig.updateMethods.some((m) => m !== BARE_CALL)) {
      yield `return this.mapReturnValue<TMethod>(this.appClient.update({ ...this.mapMethodArgs(args), ...params, }))`
    } else {
      yield `return this.appClient.update({ ...args, ...params, })`
    }
    yield DecIndentAndCloseBlock
    yield NewLine
  }

  if (callConfig.deleteMethods.length) {
    yield `/**`
    yield ` * Deletes an existing instance of the ${app.contract.name} smart contract.`
    yield ` * @param args The arguments for the contract call`
    yield ` * @param params Any additional parameters for the call`
    yield ` * @returns The deletion result`
    yield ` */`
    yield `public delete<TMethod extends string>(args: { method?: TMethod } & ${name}DeleteArgs${
      callConfig.deleteMethods.some((m) => m === BARE_CALL) ? ' = {}' : ''
    }, params?: AppClientCallCoreParams & CoreAppCallArgs) {`
    yield IncIndent
    if (callConfig.deleteMethods.some((m) => m !== BARE_CALL)) {
      yield `return this.mapReturnValue<TMethod>(this.appClient.delete({ ...this.mapMethodArgs(args), ...params, }))`
    } else {
      yield `return this.appClient.delete({ ...args, ...params, })`
    }
    yield DecIndentAndCloseBlock
    yield NewLine
  }
}

function* optInMethod({ app, name, callConfig }: GeneratorContext): DocumentParts {
  if (callConfig.optInMethods.length) {
    yield `/**`
    yield ` * Opts the user into an existing instance of the ${app.contract.name} smart contract.`
    yield ` * @param args The arguments for the contract call`
    yield ` * @param params Any additional parameters for the call`
    yield ` * @returns The opt in result`
    yield ` */`
    yield `public optIn<TMethod extends string>(args: { method?: TMethod } & ${name}OptInArgs${
      callConfig.optInMethods.some((m) => m === BARE_CALL) ? ' = {}' : ''
    }, params?: AppClientCallCoreParams & AppClientCompilationParams & CoreAppCallArgs) {`
    yield IncIndent
    if (callConfig.optInMethods.some((m) => m !== BARE_CALL)) {
      yield `return this.mapReturnValue<TMethod>(this.appClient.create({ ...this.mapMethodArgs(args), ...params, }))`
    } else {
      yield `return this.appClient.create({ ...args, ...params, })`
    }
    yield DecIndentAndCloseBlock
    yield NewLine
  }
}

function* closeOutMethod({ app, name, callConfig }: GeneratorContext): DocumentParts {
  if (callConfig.closeOutMethods.length) {
    yield `/**`
    yield ` * Makes a close_out call to an existing instance of the ${app.contract.name} smart contract.`
    yield ` * @param args The arguments for the contract call`
    yield ` * @param params Any additional parameters for the call`
    yield ` * @returns The close_out result`
    yield ` */`
    yield `public closeOut<TMethod extends string>(args: { method?: TMethod } & ${name}CloseOutArgs${
      callConfig.closeOutMethods.some((m) => m === BARE_CALL) ? ' = {}' : ''
    }, params?: AppClientCallCoreParams & CoreAppCallArgs) {`
    yield IncIndent
    if (callConfig.closeOutMethods.some((m) => m !== BARE_CALL)) {
      yield `return this.mapReturnValue<TMethod>(this.appClient.closeOut({ ...this.mapMethodArgs(args), ...params, }))`
    } else {
      yield `return this.appClient.closeOut({ ...args, ...params, })`
    }
    yield DecIndentAndCloseBlock
    yield NewLine
  }
}
function* clearState({ app, name, callConfig }: GeneratorContext): DocumentParts {
  yield `/**`
  yield ` * Makes a clear_state call to an existing instance of the ${app.contract.name} smart contract.`
  yield ` * @param args The arguments for the contract call`
  yield ` * @param params Any additional parameters for the call`
  yield ` * @returns The clear_state result`
  yield ` */`
  yield `public clearState(args: BareCallArgs, params?: AppClientCallCoreParams & CoreAppCallArgs) {`
  yield IncIndent
  yield `return this.appClient.clearState({ ...args, ...params, })`
  yield DecIndentAndCloseBlock
  yield NewLine
}

function* clientCallMethods({ app, name, callConfig }: GeneratorContext): DocumentParts {
  for (const method of app.contract.methods) {
    const methodSignature = algokit.getABIMethodSignature(method)
    // Skip methods which don't support a no_op call config
    if (!callConfig.callMethods.includes(methodSignature)) continue
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
    yield `return this.call(${name}CallFactory.${makeSafeMethodIdentifier(method.name)}(args, params))`
    yield DecIndent
    yield '}'
    yield NewLine
  }
}
