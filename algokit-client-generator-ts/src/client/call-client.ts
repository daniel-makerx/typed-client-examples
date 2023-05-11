import { DecIndent, DecIndentAndCloseBlock, DocumentParts, IncIndent, indent, inline, NewLine } from '../output/writer'
import * as algokit from '@algorandfoundation/algokit-utils'
import { notFalsy } from '../util/not-falsy'
import { makeSafeMethodIdentifier, makeSafeTypeIdentifier } from '../util/sanitization'
import { extractMethodNameFromSignature } from './helpers/extract-method-name-from-signature'
import { BARE_CALL, MethodList } from './helpers/get-call-config-summary'
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
    `public async mapReturnValue<TReturn>`,
    `(resultPromise: Promise<AppCallTransactionResult> | AppCallTransactionResult): `,
    `Promise<AppCallTransactionResultOfType<TReturn>> {`,
  )
  yield IncIndent
  yield `const result = await resultPromise`
  yield `if(result.return?.decodeError) {`
  yield* indent(`throw result.return.decodeError`)
  yield `}`
  yield `const returnValue = result.return?.returnValue as TReturn`
  yield `return { ...result, return: returnValue }`
  yield DecIndentAndCloseBlock
  yield NewLine

  yield `public call<TSignature extends keyof ${name}['methods']>(params: CallRequest<TSignature, any>) {`
  yield IncIndent
  yield `return this.mapReturnValue<MethodReturn<TSignature>>(this.appClient.call(params))`
  yield DecIndentAndCloseBlock
  yield NewLine

  yield* deployMethods(ctx)
  yield* clearState(ctx)
  yield* clientCallMethods(ctx)
  // yield* getStateMethods(ctx)

  yield DecIndentAndCloseBlock
}

function* deployMethods({ app, callConfig, name }: GeneratorContext): DocumentParts {
  // yield `/**`
  // yield ` * Idempotently deploys the ${app.contract.name} smart contract.`
  // yield ` * @param params The arguments for the contract calls and any additional parameters for the call`
  // yield ` * @returns The deployment result`
  // yield ` */`
  // yield `public deploy(params: ${name}DeployArgs & AppClientDeployCoreParams = {}) {`
  // yield IncIndent
  // if (callConfig.createMethods.some((m) => m !== BARE_CALL)) {
  //   yield `const { boxes: create_boxes, lease: create_lease, onCompleteAction: createOnCompleteAction, ...createArgs } = params.createArgs ?? {}`
  // } else {
  //   yield `const { onCompleteAction: createOnCompleteAction } = params.createArgs ?? {}`
  // }
  // if (callConfig.updateMethods.some((m) => m !== BARE_CALL))
  //   yield `const { boxes: update_boxes, lease: update_lease, ...updateArgs } = params.updateArgs ?? {}`
  // if (callConfig.deleteMethods.some((m) => m !== BARE_CALL))
  //   yield `const { boxes: delete_boxes, lease: delete_lease, ...deleteArgs } = params.deleteArgs ?? {}`
  // yield `return this.appClient.deploy({ `
  // yield IncIndent
  // yield `...params,`
  // if (callConfig.createMethods.some((m) => m !== BARE_CALL))
  //   yield `createArgs: params.createArgs ? this.mapMethodArgs(createArgs, { boxes: create_boxes, lease: create_lease }) : undefined,`
  // yield `createOnCompleteAction,`
  // if (callConfig.updateMethods.some((m) => m !== BARE_CALL))
  //   yield `updateArgs: params.updateArgs ? this.mapMethodArgs(updateArgs, { boxes: update_boxes, lease: update_lease }) : undefined,`
  // if (callConfig.deleteMethods.some((m) => m !== BARE_CALL))
  //   yield `deleteArgs: params.deleteArgs ? this.mapMethodArgs(deleteArgs, { boxes: delete_boxes, lease: delete_lease }) : undefined,`
  // yield DecIndent
  // yield `})`
  //  yield DecIndentAndCloseBlock
  yield NewLine
  yield* overloadedMethod(`Creates a new instance of the ${app.contract.name} smart contract`, callConfig.createMethods, 'create', true)
  yield* overloadedMethod(
    `Updates an existing instance of the ${app.contract.name} smart contract`,
    callConfig.updateMethods,
    'update',
    true,
  )
  yield* overloadedMethod(`Deletes an existing instance of the ${app.contract.name} smart contract`, callConfig.deleteMethods, 'delete')
  yield* overloadedMethod(
    `Opts the user into an existing instance of the ${app.contract.name} smart contract`,
    callConfig.optInMethods,
    'optIn',
  )
  yield* overloadedMethod(
    `Makes a close out call to an existing instance of the ${app.contract.name} smart contract`,
    callConfig.closeOutMethods,
    'closeOut',
  )
}

function* overloadedMethod(
  description: string,
  methods: MethodList,
  verb: 'create' | 'update' | 'optIn' | 'closeOut' | 'delete',
  includeCompilation?: boolean,
): DocumentParts {
  if (methods.length) {
    for (const methodSig of methods) {
      if (methodSig === BARE_CALL) {
        yield `/**`
        yield ` * ${description} using a bare ABI call.`
        yield ` * @param args The arguments for the contract call`
        yield ` * @param params Any additional parameters for the call`
        yield ` * @returns The ${verb} result`
        yield ` */`
        yield `public ${verb}(args: BareCallArgs, params?: AppClientCallCoreParams ${
          includeCompilation ? '& AppClientCompilationParams ' : ''
        }& CoreAppCallArgs): Promise<AppCallTransactionResultOfType<undefined>>;`
      } else {
        yield `/**`
        yield ` * ${description} using the ${methodSig} ABI method.`
        yield ` * @param method The ABI method to use`
        yield ` * @param args The arguments for the contract call`
        yield ` * @param params Any additional parameters for the call`
        yield ` * @returns The ${verb} result`
        yield ` */`
        yield `public ${verb}(method: '${methodSig}', args: MethodArgs<'${methodSig}'>, params?: AppClientCallCoreParams ${
          includeCompilation ? '& AppClientCompilationParams ' : ''
        }): Promise<AppCallTransactionResultOfType<MethodReturn<'${methodSig}'>>>;`
      }
    }
    yield `public ${verb}(...args: any[]): Promise<AppCallTransactionResultOfType<unknown>> {`
    yield IncIndent
    yield `if(typeof args[0] !== 'string') {`
    yield* indent(`return this.appClient.${verb}({...args[0], ...args[1], })`)
    yield '} else {'
    yield* indent(`return this.appClient.${verb}({ ...mapBySignature(args[0] as any, args[1], args[2]), })`)
    yield '}'
    yield DecIndentAndCloseBlock
    yield NewLine
  }
}

function* clearState({ app }: GeneratorContext): DocumentParts {
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

function* clientCallMethods({ app, name, callConfig, methodSignatureToUniqueName }: GeneratorContext): DocumentParts {
  for (const method of app.contract.methods) {
    const methodSignature = algokit.getABIMethodSignature(method)
    const methodName = makeSafeMethodIdentifier(methodSignatureToUniqueName[methodSignature])
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
    yield `public ${methodName}(args: MethodArgs<'${methodSignature}'>, params?: AppClientCallCoreParams & CoreAppCallArgs) {`
    yield IncIndent
    yield `return this.call(${name}CallFactory.${methodName}(args, params))`
    yield DecIndent
    yield '}'
    yield NewLine
  }
}

function* getStateMethods({ app }: GeneratorContext): DocumentParts {
  yield `public getGlobalState(): void {`
  yield IncIndent
  yield DecIndentAndCloseBlock
  yield NewLine
}
