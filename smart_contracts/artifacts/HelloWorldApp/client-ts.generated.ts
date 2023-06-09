/* eslint-disable */
/**
 * This file was automatically generated by algokit-client-generator.
 * DO NOT MODIFY IT BY HAND.
 */
import * as algokit from '@algorandfoundation/algokit-utils'
import {
  AppCallTransactionResult,
  AppCallTransactionResultOfType,
  CoreAppCallArgs,
  RawAppCallArgs,
  AppState,
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
import { SendTransactionResult, TransactionToSign, SendTransactionFrom } from '@algorandfoundation/algokit-utils/types/transaction'
import { Algodv2, OnApplicationComplete, Transaction } from 'algosdk'
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

export type CallRequest<TSignature extends string, TArgs = undefined> = {
  method: TSignature
  methodArgs: TArgs
} & AppClientCallCoreParams & CoreAppCallArgs
export type BareCallArgs = Omit<RawAppCallArgs, keyof CoreAppCallArgs>
export type OnCompleteNoOp =  { onCompleteAction?: 'no_op' | OnApplicationComplete.NoOpOC }
export type OnCompleteOptIn =  { onCompleteAction: 'opt_in' | OnApplicationComplete.OptInOC }
export type OnCompleteCloseOut =  { onCompleteAction: 'close_out' | OnApplicationComplete.CloseOutOC }
export type OnCompleteDelApp =  { onCompleteAction: 'delete_application' | OnApplicationComplete.DeleteApplicationOC }
export type OnCompleteUpdApp =  { onCompleteAction: 'update_application' | OnApplicationComplete.UpdateApplicationOC }

export type HelloWorldApp = {
  methods: 
    & Record<'hello(string)string' | 'hello', {
      argsObj: {
        name: string
      }
      argsTuple: [name: string]
      returns: string
    }>
    & Record<'hello_world_check(string)void' | 'hello_world_check', {
      argsObj: {
        name: string
      }
      argsTuple: [name: string]
      returns: void
    }>
}
export type IntegerState = { asBigInt(): bigint, asNumber(): number }
export type BinaryState = { asByteArray(): Uint8Array, asString(): string }
export type MethodArgs<TSignature extends keyof HelloWorldApp['methods']> = HelloWorldApp['methods'][TSignature]['argsObj' | 'argsTuple']
export type MethodReturn<TSignature extends keyof HelloWorldApp['methods']> = HelloWorldApp['methods'][TSignature]['returns']
type MapperArgs<TSignature extends keyof HelloWorldApp['methods']> = TSignature extends any ? [signature: TSignature, args: MethodArgs<TSignature>, params: AppClientCallCoreParams & CoreAppCallArgs ] : never

export type HelloWorldAppCreateArgs =
  | (BareCallArgs & CoreAppCallArgs & (OnCompleteNoOp))
export type HelloWorldAppUpdateArgs =
  | BareCallArgs & CoreAppCallArgs
export type HelloWorldAppDeleteArgs =
  | BareCallArgs & CoreAppCallArgs
export type HelloWorldAppDeployArgs = {
  deployTimeParams?: TealTemplateParams
  createArgs?: HelloWorldAppCreateArgs
  updateArgs?: HelloWorldAppUpdateArgs
  deleteArgs?: HelloWorldAppDeleteArgs
}

export abstract class HelloWorldAppCallFactory {
  static hello(args: MethodArgs<'hello(string)string'>, params: AppClientCallCoreParams & CoreAppCallArgs = {}) {
    return {
      method: 'hello(string)string' as const,
      methodArgs: Array.isArray(args) ? args : [args.name],
      ...params,
    }
  }
  static helloWorldCheck(args: MethodArgs<'hello_world_check(string)void'>, params: AppClientCallCoreParams & CoreAppCallArgs = {}) {
    return {
      method: 'hello_world_check(string)void' as const,
      methodArgs: Array.isArray(args) ? args : [args.name],
      ...params,
    }
  }
}
function mapBySignature(...[signature, args, params]: MapperArgs<keyof HelloWorldApp['methods']>) {
  switch(signature) {
    case 'hello(string)string':
    case 'hello':
      return HelloWorldAppCallFactory.hello(args, params)
    case 'hello_world_check(string)void':
    case 'hello_world_check':
      return HelloWorldAppCallFactory.helloWorldCheck(args, params)
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

  protected async mapReturnValue<TReturn>(resultPromise: Promise<AppCallTransactionResult> | AppCallTransactionResult, returnValueFormatter?: (value: any) => TReturn): Promise<AppCallTransactionResultOfType<TReturn>> {
    const result = await resultPromise
    if(result.return?.decodeError) {
      throw result.return.decodeError
    }
    const returnValue = result.return?.returnValue !== undefined && returnValueFormatter !== undefined
      ? returnValueFormatter(result.return.returnValue)
      : result.return?.returnValue as TReturn | undefined
      return { ...result, return: returnValue }
  }

  /**
   * Calls the ABI method with the matching signature using an onCompletion code of NO_OP
   * @param request A request object containing the method signature, args, and any other relevant properties
   * @param returnValueFormatter An optional delegate which when provided will be used to map non-undefined return values to the target type
   */
  public call<TSignature extends keyof HelloWorldApp['methods']>(request: CallRequest<TSignature, any>, returnValueFormatter?: (value: any) => MethodReturn<TSignature>) {
    return this.mapReturnValue<MethodReturn<TSignature>>(this.appClient.call(request), returnValueFormatter)
  }

  /**
   * Idempotently deploys the HelloWorldApp smart contract.
   * @param params The arguments for the contract calls and any additional parameters for the call
   * @returns The deployment result
   */
  public deploy(params: HelloWorldAppDeployArgs & AppClientDeployCoreParams = {}) {
    return this.appClient.deploy({ 
      ...params,
      createArgs: Array.isArray(params.createArgs) ? mapBySignature(...params.createArgs as [any, any, any]): params.createArgs,
      deleteArgs: Array.isArray(params.deleteArgs) ? mapBySignature(...params.deleteArgs as [any, any, any]): params.deleteArgs,
      updateArgs: Array.isArray(params.updateArgs) ? mapBySignature(...params.updateArgs as [any, any, any]): params.updateArgs,
    })
  }

  /**
   * Creates a new instance of the HelloWorldApp smart contract using a bare call.
   * @param args The arguments for the bare call
   * @returns The create result
   */
  public create(args: BareCallArgs & AppClientCallCoreParams & AppClientCompilationParams & CoreAppCallArgs & (OnCompleteNoOp)): Promise<AppCallTransactionResultOfType<undefined>>;
  public create(...args: any[]): Promise<AppCallTransactionResultOfType<unknown>> {
    if(typeof args[0] !== 'string') {
      return this.appClient.create({...args[0], })
    } else {
      return this.appClient.create({ ...mapBySignature(args[0] as any, args[1], args[2]), })
    }
  }

  /**
   * Updates an existing instance of the HelloWorldApp smart contract using a bare call.
   * @param args The arguments for the bare call
   * @returns The update result
   */
  public update(args: BareCallArgs & AppClientCallCoreParams & AppClientCompilationParams & CoreAppCallArgs): Promise<AppCallTransactionResultOfType<undefined>>;
  public update(...args: any[]): Promise<AppCallTransactionResultOfType<unknown>> {
    if(typeof args[0] !== 'string') {
      return this.appClient.update({...args[0], })
    } else {
      return this.appClient.update({ ...mapBySignature(args[0] as any, args[1], args[2]), })
    }
  }

  /**
   * Deletes an existing instance of the HelloWorldApp smart contract using a bare call.
   * @param args The arguments for the bare call
   * @returns The delete result
   */
  public delete(args: BareCallArgs & AppClientCallCoreParams & CoreAppCallArgs): Promise<AppCallTransactionResultOfType<undefined>>;
  public delete(...args: any[]): Promise<AppCallTransactionResultOfType<unknown>> {
    if(typeof args[0] !== 'string') {
      return this.appClient.delete({...args[0], })
    } else {
      return this.appClient.delete({ ...mapBySignature(args[0] as any, args[1], args[2]), })
    }
  }

  /**
   * Makes a clear_state call to an existing instance of the HelloWorldApp smart contract.
   * @param args The arguments for the contract call
   * @param params Any additional parameters for the call
   * @returns The clear_state result
   */
  public clearState(args: BareCallArgs, params?: AppClientCallCoreParams & CoreAppCallArgs) {
    return this.appClient.clearState({ ...args, ...params, })
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
  public hello(args: MethodArgs<'hello(string)string'>, params?: AppClientCallCoreParams & CoreAppCallArgs) {
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
  public helloWorldCheck(args: MethodArgs<'hello_world_check(string)void'>, params?: AppClientCallCoreParams & CoreAppCallArgs) {
    return this.call(HelloWorldAppCallFactory.helloWorldCheck(args, params))
  }

}
