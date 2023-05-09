import * as algokit from '@algorandfoundation/algokit-utils'
import {
  AppCallTransactionResultOfType,
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
    },
    "create_1arg(string)void": {
      "call_config": {
        "no_op": "CREATE"
      }
    },
    "create_2arg(string,uint32)void": {
      "call_config": {
        "no_op": "CREATE"
      }
    }
  },
  "source": {
    "approval": "I3ByYWdtYSB2ZXJzaW9uIDgKaW50Y2Jsb2NrIDAgMQpieXRlY2Jsb2NrIDB4NzQ2OTZkNjU3MyAweDY3NzI2NTY1NzQ2OTZlNjcgMHgKdHhuIE51bUFwcEFyZ3MKaW50Y18wIC8vIDAKPT0KYm56IG1haW5fbDgKdHhuYSBBcHBsaWNhdGlvbkFyZ3MgMApwdXNoYnl0ZXMgMHgwMmJlY2UxMSAvLyAiaGVsbG8oc3RyaW5nKXN0cmluZyIKPT0KYm56IG1haW5fbDcKdHhuYSBBcHBsaWNhdGlvbkFyZ3MgMApwdXNoYnl0ZXMgMHhjNmMzZTAwYSAvLyAiY3JlYXRlXzFhcmcoc3RyaW5nKXZvaWQiCj09CmJueiBtYWluX2w2CnR4bmEgQXBwbGljYXRpb25BcmdzIDAKcHVzaGJ5dGVzIDB4ZDg2OWY2MzYgLy8gImNyZWF0ZV8yYXJnKHN0cmluZyx1aW50MzIpdm9pZCIKPT0KYm56IG1haW5fbDUKZXJyCm1haW5fbDU6CnR4biBPbkNvbXBsZXRpb24KaW50Y18wIC8vIE5vT3AKPT0KdHhuIEFwcGxpY2F0aW9uSUQKaW50Y18wIC8vIDAKPT0KJiYKYXNzZXJ0CnR4bmEgQXBwbGljYXRpb25BcmdzIDEKc3RvcmUgMQp0eG5hIEFwcGxpY2F0aW9uQXJncyAyCmludGNfMCAvLyAwCmV4dHJhY3RfdWludDMyCnN0b3JlIDIKbG9hZCAxCmxvYWQgMgpjYWxsc3ViIGNyZWF0ZTJhcmdfNQppbnRjXzEgLy8gMQpyZXR1cm4KbWFpbl9sNjoKdHhuIE9uQ29tcGxldGlvbgppbnRjXzAgLy8gTm9PcAo9PQp0eG4gQXBwbGljYXRpb25JRAppbnRjXzAgLy8gMAo9PQomJgphc3NlcnQKdHhuYSBBcHBsaWNhdGlvbkFyZ3MgMQpjYWxsc3ViIGNyZWF0ZTFhcmdfNAppbnRjXzEgLy8gMQpyZXR1cm4KbWFpbl9sNzoKdHhuIE9uQ29tcGxldGlvbgppbnRjXzAgLy8gTm9PcAo9PQp0eG4gQXBwbGljYXRpb25JRAppbnRjXzAgLy8gMAohPQomJgphc3NlcnQKdHhuYSBBcHBsaWNhdGlvbkFyZ3MgMQpjYWxsc3ViIGhlbGxvXzIKc3RvcmUgMApwdXNoYnl0ZXMgMHgxNTFmN2M3NSAvLyAweDE1MWY3Yzc1CmxvYWQgMApjb25jYXQKbG9nCmludGNfMSAvLyAxCnJldHVybgptYWluX2w4Ogp0eG4gT25Db21wbGV0aW9uCmludGNfMCAvLyBOb09wCj09CmJueiBtYWluX2wxNAp0eG4gT25Db21wbGV0aW9uCnB1c2hpbnQgNCAvLyBVcGRhdGVBcHBsaWNhdGlvbgo9PQpibnogbWFpbl9sMTMKdHhuIE9uQ29tcGxldGlvbgpwdXNoaW50IDUgLy8gRGVsZXRlQXBwbGljYXRpb24KPT0KYm56IG1haW5fbDEyCmVycgptYWluX2wxMjoKdHhuIEFwcGxpY2F0aW9uSUQKaW50Y18wIC8vIDAKIT0KYXNzZXJ0CmNhbGxzdWIgZGVsZXRlXzEKaW50Y18xIC8vIDEKcmV0dXJuCm1haW5fbDEzOgp0eG4gQXBwbGljYXRpb25JRAppbnRjXzAgLy8gMAohPQphc3NlcnQKY2FsbHN1YiB1cGRhdGVfMAppbnRjXzEgLy8gMQpyZXR1cm4KbWFpbl9sMTQ6CnR4biBBcHBsaWNhdGlvbklECmludGNfMCAvLyAwCj09CmFzc2VydApjYWxsc3ViIGJhcmVjcmVhdGVfMwppbnRjXzEgLy8gMQpyZXR1cm4KCi8vIHVwZGF0ZQp1cGRhdGVfMDoKcHJvdG8gMCAwCnR4biBTZW5kZXIKZ2xvYmFsIENyZWF0b3JBZGRyZXNzCj09Ci8vIHVuYXV0aG9yaXplZAphc3NlcnQKcHVzaGludCBUTVBMX1VQREFUQUJMRSAvLyBUTVBMX1VQREFUQUJMRQovLyBDaGVjayBhcHAgaXMgdXBkYXRhYmxlCmFzc2VydApyZXRzdWIKCi8vIGRlbGV0ZQpkZWxldGVfMToKcHJvdG8gMCAwCnR4biBTZW5kZXIKZ2xvYmFsIENyZWF0b3JBZGRyZXNzCj09Ci8vIHVuYXV0aG9yaXplZAphc3NlcnQKcHVzaGludCBUTVBMX0RFTEVUQUJMRSAvLyBUTVBMX0RFTEVUQUJMRQovLyBDaGVjayBhcHAgaXMgZGVsZXRhYmxlCmFzc2VydApyZXRzdWIKCi8vIGhlbGxvCmhlbGxvXzI6CnByb3RvIDEgMQpieXRlY18yIC8vICIiCmJ5dGVjXzIgLy8gIiIKc3RvcmUgMwppbnRjXzAgLy8gMApzdG9yZSA0CmhlbGxvXzJfbDE6CmxvYWQgNApieXRlY18wIC8vICJ0aW1lcyIKYXBwX2dsb2JhbF9nZXQKPApieiBoZWxsb18yX2wzCmxvYWQgMwpieXRlY18xIC8vICJncmVldGluZyIKYXBwX2dsb2JhbF9nZXQKY29uY2F0CnB1c2hieXRlcyAweDJjMjAgLy8gIiwgIgpjb25jYXQKZnJhbWVfZGlnIC0xCmV4dHJhY3QgMiAwCmNvbmNhdApwdXNoYnl0ZXMgMHgwYSAvLyAiXG4iCmNvbmNhdApzdG9yZSAzCmxvYWQgNAppbnRjXzEgLy8gMQorCnN0b3JlIDQKYiBoZWxsb18yX2wxCmhlbGxvXzJfbDM6CmxvYWQgMwpmcmFtZV9idXJ5IDAKZnJhbWVfZGlnIDAKbGVuCml0b2IKZXh0cmFjdCA2IDAKZnJhbWVfZGlnIDAKY29uY2F0CmZyYW1lX2J1cnkgMApyZXRzdWIKCi8vIGJhcmVfY3JlYXRlCmJhcmVjcmVhdGVfMzoKcHJvdG8gMCAwCmJ5dGVjXzEgLy8gImdyZWV0aW5nIgpwdXNoYnl0ZXMgMHg0ODY1NmM2YzZmIC8vICJIZWxsbyIKYXBwX2dsb2JhbF9wdXQKYnl0ZWNfMCAvLyAidGltZXMiCmludGNfMSAvLyAxCmFwcF9nbG9iYWxfcHV0CmludGNfMSAvLyAxCnJldHVybgoKLy8gY3JlYXRlXzFhcmcKY3JlYXRlMWFyZ180Ogpwcm90byAxIDAKYnl0ZWNfMSAvLyAiZ3JlZXRpbmciCmZyYW1lX2RpZyAtMQpleHRyYWN0IDIgMAphcHBfZ2xvYmFsX3B1dApieXRlY18wIC8vICJ0aW1lcyIKaW50Y18xIC8vIDEKYXBwX2dsb2JhbF9wdXQKaW50Y18xIC8vIDEKcmV0dXJuCgovLyBjcmVhdGVfMmFyZwpjcmVhdGUyYXJnXzU6CnByb3RvIDIgMApieXRlY18xIC8vICJncmVldGluZyIKZnJhbWVfZGlnIC0yCmV4dHJhY3QgMiAwCmFwcF9nbG9iYWxfcHV0CmJ5dGVjXzAgLy8gInRpbWVzIgpmcmFtZV9kaWcgLTEKYXBwX2dsb2JhbF9wdXQKaW50Y18xIC8vIDEKcmV0dXJu",
    "clear": "I3ByYWdtYSB2ZXJzaW9uIDgKcHVzaGludCAwIC8vIDAKcmV0dXJu"
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
        "name": "create_1arg",
        "args": [
          {
            "type": "string",
            "name": "greeting"
          }
        ],
        "returns": {
          "type": "void"
        }
      },
      {
        "name": "create_2arg",
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
export type BareCallArgs = Omit<RawAppCallArgs, keyof CoreAppCallArgs>

export type HelloArgsObj = {
  'name': string
}
export type HelloArgsTuple = [name: string]
export type HelloArgs = HelloArgsObj | HelloArgsTuple
export type Create_1argArgsObj = {
  'greeting': string
}
export type Create_1argArgsTuple = [greeting: string]
export type Create_1argArgs = Create_1argArgsObj | Create_1argArgsTuple
export type Create_2argArgsObj = {
  'greeting': string
  'times': uint32
}
export type Create_2argArgsTuple = [greeting: string,times: uint32]
export type Create_2argArgs = Create_2argArgsObj | Create_2argArgsTuple

export type LifeCycleAppCreateArgs = BareCallArgs
export type LifeCycleAppUpdateArgs = BareCallArgs
export type LifeCycleAppDeleteArgs = BareCallArgs
export type LifeCycleAppDeployArgs = {
  deployTimeParams?: TealTemplateParams
  createArgs?: LifeCycleAppCreateArgs & CoreAppCallArgs
  updateArgs?: LifeCycleAppUpdateArgs & CoreAppCallArgs
  deleteArgs?: LifeCycleAppDeleteArgs & CoreAppCallArgs
}

export abstract class LifeCycleAppCallFactory {
  static hello(args: HelloArgs, params: AppClientCallCoreParams & AppClientCompilationParams = {}): CallRequest<string, HelloArgs>  {
    return {
      method: 'hello(string)string',
      methodArgs: Array.isArray(args) ? args : [args.name],
      ...params,
    }
  }
  static create_1arg(args: Create_1argArgs, params: AppClientCallCoreParams & AppClientCompilationParams = {}): CallRequest<void, Create_1argArgs>  {
    return {
      method: 'create_1arg(string)void',
      methodArgs: Array.isArray(args) ? args : [args.greeting],
      ...params,
    }
  }
  static create_2arg(args: Create_2argArgs, params: AppClientCallCoreParams & AppClientCompilationParams = {}): CallRequest<void, Create_2argArgs>  {
    return {
      method: 'create_2arg(string,uint32)void',
      methodArgs: Array.isArray(args) ? args : [args.greeting,args.times],
      ...params,
    }
  }
}

export class LifeCycleAppClient {
  public readonly appClient: ApplicationClient

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

  public hello(args: HelloArgs, params?: AppClientCallCoreParams & AppClientCompilationParams) {
    return this.call(LifeCycleAppCallFactory.hello(args, params))
  }

  public create_1arg(args: Create_1argArgs, params?: AppClientCallCoreParams & AppClientCompilationParams) {
    return this.call(LifeCycleAppCallFactory.create_1arg(args, params))
  }

  public create_2arg(args: Create_2argArgs, params?: AppClientCallCoreParams & AppClientCompilationParams) {
    return this.call(LifeCycleAppCallFactory.create_2arg(args, params))
  }

  public deploy(args?: LifeCycleAppDeployArgs, params?: AppClientDeployCoreParams) {
    return this.appClient.deploy({ ...args, ...params, })
  }

  public create(args?: LifeCycleAppCreateArgs, params?: AppClientCallCoreParams & AppClientCompilationParams & CoreAppCallArgs) {
    return this.appClient.create({ ...args, ...params, })
  }

  public update(args?: LifeCycleAppUpdateArgs, params?: AppClientCallCoreParams & AppClientCompilationParams & CoreAppCallArgs) {
    return this.appClient.update({ ...args, ...params, })
  }

  public delete(args?: LifeCycleAppDeleteArgs, params?: AppClientCallCoreParams & AppClientCompilationParams & CoreAppCallArgs) {
    return this.appClient.delete({ ...args, ...params, })
  }

}
