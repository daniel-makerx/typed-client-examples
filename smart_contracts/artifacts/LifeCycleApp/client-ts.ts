import * as algokit from '@algorandfoundation/algokit-utils'
import {
  AppCallTransactionResult,
  AppCallTransactionResultOfType,
  CoreAppCallArgs,
  RawAppCallArgs,
  TealTemplateParams,
} from '@algorandfoundation/algokit-utils/types/app'
import {
  AppClientCallArgs,
  AppClientCallCoreParams,
  AppClientCompilationParams,
  AppClientDeployCoreParams,
  AppDetails,
  ApplicationClient,
} from '@algorandfoundation/algokit-utils/types/app-client'
import { AppSpec } from '@algorandfoundation/algokit-utils/types/app-spec'
import { Algodv2 } from 'algosdk'
import app from './application.json'

export type CallRequest<TReturn, TArgs = undefined> = {
  method: string
  methodArgs: TArgs
} & AppClientCallCoreParams &
  CoreAppCallArgs
export type BareCallArgs = Omit<RawAppCallArgs, keyof CoreAppCallArgs>

export type HelloArgsObj = {
  name: string
}
export type HelloArgsTuple = [name: string]
export type HelloArgs = HelloArgsObj | HelloArgsTuple
export type Create_1argArgsObj = {
  greeting: string
}
export type Create_1argArgsTuple = [greeting: string]
export type Create_1argArgs = Create_1argArgsObj | Create_1argArgsTuple
export type Create_2argArgsObj = {
  greeting: string
  times: number
}
export type Create_2argArgsTuple = [greeting: string, times: number]
export type Create_2argArgs = Create_2argArgsObj | Create_2argArgsTuple

export type MethodSelector<TMethod extends string | undefined, TResult> = {
  method: TMethod
}
export type BareMethodSelector = MethodSelector<undefined, undefined>

export type LifeCycleAppCreateArgs =
  | (BareCallArgs & BareMethodSelector)
  | (Create_1argArgs & MethodSelector<'create_1', string>)
  | (Create_2argArgs & MethodSelector<'create_2', void>)
export type LifeCycleAppUpdateArgs = BareCallArgs
export type LifeCycleAppDeleteArgs = undefined
export type LifeCycleAppDeployArgs = {
  deployTimeParams?: TealTemplateParams
  createArgs: LifeCycleAppCreateArgs & CoreAppCallArgs
  updateArgs?: LifeCycleAppUpdateArgs & CoreAppCallArgs
  deleteArgs?: LifeCycleAppDeleteArgs
}

export abstract class LifeCycleAppCallFactory {
  static hello(
    args: HelloArgs,
    params: AppClientCallCoreParams & CoreAppCallArgs = {},
  ): CallRequest<string, HelloArgsTuple> {
    return {
      method: 'hello(string)string',
      methodArgs: Array.isArray(args) ? args : [args.name],
      ...params,
    }
  }
  static create_1arg(
    args: Create_1argArgs,
    params: AppClientCallCoreParams & CoreAppCallArgs = {},
  ): CallRequest<string, Create_1argArgsTuple> {
    return {
      method: 'create_1arg(string)string',
      methodArgs: Array.isArray(args) ? args : [args.greeting],
      ...params,
    }
  }
  static create_2arg(
    args: Create_2argArgs,
    params: AppClientCallCoreParams & CoreAppCallArgs = {},
  ): CallRequest<void, Create_2argArgsTuple> {
    return {
      method: 'create_2arg(string,uint32)void',
      methodArgs: Array.isArray(args) ? args : [args.greeting, args.times],
      ...params,
    }
  }
}

/** A client to make calls to the LifeCycleApp smart contract */
export class LifeCycleAppClient {
  /** The underlying `ApplicationClient` for when you want to have more flexibility */
  public readonly appClient: ApplicationClient

  /**
   * Creates a new instance of `LifeCycleAppClient`
   * @param appDetails The details to identify the app to deploy
   * @param algod An algod client instance
   */
  constructor(appDetails: AppDetails, algod: Algodv2) {
    this.appClient = algokit.getAppClient(
      {
        ...appDetails,
        app: app as unknown as AppSpec,
      },
      algod,
    )
  }

  private convertResult<TReturn>(result: AppCallTransactionResult): AppCallTransactionResultOfType<TReturn> {
    if (result.return?.decodeError) {
      throw result.return.decodeError
    }
    const returnValue = result.return?.returnValue as TReturn
    return { ...result, return: returnValue }
  }

  public async call<TReturn>(params: CallRequest<TReturn, any>): Promise<AppCallTransactionResultOfType<TReturn>> {
    return this.convertResult<TReturn>(await this.appClient.call(params))
  }

  private getCreateArgs(createArgs: LifeCycleAppCreateArgs & CoreAppCallArgs): AppClientCallArgs {
    if (!createArgs.method) {
      return createArgs
    }
    switch (createArgs.method) {
      case 'create_1':
        return LifeCycleAppCallFactory.create_1arg(createArgs)
      case 'create_2':
        return LifeCycleAppCallFactory.create_2arg(createArgs)
    }
  }

  /**
   * Idempotently deploys the LifeCycleApp smart contract.
   * @param params The arguments for the contract calls and any additional parameters for the call
   * @returns The deployment result
   */
  public deploy(params: LifeCycleAppDeployArgs & AppClientDeployCoreParams) {
    return this.appClient.deploy({ ...params, createArgs: this.getCreateArgs(params.createArgs) })
  }

  /**
   * Creates a new instance of the LifeCycleApp smart contract.
   * @param args The arguments for the contract call
   * @param params Any additional parameters for the call
   * @returns The creation result
   */
  public async create<TMethod extends string, TReturn>(
    args: LifeCycleAppCreateArgs & MethodSelector<TMethod, TReturn>,
    params?: AppClientCallCoreParams & AppClientCompilationParams & CoreAppCallArgs,
  ) {
    const call = this.getCreateArgs(args)
    return this.convertResult<TReturn>(await this.appClient.create({ ...call, ...params }))
  }

  /**
   * Updates an existing instance of the LifeCycleApp smart contract.
   * @param args The arguments for the contract call
   * @param params Any additional parameters for the call
   * @returns The update result
   */
  public update(
    args: LifeCycleAppUpdateArgs = {},
    params?: AppClientCallCoreParams & AppClientCompilationParams & CoreAppCallArgs,
  ) {
    return this.appClient.update({ ...args, ...params })
  }

  /**
   * Calls the hello(string)string ABI method.
   *
   * @param args The arguments for the ABI method
   * @param params Any additional parameters for the call
   * @returns The result of the call
   */
  public hello(args: HelloArgs, params?: AppClientCallCoreParams & CoreAppCallArgs) {
    return this.call(LifeCycleAppCallFactory.hello(args, params))
  }
}
