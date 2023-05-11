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
import { SendTransactionResult, TransactionToSign } from '@algorandfoundation/algokit-utils/types/transaction'
import { Algodv2, OnApplicationComplete, Transaction } from 'algosdk'
export const APP_SPEC: AppSpec = {
  "hints": {
    "call_abi(string)string": {
      "read_only": true,
      "call_config": {
        "no_op": "CALL"
      }
    },
    "call_abi_txn(pay,string)string": {
      "read_only": true,
      "call_config": {
        "no_op": "CALL"
      }
    },
    "set_global(uint64,uint64,string,byte[4])void": {
      "call_config": {
        "no_op": "CALL"
      }
    },
    "set_local(uint64,uint64,string,byte[4])void": {
      "call_config": {
        "no_op": "CALL"
      }
    },
    "set_box(byte[4],string)void": {
      "call_config": {
        "no_op": "CALL"
      }
    },
    "error()void": {
      "read_only": true,
      "call_config": {
        "no_op": "CALL"
      }
    },
    "create_abi(string)string": {
      "call_config": {
        "no_op": "CREATE"
      }
    },
    "update_abi(string)string": {
      "call_config": {
        "update_application": "CALL"
      }
    },
    "delete_abi(string)string": {
      "call_config": {
        "delete_application": "CALL"
      }
    },
    "opt_in()void": {
      "call_config": {
        "opt_in": "CALL"
      }
    }
  },
  "source": {
    "approval": "I3ByYWdtYSB2ZXJzaW9uIDgKaW50Y2Jsb2NrIDAgMSAxMCA1IFRNUExfVVBEQVRBQkxFIFRNUExfREVMRVRBQkxFCmJ5dGVjYmxvY2sgMHggMHgxNTFmN2M3NQp0eG4gTnVtQXBwQXJncwppbnRjXzAgLy8gMAo9PQpibnogbWFpbl9sMjIKdHhuYSBBcHBsaWNhdGlvbkFyZ3MgMApwdXNoYnl0ZXMgMHhmMTdlODBhNSAvLyAiY2FsbF9hYmkoc3RyaW5nKXN0cmluZyIKPT0KYm56IG1haW5fbDIxCnR4bmEgQXBwbGljYXRpb25BcmdzIDAKcHVzaGJ5dGVzIDB4MGE5MmE4MWUgLy8gImNhbGxfYWJpX3R4bihwYXksc3RyaW5nKXN0cmluZyIKPT0KYm56IG1haW5fbDIwCnR4bmEgQXBwbGljYXRpb25BcmdzIDAKcHVzaGJ5dGVzIDB4YTRjZjhkZWEgLy8gInNldF9nbG9iYWwodWludDY0LHVpbnQ2NCxzdHJpbmcsYnl0ZVs0XSl2b2lkIgo9PQpibnogbWFpbl9sMTkKdHhuYSBBcHBsaWNhdGlvbkFyZ3MgMApwdXNoYnl0ZXMgMHhjZWMyODM0YSAvLyAic2V0X2xvY2FsKHVpbnQ2NCx1aW50NjQsc3RyaW5nLGJ5dGVbNF0pdm9pZCIKPT0KYm56IG1haW5fbDE4CnR4bmEgQXBwbGljYXRpb25BcmdzIDAKcHVzaGJ5dGVzIDB4YTRiNGEyMzAgLy8gInNldF9ib3goYnl0ZVs0XSxzdHJpbmcpdm9pZCIKPT0KYm56IG1haW5fbDE3CnR4bmEgQXBwbGljYXRpb25BcmdzIDAKcHVzaGJ5dGVzIDB4NDRkMGRhMGQgLy8gImVycm9yKCl2b2lkIgo9PQpibnogbWFpbl9sMTYKdHhuYSBBcHBsaWNhdGlvbkFyZ3MgMApwdXNoYnl0ZXMgMHg5ZDUyMzA0MCAvLyAiY3JlYXRlX2FiaShzdHJpbmcpc3RyaW5nIgo9PQpibnogbWFpbl9sMTUKdHhuYSBBcHBsaWNhdGlvbkFyZ3MgMApwdXNoYnl0ZXMgMHgzY2E1Y2ViNyAvLyAidXBkYXRlX2FiaShzdHJpbmcpc3RyaW5nIgo9PQpibnogbWFpbl9sMTQKdHhuYSBBcHBsaWNhdGlvbkFyZ3MgMApwdXNoYnl0ZXMgMHgyNzFiNGVlOSAvLyAiZGVsZXRlX2FiaShzdHJpbmcpc3RyaW5nIgo9PQpibnogbWFpbl9sMTMKdHhuYSBBcHBsaWNhdGlvbkFyZ3MgMApwdXNoYnl0ZXMgMHgzMGM2ZDU4YSAvLyAib3B0X2luKCl2b2lkIgo9PQpibnogbWFpbl9sMTIKZXJyCm1haW5fbDEyOgp0eG4gT25Db21wbGV0aW9uCmludGNfMSAvLyBPcHRJbgo9PQp0eG4gQXBwbGljYXRpb25JRAppbnRjXzAgLy8gMAohPQomJgphc3NlcnQKY2FsbHN1YiBvcHRpbl8xMwppbnRjXzEgLy8gMQpyZXR1cm4KbWFpbl9sMTM6CnR4biBPbkNvbXBsZXRpb24KaW50Y18zIC8vIERlbGV0ZUFwcGxpY2F0aW9uCj09CnR4biBBcHBsaWNhdGlvbklECmludGNfMCAvLyAwCiE9CiYmCmFzc2VydAp0eG5hIEFwcGxpY2F0aW9uQXJncyAxCmNhbGxzdWIgZGVsZXRlYWJpXzEyCnN0b3JlIDE2CmJ5dGVjXzEgLy8gMHgxNTFmN2M3NQpsb2FkIDE2CmNvbmNhdApsb2cKaW50Y18xIC8vIDEKcmV0dXJuCm1haW5fbDE0Ogp0eG4gT25Db21wbGV0aW9uCnB1c2hpbnQgNCAvLyBVcGRhdGVBcHBsaWNhdGlvbgo9PQp0eG4gQXBwbGljYXRpb25JRAppbnRjXzAgLy8gMAohPQomJgphc3NlcnQKdHhuYSBBcHBsaWNhdGlvbkFyZ3MgMQpjYWxsc3ViIHVwZGF0ZWFiaV8xMApzdG9yZSAxNQpieXRlY18xIC8vIDB4MTUxZjdjNzUKbG9hZCAxNQpjb25jYXQKbG9nCmludGNfMSAvLyAxCnJldHVybgptYWluX2wxNToKdHhuIE9uQ29tcGxldGlvbgppbnRjXzAgLy8gTm9PcAo9PQp0eG4gQXBwbGljYXRpb25JRAppbnRjXzAgLy8gMAo9PQomJgphc3NlcnQKdHhuYSBBcHBsaWNhdGlvbkFyZ3MgMQpjYWxsc3ViIGNyZWF0ZWFiaV84CnN0b3JlIDE0CmJ5dGVjXzEgLy8gMHgxNTFmN2M3NQpsb2FkIDE0CmNvbmNhdApsb2cKaW50Y18xIC8vIDEKcmV0dXJuCm1haW5fbDE2Ogp0eG4gT25Db21wbGV0aW9uCmludGNfMCAvLyBOb09wCj09CnR4biBBcHBsaWNhdGlvbklECmludGNfMCAvLyAwCiE9CiYmCmFzc2VydApjYWxsc3ViIGVycm9yXzYKaW50Y18xIC8vIDEKcmV0dXJuCm1haW5fbDE3Ogp0eG4gT25Db21wbGV0aW9uCmludGNfMCAvLyBOb09wCj09CnR4biBBcHBsaWNhdGlvbklECmludGNfMCAvLyAwCiE9CiYmCmFzc2VydAp0eG5hIEFwcGxpY2F0aW9uQXJncyAxCnN0b3JlIDEyCnR4bmEgQXBwbGljYXRpb25BcmdzIDIKc3RvcmUgMTMKbG9hZCAxMgpsb2FkIDEzCmNhbGxzdWIgc2V0Ym94XzUKaW50Y18xIC8vIDEKcmV0dXJuCm1haW5fbDE4Ogp0eG4gT25Db21wbGV0aW9uCmludGNfMCAvLyBOb09wCj09CnR4biBBcHBsaWNhdGlvbklECmludGNfMCAvLyAwCiE9CiYmCmFzc2VydAp0eG5hIEFwcGxpY2F0aW9uQXJncyAxCmJ0b2kKc3RvcmUgOAp0eG5hIEFwcGxpY2F0aW9uQXJncyAyCmJ0b2kKc3RvcmUgOQp0eG5hIEFwcGxpY2F0aW9uQXJncyAzCnN0b3JlIDEwCnR4bmEgQXBwbGljYXRpb25BcmdzIDQKc3RvcmUgMTEKbG9hZCA4CmxvYWQgOQpsb2FkIDEwCmxvYWQgMTEKY2FsbHN1YiBzZXRsb2NhbF80CmludGNfMSAvLyAxCnJldHVybgptYWluX2wxOToKdHhuIE9uQ29tcGxldGlvbgppbnRjXzAgLy8gTm9PcAo9PQp0eG4gQXBwbGljYXRpb25JRAppbnRjXzAgLy8gMAohPQomJgphc3NlcnQKdHhuYSBBcHBsaWNhdGlvbkFyZ3MgMQpidG9pCnN0b3JlIDQKdHhuYSBBcHBsaWNhdGlvbkFyZ3MgMgpidG9pCnN0b3JlIDUKdHhuYSBBcHBsaWNhdGlvbkFyZ3MgMwpzdG9yZSA2CnR4bmEgQXBwbGljYXRpb25BcmdzIDQKc3RvcmUgNwpsb2FkIDQKbG9hZCA1CmxvYWQgNgpsb2FkIDcKY2FsbHN1YiBzZXRnbG9iYWxfMwppbnRjXzEgLy8gMQpyZXR1cm4KbWFpbl9sMjA6CnR4biBPbkNvbXBsZXRpb24KaW50Y18wIC8vIE5vT3AKPT0KdHhuIEFwcGxpY2F0aW9uSUQKaW50Y18wIC8vIDAKIT0KJiYKYXNzZXJ0CnR4bmEgQXBwbGljYXRpb25BcmdzIDEKc3RvcmUgMgp0eG4gR3JvdXBJbmRleAppbnRjXzEgLy8gMQotCnN0b3JlIDEKbG9hZCAxCmd0eG5zIFR5cGVFbnVtCmludGNfMSAvLyBwYXkKPT0KYXNzZXJ0CmxvYWQgMQpsb2FkIDIKY2FsbHN1YiBjYWxsYWJpdHhuXzIKc3RvcmUgMwpieXRlY18xIC8vIDB4MTUxZjdjNzUKbG9hZCAzCmNvbmNhdApsb2cKaW50Y18xIC8vIDEKcmV0dXJuCm1haW5fbDIxOgp0eG4gT25Db21wbGV0aW9uCmludGNfMCAvLyBOb09wCj09CnR4biBBcHBsaWNhdGlvbklECmludGNfMCAvLyAwCiE9CiYmCmFzc2VydAp0eG5hIEFwcGxpY2F0aW9uQXJncyAxCmNhbGxzdWIgY2FsbGFiaV8wCnN0b3JlIDAKYnl0ZWNfMSAvLyAweDE1MWY3Yzc1CmxvYWQgMApjb25jYXQKbG9nCmludGNfMSAvLyAxCnJldHVybgptYWluX2wyMjoKdHhuIE9uQ29tcGxldGlvbgppbnRjXzAgLy8gTm9PcAo9PQpibnogbWFpbl9sMzAKdHhuIE9uQ29tcGxldGlvbgppbnRjXzEgLy8gT3B0SW4KPT0KYm56IG1haW5fbDI5CnR4biBPbkNvbXBsZXRpb24KcHVzaGludCA0IC8vIFVwZGF0ZUFwcGxpY2F0aW9uCj09CmJueiBtYWluX2wyOAp0eG4gT25Db21wbGV0aW9uCmludGNfMyAvLyBEZWxldGVBcHBsaWNhdGlvbgo9PQpibnogbWFpbl9sMjcKZXJyCm1haW5fbDI3Ogp0eG4gQXBwbGljYXRpb25JRAppbnRjXzAgLy8gMAohPQphc3NlcnQKY2FsbHN1YiBkZWxldGVfMTEKaW50Y18xIC8vIDEKcmV0dXJuCm1haW5fbDI4Ogp0eG4gQXBwbGljYXRpb25JRAppbnRjXzAgLy8gMAohPQphc3NlcnQKY2FsbHN1YiB1cGRhdGVfOQppbnRjXzEgLy8gMQpyZXR1cm4KbWFpbl9sMjk6CnR4biBBcHBsaWNhdGlvbklECmludGNfMCAvLyAwCj09CmFzc2VydApjYWxsc3ViIGNyZWF0ZV83CmludGNfMSAvLyAxCnJldHVybgptYWluX2wzMDoKdHhuIEFwcGxpY2F0aW9uSUQKaW50Y18wIC8vIDAKPT0KYXNzZXJ0CmNhbGxzdWIgY3JlYXRlXzcKaW50Y18xIC8vIDEKcmV0dXJuCgovLyBjYWxsX2FiaQpjYWxsYWJpXzA6CnByb3RvIDEgMQpieXRlY18wIC8vICIiCnB1c2hieXRlcyAweDQ4NjU2YzZjNmYyYzIwIC8vICJIZWxsbywgIgpmcmFtZV9kaWcgLTEKZXh0cmFjdCAyIDAKY29uY2F0CmZyYW1lX2J1cnkgMApmcmFtZV9kaWcgMApsZW4KaXRvYgpleHRyYWN0IDYgMApmcmFtZV9kaWcgMApjb25jYXQKZnJhbWVfYnVyeSAwCnJldHN1YgoKLy8gaXRvYQppdG9hXzE6CnByb3RvIDEgMQpmcmFtZV9kaWcgLTEKaW50Y18wIC8vIDAKPT0KYm56IGl0b2FfMV9sNQpmcmFtZV9kaWcgLTEKaW50Y18yIC8vIDEwCi8KaW50Y18wIC8vIDAKPgpibnogaXRvYV8xX2w0CmJ5dGVjXzAgLy8gIiIKaXRvYV8xX2wzOgpwdXNoYnl0ZXMgMHgzMDMxMzIzMzM0MzUzNjM3MzgzOSAvLyAiMDEyMzQ1Njc4OSIKZnJhbWVfZGlnIC0xCmludGNfMiAvLyAxMAolCmludGNfMSAvLyAxCmV4dHJhY3QzCmNvbmNhdApiIGl0b2FfMV9sNgppdG9hXzFfbDQ6CmZyYW1lX2RpZyAtMQppbnRjXzIgLy8gMTAKLwpjYWxsc3ViIGl0b2FfMQpiIGl0b2FfMV9sMwppdG9hXzFfbDU6CnB1c2hieXRlcyAweDMwIC8vICIwIgppdG9hXzFfbDY6CnJldHN1YgoKLy8gY2FsbF9hYmlfdHhuCmNhbGxhYml0eG5fMjoKcHJvdG8gMiAxCmJ5dGVjXzAgLy8gIiIKcHVzaGJ5dGVzIDB4NTM2NTZlNzQyMCAvLyAiU2VudCAiCmZyYW1lX2RpZyAtMgpndHhucyBBbW91bnQKY2FsbHN1YiBpdG9hXzEKY29uY2F0CnB1c2hieXRlcyAweDJlMjAgLy8gIi4gIgpjb25jYXQKZnJhbWVfZGlnIC0xCmV4dHJhY3QgMiAwCmNvbmNhdApmcmFtZV9idXJ5IDAKZnJhbWVfZGlnIDAKbGVuCml0b2IKZXh0cmFjdCA2IDAKZnJhbWVfZGlnIDAKY29uY2F0CmZyYW1lX2J1cnkgMApyZXRzdWIKCi8vIHNldF9nbG9iYWwKc2V0Z2xvYmFsXzM6CnByb3RvIDQgMApwdXNoYnl0ZXMgMHg2OTZlNzQzMSAvLyAiaW50MSIKZnJhbWVfZGlnIC00CmFwcF9nbG9iYWxfcHV0CnB1c2hieXRlcyAweDY5NmU3NDMyIC8vICJpbnQyIgpmcmFtZV9kaWcgLTMKYXBwX2dsb2JhbF9wdXQKcHVzaGJ5dGVzIDB4NjI3OTc0NjU3MzMxIC8vICJieXRlczEiCmZyYW1lX2RpZyAtMgpleHRyYWN0IDIgMAphcHBfZ2xvYmFsX3B1dApwdXNoYnl0ZXMgMHg2Mjc5NzQ2NTczMzIgLy8gImJ5dGVzMiIKZnJhbWVfZGlnIC0xCmFwcF9nbG9iYWxfcHV0CnJldHN1YgoKLy8gc2V0X2xvY2FsCnNldGxvY2FsXzQ6CnByb3RvIDQgMAp0eG4gU2VuZGVyCnB1c2hieXRlcyAweDZjNmY2MzYxNmM1ZjY5NmU3NDMxIC8vICJsb2NhbF9pbnQxIgpmcmFtZV9kaWcgLTQKYXBwX2xvY2FsX3B1dAp0eG4gU2VuZGVyCnB1c2hieXRlcyAweDZjNmY2MzYxNmM1ZjY5NmU3NDMyIC8vICJsb2NhbF9pbnQyIgpmcmFtZV9kaWcgLTMKYXBwX2xvY2FsX3B1dAp0eG4gU2VuZGVyCnB1c2hieXRlcyAweDZjNmY2MzYxNmM1ZjYyNzk3NDY1NzMzMSAvLyAibG9jYWxfYnl0ZXMxIgpmcmFtZV9kaWcgLTIKZXh0cmFjdCAyIDAKYXBwX2xvY2FsX3B1dAp0eG4gU2VuZGVyCnB1c2hieXRlcyAweDZjNmY2MzYxNmM1ZjYyNzk3NDY1NzMzMiAvLyAibG9jYWxfYnl0ZXMyIgpmcmFtZV9kaWcgLTEKYXBwX2xvY2FsX3B1dApyZXRzdWIKCi8vIHNldF9ib3gKc2V0Ym94XzU6CnByb3RvIDIgMApmcmFtZV9kaWcgLTIKYm94X2RlbApwb3AKZnJhbWVfZGlnIC0yCmZyYW1lX2RpZyAtMQpleHRyYWN0IDIgMApib3hfcHV0CnJldHN1YgoKLy8gZXJyb3IKZXJyb3JfNjoKcHJvdG8gMCAwCmludGNfMCAvLyAwCi8vIERlbGliZXJhdGUgZXJyb3IKYXNzZXJ0CnJldHN1YgoKLy8gY3JlYXRlCmNyZWF0ZV83Ogpwcm90byAwIDAKdHhuIFNlbmRlcgpnbG9iYWwgQ3JlYXRvckFkZHJlc3MKPT0KLy8gdW5hdXRob3JpemVkCmFzc2VydApwdXNoYnl0ZXMgMHg3NjYxNmM3NTY1IC8vICJ2YWx1ZSIKcHVzaGludCBUTVBMX1ZBTFVFIC8vIFRNUExfVkFMVUUKYXBwX2dsb2JhbF9wdXQKcmV0c3ViCgovLyBjcmVhdGVfYWJpCmNyZWF0ZWFiaV84Ogpwcm90byAxIDEKYnl0ZWNfMCAvLyAiIgp0eG4gU2VuZGVyCmdsb2JhbCBDcmVhdG9yQWRkcmVzcwo9PQovLyB1bmF1dGhvcml6ZWQKYXNzZXJ0CmZyYW1lX2RpZyAtMQpleHRyYWN0IDIgMApmcmFtZV9idXJ5IDAKZnJhbWVfZGlnIDAKbGVuCml0b2IKZXh0cmFjdCA2IDAKZnJhbWVfZGlnIDAKY29uY2F0CmZyYW1lX2J1cnkgMApyZXRzdWIKCi8vIHVwZGF0ZQp1cGRhdGVfOToKcHJvdG8gMCAwCnR4biBTZW5kZXIKZ2xvYmFsIENyZWF0b3JBZGRyZXNzCj09Ci8vIHVuYXV0aG9yaXplZAphc3NlcnQKaW50YyA0IC8vIFRNUExfVVBEQVRBQkxFCi8vIENoZWNrIGFwcCBpcyB1cGRhdGFibGUKYXNzZXJ0CnJldHN1YgoKLy8gdXBkYXRlX2FiaQp1cGRhdGVhYmlfMTA6CnByb3RvIDEgMQpieXRlY18wIC8vICIiCnR4biBTZW5kZXIKZ2xvYmFsIENyZWF0b3JBZGRyZXNzCj09Ci8vIHVuYXV0aG9yaXplZAphc3NlcnQKaW50YyA0IC8vIFRNUExfVVBEQVRBQkxFCi8vIENoZWNrIGFwcCBpcyB1cGRhdGFibGUKYXNzZXJ0CmZyYW1lX2RpZyAtMQpleHRyYWN0IDIgMApmcmFtZV9idXJ5IDAKZnJhbWVfZGlnIDAKbGVuCml0b2IKZXh0cmFjdCA2IDAKZnJhbWVfZGlnIDAKY29uY2F0CmZyYW1lX2J1cnkgMApyZXRzdWIKCi8vIGRlbGV0ZQpkZWxldGVfMTE6CnByb3RvIDAgMAp0eG4gU2VuZGVyCmdsb2JhbCBDcmVhdG9yQWRkcmVzcwo9PQovLyB1bmF1dGhvcml6ZWQKYXNzZXJ0CmludGMgNSAvLyBUTVBMX0RFTEVUQUJMRQovLyBDaGVjayBhcHAgaXMgZGVsZXRhYmxlCmFzc2VydApyZXRzdWIKCi8vIGRlbGV0ZV9hYmkKZGVsZXRlYWJpXzEyOgpwcm90byAxIDEKYnl0ZWNfMCAvLyAiIgp0eG4gU2VuZGVyCmdsb2JhbCBDcmVhdG9yQWRkcmVzcwo9PQovLyB1bmF1dGhvcml6ZWQKYXNzZXJ0CmludGMgNSAvLyBUTVBMX0RFTEVUQUJMRQovLyBDaGVjayBhcHAgaXMgZGVsZXRhYmxlCmFzc2VydApmcmFtZV9kaWcgLTEKZXh0cmFjdCAyIDAKZnJhbWVfYnVyeSAwCmZyYW1lX2RpZyAwCmxlbgppdG9iCmV4dHJhY3QgNiAwCmZyYW1lX2RpZyAwCmNvbmNhdApmcmFtZV9idXJ5IDAKcmV0c3ViCgovLyBvcHRfaW4Kb3B0aW5fMTM6CnByb3RvIDAgMAppbnRjXzEgLy8gMQpyZXR1cm4=",
    "clear": "I3ByYWdtYSB2ZXJzaW9uIDgKcHVzaGludCAwIC8vIDAKcmV0dXJu"
  },
  "state": {
    "global": {
      "num_byte_slices": 2,
      "num_uints": 3
    },
    "local": {
      "num_byte_slices": 2,
      "num_uints": 2
    }
  },
  "schema": {
    "global": {
      "declared": {
        "bytes1": {
          "type": "bytes",
          "key": "bytes1",
          "descr": ""
        },
        "bytes2": {
          "type": "bytes",
          "key": "bytes2",
          "descr": ""
        },
        "int1": {
          "type": "uint64",
          "key": "int1",
          "descr": ""
        },
        "int2": {
          "type": "uint64",
          "key": "int2",
          "descr": ""
        },
        "value": {
          "type": "uint64",
          "key": "value",
          "descr": ""
        }
      },
      "reserved": {}
    },
    "local": {
      "declared": {
        "local_bytes1": {
          "type": "bytes",
          "key": "local_bytes1",
          "descr": ""
        },
        "local_bytes2": {
          "type": "bytes",
          "key": "local_bytes2",
          "descr": ""
        },
        "local_int1": {
          "type": "uint64",
          "key": "local_int1",
          "descr": ""
        },
        "local_int2": {
          "type": "uint64",
          "key": "local_int2",
          "descr": ""
        }
      },
      "reserved": {}
    }
  },
  "contract": {
    "name": "TestingApp",
    "methods": [
      {
        "name": "call_abi",
        "args": [
          {
            "type": "string",
            "name": "value"
          }
        ],
        "returns": {
          "type": "string"
        }
      },
      {
        "name": "call_abi_txn",
        "args": [
          {
            "type": "pay",
            "name": "txn"
          },
          {
            "type": "string",
            "name": "value"
          }
        ],
        "returns": {
          "type": "string"
        }
      },
      {
        "name": "set_global",
        "args": [
          {
            "type": "uint64",
            "name": "int1"
          },
          {
            "type": "uint64",
            "name": "int2"
          },
          {
            "type": "string",
            "name": "bytes1"
          },
          {
            "type": "byte[4]",
            "name": "bytes2"
          }
        ],
        "returns": {
          "type": "void"
        }
      },
      {
        "name": "set_local",
        "args": [
          {
            "type": "uint64",
            "name": "int1"
          },
          {
            "type": "uint64",
            "name": "int2"
          },
          {
            "type": "string",
            "name": "bytes1"
          },
          {
            "type": "byte[4]",
            "name": "bytes2"
          }
        ],
        "returns": {
          "type": "void"
        }
      },
      {
        "name": "set_box",
        "args": [
          {
            "type": "byte[4]",
            "name": "name"
          },
          {
            "type": "string",
            "name": "value"
          }
        ],
        "returns": {
          "type": "void"
        }
      },
      {
        "name": "error",
        "args": [],
        "returns": {
          "type": "void"
        }
      },
      {
        "name": "create_abi",
        "args": [
          {
            "type": "string",
            "name": "input"
          }
        ],
        "returns": {
          "type": "string"
        }
      },
      {
        "name": "update_abi",
        "args": [
          {
            "type": "string",
            "name": "input"
          }
        ],
        "returns": {
          "type": "string"
        }
      },
      {
        "name": "delete_abi",
        "args": [
          {
            "type": "string",
            "name": "input"
          }
        ],
        "returns": {
          "type": "string"
        }
      },
      {
        "name": "opt_in",
        "args": [],
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
    "opt_in": "CREATE",
    "update_application": "CALL"
  }
}

export type CallRequest<TSignature extends string, TArgs = undefined> = {
  method: TSignature
  methodArgs: TArgs
} & AppClientCallCoreParams & CoreAppCallArgs
export type BareCallArgs = Omit<RawAppCallArgs, keyof CoreAppCallArgs>

export type TestingAppReturnTypes = {
  'call_abi(string)string': string
  'call_abi': string
  'call_abi_txn(pay,string)string': string
  'call_abi_txn': string
  'set_global(uint64,uint64,string,byte[4])void': void
  'set_global': void
  'set_local(uint64,uint64,string,byte[4])void': void
  'set_local': void
  'set_box(byte[4],string)void': void
  'set_box': void
  'error()void': void
  'error': void
  'create_abi(string)string': string
  'create_abi': string
  'update_abi(string)string': string
  'update_abi': string
  'delete_abi(string)string': string
  'delete_abi': string
  'opt_in()void': void
  'opt_in': void
}
export type TestingAppReturnTypeFor<TSignatureOrMethod> = TSignatureOrMethod extends keyof TestingAppReturnTypes
  ? TestingAppReturnTypes[TSignatureOrMethod]
  : undefined
export type CallAbiArgsObj = {
  value: string
}
export type CallAbiArgsTuple = [value: string]
export type CallAbiArgs = CallAbiArgsObj | CallAbiArgsTuple
export type CallAbiTxnArgsObj = {
  txn: TransactionToSign | Transaction | Promise<SendTransactionResult>
  value: string
}
export type CallAbiTxnArgsTuple = [txn: TransactionToSign | Transaction | Promise<SendTransactionResult>, value: string]
export type CallAbiTxnArgs = CallAbiTxnArgsObj | CallAbiTxnArgsTuple
export type SetGlobalArgsObj = {
  int1: bigint
  int2: bigint
  bytes1: string
  bytes2: Uint8Array
}
export type SetGlobalArgsTuple = [int1: bigint, int2: bigint, bytes1: string, bytes2: Uint8Array]
export type SetGlobalArgs = SetGlobalArgsObj | SetGlobalArgsTuple
export type SetLocalArgsObj = {
  int1: bigint
  int2: bigint
  bytes1: string
  bytes2: Uint8Array
}
export type SetLocalArgsTuple = [int1: bigint, int2: bigint, bytes1: string, bytes2: Uint8Array]
export type SetLocalArgs = SetLocalArgsObj | SetLocalArgsTuple
export type SetBoxArgsObj = {
  name: Uint8Array
  value: string
}
export type SetBoxArgsTuple = [name: Uint8Array, value: string]
export type SetBoxArgs = SetBoxArgsObj | SetBoxArgsTuple
export type ErrorArgsObj = {
}
export type ErrorArgsTuple = []
export type ErrorArgs = ErrorArgsObj | ErrorArgsTuple
export type CreateAbiArgsObj = {
  input: string
}
export type CreateAbiArgsTuple = [input: string]
export type CreateAbiArgs = CreateAbiArgsObj | CreateAbiArgsTuple
export type UpdateAbiArgsObj = {
  input: string
}
export type UpdateAbiArgsTuple = [input: string]
export type UpdateAbiArgs = UpdateAbiArgsObj | UpdateAbiArgsTuple
export type DeleteAbiArgsObj = {
  input: string
}
export type DeleteAbiArgsTuple = [input: string]
export type DeleteAbiArgs = DeleteAbiArgsObj | DeleteAbiArgsTuple
export type OptInArgsObj = {
}
export type OptInArgsTuple = []
export type OptInArgs = OptInArgsObj | OptInArgsTuple

export type TestingAppCreateArgs =
  | BareCallArgs  & { onCompleteAction?: 'no_op' | OnApplicationComplete.NoOpOC | 'opt_in' | OnApplicationComplete.OptInOC }
  | ({ method: 'create_abi' } & CreateAbiArgsObj)  & { onCompleteAction?: 'no_op' | OnApplicationComplete.NoOpOC }
export type TestingAppUpdateArgs =
  | BareCallArgs
  | ({ method: 'update_abi' } & UpdateAbiArgsObj)
export type TestingAppDeleteArgs =
  | BareCallArgs
  | ({ method: 'delete_abi' } & DeleteAbiArgsObj)
export type TestingAppOptInArgs =
  | ({ method: 'opt_in' } & OptInArgsObj)
export type TestingAppDeployArgs = {
  deployTimeParams?: TealTemplateParams
  createArgs?: TestingAppCreateArgs & CoreAppCallArgs
  updateArgs?: TestingAppUpdateArgs & CoreAppCallArgs
  deleteArgs?: TestingAppDeleteArgs & CoreAppCallArgs
}

export abstract class TestingAppCallFactory {
  static callAbi(args: CallAbiArgs, params: AppClientCallCoreParams & CoreAppCallArgs = {}) {
    return {
      method: 'call_abi(string)string' as const,
      methodArgs: Array.isArray(args) ? args : [args.value],
      ...params,
    }
  }
  static callAbiTxn(args: CallAbiTxnArgs, params: AppClientCallCoreParams & CoreAppCallArgs = {}) {
    return {
      method: 'call_abi_txn(pay,string)string' as const,
      methodArgs: Array.isArray(args) ? args : [args.txn, args.value],
      ...params,
    }
  }
  static setGlobal(args: SetGlobalArgs, params: AppClientCallCoreParams & CoreAppCallArgs = {}) {
    return {
      method: 'set_global(uint64,uint64,string,byte[4])void' as const,
      methodArgs: Array.isArray(args) ? args : [args.int1, args.int2, args.bytes1, args.bytes2],
      ...params,
    }
  }
  static setLocal(args: SetLocalArgs, params: AppClientCallCoreParams & CoreAppCallArgs = {}) {
    return {
      method: 'set_local(uint64,uint64,string,byte[4])void' as const,
      methodArgs: Array.isArray(args) ? args : [args.int1, args.int2, args.bytes1, args.bytes2],
      ...params,
    }
  }
  static setBox(args: SetBoxArgs, params: AppClientCallCoreParams & CoreAppCallArgs = {}) {
    return {
      method: 'set_box(byte[4],string)void' as const,
      methodArgs: Array.isArray(args) ? args : [args.name, args.value],
      ...params,
    }
  }
  static error(args: ErrorArgs, params: AppClientCallCoreParams & CoreAppCallArgs = {}) {
    return {
      method: 'error()void' as const,
      methodArgs: Array.isArray(args) ? args : [],
      ...params,
    }
  }
  static createAbi(args: CreateAbiArgs, params: AppClientCallCoreParams & CoreAppCallArgs = {}) {
    return {
      method: 'create_abi(string)string' as const,
      methodArgs: Array.isArray(args) ? args : [args.input],
      ...params,
    }
  }
  static updateAbi(args: UpdateAbiArgs, params: AppClientCallCoreParams & CoreAppCallArgs = {}) {
    return {
      method: 'update_abi(string)string' as const,
      methodArgs: Array.isArray(args) ? args : [args.input],
      ...params,
    }
  }
  static deleteAbi(args: DeleteAbiArgs, params: AppClientCallCoreParams & CoreAppCallArgs = {}) {
    return {
      method: 'delete_abi(string)string' as const,
      methodArgs: Array.isArray(args) ? args : [args.input],
      ...params,
    }
  }
  static optIn(args: OptInArgs, params: AppClientCallCoreParams & CoreAppCallArgs = {}) {
    return {
      method: 'opt_in()void' as const,
      methodArgs: Array.isArray(args) ? args : [],
      ...params,
    }
  }
}

/** A client to make calls to the TestingApp smart contract */
export class TestingAppClient {
  /** The underlying `ApplicationClient` for when you want to have more flexibility */
  public readonly appClient: ApplicationClient

  /**
   * Creates a new instance of `TestingAppClient`
   * @param appDetails The details to identify the app to deploy
   * @param algod An algod client instance
   */
  constructor(appDetails: AppDetails, algod: Algodv2) {
    this.appClient = algokit.getAppClient({
      ...appDetails,
      app: APP_SPEC
    }, algod)
  }

  public async mapReturnValue<TSignatureOrMethod extends string>(resultPromise: Promise<AppCallTransactionResult> | AppCallTransactionResult): Promise<AppCallTransactionResultOfType<TestingAppReturnTypeFor<TSignatureOrMethod>>> {
    const result = await resultPromise
    if(result.return?.decodeError) {
      throw result.return.decodeError
    }
    const returnValue = result.return?.returnValue as TestingAppReturnTypeFor<TSignatureOrMethod>
    return { ...result, return: returnValue }
  }

  public call<TSignature extends string>(params: CallRequest<TSignature, any>) {
    return this.mapReturnValue<TSignature>(this.appClient.call(params))
  }

  private mapMethodArgs(args: TestingAppCreateArgs | TestingAppUpdateArgs | TestingAppDeleteArgs | TestingAppOptInArgs, params?: CoreAppCallArgs): AppClientCallArgs {
    switch (args.method) {
      case 'create_abi':
        return TestingAppCallFactory.createAbi(args, params)
      case 'update_abi':
        return TestingAppCallFactory.updateAbi(args, params)
      case 'delete_abi':
        return TestingAppCallFactory.deleteAbi(args, params)
      case 'opt_in':
        return TestingAppCallFactory.optIn(args, params)
      default:
        return args
    }
  }

  /**
   * Idempotently deploys the TestingApp smart contract.
   * @param params The arguments for the contract calls and any additional parameters for the call
   * @returns The deployment result
   */
  public deploy(params: TestingAppDeployArgs & AppClientDeployCoreParams = {}) {
    const { boxes: create_boxes, lease: create_lease, onCompleteAction: createOnCompleteAction, ...createArgs } = params.createArgs ?? {}
    const { boxes: update_boxes, lease: update_lease, ...updateArgs } = params.updateArgs ?? {}
    const { boxes: delete_boxes, lease: delete_lease, ...deleteArgs } = params.deleteArgs ?? {}
    return this.appClient.deploy({ 
      ...params,
      createArgs: params.createArgs ? this.mapMethodArgs(createArgs, { boxes: create_boxes, lease: create_lease }) : undefined,
      createOnCompleteAction,
      updateArgs: params.updateArgs ? this.mapMethodArgs(updateArgs, { boxes: update_boxes, lease: update_lease }) : undefined,
      deleteArgs: params.deleteArgs ? this.mapMethodArgs(deleteArgs, { boxes: delete_boxes, lease: delete_lease }) : undefined,
    })
  }

  /**
   * Creates a new instance of the TestingApp smart contract.
   * @param args The arguments for the contract call
   * @param params Any additional parameters for the call
   * @returns The creation result
   */
  public create<TMethod extends string>(args: { method?: TMethod } & TestingAppCreateArgs = {}, params?: AppClientCallCoreParams & AppClientCompilationParams & CoreAppCallArgs) {
    const onCompleteAction = args.onCompleteAction
    return this.mapReturnValue<TMethod>(this.appClient.create({ ...this.mapMethodArgs(args), ...params, ...{ onCompleteAction } }))
  }

  /**
   * Updates an existing instance of the TestingApp smart contract.
   * @param args The arguments for the contract call
   * @param params Any additional parameters for the call
   * @returns The update result
   */
  public update<TMethod extends string>(args: { method?: TMethod } & TestingAppUpdateArgs = {}, params?: AppClientCallCoreParams & AppClientCompilationParams & CoreAppCallArgs) {
    return this.mapReturnValue<TMethod>(this.appClient.update({ ...this.mapMethodArgs(args), ...params, }))
  }

  /**
   * Deletes an existing instance of the TestingApp smart contract.
   * @param args The arguments for the contract call
   * @param params Any additional parameters for the call
   * @returns The deletion result
   */
  public delete<TMethod extends string>(args: { method?: TMethod } & TestingAppDeleteArgs = {}, params?: AppClientCallCoreParams & CoreAppCallArgs) {
    return this.mapReturnValue<TMethod>(this.appClient.delete({ ...this.mapMethodArgs(args), ...params, }))
  }

  /**
   * Opts the user into an existing instance of the TestingApp smart contract.
   * @param args The arguments for the contract call
   * @param params Any additional parameters for the call
   * @returns The opt in result
   */
  public optIn<TMethod extends string>(args: { method?: TMethod } & TestingAppOptInArgs, params?: AppClientCallCoreParams & AppClientCompilationParams & CoreAppCallArgs) {
    return this.mapReturnValue<TMethod>(this.appClient.create({ ...this.mapMethodArgs(args), ...params, }))
  }

  /**
   * Makes a clear_state call to an existing instance of the TestingApp smart contract.
   * @param args The arguments for the contract call
   * @param params Any additional parameters for the call
   * @returns The clear_state result
   */
  public clearState(args: BareCallArgs, params?: AppClientCallCoreParams & CoreAppCallArgs) {
    return this.appClient.clearState({ ...args, ...params, })
  }

  /**
   * Calls the call_abi(string)string ABI method.
   *
   * @param args The arguments for the ABI method
   * @param params Any additional parameters for the call
   * @returns The result of the call
   */
  public callAbi(args: CallAbiArgs, params?: AppClientCallCoreParams & CoreAppCallArgs) {
    return this.call(TestingAppCallFactory.callAbi(args, params))
  }

  /**
   * Calls the call_abi_txn(pay,string)string ABI method.
   *
   * @param args The arguments for the ABI method
   * @param params Any additional parameters for the call
   * @returns The result of the call
   */
  public callAbiTxn(args: CallAbiTxnArgs, params?: AppClientCallCoreParams & CoreAppCallArgs) {
    return this.call(TestingAppCallFactory.callAbiTxn(args, params))
  }

  /**
   * Calls the set_global(uint64,uint64,string,byte[4])void ABI method.
   *
   * @param args The arguments for the ABI method
   * @param params Any additional parameters for the call
   * @returns The result of the call
   */
  public setGlobal(args: SetGlobalArgs, params?: AppClientCallCoreParams & CoreAppCallArgs) {
    return this.call(TestingAppCallFactory.setGlobal(args, params))
  }

  /**
   * Calls the set_local(uint64,uint64,string,byte[4])void ABI method.
   *
   * @param args The arguments for the ABI method
   * @param params Any additional parameters for the call
   * @returns The result of the call
   */
  public setLocal(args: SetLocalArgs, params?: AppClientCallCoreParams & CoreAppCallArgs) {
    return this.call(TestingAppCallFactory.setLocal(args, params))
  }

  /**
   * Calls the set_box(byte[4],string)void ABI method.
   *
   * @param args The arguments for the ABI method
   * @param params Any additional parameters for the call
   * @returns The result of the call
   */
  public setBox(args: SetBoxArgs, params?: AppClientCallCoreParams & CoreAppCallArgs) {
    return this.call(TestingAppCallFactory.setBox(args, params))
  }

  /**
   * Calls the error()void ABI method.
   *
   * @param args The arguments for the ABI method
   * @param params Any additional parameters for the call
   * @returns The result of the call
   */
  public error(args: ErrorArgs, params?: AppClientCallCoreParams & CoreAppCallArgs) {
    return this.call(TestingAppCallFactory.error(args, params))
  }

}
