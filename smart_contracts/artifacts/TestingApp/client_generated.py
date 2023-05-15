# flake8: noqa
import dataclasses
import typing
from abc import ABC, abstractmethod

import algokit_utils
import algosdk
from algosdk.atomic_transaction_composer import TransactionSigner, TransactionWithSigner

APP_SPEC = """{
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
}"""
_T = typing.TypeVar("_T")
_TReturn = typing.TypeVar("_TReturn")


class _ArgsBase(ABC, typing.Generic[_TReturn]):
    @staticmethod
    @abstractmethod
    def method() -> str:
        ...


def _as_dict(data: _T | None) -> dict[str, typing.Any]:
    if data is None:
        return {}
    if not dataclasses.is_dataclass(data):
        raise TypeError(f"{data} must be a dataclass")
    return {f.name: getattr(data, f.name) for f in dataclasses.fields(data)}


def _convert_on_complete(on_complete: algokit_utils.OnCompleteActionName) -> algosdk.transaction.OnComplete:
    on_complete_enum = on_complete.replace("_", " ").title().replace(" ", "") + "OC"
    return getattr(algosdk.transaction.OnComplete, on_complete_enum)


@dataclasses.dataclass(kw_only=True)
class CallAbiArgs(_ArgsBase[str]):
    value: str

    @staticmethod
    def method() -> str:
        return "call_abi(string)string"


@dataclasses.dataclass(kw_only=True)
class CallAbiTxnArgs(_ArgsBase[str]):
    txn: TransactionWithSigner
    value: str

    @staticmethod
    def method() -> str:
        return "call_abi_txn(pay,string)string"


@dataclasses.dataclass(kw_only=True)
class SetGlobalArgs(_ArgsBase[None]):
    int1: int
    int2: int
    bytes1: str
    bytes2: tuple[bytes, bytes, bytes, bytes]

    @staticmethod
    def method() -> str:
        return "set_global(uint64,uint64,string,byte[4])void"


@dataclasses.dataclass(kw_only=True)
class SetLocalArgs(_ArgsBase[None]):
    int1: int
    int2: int
    bytes1: str
    bytes2: tuple[bytes, bytes, bytes, bytes]

    @staticmethod
    def method() -> str:
        return "set_local(uint64,uint64,string,byte[4])void"


@dataclasses.dataclass(kw_only=True)
class SetBoxArgs(_ArgsBase[None]):
    name: tuple[bytes, bytes, bytes, bytes]
    value: str

    @staticmethod
    def method() -> str:
        return "set_box(byte[4],string)void"


@dataclasses.dataclass(kw_only=True)
class ErrorArgs(_ArgsBase[None]):
    @staticmethod
    def method() -> str:
        return "error()void"


@dataclasses.dataclass(kw_only=True)
class CreateAbiArgs(_ArgsBase[str]):
    input: str

    @staticmethod
    def method() -> str:
        return "create_abi(string)string"


@dataclasses.dataclass(kw_only=True)
class UpdateAbiArgs(_ArgsBase[str]):
    input: str

    @staticmethod
    def method() -> str:
        return "update_abi(string)string"


@dataclasses.dataclass(kw_only=True)
class DeleteAbiArgs(_ArgsBase[str]):
    input: str

    @staticmethod
    def method() -> str:
        return "delete_abi(string)string"


@dataclasses.dataclass(kw_only=True)
class OptInArgs(_ArgsBase[None]):
    @staticmethod
    def method() -> str:
        return "opt_in()void"


