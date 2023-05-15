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
    "hello()string": {
      "call_config": {
        "no_op": "CALL"
      }
    },
    "create(string)string": {
      "call_config": {
        "no_op": "CREATE"
      }
    },
    "create(string,uint32)void": {
      "call_config": {
        "no_op": "CREATE"
      }
    }
  },
  "source": {
    "approval": "I3ByYWdtYSB2ZXJzaW9uIDgKaW50Y2Jsb2NrIDAgMSAxMApieXRlY2Jsb2NrIDB4IDB4NzQ2OTZkNjU3MyAweDY3NzI2NTY1NzQ2OTZlNjcgMHgxNTFmN2M3NQp0eG4gTnVtQXBwQXJncwppbnRjXzAgLy8gMAo9PQpibnogbWFpbl9sMTAKdHhuYSBBcHBsaWNhdGlvbkFyZ3MgMApwdXNoYnl0ZXMgMHgwMmJlY2UxMSAvLyAiaGVsbG8oc3RyaW5nKXN0cmluZyIKPT0KYm56IG1haW5fbDkKdHhuYSBBcHBsaWNhdGlvbkFyZ3MgMApwdXNoYnl0ZXMgMHhhYjA2YzFhOCAvLyAiaGVsbG8oKXN0cmluZyIKPT0KYm56IG1haW5fbDgKdHhuYSBBcHBsaWNhdGlvbkFyZ3MgMApwdXNoYnl0ZXMgMHg5N2YxZmMxMSAvLyAiY3JlYXRlKHN0cmluZylzdHJpbmciCj09CmJueiBtYWluX2w3CnR4bmEgQXBwbGljYXRpb25BcmdzIDAKcHVzaGJ5dGVzIDB4NjAxOTMyNjQgLy8gImNyZWF0ZShzdHJpbmcsdWludDMyKXZvaWQiCj09CmJueiBtYWluX2w2CmVycgptYWluX2w2Ogp0eG4gT25Db21wbGV0aW9uCmludGNfMCAvLyBOb09wCj09CnR4biBBcHBsaWNhdGlvbklECmludGNfMCAvLyAwCj09CiYmCmFzc2VydAp0eG5hIEFwcGxpY2F0aW9uQXJncyAxCnN0b3JlIDMKdHhuYSBBcHBsaWNhdGlvbkFyZ3MgMgppbnRjXzAgLy8gMApleHRyYWN0X3VpbnQzMgpzdG9yZSA0CmxvYWQgMwpsb2FkIDQKY2FsbHN1YiBjcmVhdGVfNwppbnRjXzEgLy8gMQpyZXR1cm4KbWFpbl9sNzoKdHhuIE9uQ29tcGxldGlvbgppbnRjXzAgLy8gTm9PcAo9PQp0eG4gQXBwbGljYXRpb25JRAppbnRjXzAgLy8gMAo9PQomJgphc3NlcnQKdHhuYSBBcHBsaWNhdGlvbkFyZ3MgMQpjYWxsc3ViIGNyZWF0ZV82CnN0b3JlIDIKYnl0ZWNfMyAvLyAweDE1MWY3Yzc1CmxvYWQgMgpjb25jYXQKbG9nCmludGNfMSAvLyAxCnJldHVybgptYWluX2w4Ogp0eG4gT25Db21wbGV0aW9uCmludGNfMCAvLyBOb09wCj09CnR4biBBcHBsaWNhdGlvbklECmludGNfMCAvLyAwCiE9CiYmCmFzc2VydApjYWxsc3ViIGhlbGxvXzQKc3RvcmUgMQpieXRlY18zIC8vIDB4MTUxZjdjNzUKbG9hZCAxCmNvbmNhdApsb2cKaW50Y18xIC8vIDEKcmV0dXJuCm1haW5fbDk6CnR4biBPbkNvbXBsZXRpb24KaW50Y18wIC8vIE5vT3AKPT0KdHhuIEFwcGxpY2F0aW9uSUQKaW50Y18wIC8vIDAKIT0KJiYKYXNzZXJ0CnR4bmEgQXBwbGljYXRpb25BcmdzIDEKY2FsbHN1YiBoZWxsb18zCnN0b3JlIDAKYnl0ZWNfMyAvLyAweDE1MWY3Yzc1CmxvYWQgMApjb25jYXQKbG9nCmludGNfMSAvLyAxCnJldHVybgptYWluX2wxMDoKdHhuIE9uQ29tcGxldGlvbgppbnRjXzAgLy8gTm9PcAo9PQpibnogbWFpbl9sMTYKdHhuIE9uQ29tcGxldGlvbgppbnRjXzEgLy8gT3B0SW4KPT0KYm56IG1haW5fbDE1CnR4biBPbkNvbXBsZXRpb24KcHVzaGludCA0IC8vIFVwZGF0ZUFwcGxpY2F0aW9uCj09CmJueiBtYWluX2wxNAplcnIKbWFpbl9sMTQ6CnR4biBBcHBsaWNhdGlvbklECmludGNfMCAvLyAwCiE9CmFzc2VydApjYWxsc3ViIHVwZGF0ZV8yCmludGNfMSAvLyAxCnJldHVybgptYWluX2wxNToKdHhuIEFwcGxpY2F0aW9uSUQKaW50Y18wIC8vIDAKPT0KYXNzZXJ0CmNhbGxzdWIgYmFyZWNyZWF0ZV81CmludGNfMSAvLyAxCnJldHVybgptYWluX2wxNjoKdHhuIEFwcGxpY2F0aW9uSUQKaW50Y18wIC8vIDAKPT0KYXNzZXJ0CmNhbGxzdWIgYmFyZWNyZWF0ZV81CmludGNfMSAvLyAxCnJldHVybgoKLy8gaW50X3RvX2FzY2lpCmludHRvYXNjaWlfMDoKcHJvdG8gMSAxCnB1c2hieXRlcyAweDMwMzEzMjMzMzQzNTM2MzczODM5IC8vICIwMTIzNDU2Nzg5IgpmcmFtZV9kaWcgLTEKaW50Y18xIC8vIDEKZXh0cmFjdDMKcmV0c3ViCgovLyBpdG9hCml0b2FfMToKcHJvdG8gMSAxCmZyYW1lX2RpZyAtMQppbnRjXzAgLy8gMAo9PQpibnogaXRvYV8xX2w1CmZyYW1lX2RpZyAtMQppbnRjXzIgLy8gMTAKLwppbnRjXzAgLy8gMAo+CmJueiBpdG9hXzFfbDQKYnl0ZWNfMCAvLyAiIgppdG9hXzFfbDM6CmZyYW1lX2RpZyAtMQppbnRjXzIgLy8gMTAKJQpjYWxsc3ViIGludHRvYXNjaWlfMApjb25jYXQKYiBpdG9hXzFfbDYKaXRvYV8xX2w0OgpmcmFtZV9kaWcgLTEKaW50Y18yIC8vIDEwCi8KY2FsbHN1YiBpdG9hXzEKYiBpdG9hXzFfbDMKaXRvYV8xX2w1OgpwdXNoYnl0ZXMgMHgzMCAvLyAiMCIKaXRvYV8xX2w2OgpyZXRzdWIKCi8vIHVwZGF0ZQp1cGRhdGVfMjoKcHJvdG8gMCAwCnR4biBTZW5kZXIKZ2xvYmFsIENyZWF0b3JBZGRyZXNzCj09Ci8vIHVuYXV0aG9yaXplZAphc3NlcnQKcHVzaGludCBUTVBMX1VQREFUQUJMRSAvLyBUTVBMX1VQREFUQUJMRQovLyBDaGVjayBhcHAgaXMgdXBkYXRhYmxlCmFzc2VydApyZXRzdWIKCi8vIGhlbGxvCmhlbGxvXzM6CnByb3RvIDEgMQpieXRlY18wIC8vICIiCmJ5dGVjXzAgLy8gIiIKc3RvcmUgNQppbnRjXzAgLy8gMApzdG9yZSA2CmhlbGxvXzNfbDE6CmxvYWQgNgpieXRlY18xIC8vICJ0aW1lcyIKYXBwX2dsb2JhbF9nZXQKPApieiBoZWxsb18zX2wzCmxvYWQgNQpieXRlY18yIC8vICJncmVldGluZyIKYXBwX2dsb2JhbF9nZXQKY29uY2F0CnB1c2hieXRlcyAweDJjMjAgLy8gIiwgIgpjb25jYXQKZnJhbWVfZGlnIC0xCmV4dHJhY3QgMiAwCmNvbmNhdApwdXNoYnl0ZXMgMHgwYSAvLyAiXG4iCmNvbmNhdApzdG9yZSA1CmxvYWQgNgppbnRjXzEgLy8gMQorCnN0b3JlIDYKYiBoZWxsb18zX2wxCmhlbGxvXzNfbDM6CmxvYWQgNQpmcmFtZV9idXJ5IDAKZnJhbWVfZGlnIDAKbGVuCml0b2IKZXh0cmFjdCA2IDAKZnJhbWVfZGlnIDAKY29uY2F0CmZyYW1lX2J1cnkgMApyZXRzdWIKCi8vIGhlbGxvCmhlbGxvXzQ6CnByb3RvIDAgMQpieXRlY18wIC8vICIiCmJ5dGVjXzAgLy8gIiIKc3RvcmUgNwppbnRjXzAgLy8gMApzdG9yZSA4CmhlbGxvXzRfbDE6CmxvYWQgOApieXRlY18xIC8vICJ0aW1lcyIKYXBwX2dsb2JhbF9nZXQKPApieiBoZWxsb180X2wzCmxvYWQgNwpieXRlY18yIC8vICJncmVldGluZyIKYXBwX2dsb2JhbF9nZXQKY29uY2F0CnB1c2hieXRlcyAweDJjMjA2ZDc5NzM3NDY1NzI3OTIwNzA2NTcyNzM2ZjZlMGEgLy8gIiwgbXlzdGVyeSBwZXJzb25cbiIKY29uY2F0CnN0b3JlIDcKbG9hZCA4CmludGNfMSAvLyAxCisKc3RvcmUgOApiIGhlbGxvXzRfbDEKaGVsbG9fNF9sMzoKbG9hZCA3CmZyYW1lX2J1cnkgMApmcmFtZV9kaWcgMApsZW4KaXRvYgpleHRyYWN0IDYgMApmcmFtZV9kaWcgMApjb25jYXQKZnJhbWVfYnVyeSAwCnJldHN1YgoKLy8gYmFyZV9jcmVhdGUKYmFyZWNyZWF0ZV81Ogpwcm90byAwIDAKYnl0ZWNfMiAvLyAiZ3JlZXRpbmciCnB1c2hieXRlcyAweDQ4NjU2YzZjNmYgLy8gIkhlbGxvIgphcHBfZ2xvYmFsX3B1dApieXRlY18xIC8vICJ0aW1lcyIKaW50Y18xIC8vIDEKYXBwX2dsb2JhbF9wdXQKaW50Y18xIC8vIDEKcmV0dXJuCgovLyBjcmVhdGUKY3JlYXRlXzY6CnByb3RvIDEgMQpieXRlY18wIC8vICIiCmJ5dGVjXzIgLy8gImdyZWV0aW5nIgpmcmFtZV9kaWcgLTEKZXh0cmFjdCAyIDAKYXBwX2dsb2JhbF9wdXQKYnl0ZWNfMSAvLyAidGltZXMiCmludGNfMSAvLyAxCmFwcF9nbG9iYWxfcHV0CmZyYW1lX2RpZyAtMQpleHRyYWN0IDIgMApwdXNoYnl0ZXMgMHg1ZiAvLyAiXyIKY29uY2F0CmJ5dGVjXzEgLy8gInRpbWVzIgphcHBfZ2xvYmFsX2dldApjYWxsc3ViIGl0b2FfMQpjb25jYXQKZnJhbWVfYnVyeSAwCmZyYW1lX2RpZyAwCmxlbgppdG9iCmV4dHJhY3QgNiAwCmZyYW1lX2RpZyAwCmNvbmNhdApmcmFtZV9idXJ5IDAKcmV0c3ViCgovLyBjcmVhdGUKY3JlYXRlXzc6CnByb3RvIDIgMApieXRlY18yIC8vICJncmVldGluZyIKZnJhbWVfZGlnIC0yCmV4dHJhY3QgMiAwCmFwcF9nbG9iYWxfcHV0CmJ5dGVjXzEgLy8gInRpbWVzIgpmcmFtZV9kaWcgLTEKYXBwX2dsb2JhbF9wdXQKaW50Y18xIC8vIDEKcmV0dXJu",
    "clear": "I3ByYWdtYSB2ZXJzaW9uIDgKaW50Y2Jsb2NrIDEKY2FsbHN1YiBjbGVhcl8wCmludGNfMCAvLyAxCnJldHVybgoKLy8gY2xlYXIKY2xlYXJfMDoKcHJvdG8gMCAwCmludGNfMCAvLyAxCnJldHVybg=="
  },
  "state": {
    "global": {
      "num_byte_slices": 1,
      "num_uints": 1
    },
    "local": {
      "num_byte_slices": 0,
      "num_uints": 0
    }
  },
  "schema": {
    "global": {
      "declared": {
        "greeting": {
          "type": "bytes",
          "key": "greeting",
          "descr": ""
        },
        "times": {
          "type": "uint64",
          "key": "times",
          "descr": ""
        }
      },
      "reserved": {}
    },
    "local": {
      "declared": {},
      "reserved": {}
    }
  },
  "contract": {
    "name": "LifeCycleApp",
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
      },
      {
        "name": "hello",
        "args": [],
        "returns": {
          "type": "string"
        }
      },
      {
        "name": "create",
        "args": [
          {
            "type": "string",
            "name": "greeting"
          }
        ],
        "returns": {
          "type": "string"
        },
        "desc": "ABI create method with 1 argument"
      },
      {
        "name": "create",
        "args": [
          {
            "type": "string",
            "name": "greeting"
          },
          {
            "type": "uint32",
            "name": "times"
          }
        ],
        "returns": {
          "type": "void"
        },
        "desc": "ABI create method with 2 arguments"
      }
    ],
    "networks": {}
  },
  "bare_call_config": {
    "no_op": "CREATE",
    "opt_in": "CREATE",
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

export type LifeCycleApp = {
  methods: 
    & Record<'hello(string)string', {
      argsObj: {
        name: string
      }
      argsTuple: [name: string]
      returns: string
    }>
    & Record<'hello()string', {
      argsObj: {
      }
      argsTuple: []
      returns: string
    }>
    & Record<'create(string)string', {
      argsObj: {
        greeting: string
      }
      argsTuple: [greeting: string]
      returns: string
    }>
    & Record<'create(string,uint32)void', {
      argsObj: {
        greeting: string
        times: number
      }
      argsTuple: [greeting: string, times: number]
      returns: void
    }>
  state: {
    global: {
      'greeting'?: BinaryState
      'times'?: IntegerState
    }
  }
}
export type IntegerState = { asBigInt(): bigint, asNumber(): number }
export type BinaryState = { asByteArray(): Uint8Array, asString(): string }
export type MethodArgs<TSignature extends keyof LifeCycleApp['methods']> = LifeCycleApp['methods'][TSignature]['argsObj' | 'argsTuple']
export type MethodReturn<TSignature extends keyof LifeCycleApp['methods']> = LifeCycleApp['methods'][TSignature]['returns']
type MapperArgs<TSignature extends keyof LifeCycleApp['methods']> = TSignature extends any ? [signature: TSignature, args: MethodArgs<TSignature>, params: AppClientCallCoreParams & CoreAppCallArgs ] : never

export type LifeCycleAppCreateArgs =
  | (BareCallArgs & CoreAppCallArgs & (OnCompleteNoOp | OnCompleteOptIn))
  | ['create(string)string', MethodArgs<'create(string)string'>, (CoreAppCallArgs & (OnCompleteNoOp))?]
  | ['create(string,uint32)void', MethodArgs<'create(string,uint32)void'>, (CoreAppCallArgs & (OnCompleteNoOp))?]
export type LifeCycleAppUpdateArgs =
  | BareCallArgs & CoreAppCallArgs
export type LifeCycleAppDeployArgs = {
  deployTimeParams?: TealTemplateParams
  createArgs?: LifeCycleAppCreateArgs
  updateArgs?: LifeCycleAppUpdateArgs
}

export abstract class LifeCycleAppCallFactory {
  static helloStringString(args: MethodArgs<'hello(string)string'>, params: AppClientCallCoreParams & CoreAppCallArgs = {}) {
    return {
      method: 'hello(string)string' as const,
      methodArgs: Array.isArray(args) ? args : [args.name],
      ...params,
    }
  }
  static helloString(args: MethodArgs<'hello()string'>, params: AppClientCallCoreParams & CoreAppCallArgs = {}) {
    return {
      method: 'hello()string' as const,
      methodArgs: Array.isArray(args) ? args : [],
      ...params,
    }
  }
  static createStringString(args: MethodArgs<'create(string)string'>, params: AppClientCallCoreParams & CoreAppCallArgs = {}) {
    return {
      method: 'create(string)string' as const,
      methodArgs: Array.isArray(args) ? args : [args.greeting],
      ...params,
    }
  }
  static createStringUint32Void(args: MethodArgs<'create(string,uint32)void'>, params: AppClientCallCoreParams & CoreAppCallArgs = {}) {
    return {
      method: 'create(string,uint32)void' as const,
      methodArgs: Array.isArray(args) ? args : [args.greeting, args.times],
      ...params,
    }
  }
}
function mapBySignature(...[signature, args, params]: MapperArgs<keyof LifeCycleApp['methods']>) {
  switch(signature) {
    case 'hello(string)string':
      return LifeCycleAppCallFactory.helloStringString(args, params)
    case 'hello()string':
      return LifeCycleAppCallFactory.helloString(args, params)
    case 'create(string)string':
      return LifeCycleAppCallFactory.createStringString(args, params)
    case 'create(string,uint32)void':
      return LifeCycleAppCallFactory.createStringUint32Void(args, params)
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
  public call<TSignature extends keyof LifeCycleApp['methods']>(request: CallRequest<TSignature, any>, returnValueFormatter?: (value: any) => MethodReturn<TSignature>) {
    return this.mapReturnValue<MethodReturn<TSignature>>(this.appClient.call(request), returnValueFormatter)
  }

  /**
   * Idempotently deploys the LifeCycleApp smart contract.
   * @param params The arguments for the contract calls and any additional parameters for the call
   * @returns The deployment result
   */
  public deploy(params: LifeCycleAppDeployArgs & AppClientDeployCoreParams = {}) {
    return this.appClient.deploy({ 
      ...params,
      createArgs: Array.isArray(params.createArgs) ? mapBySignature(...params.createArgs as [any, any, any]): params.createArgs,
      updateArgs: Array.isArray(params.updateArgs) ? mapBySignature(...params.updateArgs as [any, any, any]): params.updateArgs,
    })
  }

  /**
   * Creates a new instance of the LifeCycleApp smart contract using a bare call.
   * @param args The arguments for the bare call
   * @returns The create result
   */
  public create(args: BareCallArgs & AppClientCallCoreParams & AppClientCompilationParams & CoreAppCallArgs & (OnCompleteNoOp | OnCompleteOptIn)): Promise<AppCallTransactionResultOfType<undefined>>;
  /**
   * Creates a new instance of the LifeCycleApp smart contract using the create(string)string ABI method.
   * @param method The ABI method to use
   * @param args The arguments for the contract call
   * @param params Any additional parameters for the call
   * @returns The create result
   */
  public create(method: 'create(string)string', args: MethodArgs<'create(string)string'>, params?: AppClientCallCoreParams & AppClientCompilationParams  & (OnCompleteNoOp)): Promise<AppCallTransactionResultOfType<MethodReturn<'create(string)string'>>>;
  /**
   * Creates a new instance of the LifeCycleApp smart contract using the create(string,uint32)void ABI method.
   * @param method The ABI method to use
   * @param args The arguments for the contract call
   * @param params Any additional parameters for the call
   * @returns The create result
   */
  public create(method: 'create(string,uint32)void', args: MethodArgs<'create(string,uint32)void'>, params?: AppClientCallCoreParams & AppClientCompilationParams  & (OnCompleteNoOp)): Promise<AppCallTransactionResultOfType<MethodReturn<'create(string,uint32)void'>>>;
  public create(...args: any[]): Promise<AppCallTransactionResultOfType<unknown>> {
    if(typeof args[0] !== 'string') {
      return this.appClient.create({...args[0], })
    } else {
      return this.appClient.create({ ...mapBySignature(args[0] as any, args[1], args[2]), })
    }
  }

  /**
   * Updates an existing instance of the LifeCycleApp smart contract using a bare call.
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
   * Makes a clear_state call to an existing instance of the LifeCycleApp smart contract.
   * @param args The arguments for the contract call
   * @param params Any additional parameters for the call
   * @returns The clear_state result
   */
  public clearState(args: BareCallArgs, params?: AppClientCallCoreParams & CoreAppCallArgs) {
    return this.appClient.clearState({ ...args, ...params, })
  }

  /**
   * Calls the hello(string)string ABI method.
   *
   * @param args The arguments for the ABI method
   * @param params Any additional parameters for the call
   * @returns The result of the call
   */
  public helloStringString(args: MethodArgs<'hello(string)string'>, params?: AppClientCallCoreParams & CoreAppCallArgs) {
    return this.call(LifeCycleAppCallFactory.helloStringString(args, params))
  }

  /**
   * Calls the hello()string ABI method.
   *
   * @param args The arguments for the ABI method
   * @param params Any additional parameters for the call
   * @returns The result of the call
   */
  public helloString(args: MethodArgs<'hello()string'>, params?: AppClientCallCoreParams & CoreAppCallArgs) {
    return this.call(LifeCycleAppCallFactory.helloString(args, params))
  }

  private static getBinaryState(state: AppState, key: string): BinaryState | undefined {
    const value = state[key]
    if (!value) return undefined
    if (!('valueRaw' in value))
      throw new Error(`Failed to parse state value for ${key}; received an int when expected a byte array`)
    return {
      asString(): string {
        return value.value
      },
      asByteArray(): Uint8Array {
        return value.valueRaw
      }
    }
  }

  private static getIntegerState(state: AppState, key: string): IntegerState | undefined {
    const value = state[key]
    if (!value) return undefined
    if ('valueRaw' in value)
      throw new Error(`Failed to parse state value for ${key}; received a byte array when expected a number`)
    return {
      asBigInt() {
        return typeof value.value === 'bigint' ? value.value : BigInt(value.value)
      },
      asNumber(): number {
        return typeof value.value === 'bigint' ? Number(value.value) : value.value
      },
    }
  }

  /**
   * Returns the application's global state wrapped in a strongly typed accessor with options to format the stored value
   */
  public async getGlobalState(): Promise<LifeCycleApp['state']['global']> {
    const state = await this.appClient.getGlobalState()
    return {
      get greeting() {
        return LifeCycleAppClient.getBinaryState(state, 'greeting')
      },
      get times() {
        return LifeCycleAppClient.getIntegerState(state, 'times')
      },
    }
  }

}
