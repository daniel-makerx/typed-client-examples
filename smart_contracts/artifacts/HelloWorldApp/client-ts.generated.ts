/* eslint-disable */
/**
 * This file was automatically generated by algokit-client-generator.
 * DO NOT MODIFY IT BY HAND.
 */
import * as algokit from '@algorandfoundation/algokit-utils'
import {
  AppCallTransactionResultOfType,
  CoreAppCallArgs,
  RawAppCallArgs,
  TealTemplateParams,
} from '@algorandfoundation/algokit-utils/types/app'
import {
  AppClientCallCoreParams,
  AppClientCompilationParams,
  AppClientDeployCoreParams,
  AppDetails,
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
    },
    "hello_world_check(string)void": {
      "call_config": {
        "no_op": "CALL"
      }
    }
  },
  "source": {
    "approval": "I3ByYWdtYSB2ZXJzaW9uIDgKaW50Y2Jsb2NrIDAgMQp0eG4gTnVtQXBwQXJncwppbnRjXzAgLy8gMAo9PQpibnogbWFpbl9sNgp0eG5hIEFwcGxpY2F0aW9uQXJncyAwCnB1c2hieXRlcyAweDAyYmVjZTExIC8vICJoZWxsbyhzdHJpbmcpc3RyaW5nIgo9PQpibnogbWFpbl9sNQp0eG5hIEFwcGxpY2F0aW9uQXJncyAwCnB1c2hieXRlcyAweGJmOWMxZWRmIC8vICJoZWxsb193b3JsZF9jaGVjayhzdHJpbmcpdm9pZCIKPT0KYm56IG1haW5fbDQKZXJyCm1haW5fbDQ6CnR4biBPbkNvbXBsZXRpb24KaW50Y18wIC8vIE5vT3AKPT0KdHhuIEFwcGxpY2F0aW9uSUQKaW50Y18wIC8vIDAKIT0KJiYKYXNzZXJ0CnR4bmEgQXBwbGljYXRpb25BcmdzIDEKY2FsbHN1YiBoZWxsb3dvcmxkY2hlY2tfMwppbnRjXzEgLy8gMQpyZXR1cm4KbWFpbl9sNToKdHhuIE9uQ29tcGxldGlvbgppbnRjXzAgLy8gTm9PcAo9PQp0eG4gQXBwbGljYXRpb25JRAppbnRjXzAgLy8gMAohPQomJgphc3NlcnQKdHhuYSBBcHBsaWNhdGlvbkFyZ3MgMQpjYWxsc3ViIGhlbGxvXzIKc3RvcmUgMApwdXNoYnl0ZXMgMHgxNTFmN2M3NSAvLyAweDE1MWY3Yzc1CmxvYWQgMApjb25jYXQKbG9nCmludGNfMSAvLyAxCnJldHVybgptYWluX2w2Ogp0eG4gT25Db21wbGV0aW9uCmludGNfMCAvLyBOb09wCj09CmJueiBtYWluX2wxMgp0eG4gT25Db21wbGV0aW9uCnB1c2hpbnQgNCAvLyBVcGRhdGVBcHBsaWNhdGlvbgo9PQpibnogbWFpbl9sMTEKdHhuIE9uQ29tcGxldGlvbgpwdXNoaW50IDUgLy8gRGVsZXRlQXBwbGljYXRpb24KPT0KYm56IG1haW5fbDEwCmVycgptYWluX2wxMDoKdHhuIEFwcGxpY2F0aW9uSUQKaW50Y18wIC8vIDAKIT0KYXNzZXJ0CmNhbGxzdWIgZGVsZXRlXzEKaW50Y18xIC8vIDEKcmV0dXJuCm1haW5fbDExOgp0eG4gQXBwbGljYXRpb25JRAppbnRjXzAgLy8gMAohPQphc3NlcnQKY2FsbHN1YiB1cGRhdGVfMAppbnRjXzEgLy8gMQpyZXR1cm4KbWFpbl9sMTI6CnR4biBBcHBsaWNhdGlvbklECmludGNfMCAvLyAwCj09CmFzc2VydAppbnRjXzEgLy8gMQpyZXR1cm4KCi8vIHVwZGF0ZQp1cGRhdGVfMDoKcHJvdG8gMCAwCnR4biBTZW5kZXIKZ2xvYmFsIENyZWF0b3JBZGRyZXNzCj09Ci8vIHVuYXV0aG9yaXplZAphc3NlcnQKcHVzaGludCBUTVBMX1VQREFUQUJMRSAvLyBUTVBMX1VQREFUQUJMRQovLyBDaGVjayBhcHAgaXMgdXBkYXRhYmxlCmFzc2VydApyZXRzdWIKCi8vIGRlbGV0ZQpkZWxldGVfMToKcHJvdG8gMCAwCnR4biBTZW5kZXIKZ2xvYmFsIENyZWF0b3JBZGRyZXNzCj09Ci8vIHVuYXV0aG9yaXplZAphc3NlcnQKcHVzaGludCBUTVBMX0RFTEVUQUJMRSAvLyBUTVBMX0RFTEVUQUJMRQovLyBDaGVjayBhcHAgaXMgZGVsZXRhYmxlCmFzc2VydApyZXRzdWIKCi8vIGhlbGxvCmhlbGxvXzI6CnByb3RvIDEgMQpwdXNoYnl0ZXMgMHggLy8gIiIKcHVzaGJ5dGVzIDB4NDg2NTZjNmM2ZjJjMjAgLy8gIkhlbGxvLCAiCmZyYW1lX2RpZyAtMQpleHRyYWN0IDIgMApjb25jYXQKZnJhbWVfYnVyeSAwCmZyYW1lX2RpZyAwCmxlbgppdG9iCmV4dHJhY3QgNiAwCmZyYW1lX2RpZyAwCmNvbmNhdApmcmFtZV9idXJ5IDAKcmV0c3ViCgovLyBoZWxsb193b3JsZF9jaGVjawpoZWxsb3dvcmxkY2hlY2tfMzoKcHJvdG8gMSAwCmZyYW1lX2RpZyAtMQpleHRyYWN0IDIgMApwdXNoYnl0ZXMgMHg1NzZmNzI2YzY0IC8vICJXb3JsZCIKPT0KYXNzZXJ0CnJldHN1Yg==",
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
        },
        "desc": "Returns Hello, {name}"
      },
      {
        "name": "hello_world_check",
        "args": [
          {
            "type": "string",
            "name": "name"
          }
        ],
        "returns": {
          "type": "void"
        },
        "desc": "Asserts {name} is \"World\""
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
export type BareCallArgs = Omit<RawAppCallArgs, keyof CoreAppCallArgs>

export type HelloArgsObj = {
  'name': string
}
export type HelloArgsTuple = [name: string]
export type HelloArgs = HelloArgsObj | HelloArgsTuple
export type HelloWorldCheckArgsObj = {
  'name': string
}
export type HelloWorldCheckArgsTuple = [name: string]
export type HelloWorldCheckArgs = HelloWorldCheckArgsObj | HelloWorldCheckArgsTuple

export type HelloWorldAppCreateArgs = BareCallArgs
export type HelloWorldAppUpdateArgs = BareCallArgs
export type HelloWorldAppDeleteArgs = BareCallArgs
export type HelloWorldAppDeployArgs = {
  deployTimeParams?: TealTemplateParams
  createArgs?: HelloWorldAppCreateArgs & CoreAppCallArgs
  updateArgs?: HelloWorldAppUpdateArgs & CoreAppCallArgs
  deleteArgs?: HelloWorldAppDeleteArgs & CoreAppCallArgs
}

export abstract class HelloWorldAppCallFactory {
  static hello(args: HelloArgs, params: AppClientCallCoreParams & CoreAppCallArgs = {}): CallRequest<string, HelloArgsTuple>  {
    return {
      method: 'hello(string)string',
      methodArgs: Array.isArray(args) ? args : [args.name],
      ...params,
    }
  }
  static helloWorldCheck(args: HelloWorldCheckArgs, params: AppClientCallCoreParams & CoreAppCallArgs = {}): CallRequest<void, HelloWorldCheckArgsTuple>  {
    return {
      method: 'hello_world_check(string)void',
      methodArgs: Array.isArray(args) ? args : [args.name],
      ...params,
    }
  }
}

/** A client to make calls to the HelloWorldApp smart contract */
export class HelloWorldAppClient {
  /** The underlying `ApplicationClient` for when you want to have more flexibility */
  public readonly appClient: ApplicationClient

  /**
   * Creates a new instance of `HelloWorldAppClient`
   * @param appDetails The details to identify the app to deploy
   * @param algod An algod client instance
   */
  constructor(appDetails: AppDetails, algod: Algodv2) {
    this.appClient = algokit.getAppClient({
      ...appDetails,
      app: APP_SPEC
    }, algod)
  }

  public async call<TReturn>(params: CallRequest<TReturn, any>): Promise<AppCallTransactionResultOfType<TReturn>> {
    const result = await this.appClient.call(params)
    if(result.return?.decodeError) {
      throw result.return.decodeError
    }
    const returnValue = result.return?.returnValue as TReturn
    return { ...result, return: returnValue }
  }

  /**
   * Idempotently deploys the HelloWorldApp smart contract.
   * @param args The arguments for the contract call
   * @param params Any additional parameters for the call
   * @returns The deployment result
   */
  public deploy(args: HelloWorldAppDeployArgs = {}, params?: AppClientDeployCoreParams) {
    return this.appClient.deploy({ ...args, ...params, })
  }

  /**
   * Creates a new instance of the HelloWorldApp smart contract.
   * @param args The arguments for the contract call
   * @param params Any additional parameters for the call
   * @returns The creation result
   */
  public create(args: HelloWorldAppCreateArgs = {}, params?: AppClientCallCoreParams & AppClientCompilationParams & CoreAppCallArgs) {
    return this.appClient.create({ ...args, ...params, })
  }

  /**
   * Updates an existing instance of the HelloWorldApp smart contract.
   * @param args The arguments for the contract call
   * @param params Any additional parameters for the call
   * @returns The update result
   */
  public update(args: HelloWorldAppUpdateArgs = {}, params?: AppClientCallCoreParams & AppClientCompilationParams & CoreAppCallArgs) {
    return this.appClient.update({ ...args, ...params, })
  }

  /**
   * Deletes an existing instance of the HelloWorldApp smart contract.
   * @param args The arguments for the contract call
   * @param params Any additional parameters for the call
   * @returns The deletion result
   */
  public delete(args: HelloWorldAppDeleteArgs = {}, params?: AppClientCallCoreParams & AppClientCompilationParams & CoreAppCallArgs) {
    return this.appClient.delete({ ...args, ...params, })
  }

  /**
   * Returns Hello, {name}
   *
   * Calls the hello(string)string ABI method.
   *
   * @param args The arguments for the ABI method
   * @param params Any additional parameters for the call
   * @returns The result of the call
   */
  public hello(args: HelloArgs, params?: AppClientCallCoreParams & CoreAppCallArgs) {
    return this.call(HelloWorldAppCallFactory.hello(args, params))
  }

  /**
   * Asserts {name} is "World"
   *
   * Calls the hello_world_check(string)void ABI method.
   *
   * @param args The arguments for the ABI method
   * @param params Any additional parameters for the call
   * @returns The result of the call
   */
  public helloWorldCheck(args: HelloWorldCheckArgs, params?: AppClientCallCoreParams & CoreAppCallArgs) {
    return this.call(HelloWorldAppCallFactory.helloWorldCheck(args, params))
  }

}