class TestingAppClient:
    @typing.overload
    def __init__(
        self,
        algod_client: algosdk.v2client.algod.AlgodClient,
        *,
        app_id: int = 0,
        signer: TransactionSigner | algokit_utils.Account | None = None,
        sender: str | None = None,
        suggested_params: algosdk.transaction.SuggestedParams | None = None,
        template_values: algokit_utils.TemplateValueMapping | None = None,
    ):
        ...

    @typing.overload
    def __init__(
        self,
        algod_client: algosdk.v2client.algod.AlgodClient,
        *,
        creator: str | algokit_utils.Account,
        indexer_client: algosdk.v2client.indexer.IndexerClient | None = None,
        existing_deployments: algokit_utils.AppLookup | None = None,
        signer: TransactionSigner | algokit_utils.Account | None = None,
        sender: str | None = None,
        suggested_params: algosdk.transaction.SuggestedParams | None = None,
        template_values: algokit_utils.TemplateValueMapping | None = None,
    ):
        ...

    def __init__(
        self,
        algod_client: algosdk.v2client.algod.AlgodClient,
        *,
        creator: str | algokit_utils.Account | None = None,
        indexer_client: algosdk.v2client.indexer.IndexerClient | None = None,
        existing_deployments: algokit_utils.AppLookup | None = None,
        app_id: int = 0,
        signer: TransactionSigner | algokit_utils.Account | None = None,
        sender: str | None = None,
        suggested_params: algosdk.transaction.SuggestedParams | None = None,
        template_values: algokit_utils.TemplateValueMapping | None = None,
    ):
        self.app_spec = APP_SPEC

        # calling full __init__ signature, so ignoring mypy warning about overloads
        self.app_client = algokit_utils.ApplicationClient(  # type: ignore[call-overload, misc]
            algod_client=algod_client,
            app_spec=self.app_spec,
            app_id=app_id,
            creator=creator,
            indexer_client=indexer_client,
            existing_deployments=existing_deployments,
            signer=signer,
            sender=sender,
            suggested_params=suggested_params,
            template_values=template_values,
        )

    def call_abi(
        self,
        *,
        value: str,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
    ) -> algokit_utils.ABITransactionResponse[str]:
        args = CallAbiArgs(
            value=value,
        )
        return self.app_client.call(
            call_abi_method=args.method(),
            transaction_parameters=_as_dict(transaction_parameters),
            **_as_dict(args),
        )

    def call_abi_txn(
        self,
        *,
        txn: TransactionWithSigner,
        value: str,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
    ) -> algokit_utils.ABITransactionResponse[str]:
        args = CallAbiTxnArgs(
            txn=txn,
            value=value,
        )
        return self.app_client.call(
            call_abi_method=args.method(),
            transaction_parameters=_as_dict(transaction_parameters),
            **_as_dict(args),
        )

    def set_global(
        self,
        *,
        int1: int,
        int2: int,
        bytes1: str,
        bytes2: tuple[bytes, bytes, bytes, bytes],
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
    ) -> algokit_utils.ABITransactionResponse[None]:
        args = SetGlobalArgs(
            int1=int1,
            int2=int2,
            bytes1=bytes1,
            bytes2=bytes2,
        )
        return self.app_client.call(
            call_abi_method=args.method(),
            transaction_parameters=_as_dict(transaction_parameters),
            **_as_dict(args),
        )

    def set_local(
        self,
        *,
        int1: int,
        int2: int,
        bytes1: str,
        bytes2: tuple[bytes, bytes, bytes, bytes],
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
    ) -> algokit_utils.ABITransactionResponse[None]:
        args = SetLocalArgs(
            int1=int1,
            int2=int2,
            bytes1=bytes1,
            bytes2=bytes2,
        )
        return self.app_client.call(
            call_abi_method=args.method(),
            transaction_parameters=_as_dict(transaction_parameters),
            **_as_dict(args),
        )

    def set_box(
        self,
        *,
        name: tuple[bytes, bytes, bytes, bytes],
        value: str,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
    ) -> algokit_utils.ABITransactionResponse[None]:
        args = SetBoxArgs(
            name=name,
            value=value,
        )
        return self.app_client.call(
            call_abi_method=args.method(),
            transaction_parameters=_as_dict(transaction_parameters),
            **_as_dict(args),
        )

    def error(
        self,
        *,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
    ) -> algokit_utils.ABITransactionResponse[None]:
        args = ErrorArgs()
        return self.app_client.call(
            call_abi_method=args.method(),
            transaction_parameters=_as_dict(transaction_parameters),
            **_as_dict(args),
        )

    @typing.overload
    def create(
        self,
        *,
        args: typing.Literal[None] = None,
        on_complete: typing.Literal["no_op", "opt_in"] = "no_op",
        transaction_parameters: algokit_utils.CreateTransactionParameters | None = None,
    ) -> algokit_utils.TransactionResponse:
        ...

    @typing.overload
    def create(
        self,
        *,
        args: CreateAbiArgs,
        on_complete: typing.Literal["no_op"] = "no_op",
        transaction_parameters: algokit_utils.CreateTransactionParameters | None = None,
    ) -> algokit_utils.ABITransactionResponse[str]:
        ...

    def create(
        self,
        *,
        args: CreateAbiArgs | None = None,
        on_complete: typing.Literal["no_op", "opt_in"] = "no_op",
        transaction_parameters: algokit_utils.CreateTransactionParameters | None = None,
    ) -> algokit_utils.TransactionResponse | algokit_utils.ABITransactionResponse[str]:
        transaction_parameters_dict = _as_dict(transaction_parameters)
        transaction_parameters_dict["on_complete"] = _convert_on_complete(on_complete)
        return self.app_client.create(
            call_abi_method=args.method() if args else False,
            transaction_parameters=transaction_parameters_dict,
            **_as_dict(args),
        )

    @typing.overload
    def update(
        self,
        *,
        args: typing.Literal[None] = None,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
    ) -> algokit_utils.TransactionResponse:
        ...

    @typing.overload
    def update(
        self,
        *,
        args: UpdateAbiArgs,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
    ) -> algokit_utils.ABITransactionResponse[str]:
        ...

    def update(
        self,
        *,
        args: UpdateAbiArgs | None = None,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
    ) -> algokit_utils.TransactionResponse | algokit_utils.ABITransactionResponse[str]:
        return self.app_client.update(
            call_abi_method=args.method() if args else False,
            transaction_parameters=_as_dict(transaction_parameters),
            **_as_dict(args),
        )

    @typing.overload
    def delete(
        self,
        *,
        args: typing.Literal[None] = None,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
    ) -> algokit_utils.TransactionResponse:
        ...

    @typing.overload
    def delete(
        self,
        *,
        args: DeleteAbiArgs,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
    ) -> algokit_utils.ABITransactionResponse[str]:
        ...

    def delete(
        self,
        *,
        args: DeleteAbiArgs | None = None,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
    ) -> algokit_utils.TransactionResponse | algokit_utils.ABITransactionResponse[str]:
        return self.app_client.delete(
            call_abi_method=args.method() if args else False,
            transaction_parameters=_as_dict(transaction_parameters),
            **_as_dict(args),
        )

    def opt_in(
        self,
        *,
        args: OptInArgs,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
    ) -> algokit_utils.ABITransactionResponse[None]:
        return self.app_client.opt_in(
            call_abi_method=args.method() if args else False,
            transaction_parameters=_as_dict(transaction_parameters),
            **_as_dict(args),
        )

    def clear_state(
        self,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
        app_args: list[bytes] | None = None,
    ) -> algokit_utils.TransactionResponse:
        return self.app_client.clear_state(_as_dict(transaction_parameters), app_args)

    def deploy(
        self,
        version: str | None = None,
        *,
        signer: TransactionSigner | None = None,
        sender: str | None = None,
        allow_update: bool | None = None,
        allow_delete: bool | None = None,
        on_update: algokit_utils.OnUpdate = algokit_utils.OnUpdate.Fail,
        on_schema_break: algokit_utils.OnSchemaBreak = algokit_utils.OnSchemaBreak.Fail,
        template_values: algokit_utils.TemplateValueMapping | None = None,
        create_args: algokit_utils.DeployCallArgs | None = None,
        update_args: algokit_utils.DeployCallArgs | None = None,
        delete_args: algokit_utils.DeployCallArgs | None = None,
    ) -> algokit_utils.DeployResponse:
        return self.app_client.deploy(
            version,
            signer=signer,
            sender=sender,
            allow_update=allow_update,
            allow_delete=allow_delete,
            on_update=on_update,
            on_schema_break=on_schema_break,
            template_values=template_values,
            create_args=create_args,
            update_args=update_args,
            delete_args=delete_args,
        )