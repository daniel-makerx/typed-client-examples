import * as algokit from '@algorandfoundation/algokit-utils'
import {
  AppCallTransactionResultOfType,
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
import { Algodv2 } from 'algosdk'
import appspec from './application.json'

/** Arguments for hello(name) call */
export interface HelloArgs {
  name: string
}

export interface HelloWorldAppDeployArgs {
  /** Any deploy-time parameters to replace in the TEAL code */
  deployTimeParams?: TealTemplateParams
  /** Any args to pass to any create transaction that is issued as part of deployment */
  createArgs?: RawAppCallArgs
  /** Any args to pass to any update transaction that is issued as part of deployment */
  updateArgs?: RawAppCallArgs
  /** Any args to pass to any delete transaction that is issued as part of deployment */
  deleteArgs?: RawAppCallArgs
}

/** Builder class that generates call arguments for calls to the HelloWorldApp smart contract. */
export class HelloWorldAppBuilder {
  // Note: This should be embedded, not imported
  /** The ARC-0032 application specification for the HelloWorldApp smart contract */
  public appSpec: AppSpec = appspec as unknown as AppSpec

  /**
   * Returns the call arguments for the hello(name) smart contract call.
   * @param args The arguments needed
   * @returns The call arguments, ready to pass in to an `ApplicationClient`
   */
  hello(args: HelloArgs): AppClientCallArgs {
    return {
      method: 'hello(string)string',
      methodArgs: [args.name],
    }
  }
}

/** A client to make calls to the HelloWorldApp smart contract */
export class HelloWorldAppClient {
  /** The underlying `ApplicationClient` for when you want to have more flexibility */
  public appClient: ApplicationClient
  /** An instance of `HelloWorldAppBuilder` */
  public builder: HelloWorldAppBuilder

  /**
   * Creates a new instance of `HelloWorldAppClient`
   * @param appDetails The details to identify the app to deploy
   * @param algod An algod client instance
   */
  constructor(appDetails: AppDetails, algod: Algodv2) {
    this.builder = new HelloWorldAppBuilder()
    const app: AppSpecAppDetails = {
      ...appDetails,
      app: this.builder.appSpec,
    }
    this.appClient = algokit.getAppClient(app, algod)
  }

  private async _call<TReturn>(params: AppClientCallParams) {
    const result = await this.appClient.call(params)
    if (result.return?.decodeError) {
      throw result.return.decodeError
    }
    const returnValue = result.return?.returnValue
    return { ...result, return: returnValue as TReturn }
  }

  /**
   * Idempotently deploys the HelloWorldApp smart contract.
   * @param args The arguments for the contract call
   * @param params Any additional parameters for the call
   * @returns
   */
  public async deploy(args?: HelloWorldAppDeployArgs, params?: AppClientDeployCoreParams) {
    const result = await this.appClient.deploy({
      ...(args ?? {}),
      ...(params ?? {}),
    })
    return result
  }

  /**
   * Creates a new instance of the HelloWorldApp smart contract.
   * @param args The arguments for the contract call
   * @param params Any additional parameters for the call
   * @returns
   */
  public async create(args?: RawAppCallArgs, params?: AppClientCallCoreParams & AppClientCompilationParams) {
    const { return: r, ...result } = await this.appClient.create({
      args,
      ...(params ?? {}),
    })
    return result
  }

  /**
   * Updates an existing instance of the HelloWorldApp smart contract.
   * @param args The arguments for the contract call
   * @param params Any additional parameters for the call
   * @returns
   */
  public async update(args?: RawAppCallArgs, params?: AppClientCallCoreParams & AppClientCompilationParams) {
    const { return: r, ...result } = await this.appClient.update({
      args,
      ...(params ?? {}),
    })
    return result
  }

  /**
   * Deletes an existing instance of the HelloWorldApp smart contract.
   * @param args The arguments for the contract call
   * @param params Any additional parameters for the call
   * @returns
   */
  public async delete(args?: RawAppCallArgs, params?: AppClientCallCoreParams) {
    const { return: r, ...result } = await this.appClient.delete({
      args,
      ...(params ?? {}),
    })
    return result
  }

  /**
   * Calls the hello(name) ABI method.
   *
   * Uses OnComplete = NoOp.
   * @param args The arguments for the ABI method
   * @param params Any additional parameters for the call
   * @returns The result of the call
   */
  public async hello(
    args: HelloArgs,
    params?: AppClientCallCoreParams & CoreAppCallArgs,
  ): Promise<AppCallTransactionResultOfType<string>> {
    return this._call<string>({
      ...this.builder.hello(args),
      ...(params ?? {}),
    })
  }
}
