import * as algokit from '@algorandfoundation/algokit-utils'
import { DecIndent, DecIndentAndCloseBlock, DocumentParts, IncIndent, indent, inline, NewLine } from '../output/writer'
import { AlgoAppSpec } from '../schema/application'
import { notFalsy } from '../util/not-falsy'
import { makeSafeMethodIdentifier, makeSafeTypeIdentifier } from '../util/sanitization'
import { extractMethodNameFromSignature } from './helpers/extract-method-name-from-signature'
import { BARE_CALL, CallConfigSummary } from './helpers/get-call-config-summary'

export function* callClient(app: AlgoAppSpec, callConfig: CallConfigSummary): DocumentParts {
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

  yield* deployMethods(app, callConfig)
  yield* onCompleteMethods(app, callConfig)
  yield* clientCallMethods(app, callConfig)
  yield DecIndentAndCloseBlock
}

function* deployMethods(app: AlgoAppSpec, callConfig: CallConfigSummary): DocumentParts {
  const name = makeSafeTypeIdentifier(app.contract.name)
  const createUpdateDeleteMethods = callConfig.createMethods.concat(callConfig.updateMethods).concat(callConfig.deleteMethods)

  if (createUpdateDeleteMethods.some((m) => m !== BARE_CALL)) {
    const args = [
      callConfig.createMethods.length && `${name}CreateArgs`,
      callConfig.updateMethods.length && `${name}UpdateArgs`,
      callConfig.deleteMethods.length && `${name}DeleteArgs`,
    ].filter(notFalsy)

    yield `private mapDeployMethodArgs(args: ${args.join(' | ')}, params?: CoreAppCallArgs): AppClientCallArgs {`
    yield IncIndent
    yield `switch (args.method) {`
    yield IncIndent
    for (const methodSignature of createUpdateDeleteMethods) {
      if (methodSignature == BARE_CALL) continue
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
    yield `createArgs: params.createArgs ? this.mapDeployMethodArgs(createArgs, { boxes: create_boxes, lease: create_lease }) : undefined,`
  yield `createOnCompleteAction,`
  if (callConfig.updateMethods.some((m) => m !== BARE_CALL))
    yield `updateArgs: params.updateArgs ? this.mapDeployMethodArgs(updateArgs, { boxes: update_boxes, lease: update_lease }) : undefined,`
  if (callConfig.deleteMethods.some((m) => m !== BARE_CALL))
    yield `deleteArgs: params.deleteArgs ? this.mapDeployMethodArgs(deleteArgs, { boxes: delete_boxes, lease: delete_lease }) : undefined,`
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
      yield `return this.mapReturnValue<TMethod>(this.appClient.create({ ...this.mapDeployMethodArgs(args), ...params, ...{ onCompleteAction } }))`
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
      yield `return this.mapReturnValue<TMethod>(this.appClient.update({ ...this.mapDeployMethodArgs(args), ...params, }))`
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
      yield `return this.mapReturnValue<TMethod>(this.appClient.delete({ ...this.mapDeployMethodArgs(args), ...params, }))`
    } else {
      yield `return this.appClient.delete({ ...args, ...params, })`
    }
    yield DecIndentAndCloseBlock
    yield NewLine
  }
}

function* onCompleteMethods(app: AlgoAppSpec, callConfig: CallConfigSummary): DocumentParts {
  const name = makeSafeTypeIdentifier(app.contract.name)
  const onCompleteMethods = callConfig.optInMethods.concat(callConfig.closeOutMethods)

  if (onCompleteMethods.some((m) => m !== BARE_CALL)) {
    const args = [callConfig.optInMethods.length && `${name}OptInArgs`, callConfig.closeOutMethods.length && `${name}CloseOutArgs`].filter(
      notFalsy,
    )

    yield `private mapMethodArgs(args: ${args.join(' | ')}): AppClientCallArgs {`
    yield IncIndent
    yield `switch (args.method) {`
    yield IncIndent
    for (const methodSignature of onCompleteMethods) {
      if (methodSignature == BARE_CALL) continue
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
  yield ` * Makes a clear_state call to an existing instance of the ${app.contract.name} smart contract.`
  yield ` * @param args The arguments for the contract call`
  yield ` * @param params Any additional parameters for the call`
  yield ` * @returns The clear state result`
  yield ` */`
  yield `public clearState(args: BareCallArgs, params?: AppClientCallCoreParams & CoreAppCallArgs) {`
  yield IncIndent
  yield `return this.appClient.clearState({ ...args, ...params })`
  yield DecIndentAndCloseBlock
  yield NewLine

  if (callConfig.optInMethods.length) {
    yield `/**`
    yield ` * Makes an opt_in call to an existing instance of the ${app.contract.name} smart contract.`
    yield ` * @param args The arguments for the contract call`
    yield ` * @param params Any additional parameters for the call`
    yield ` * @returns The opt_in result`
    yield ` */`
    yield `public optIn<TMethod extends string>(args: { method?: TMethod } & ${name}OptInArgs${
      callConfig.optInMethods.some((m) => m === BARE_CALL) ? ' = {}' : ''
    }, params?: AppClientCallCoreParams & CoreAppCallArgs) {`
    yield IncIndent
    if (callConfig.optInMethods.some((m) => m !== BARE_CALL)) {
      yield `return this.mapReturnValue<TMethod>(this.appClient.optIn({ ...this.mapMethodArgs(args), ...params, }))`
    } else {
      yield `return this.appClient.optIn({ ...args, ...params, })`
    }
    yield DecIndentAndCloseBlock
    yield NewLine
  }

  if (callConfig.closeOutMethods.length) {
    yield `/**`
    yield ` * Makes an close_out call to an existing instance of the ${app.contract.name} smart contract.`
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

function* clientCallMethods(app: AlgoAppSpec, callConfig: CallConfigSummary): DocumentParts {
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
    yield `return this.call(${makeSafeTypeIdentifier(app.contract.name)}CallFactory.${makeSafeMethodIdentifier(method.name)}(args, params))`
    yield DecIndent
    yield '}'
    yield NewLine
  }
}
