import * as algokit from '@algorandfoundation/algokit-utils'
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
import { Algodv2 } from 'algosdk'
export const APP_SPEC: AppSpec = {
  "hints": {
    "hello(string)string": {
      "call_config": {
        "no_op": "CALL"
      }
    }
  },
  "source": {
    "approval": "I3ByYWdtYSB2ZXJzaW9uIDgKaW50Y2Jsb2NrIDAgMQp0eG4gTnVtQXBwQXJncwppbnRjXzAgLy8gMAo9PQpibnogbWFpbl9sNAp0eG5hIEFwcGxpY2F0aW9uQXJncyAwCnB1c2hieXRlcyAweDAyYmVjZTExIC8vICJoZWxsbyhzdHJpbmcpc3RyaW5nIgo9PQpibnogbWFpbl9sMwplcnIKbWFpbl9sMzoKdHhuIE9uQ29tcGxldGlvbgppbnRjXzAgLy8gTm9PcAo9PQp0eG4gQXBwbGljYXRpb25JRAppbnRjXzAgLy8gMAohPQomJgphc3NlcnQKdHhuYSBBcHBsaWNhdGlvbkFyZ3MgMQpjYWxsc3ViIGhlbGxvXzIKc3RvcmUgMApwdXNoYnl0ZXMgMHgxNTFmN2M3NSAvLyAweDE1MWY3Yzc1CmxvYWQgMApjb25jYXQKbG9nCmludGNfMSAvLyAxCnJldHVybgptYWluX2w0Ogp0eG4gT25Db21wbGV0aW9uCmludGNfMCAvLyBOb09wCj09CmJueiBtYWluX2wxMAp0eG4gT25Db21wbGV0aW9uCnB1c2hpbnQgNCAvLyBVcGRhdGVBcHBsaWNhdGlvbgo9PQpibnogbWFpbl9sOQp0eG4gT25Db21wbGV0aW9uCnB1c2hpbnQgNSAvLyBEZWxldGVBcHBsaWNhdGlvbgo9PQpibnogbWFpbl9sOAplcnIKbWFpbl9sODoKdHhuIEFwcGxpY2F0aW9uSUQKaW50Y18wIC8vIDAKIT0KYXNzZXJ0CmNhbGxzdWIgZGVsZXRlXzEKaW50Y18xIC8vIDEKcmV0dXJuCm1haW5fbDk6CnR4biBBcHBsaWNhdGlvbklECmludGNfMCAvLyAwCiE9CmFzc2VydApjYWxsc3ViIHVwZGF0ZV8wCmludGNfMSAvLyAxCnJldHVybgptYWluX2wxMDoKdHhuIEFwcGxpY2F0aW9uSUQKaW50Y18wIC8vIDAKPT0KYXNzZXJ0CmludGNfMSAvLyAxCnJldHVybgoKLy8gdXBkYXRlCnVwZGF0ZV8wOgpwcm90byAwIDAKdHhuIFNlbmRlcgpnbG9iYWwgQ3JlYXRvckFkZHJlc3MKPT0KLy8gdW5hdXRob3JpemVkCmFzc2VydApwdXNoaW50IFRNUExfVVBEQVRBQkxFIC8vIFRNUExfVVBEQVRBQkxFCi8vIENoZWNrIGFwcCBpcyB1cGRhdGFibGUKYXNzZXJ0CnJldHN1YgoKLy8gZGVsZXRlCmRlbGV0ZV8xOgpwcm90byAwIDAKdHhuIFNlbmRlcgpnbG9iYWwgQ3JlYXRvckFkZHJlc3MKPT0KLy8gdW5hdXRob3JpemVkCmFzc2VydApwdXNoaW50IFRNUExfREVMRVRBQkxFIC8vIFRNUExfREVMRVRBQkxFCi8vIENoZWNrIGFwcCBpcyBkZWxldGFibGUKYXNzZXJ0CnJldHN1YgoKLy8gaGVsbG8KaGVsbG9fMjoKcHJvdG8gMSAxCnB1c2hieXRlcyAweCAvLyAiIgpwdXNoYnl0ZXMgMHg0ODY1NmM2YzZmMmMyMCAvLyAiSGVsbG8sICIKZnJhbWVfZGlnIC0xCmV4dHJhY3QgMiAwCmNvbmNhdApmcmFtZV9idXJ5IDAKZnJhbWVfZGlnIDAKbGVuCml0b2IKZXh0cmFjdCA2IDAKZnJhbWVfZGlnIDAKY29uY2F0CmZyYW1lX2J1cnkgMApyZXRzdWI=",
    "clear": "I3ByYWdtYSB2ZXJzaW9uIDgKcHVzaGludCAwIC8vIDAKcmV0dXJu"
  },
  "state": {
    "global": {
      "num_byte_slices": 0,
      "num_uints": 0
    },
    "local": {
      "num_byte_slices": 0,
      "num_uints": 0
    }
  },
  "schema": {
    "global": {
      "declared": {},
      "reserved": {}
    },
    "local": {
      "declared": {},
      "reserved": {}
    }
  },
  "contract": {
    "name": "HelloWorldApp",
    "methods": [
      {
        "name": "hello",
        "args": [
          {
            "type": "string",
            "name": "name"
          }
        ],
        "returns": {
          "type": "string"
        }
      }
    ],
    "networks": {}
  },
  "bare_call_config": {
    "delete_application": "CALL",
    "no_op": "CREATE",
    "update_application": "CALL"
  }
}

export type CallRequest<TReturn, TArgs = undefined> = {
  method: string
  methodArgs: TArgs
} & AppClientCallCoreParams & CoreAppCallArgs
export type CallResult<TReturn> = {
  return: TReturn
} & Omit<AppCallTransactionResult, 'return'>

export type HelloArgsObj = {
  'name': string
}
export type HelloArgsTuple = [string]

export abstract class HelloWorldAppCallFactory {
  static hello(args: HelloArgsObj, params?: AppClientCallCoreParams & AppClientCompilationParams = {}): CallRequest<string, HelloArgsTuple>  {
    return {
      method: 'hello(string)string',
      methodArgs: [args.name], 
      ...params,
    }
  }
}

export class HelloWorldAppClient {
  public readonly appClient: ApplicationClient
  constructor(appDetails: AppDetails, algod: Algodv2) {
    this.appClient = algokit.getAppClient({
      ...appDetails,
      app: APP_SPEC
    }, algod)
  }

  public async call<TReturn>(params: CallRequest<TReturn, any>): Promise<CallResult<TReturn>> {
    const result = await this.appClient.call(params)
    if(result.return?.decodeError) {
      throw result.return.decodeError
    }
    const returnValue = result.return?.returnValue as TReturn
    return { ...result, return: returnValue }
  }
  public hello(args: HelloArgsObj, params?: AppClientCallCoreParams & AppClientCompilationParams) {
    return this.call(HelloWorldAppCallFactory.hello(args, params))
  }
}
