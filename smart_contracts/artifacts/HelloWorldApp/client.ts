import * as algokit from '@algorandfoundation/algokit-utils'
import { AppCallTransactionResultOfType } from '@algorandfoundation/algokit-utils/types/app'
import {
  AppClientCallArgs,
  AppClientCallCoreParams,
  AppClientCallParams,
  AppDetails,
  AppSpecAppDetails,
  ApplicationClient,
} from '@algorandfoundation/algokit-utils/types/app-client'
import { AppSpec } from '@algorandfoundation/algokit-utils/types/app-spec'
import { Algodv2 } from 'algosdk'
import appspec from './application.json'

export class HelloWorldAppBuilder {
  // Note: This should be embedded, not imported
  public appSpec: AppSpec = appspec as unknown as AppSpec

  hello(name: string): AppClientCallArgs {
    return {
      method: 'hello(string)string',
      methodArgs: [name],
    }
  }
}

export class HelloWorldAppClient {
  public appClient: ApplicationClient
  public builder: HelloWorldAppBuilder
  constructor(appDetails: AppDetails, algod: Algodv2) {
    this.builder = new HelloWorldAppBuilder()
    const app: AppSpecAppDetails = {
      ...appDetails,
      app: this.builder.appSpec,
    }
    this.appClient = algokit.getAppClient(app, algod)
  }

  // Example if there was a method without a return value
  /*
  async helloNoReturn(
    name: string,
    params?: Omit<AppClientCallParams, 'method' | 'methodArgs'>,
  ): Promise<Omit<AppCallTransactionResult, 'return'>> {
    return await this.appClient.call({
      method: 'hello_no_return(string)',
      methodArgs: [name],
      ...(params ?? {}),
    })
  }
  */

  async _call<TReturn>(params: AppClientCallParams) {
    const result = await this.appClient.call(params)
    if (result.return?.decodeError) {
      throw result.return.decodeError
    }
    const returnValue = result.return?.returnValue
    return { ...result, return: returnValue as TReturn }
  }

  async hello(name: string, params?: AppClientCallCoreParams): Promise<AppCallTransactionResultOfType<string>> {
    return this._call<string>({
      ...this.builder.hello(name),
      ...(params ?? {}),
    })
  }
}
