import * as algokit from '@algorandfoundation/algokit-utils'
import {
  AppSpecAppDetails,
  ApplicationClient,
  ResolveAppByCreatorAndName,
  ResolveAppById,
} from '@algorandfoundation/algokit-utils/types/app-client'
import { AppSpec } from '@algorandfoundation/algokit-utils/types/app-spec'
import { SendTransactionFrom } from '@algorandfoundation/algokit-utils/types/transaction'
import { Algodv2, SuggestedParams } from 'algosdk'
import fs from 'fs/promises'
import path from 'path'

export class HelloWorldAppClient {
  appClient: ApplicationClient
  constructor(appDetails: AppSpecAppDetails, algod: Algodv2) {
    this.appClient = algokit.getAppClient(appDetails, algod)
  }
  deploy() {}

  async hello(name: string): Promise<string> {
    const response = await this.appClient.call({
      method: 'hello(string)string',
      methodArgs: [name],
    })
    const result = response.return?.returnValue
    return result as string
  }
}

export async function getHelloWorldAppClient(
  appDetails: {
    /** Default sender to use for transactions issued by this application client */
    sender?: SendTransactionFrom
    /** Default suggested params object to use */
    params?: SuggestedParams
  } & (ResolveAppById | ResolveAppByCreatorAndName),
  algod: Algodv2,
): Promise<HelloWorldAppClient> {
  const appSpecJson = await fs.readFile(path.join(__dirname, 'application.json'))
  const app = JSON.parse(appSpecJson.toString('utf-8')) as AppSpec
  return new HelloWorldAppClient(
    {
      ...appDetails,
      app,
    },
    algod,
  )
}
