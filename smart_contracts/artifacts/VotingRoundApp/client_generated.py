# flake8: noqa
# fmt: off
# This file was automatically generated by algokit-client-generator.
# DO NOT MODIFY IT BY HAND.
import base64
import dataclasses
import typing
from abc import ABC, abstractmethod

import algokit_utils
import algosdk
from algosdk.atomic_transaction_composer import TransactionSigner, TransactionWithSigner

_APP_SPEC_JSON = r"""{
    "hints": {
        "create(string,byte[],string,uint64,uint64,uint8[],uint64,string)void": {
            "call_config": {
                "no_op": "CREATE"
            }
        },
        "bootstrap(pay)void": {
            "call_config": {
                "no_op": "CALL"
            }
        },
        "close()void": {
            "call_config": {
                "no_op": "CALL"
            }
        },
        "get_preconditions(byte[])(uint64,uint64,uint64,uint64)": {
            "read_only": true,
            "structs": {
                "output": {
                    "name": "VotingPreconditions",
                    "elements": [
                        [
                            "is_voting_open",
                            "uint64"
                        ],
                        [
                            "is_allowed_to_vote",
                            "uint64"
                        ],
                        [
                            "has_already_voted",
                            "uint64"
                        ],
                        [
                            "current_time",
                            "uint64"
                        ]
                    ]
                }
            },
            "call_config": {
                "no_op": "CALL"
            }
        },
        "vote(pay,byte[],uint8[])void": {
            "call_config": {
                "no_op": "CALL"
            }
        }
    },
    "source": {
        "approval": "I3ByYWdtYSB2ZXJzaW9uIDgKaW50Y2Jsb2NrIDAgMSAxMCA1CmJ5dGVjYmxvY2sgMHggMHgwNjgxMDEgMHg3NjZmNzQ2NTVmNjk2NCAweDZmNzA3NDY5NmY2ZTVmNjM2Zjc1NmU3NDczIDB4Njk3MzVmNjI2ZjZmNzQ3Mzc0NzI2MTcwNzA2NTY0IDB4NzY2Zjc0NjU3MjVmNjM2Zjc1NmU3NCAweDYzNmM2ZjczNjU1Zjc0Njk2ZDY1IDB4NzQ2Zjc0NjE2YzVmNmY3MDc0Njk2ZjZlNzMgMHg1NiAweDczNmU2MTcwNzM2ODZmNzQ1ZjcwNzU2MjZjNjk2MzVmNmI2NTc5IDB4NmQ2NTc0NjE2NDYxNzQ2MTVmNjk3MDY2NzM1ZjYzNjk2NCAweDczNzQ2MTcyNzQ1Zjc0Njk2ZDY1IDB4NjU2ZTY0NWY3NDY5NmQ2NSAweDcxNzU2ZjcyNzU2ZCAweDZlNjY3NDVmNjk2ZDYxNjc2NTVmNzU3MjZjIDB4NmU2Njc0NWY2MTczNzM2NTc0NWY2OTY0IDB4MmMKdHhuIE51bUFwcEFyZ3MKaW50Y18wIC8vIDAKPT0KYm56IG1haW5fbDEyCnR4bmEgQXBwbGljYXRpb25BcmdzIDAKcHVzaGJ5dGVzIDB4YWU4OTdmNmIgLy8gImNyZWF0ZShzdHJpbmcsYnl0ZVtdLHN0cmluZyx1aW50NjQsdWludDY0LHVpbnQ4W10sdWludDY0LHN0cmluZyl2b2lkIgo9PQpibnogbWFpbl9sMTEKdHhuYSBBcHBsaWNhdGlvbkFyZ3MgMApwdXNoYnl0ZXMgMHhhNGU4ZDE2NCAvLyAiYm9vdHN0cmFwKHBheSl2b2lkIgo9PQpibnogbWFpbl9sMTAKdHhuYSBBcHBsaWNhdGlvbkFyZ3MgMApwdXNoYnl0ZXMgMHg5NjU2MDQ3YSAvLyAiY2xvc2UoKXZvaWQiCj09CmJueiBtYWluX2w5CnR4bmEgQXBwbGljYXRpb25BcmdzIDAKcHVzaGJ5dGVzIDB4YmNiMTU4OTYgLy8gImdldF9wcmVjb25kaXRpb25zKGJ5dGVbXSkodWludDY0LHVpbnQ2NCx1aW50NjQsdWludDY0KSIKPT0KYm56IG1haW5fbDgKdHhuYSBBcHBsaWNhdGlvbkFyZ3MgMApwdXNoYnl0ZXMgMHg4NGE1M2M2ZSAvLyAidm90ZShwYXksYnl0ZVtdLHVpbnQ4W10pdm9pZCIKPT0KYm56IG1haW5fbDcKZXJyCm1haW5fbDc6CnR4biBPbkNvbXBsZXRpb24KaW50Y18wIC8vIE5vT3AKPT0KdHhuIEFwcGxpY2F0aW9uSUQKaW50Y18wIC8vIDAKIT0KJiYKYXNzZXJ0CnR4bmEgQXBwbGljYXRpb25BcmdzIDEKc3RvcmUgMTEKdHhuYSBBcHBsaWNhdGlvbkFyZ3MgMgpzdG9yZSAxMgp0eG4gR3JvdXBJbmRleAppbnRjXzEgLy8gMQotCnN0b3JlIDEwCmxvYWQgMTAKZ3R4bnMgVHlwZUVudW0KaW50Y18xIC8vIHBheQo9PQphc3NlcnQKbG9hZCAxMApsb2FkIDExCmxvYWQgMTIKY2FsbHN1YiB2b3RlXzkKaW50Y18xIC8vIDEKcmV0dXJuCm1haW5fbDg6CnR4biBPbkNvbXBsZXRpb24KaW50Y18wIC8vIE5vT3AKPT0KdHhuIEFwcGxpY2F0aW9uSUQKaW50Y18wIC8vIDAKIT0KJiYKYXNzZXJ0CnR4bmEgQXBwbGljYXRpb25BcmdzIDEKY2FsbHN1YiBnZXRwcmVjb25kaXRpb25zXzgKc3RvcmUgOQpwdXNoYnl0ZXMgMHgxNTFmN2M3NSAvLyAweDE1MWY3Yzc1CmxvYWQgOQpjb25jYXQKbG9nCmludGNfMSAvLyAxCnJldHVybgptYWluX2w5Ogp0eG4gT25Db21wbGV0aW9uCmludGNfMCAvLyBOb09wCj09CnR4biBBcHBsaWNhdGlvbklECmludGNfMCAvLyAwCiE9CiYmCmFzc2VydApjYWxsc3ViIGNsb3NlXzMKaW50Y18xIC8vIDEKcmV0dXJuCm1haW5fbDEwOgp0eG4gT25Db21wbGV0aW9uCmludGNfMCAvLyBOb09wCj09CnR4biBBcHBsaWNhdGlvbklECmludGNfMCAvLyAwCiE9CiYmCmFzc2VydAp0eG4gR3JvdXBJbmRleAppbnRjXzEgLy8gMQotCnN0b3JlIDgKbG9hZCA4Cmd0eG5zIFR5cGVFbnVtCmludGNfMSAvLyBwYXkKPT0KYXNzZXJ0CmxvYWQgOApjYWxsc3ViIGJvb3RzdHJhcF8yCmludGNfMSAvLyAxCnJldHVybgptYWluX2wxMToKdHhuIE9uQ29tcGxldGlvbgppbnRjXzAgLy8gTm9PcAo9PQp0eG4gQXBwbGljYXRpb25JRAppbnRjXzAgLy8gMAo9PQomJgphc3NlcnQKdHhuYSBBcHBsaWNhdGlvbkFyZ3MgMQpzdG9yZSAwCnR4bmEgQXBwbGljYXRpb25BcmdzIDIKc3RvcmUgMQp0eG5hIEFwcGxpY2F0aW9uQXJncyAzCnN0b3JlIDIKdHhuYSBBcHBsaWNhdGlvbkFyZ3MgNApidG9pCnN0b3JlIDMKdHhuYSBBcHBsaWNhdGlvbkFyZ3MgNQpidG9pCnN0b3JlIDQKdHhuYSBBcHBsaWNhdGlvbkFyZ3MgNgpzdG9yZSA1CnR4bmEgQXBwbGljYXRpb25BcmdzIDcKYnRvaQpzdG9yZSA2CnR4bmEgQXBwbGljYXRpb25BcmdzIDgKc3RvcmUgNwpsb2FkIDAKbG9hZCAxCmxvYWQgMgpsb2FkIDMKbG9hZCA0CmxvYWQgNQpsb2FkIDYKbG9hZCA3CmNhbGxzdWIgY3JlYXRlXzEKaW50Y18xIC8vIDEKcmV0dXJuCm1haW5fbDEyOgp0eG4gT25Db21wbGV0aW9uCmludGNfMyAvLyBEZWxldGVBcHBsaWNhdGlvbgo9PQpibnogbWFpbl9sMTQKZXJyCm1haW5fbDE0Ogp0eG4gQXBwbGljYXRpb25JRAppbnRjXzAgLy8gMAohPQphc3NlcnQKY2FsbHN1YiBkZWxldGVfMAppbnRjXzEgLy8gMQpyZXR1cm4KCi8vIGRlbGV0ZQpkZWxldGVfMDoKcHJvdG8gMCAwCnR4biBTZW5kZXIKZ2xvYmFsIENyZWF0b3JBZGRyZXNzCj09Ci8vIHVuYXV0aG9yaXplZAphc3NlcnQKcHVzaGludCBUTVBMX0RFTEVUQUJMRSAvLyBUTVBMX0RFTEVUQUJMRQovLyBDaGVjayBhcHAgaXMgZGVsZXRhYmxlCmFzc2VydApyZXRzdWIKCi8vIGNyZWF0ZQpjcmVhdGVfMToKcHJvdG8gOCAwCmludGNfMCAvLyAwCmR1cApieXRlY18wIC8vICIiCmludGNfMCAvLyAwCmR1cG4gMgpwdXNoaW50IDI4MDAgLy8gMjgwMAppbnRjXzIgLy8gMTAKKwpzdG9yZSAxMwpjcmVhdGVfMV9sMToKbG9hZCAxMwpnbG9iYWwgT3Bjb2RlQnVkZ2V0Cj4KYm56IGNyZWF0ZV8xX2w1CmZyYW1lX2RpZyAtNQpmcmFtZV9kaWcgLTQKPD0KLy8gRW5kIHRpbWUgc2hvdWxkIGJlIGFmdGVyIHN0YXJ0IHRpbWUKYXNzZXJ0CmZyYW1lX2RpZyAtNApnbG9iYWwgTGF0ZXN0VGltZXN0YW1wCj49Ci8vIEVuZCB0aW1lIHNob3VsZCBiZSBpbiB0aGUgZnV0dXJlCmFzc2VydAppbnRjXzAgLy8gMApieXRlY18yIC8vICJ2b3RlX2lkIgphcHBfZ2xvYmFsX2dldF9leApzdG9yZSAxNQpzdG9yZSAxNApsb2FkIDE1CiEKYXNzZXJ0CmJ5dGVjXzIgLy8gInZvdGVfaWQiCmZyYW1lX2RpZyAtOApleHRyYWN0IDIgMAphcHBfZ2xvYmFsX3B1dAppbnRjXzAgLy8gMApieXRlYyA5IC8vICJzbmFwc2hvdF9wdWJsaWNfa2V5IgphcHBfZ2xvYmFsX2dldF9leApzdG9yZSAxNwpzdG9yZSAxNgpsb2FkIDE3CiEKYXNzZXJ0CmJ5dGVjIDkgLy8gInNuYXBzaG90X3B1YmxpY19rZXkiCmZyYW1lX2RpZyAtNwpleHRyYWN0IDIgMAphcHBfZ2xvYmFsX3B1dAppbnRjXzAgLy8gMApieXRlYyAxMCAvLyAibWV0YWRhdGFfaXBmc19jaWQiCmFwcF9nbG9iYWxfZ2V0X2V4CnN0b3JlIDE5CnN0b3JlIDE4CmxvYWQgMTkKIQphc3NlcnQKYnl0ZWMgMTAgLy8gIm1ldGFkYXRhX2lwZnNfY2lkIgpmcmFtZV9kaWcgLTYKZXh0cmFjdCAyIDAKYXBwX2dsb2JhbF9wdXQKaW50Y18wIC8vIDAKYnl0ZWMgMTEgLy8gInN0YXJ0X3RpbWUiCmFwcF9nbG9iYWxfZ2V0X2V4CnN0b3JlIDIxCnN0b3JlIDIwCmxvYWQgMjEKIQphc3NlcnQKYnl0ZWMgMTEgLy8gInN0YXJ0X3RpbWUiCmZyYW1lX2RpZyAtNQphcHBfZ2xvYmFsX3B1dAppbnRjXzAgLy8gMApieXRlYyAxMiAvLyAiZW5kX3RpbWUiCmFwcF9nbG9iYWxfZ2V0X2V4CnN0b3JlIDIzCnN0b3JlIDIyCmxvYWQgMjMKIQphc3NlcnQKYnl0ZWMgMTIgLy8gImVuZF90aW1lIgpmcmFtZV9kaWcgLTQKYXBwX2dsb2JhbF9wdXQKaW50Y18wIC8vIDAKYnl0ZWMgMTMgLy8gInF1b3J1bSIKYXBwX2dsb2JhbF9nZXRfZXgKc3RvcmUgMjUKc3RvcmUgMjQKbG9hZCAyNQohCmFzc2VydApieXRlYyAxMyAvLyAicXVvcnVtIgpmcmFtZV9kaWcgLTIKYXBwX2dsb2JhbF9wdXQKYnl0ZWMgNCAvLyAiaXNfYm9vdHN0cmFwcGVkIgppbnRjXzAgLy8gMAphcHBfZ2xvYmFsX3B1dApieXRlYyA1IC8vICJ2b3Rlcl9jb3VudCIKaW50Y18wIC8vIDAKYXBwX2dsb2JhbF9wdXQKYnl0ZWMgNiAvLyAiY2xvc2VfdGltZSIKaW50Y18wIC8vIDAKYXBwX2dsb2JhbF9wdXQKaW50Y18wIC8vIDAKYnl0ZWMgMTQgLy8gIm5mdF9pbWFnZV91cmwiCmFwcF9nbG9iYWxfZ2V0X2V4CnN0b3JlIDI3CnN0b3JlIDI2CmxvYWQgMjcKIQphc3NlcnQKYnl0ZWMgMTQgLy8gIm5mdF9pbWFnZV91cmwiCmZyYW1lX2RpZyAtMQpleHRyYWN0IDIgMAphcHBfZ2xvYmFsX3B1dApieXRlYyAxNSAvLyAibmZ0X2Fzc2V0X2lkIgppbnRjXzAgLy8gMAphcHBfZ2xvYmFsX3B1dApmcmFtZV9kaWcgLTMKaW50Y18wIC8vIDAKZXh0cmFjdF91aW50MTYKZnJhbWVfYnVyeSAwCmZyYW1lX2RpZyAwCi8vIG9wdGlvbl9jb3VudHMgc2hvdWxkIGJlIG5vbi1lbXB0eQphc3NlcnQKZnJhbWVfZGlnIC0zCmludGNfMCAvLyAwCmV4dHJhY3RfdWludDE2CmZyYW1lX2J1cnkgMQpmcmFtZV9kaWcgMQpwdXNoaW50IDExMiAvLyAxMTIKPD0KLy8gQ2FuJ3QgaGF2ZSBtb3JlIHRoYW4gMTEyIHF1ZXN0aW9ucwphc3NlcnQKaW50Y18wIC8vIDAKYnl0ZWNfMyAvLyAib3B0aW9uX2NvdW50cyIKYXBwX2dsb2JhbF9nZXRfZXgKc3RvcmUgMjkKc3RvcmUgMjgKbG9hZCAyOQohCmFzc2VydApieXRlY18zIC8vICJvcHRpb25fY291bnRzIgpmcmFtZV9kaWcgLTMKYXBwX2dsb2JhbF9wdXQKYnl0ZWNfMyAvLyAib3B0aW9uX2NvdW50cyIKYXBwX2dsb2JhbF9nZXQKZnJhbWVfYnVyeSAyCmludGNfMCAvLyAwCnN0b3JlIDMxCmZyYW1lX2RpZyAyCmludGNfMCAvLyAwCmV4dHJhY3RfdWludDE2CmZyYW1lX2J1cnkgMwpmcmFtZV9kaWcgMwpzdG9yZSAzMgppbnRjXzAgLy8gMApzdG9yZSAzMwpjcmVhdGVfMV9sMzoKbG9hZCAzMwpsb2FkIDMyCjwKYnogY3JlYXRlXzFfbDYKZnJhbWVfZGlnIDIKaW50Y18xIC8vIDEKbG9hZCAzMwoqCnB1c2hpbnQgMiAvLyAyCisKZ2V0Ynl0ZQpmcmFtZV9idXJ5IDQKbG9hZCAzMQpmcmFtZV9kaWcgNAorCnN0b3JlIDMxCmxvYWQgMzMKaW50Y18xIC8vIDEKKwpzdG9yZSAzMwpiIGNyZWF0ZV8xX2wzCmNyZWF0ZV8xX2w1OgppdHhuX2JlZ2luCnB1c2hpbnQgNiAvLyBhcHBsCml0eG5fZmllbGQgVHlwZUVudW0KaW50Y18wIC8vIDAKaXR4bl9maWVsZCBGZWUKaW50Y18zIC8vIERlbGV0ZUFwcGxpY2F0aW9uCml0eG5fZmllbGQgT25Db21wbGV0aW9uCmJ5dGVjXzEgLy8gMHgwNjgxMDEKaXR4bl9maWVsZCBBcHByb3ZhbFByb2dyYW0KYnl0ZWNfMSAvLyAweDA2ODEwMQppdHhuX2ZpZWxkIENsZWFyU3RhdGVQcm9ncmFtCml0eG5fc3VibWl0CmIgY3JlYXRlXzFfbDEKY3JlYXRlXzFfbDY6CmxvYWQgMzEKc3RvcmUgMzAKbG9hZCAzMApwdXNoaW50IDEyOCAvLyAxMjgKPD0KLy8gQ2FuJ3QgaGF2ZSBtb3JlIHRoYW4gMTI4IHZvdGUgb3B0aW9ucwphc3NlcnQKaW50Y18wIC8vIDAKYnl0ZWMgNyAvLyAidG90YWxfb3B0aW9ucyIKYXBwX2dsb2JhbF9nZXRfZXgKc3RvcmUgMzUKc3RvcmUgMzQKbG9hZCAzNQohCmFzc2VydApieXRlYyA3IC8vICJ0b3RhbF9vcHRpb25zIgpsb2FkIDMwCmFwcF9nbG9iYWxfcHV0CnJldHN1YgoKLy8gYm9vdHN0cmFwCmJvb3RzdHJhcF8yOgpwcm90byAxIDAKaW50Y18wIC8vIDAKdHhuIFNlbmRlcgpnbG9iYWwgQ3JlYXRvckFkZHJlc3MKPT0KLy8gdW5hdXRob3JpemVkCmFzc2VydApieXRlYyA0IC8vICJpc19ib290c3RyYXBwZWQiCmFwcF9nbG9iYWxfZ2V0CiEKLy8gQWxyZWFkeSBib290c3RyYXBwZWQKYXNzZXJ0CmJ5dGVjIDQgLy8gImlzX2Jvb3RzdHJhcHBlZCIKaW50Y18xIC8vIDEKYXBwX2dsb2JhbF9wdXQKcHVzaGludCAyMDM5MDAgLy8gMjAzOTAwCmJ5dGVjIDcgLy8gInRvdGFsX29wdGlvbnMiCmFwcF9nbG9iYWxfZ2V0CnB1c2hpbnQgMzIwMCAvLyAzMjAwCioKKwpzdG9yZSAzNgpmcmFtZV9kaWcgLTEKZ3R4bnMgUmVjZWl2ZXIKZ2xvYmFsIEN1cnJlbnRBcHBsaWNhdGlvbkFkZHJlc3MKPT0KLy8gUGF5bWVudCBtdXN0IGJlIHRvIGFwcCBhZGRyZXNzCmFzc2VydApsb2FkIDM2Cml0b2IKbG9nCmZyYW1lX2RpZyAtMQpndHhucyBBbW91bnQKbG9hZCAzNgo9PQovLyBQYXltZW50IG11c3QgYmUgZm9yIHRoZSBleGFjdCBtaW4gYmFsYW5jZSByZXF1aXJlbWVudAphc3NlcnQKYnl0ZWMgOCAvLyAiViIKYnl0ZWMgNyAvLyAidG90YWxfb3B0aW9ucyIKYXBwX2dsb2JhbF9nZXQKcHVzaGludCA4IC8vIDgKKgpib3hfY3JlYXRlCnBvcApyZXRzdWIKCi8vIGNsb3NlCmNsb3NlXzM6CnByb3RvIDAgMApieXRlY18wIC8vICIiCmludGNfMCAvLyAwCmR1cG4gMgp0eG4gU2VuZGVyCmdsb2JhbCBDcmVhdG9yQWRkcmVzcwo9PQovLyB1bmF1dGhvcml6ZWQKYXNzZXJ0CnB1c2hpbnQgMjAwMDAgLy8gMjAwMDAKaW50Y18yIC8vIDEwCisKc3RvcmUgMzcKY2xvc2VfM19sMToKbG9hZCAzNwpnbG9iYWwgT3Bjb2RlQnVkZ2V0Cj4KYm56IGNsb3NlXzNfbDE3CmJ5dGVjIDYgLy8gImNsb3NlX3RpbWUiCmFwcF9nbG9iYWxfZ2V0CmludGNfMCAvLyAwCj09Ci8vIEFscmVhZHkgY2xvc2VkCmFzc2VydApieXRlYyA2IC8vICJjbG9zZV90aW1lIgpnbG9iYWwgTGF0ZXN0VGltZXN0YW1wCmFwcF9nbG9iYWxfcHV0CnB1c2hieXRlcyAweDdiMjI3Mzc0NjE2ZTY0NjE3MjY0MjIzYTIyNjE3MjYzMzYzOTIyMmMyMjY0NjU3MzYzNzI2OTcwNzQ2OTZmNmUyMjNhMjI1NDY4Njk3MzIwNjk3MzIwNjEyMDc2NmY3NDY5NmU2NzIwNzI2NTczNzU2Yzc0MjA0ZTQ2NTQyMDY2NmY3MjIwNzY2Zjc0Njk2ZTY3MjA3MjZmNzU2ZTY0MjA3NzY5NzQ2ODIwNDk0NDIwIC8vICJ7XCJzdGFuZGFyZFwiOlwiYXJjNjlcIixcImRlc2NyaXB0aW9uXCI6XCJUaGlzIGlzIGEgdm90aW5nIHJlc3VsdCBORlQgZm9yIHZvdGluZyByb3VuZCB3aXRoIElEICIKYnl0ZWNfMiAvLyAidm90ZV9pZCIKYXBwX2dsb2JhbF9nZXQKY29uY2F0CnB1c2hieXRlcyAweDJlMjIyYzIyNzA3MjZmNzA2NTcyNzQ2OTY1NzMyMjNhN2IyMjZkNjU3NDYxNjQ2MTc0NjEyMjNhMjI2OTcwNjY3MzNhMmYyZiAvLyAiLlwiLFwicHJvcGVydGllc1wiOntcIm1ldGFkYXRhXCI6XCJpcGZzOi8vIgpjb25jYXQKYnl0ZWMgMTAgLy8gIm1ldGFkYXRhX2lwZnNfY2lkIgphcHBfZ2xvYmFsX2dldApjb25jYXQKcHVzaGJ5dGVzIDB4MjIyYzIyNjk2NDIyM2EyMiAvLyAiXCIsXCJpZFwiOlwiIgpjb25jYXQKYnl0ZWNfMiAvLyAidm90ZV9pZCIKYXBwX2dsb2JhbF9nZXQKY29uY2F0CnB1c2hieXRlcyAweDIyMmMyMjcxNzU2ZjcyNzU2ZDIyM2EgLy8gIlwiLFwicXVvcnVtXCI6Igpjb25jYXQKYnl0ZWMgMTMgLy8gInF1b3J1bSIKYXBwX2dsb2JhbF9nZXQKY2FsbHN1YiBpdG9hXzcKY29uY2F0CnB1c2hieXRlcyAweDJjMjI3NjZmNzQ2NTcyNDM2Zjc1NmU3NDIyM2EgLy8gIixcInZvdGVyQ291bnRcIjoiCmNvbmNhdApieXRlYyA1IC8vICJ2b3Rlcl9jb3VudCIKYXBwX2dsb2JhbF9nZXQKY2FsbHN1YiBpdG9hXzcKY29uY2F0CnB1c2hieXRlcyAweDJjMjI3NDYxNmM2YzY5NjU3MzIyM2E1YiAvLyAiLFwidGFsbGllc1wiOlsiCmNvbmNhdApzdG9yZSAzOApieXRlY18zIC8vICJvcHRpb25fY291bnRzIgphcHBfZ2xvYmFsX2dldApmcmFtZV9idXJ5IDAKZnJhbWVfZGlnIDAKaW50Y18wIC8vIDAKZXh0cmFjdF91aW50MTYKZnJhbWVfYnVyeSAxCmZyYW1lX2RpZyAxCnN0b3JlIDM5CmludGNfMCAvLyAwCnN0b3JlIDQwCmludGNfMCAvLyAwCnN0b3JlIDQxCmludGNfMCAvLyAwCnN0b3JlIDQyCmNsb3NlXzNfbDM6CmxvYWQgNDIKbG9hZCAzOQo8CmJ6IGNsb3NlXzNfbDE4CmZyYW1lX2RpZyAwCmludGNfMSAvLyAxCmxvYWQgNDIKKgpwdXNoaW50IDIgLy8gMgorCmdldGJ5dGUKZnJhbWVfYnVyeSAyCmZyYW1lX2RpZyAyCnN0b3JlIDQzCmludGNfMCAvLyAwCnN0b3JlIDQ0CmNsb3NlXzNfbDU6CmxvYWQgNDQKbG9hZCA0Mwo8CmJueiBjbG9zZV8zX2w3CmxvYWQgNDIKaW50Y18xIC8vIDEKKwpzdG9yZSA0MgpiIGNsb3NlXzNfbDMKY2xvc2VfM19sNzoKcHVzaGludCA4IC8vIDgKbG9hZCA0MQoqCnN0b3JlIDQ1CmJ5dGVjIDggLy8gIlYiCmxvYWQgNDUKcHVzaGludCA4IC8vIDgKYm94X2V4dHJhY3QKYnRvaQpzdG9yZSA0MApsb2FkIDM4CmxvYWQgNDQKaW50Y18wIC8vIDAKPT0KYm56IGNsb3NlXzNfbDE2CmJ5dGVjXzAgLy8gIiIKY2xvc2VfM19sOToKY29uY2F0CmxvYWQgNDAKY2FsbHN1YiBpdG9hXzcKY29uY2F0CmxvYWQgNDQKbG9hZCA0MwppbnRjXzEgLy8gMQotCj09CmJueiBjbG9zZV8zX2wxMgpieXRlYyAxNiAvLyAiLCIKY2xvc2VfM19sMTE6CmNvbmNhdApzdG9yZSAzOApsb2FkIDQxCmludGNfMSAvLyAxCisKc3RvcmUgNDEKbG9hZCA0NAppbnRjXzEgLy8gMQorCnN0b3JlIDQ0CmIgY2xvc2VfM19sNQpjbG9zZV8zX2wxMjoKcHVzaGJ5dGVzIDB4NWQgLy8gIl0iCmxvYWQgNDIKbG9hZCAzOQppbnRjXzEgLy8gMQotCj09CmJueiBjbG9zZV8zX2wxNQpieXRlYyAxNiAvLyAiLCIKY2xvc2VfM19sMTQ6CmNvbmNhdApiIGNsb3NlXzNfbDExCmNsb3NlXzNfbDE1OgpieXRlY18wIC8vICIiCmIgY2xvc2VfM19sMTQKY2xvc2VfM19sMTY6CnB1c2hieXRlcyAweDViIC8vICJbIgpiIGNsb3NlXzNfbDkKY2xvc2VfM19sMTc6Cml0eG5fYmVnaW4KcHVzaGludCA2IC8vIGFwcGwKaXR4bl9maWVsZCBUeXBlRW51bQppbnRjXzAgLy8gMAppdHhuX2ZpZWxkIEZlZQppbnRjXzMgLy8gRGVsZXRlQXBwbGljYXRpb24KaXR4bl9maWVsZCBPbkNvbXBsZXRpb24KYnl0ZWNfMSAvLyAweDA2ODEwMQppdHhuX2ZpZWxkIEFwcHJvdmFsUHJvZ3JhbQpieXRlY18xIC8vIDB4MDY4MTAxCml0eG5fZmllbGQgQ2xlYXJTdGF0ZVByb2dyYW0KaXR4bl9zdWJtaXQKYiBjbG9zZV8zX2wxCmNsb3NlXzNfbDE4OgppdHhuX2JlZ2luCnB1c2hpbnQgMyAvLyBhY2ZnCml0eG5fZmllbGQgVHlwZUVudW0KaW50Y18xIC8vIDEKaXR4bl9maWVsZCBDb25maWdBc3NldFRvdGFsCmludGNfMCAvLyAwCml0eG5fZmllbGQgQ29uZmlnQXNzZXREZWNpbWFscwppbnRjXzAgLy8gMAppdHhuX2ZpZWxkIENvbmZpZ0Fzc2V0RGVmYXVsdEZyb3plbgpwdXNoYnl0ZXMgMHg1YjU2NGY1NDQ1MjA1MjQ1NTM1NTRjNTQ1ZDIwIC8vICJbVk9URSBSRVNVTFRdICIKYnl0ZWNfMiAvLyAidm90ZV9pZCIKYXBwX2dsb2JhbF9nZXQKY29uY2F0Cml0eG5fZmllbGQgQ29uZmlnQXNzZXROYW1lCnB1c2hieXRlcyAweDU2NGY1NDQ1NTI1MzRjNTQgLy8gIlZPVEVSU0xUIgppdHhuX2ZpZWxkIENvbmZpZ0Fzc2V0VW5pdE5hbWUKYnl0ZWMgMTQgLy8gIm5mdF9pbWFnZV91cmwiCmFwcF9nbG9iYWxfZ2V0Cml0eG5fZmllbGQgQ29uZmlnQXNzZXRVUkwKbG9hZCAzOApwdXNoYnl0ZXMgMHg1ZDdkN2QgLy8gIl19fSIKY29uY2F0Cml0eG5fZmllbGQgTm90ZQppdHhuX3N1Ym1pdApieXRlYyAxNSAvLyAibmZ0X2Fzc2V0X2lkIgppdHhuIENyZWF0ZWRBc3NldElECmFwcF9nbG9iYWxfcHV0CnJldHN1YgoKLy8gYWxsb3dlZF90b192b3RlCmFsbG93ZWR0b3ZvdGVfNDoKcHJvdG8gMSAxCnB1c2hpbnQgMjAwMCAvLyAyMDAwCmludGNfMiAvLyAxMAorCnN0b3JlIDQ2CmFsbG93ZWR0b3ZvdGVfNF9sMToKbG9hZCA0NgpnbG9iYWwgT3Bjb2RlQnVkZ2V0Cj4KYnogYWxsb3dlZHRvdm90ZV80X2wzCml0eG5fYmVnaW4KcHVzaGludCA2IC8vIGFwcGwKaXR4bl9maWVsZCBUeXBlRW51bQppbnRjXzAgLy8gMAppdHhuX2ZpZWxkIEZlZQppbnRjXzMgLy8gRGVsZXRlQXBwbGljYXRpb24KaXR4bl9maWVsZCBPbkNvbXBsZXRpb24KYnl0ZWNfMSAvLyAweDA2ODEwMQppdHhuX2ZpZWxkIEFwcHJvdmFsUHJvZ3JhbQpieXRlY18xIC8vIDB4MDY4MTAxCml0eG5fZmllbGQgQ2xlYXJTdGF0ZVByb2dyYW0KaXR4bl9zdWJtaXQKYiBhbGxvd2VkdG92b3RlXzRfbDEKYWxsb3dlZHRvdm90ZV80X2wzOgp0eG4gU2VuZGVyCmZyYW1lX2RpZyAtMQpieXRlYyA5IC8vICJzbmFwc2hvdF9wdWJsaWNfa2V5IgphcHBfZ2xvYmFsX2dldAplZDI1NTE5dmVyaWZ5X2JhcmUKcmV0c3ViCgovLyB2b3Rpbmdfb3Blbgp2b3RpbmdvcGVuXzU6CnByb3RvIDAgMQpieXRlYyA0IC8vICJpc19ib290c3RyYXBwZWQiCmFwcF9nbG9iYWxfZ2V0CmludGNfMSAvLyAxCj09CmJ5dGVjIDYgLy8gImNsb3NlX3RpbWUiCmFwcF9nbG9iYWxfZ2V0CmludGNfMCAvLyAwCj09CiYmCmdsb2JhbCBMYXRlc3RUaW1lc3RhbXAKYnl0ZWMgMTEgLy8gInN0YXJ0X3RpbWUiCmFwcF9nbG9iYWxfZ2V0Cj49CiYmCmdsb2JhbCBMYXRlc3RUaW1lc3RhbXAKYnl0ZWMgMTIgLy8gImVuZF90aW1lIgphcHBfZ2xvYmFsX2dldAo8CiYmCnJldHN1YgoKLy8gYWxyZWFkeV92b3RlZAphbHJlYWR5dm90ZWRfNjoKcHJvdG8gMCAxCmJ5dGVjXzAgLy8gIiIKdHhuIFNlbmRlcgpmcmFtZV9idXJ5IDAKZnJhbWVfZGlnIDAKbGVuCnB1c2hpbnQgMzIgLy8gMzIKPT0KYXNzZXJ0CmZyYW1lX2RpZyAwCmJveF9sZW4Kc3RvcmUgNDgKc3RvcmUgNDcKbG9hZCA0OApmcmFtZV9idXJ5IDAKcmV0c3ViCgovLyBpdG9hCml0b2FfNzoKcHJvdG8gMSAxCmZyYW1lX2RpZyAtMQppbnRjXzAgLy8gMAo9PQpibnogaXRvYV83X2w1CmZyYW1lX2RpZyAtMQppbnRjXzIgLy8gMTAKLwppbnRjXzAgLy8gMAo+CmJueiBpdG9hXzdfbDQKYnl0ZWNfMCAvLyAiIgppdG9hXzdfbDM6CnB1c2hieXRlcyAweDMwMzEzMjMzMzQzNTM2MzczODM5IC8vICIwMTIzNDU2Nzg5IgpmcmFtZV9kaWcgLTEKaW50Y18yIC8vIDEwCiUKaW50Y18xIC8vIDEKZXh0cmFjdDMKY29uY2F0CmIgaXRvYV83X2w2Cml0b2FfN19sNDoKZnJhbWVfZGlnIC0xCmludGNfMiAvLyAxMAovCmNhbGxzdWIgaXRvYV83CmIgaXRvYV83X2wzCml0b2FfN19sNToKcHVzaGJ5dGVzIDB4MzAgLy8gIjAiCml0b2FfN19sNjoKcmV0c3ViCgovLyBnZXRfcHJlY29uZGl0aW9ucwpnZXRwcmVjb25kaXRpb25zXzg6CnByb3RvIDEgMQpieXRlY18wIC8vICIiCmludGNfMCAvLyAwCmR1cG4gNQpieXRlY18wIC8vICIiCmR1cApjYWxsc3ViIHZvdGluZ29wZW5fNQpmcmFtZV9idXJ5IDEKZnJhbWVfZGlnIC0xCmV4dHJhY3QgMiAwCmNhbGxzdWIgYWxsb3dlZHRvdm90ZV80CmZyYW1lX2J1cnkgMgpjYWxsc3ViIGFscmVhZHl2b3RlZF82CmZyYW1lX2J1cnkgMwpnbG9iYWwgTGF0ZXN0VGltZXN0YW1wCmZyYW1lX2J1cnkgNApmcmFtZV9kaWcgMQppdG9iCmZyYW1lX2RpZyAyCml0b2IKY29uY2F0CmZyYW1lX2RpZyAzCml0b2IKY29uY2F0CmZyYW1lX2RpZyA0Cml0b2IKY29uY2F0CmZyYW1lX2J1cnkgMApyZXRzdWIKCi8vIHZvdGUKdm90ZV85Ogpwcm90byAzIDAKYnl0ZWNfMCAvLyAiIgppbnRjXzAgLy8gMApkdXBuIDcKYnl0ZWNfMCAvLyAiIgpwdXNoaW50IDc3MDAgLy8gNzcwMAppbnRjXzIgLy8gMTAKKwpzdG9yZSA0OQp2b3RlXzlfbDE6CmxvYWQgNDkKZ2xvYmFsIE9wY29kZUJ1ZGdldAo+CmJueiB2b3RlXzlfbDUKZnJhbWVfZGlnIC0yCmV4dHJhY3QgMiAwCmNhbGxzdWIgYWxsb3dlZHRvdm90ZV80Ci8vIE5vdCBhbGxvd2VkIHRvIHZvdGUKYXNzZXJ0CmNhbGxzdWIgdm90aW5nb3Blbl81Ci8vIFZvdGluZyBub3Qgb3Blbgphc3NlcnQKY2FsbHN1YiBhbHJlYWR5dm90ZWRfNgohCi8vIEFscmVhZHkgdm90ZWQKYXNzZXJ0CmJ5dGVjXzMgLy8gIm9wdGlvbl9jb3VudHMiCmFwcF9nbG9iYWxfZ2V0CmZyYW1lX2J1cnkgMApmcmFtZV9kaWcgMAppbnRjXzAgLy8gMApleHRyYWN0X3VpbnQxNgpmcmFtZV9idXJ5IDEKZnJhbWVfZGlnIDEKc3RvcmUgNTAKZnJhbWVfZGlnIC0xCmludGNfMCAvLyAwCmV4dHJhY3RfdWludDE2CmZyYW1lX2J1cnkgMgpmcmFtZV9kaWcgMgpsb2FkIDUwCj09Ci8vIE51bWJlciBvZiBhbnN3ZXJzIGluY29ycmVjdAphc3NlcnQKcHVzaGludCAyNTAwIC8vIDI1MDAKcHVzaGludCAzNCAvLyAzNAppbnRjXzEgLy8gMQpmcmFtZV9kaWcgLTEKaW50Y18wIC8vIDAKZXh0cmFjdF91aW50MTYKZnJhbWVfYnVyeSA0CmZyYW1lX2RpZyA0CioKKwpwdXNoaW50IDQwMCAvLyA0MDAKKgorCnN0b3JlIDUxCmZyYW1lX2RpZyAtMwpndHhucyBSZWNlaXZlcgpnbG9iYWwgQ3VycmVudEFwcGxpY2F0aW9uQWRkcmVzcwo9PQovLyBQYXltZW50IG11c3QgYmUgdG8gYXBwIGFkZHJlc3MKYXNzZXJ0CmxvYWQgNTEKaXRvYgpsb2cKZnJhbWVfZGlnIC0zCmd0eG5zIEFtb3VudApsb2FkIDUxCj09Ci8vIFBheW1lbnQgbXVzdCBiZSB0aGUgZXhhY3QgbWluIGJhbGFuY2UgcmVxdWlyZW1lbnQKYXNzZXJ0CmludGNfMCAvLyAwCnN0b3JlIDUyCmludGNfMCAvLyAwCnN0b3JlIDUzCnZvdGVfOV9sMzoKbG9hZCA1Mwpsb2FkIDUwCjwKYnogdm90ZV85X2w2CmZyYW1lX2RpZyAtMQppbnRjXzEgLy8gMQpsb2FkIDUzCioKcHVzaGludCAyIC8vIDIKKwpnZXRieXRlCmZyYW1lX2J1cnkgNQpmcmFtZV9kaWcgMAppbnRjXzEgLy8gMQpsb2FkIDUzCioKcHVzaGludCAyIC8vIDIKKwpnZXRieXRlCmZyYW1lX2J1cnkgNwpmcmFtZV9kaWcgNQpmcmFtZV9kaWcgNwo8Ci8vIEFuc3dlciBvcHRpb24gaW5kZXggaW52YWxpZAphc3NlcnQKcHVzaGludCA4IC8vIDgKbG9hZCA1MgpmcmFtZV9kaWcgNQorCioKc3RvcmUgNTQKYnl0ZWMgOCAvLyAiViIKbG9hZCA1NApwdXNoaW50IDggLy8gOApib3hfZXh0cmFjdApidG9pCnN0b3JlIDU1CmJ5dGVjIDggLy8gIlYiCmxvYWQgNTQKbG9hZCA1NQppbnRjXzEgLy8gMQorCml0b2IKYm94X3JlcGxhY2UKbG9hZCA1MgpmcmFtZV9kaWcgNworCnN0b3JlIDUyCmxvYWQgNTMKaW50Y18xIC8vIDEKKwpzdG9yZSA1MwpiIHZvdGVfOV9sMwp2b3RlXzlfbDU6Cml0eG5fYmVnaW4KcHVzaGludCA2IC8vIGFwcGwKaXR4bl9maWVsZCBUeXBlRW51bQppbnRjXzAgLy8gMAppdHhuX2ZpZWxkIEZlZQppbnRjXzMgLy8gRGVsZXRlQXBwbGljYXRpb24KaXR4bl9maWVsZCBPbkNvbXBsZXRpb24KYnl0ZWNfMSAvLyAweDA2ODEwMQppdHhuX2ZpZWxkIEFwcHJvdmFsUHJvZ3JhbQpieXRlY18xIC8vIDB4MDY4MTAxCml0eG5fZmllbGQgQ2xlYXJTdGF0ZVByb2dyYW0KaXR4bl9zdWJtaXQKYiB2b3RlXzlfbDEKdm90ZV85X2w2Ogp0eG4gU2VuZGVyCmZyYW1lX2J1cnkgOQpmcmFtZV9kaWcgOQpsZW4KcHVzaGludCAzMiAvLyAzMgo9PQphc3NlcnQKZnJhbWVfZGlnIDkKYm94X2RlbApwb3AKZnJhbWVfZGlnIDkKZnJhbWVfZGlnIC0xCmJveF9wdXQKYnl0ZWMgNSAvLyAidm90ZXJfY291bnQiCmJ5dGVjIDUgLy8gInZvdGVyX2NvdW50IgphcHBfZ2xvYmFsX2dldAppbnRjXzEgLy8gMQorCmFwcF9nbG9iYWxfcHV0CnJldHN1Yg==",
        "clear": "I3ByYWdtYSB2ZXJzaW9uIDgKcHVzaGludCAwIC8vIDAKcmV0dXJu"
    },
    "state": {
        "global": {
            "num_byte_slices": 5,
            "num_uints": 8
        },
        "local": {
            "num_byte_slices": 0,
            "num_uints": 0
        }
    },
    "schema": {
        "global": {
            "declared": {
                "close_time": {
                    "type": "uint64",
                    "key": "close_time",
                    "descr": "The unix timestamp of the time the vote was closed"
                },
                "end_time": {
                    "type": "uint64",
                    "key": "end_time",
                    "descr": "The unix timestamp of the ending time of voting"
                },
                "is_bootstrapped": {
                    "type": "uint64",
                    "key": "is_bootstrapped",
                    "descr": "Whether or not the contract has been bootstrapped with answers"
                },
                "metadata_ipfs_cid": {
                    "type": "bytes",
                    "key": "metadata_ipfs_cid",
                    "descr": "The IPFS content ID of the voting metadata file"
                },
                "nft_asset_id": {
                    "type": "uint64",
                    "key": "nft_asset_id",
                    "descr": "The asset ID of a result NFT if one has been created"
                },
                "nft_image_url": {
                    "type": "bytes",
                    "key": "nft_image_url",
                    "descr": "The IPFS URL of the default image to use as the media of the result NFT"
                },
                "option_counts": {
                    "type": "bytes",
                    "key": "option_counts",
                    "descr": "The number of options for each question"
                },
                "quorum": {
                    "type": "uint64",
                    "key": "quorum",
                    "descr": "The minimum number of voters to reach quorum"
                },
                "snapshot_public_key": {
                    "type": "bytes",
                    "key": "snapshot_public_key",
                    "descr": "The public key of the Ed25519 compatible private key that was used to encrypt entries in the vote gating snapshot"
                },
                "start_time": {
                    "type": "uint64",
                    "key": "start_time",
                    "descr": "The unix timestamp of the starting time of voting"
                },
                "total_options": {
                    "type": "uint64",
                    "key": "total_options",
                    "descr": "The total number of options"
                },
                "vote_id": {
                    "type": "bytes",
                    "key": "vote_id",
                    "descr": "The identifier of this voting round"
                },
                "voter_count": {
                    "type": "uint64",
                    "key": "voter_count",
                    "descr": "The minimum number of voters who have voted"
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
        "name": "VotingRoundApp",
        "methods": [
            {
                "name": "create",
                "args": [
                    {
                        "type": "string",
                        "name": "vote_id"
                    },
                    {
                        "type": "byte[]",
                        "name": "snapshot_public_key"
                    },
                    {
                        "type": "string",
                        "name": "metadata_ipfs_cid"
                    },
                    {
                        "type": "uint64",
                        "name": "start_time"
                    },
                    {
                        "type": "uint64",
                        "name": "end_time"
                    },
                    {
                        "type": "uint8[]",
                        "name": "option_counts"
                    },
                    {
                        "type": "uint64",
                        "name": "quorum"
                    },
                    {
                        "type": "string",
                        "name": "nft_image_url"
                    }
                ],
                "returns": {
                    "type": "void"
                }
            },
            {
                "name": "bootstrap",
                "args": [
                    {
                        "type": "pay",
                        "name": "fund_min_bal_req"
                    }
                ],
                "returns": {
                    "type": "void"
                }
            },
            {
                "name": "close",
                "args": [],
                "returns": {
                    "type": "void"
                }
            },
            {
                "name": "get_preconditions",
                "args": [
                    {
                        "type": "byte[]",
                        "name": "signature"
                    }
                ],
                "returns": {
                    "type": "(uint64,uint64,uint64,uint64)"
                }
            },
            {
                "name": "vote",
                "args": [
                    {
                        "type": "pay",
                        "name": "fund_min_bal_req"
                    },
                    {
                        "type": "byte[]",
                        "name": "signature"
                    },
                    {
                        "type": "uint8[]",
                        "name": "answer_ids"
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
        "delete_application": "CALL"
    }
}"""
APP_SPEC = algokit_utils.ApplicationSpecification.from_json(_APP_SPEC_JSON)
_T = typing.TypeVar("_T")
_TReturn = typing.TypeVar("_TReturn")


class _ArgsBase(ABC, typing.Generic[_TReturn]):
    @staticmethod
    @abstractmethod
    def method() -> str:
        ...


_TArgs = typing.TypeVar("_TArgs", bound=_ArgsBase)


@dataclasses.dataclass(kw_only=True)
class _TypedDeployCreateArgs(algokit_utils.DeployCreateCallArgs, typing.Generic[_TArgs]):
    args: _TArgs


def _as_dict(data: _T | None) -> dict[str, typing.Any]:
    if data is None:
        return {}
    if not dataclasses.is_dataclass(data):
        raise TypeError(f"{data} must be a dataclass")
    return {f.name: getattr(data, f.name) for f in dataclasses.fields(data)}


def _convert_on_complete(on_complete: algokit_utils.OnCompleteActionName) -> algosdk.transaction.OnComplete:
    on_complete_enum = on_complete.replace("_", " ").title().replace(" ", "") + "OC"
    return getattr(algosdk.transaction.OnComplete, on_complete_enum)


def _convert_deploy_args(
    deploy_args: algokit_utils.DeployCallArgs | None,
) -> dict[str, typing.Any] | None:
    if deploy_args is None:
        return None

    deploy_args_dict = _as_dict(deploy_args)
    if hasattr(deploy_args, "args") and hasattr(deploy_args.args, "method"):
        deploy_args_dict["args"] = _as_dict(deploy_args.args)
        deploy_args_dict["method"] = deploy_args.args.method()

    return deploy_args_dict


@dataclasses.dataclass(kw_only=True)
class BootstrapArgs(_ArgsBase[None]):
    fund_min_bal_req: TransactionWithSigner

    @staticmethod
    def method() -> str:
        return "bootstrap(pay)void"


@dataclasses.dataclass(kw_only=True)
class CloseArgs(_ArgsBase[None]):
    @staticmethod
    def method() -> str:
        return "close()void"


@dataclasses.dataclass(kw_only=True)
class GetPreconditionsArgs(_ArgsBase[tuple[int, int, int, int]]):
    signature: list[int]

    @staticmethod
    def method() -> str:
        return "get_preconditions(byte[])(uint64,uint64,uint64,uint64)"


@dataclasses.dataclass(kw_only=True)
class VoteArgs(_ArgsBase[None]):
    fund_min_bal_req: TransactionWithSigner
    signature: list[int]
    answer_ids: list[int]

    @staticmethod
    def method() -> str:
        return "vote(pay,byte[],uint8[])void"


@dataclasses.dataclass(kw_only=True)
class CreateArgs(_ArgsBase[None]):
    vote_id: str
    snapshot_public_key: list[int]
    metadata_ipfs_cid: str
    start_time: int
    end_time: int
    option_counts: list[int]
    quorum: int
    nft_image_url: str

    @staticmethod
    def method() -> str:
        return "create(string,byte[],string,uint64,uint64,uint8[],uint64,string)void"


DeployCreate_CreateArgs = _TypedDeployCreateArgs[CreateArgs]


class ByteReader:
    def __init__(self, data: bytes):
        self._data = data

    @property
    def as_bytes(self) -> bytes:
        return self._data

    @property
    def as_str(self) -> str:
        return self._data.decode("utf8")

    @property
    def as_base64(self) -> str:
        return base64.b64encode(self._data).decode("utf8")

    @property
    def as_hex(self) -> str:
        return self._data.hex()


class GlobalState:
    def __init__(self, data: dict[bytes, bytes | int]):
        self.close_time = typing.cast(int, data.get(b"close_time"))
        """The unix timestamp of the time the vote was closed"""
        self.end_time = typing.cast(int, data.get(b"end_time"))
        """The unix timestamp of the ending time of voting"""
        self.is_bootstrapped = typing.cast(int, data.get(b"is_bootstrapped"))
        """Whether or not the contract has been bootstrapped with answers"""
        self.metadata_ipfs_cid = ByteReader(typing.cast(bytes, data.get(b"metadata_ipfs_cid")))
        """The IPFS content ID of the voting metadata file"""
        self.nft_asset_id = typing.cast(int, data.get(b"nft_asset_id"))
        """The asset ID of a result NFT if one has been created"""
        self.nft_image_url = ByteReader(typing.cast(bytes, data.get(b"nft_image_url")))
        """The IPFS URL of the default image to use as the media of the result NFT"""
        self.option_counts = ByteReader(typing.cast(bytes, data.get(b"option_counts")))
        """The number of options for each question"""
        self.quorum = typing.cast(int, data.get(b"quorum"))
        """The minimum number of voters to reach quorum"""
        self.snapshot_public_key = ByteReader(typing.cast(bytes, data.get(b"snapshot_public_key")))
        """The public key of the Ed25519 compatible private key that was used to encrypt entries in the vote gating snapshot"""
        self.start_time = typing.cast(int, data.get(b"start_time"))
        """The unix timestamp of the starting time of voting"""
        self.total_options = typing.cast(int, data.get(b"total_options"))
        """The total number of options"""
        self.vote_id = ByteReader(typing.cast(bytes, data.get(b"vote_id")))
        """The identifier of this voting round"""
        self.voter_count = typing.cast(int, data.get(b"voter_count"))
        """The minimum number of voters who have voted"""


class VotingRoundAppClient:
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

    def get_global_state(self) -> GlobalState:
        state = self.app_client.get_global_state(raw=True)
        return GlobalState(state)

    def bootstrap(
        self,
        *,
        fund_min_bal_req: TransactionWithSigner,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
    ) -> algokit_utils.ABITransactionResponse[None]:
        args = BootstrapArgs(
            fund_min_bal_req=fund_min_bal_req,
        )
        return self.app_client.call(
            call_abi_method=args.method(),
            transaction_parameters=_as_dict(transaction_parameters),
            **_as_dict(args),
        )

    def close(
        self,
        *,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
    ) -> algokit_utils.ABITransactionResponse[None]:
        args = CloseArgs()
        return self.app_client.call(
            call_abi_method=args.method(),
            transaction_parameters=_as_dict(transaction_parameters),
            **_as_dict(args),
        )

    def get_preconditions(
        self,
        *,
        signature: list[int],
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
    ) -> algokit_utils.ABITransactionResponse[tuple[int, int, int, int]]:
        args = GetPreconditionsArgs(
            signature=signature,
        )
        return self.app_client.call(
            call_abi_method=args.method(),
            transaction_parameters=_as_dict(transaction_parameters),
            **_as_dict(args),
        )

    def vote(
        self,
        *,
        fund_min_bal_req: TransactionWithSigner,
        signature: list[int],
        answer_ids: list[int],
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
    ) -> algokit_utils.ABITransactionResponse[None]:
        args = VoteArgs(
            fund_min_bal_req=fund_min_bal_req,
            signature=signature,
            answer_ids=answer_ids,
        )
        return self.app_client.call(
            call_abi_method=args.method(),
            transaction_parameters=_as_dict(transaction_parameters),
            **_as_dict(args),
        )

    def create(
        self,
        *,
        args: CreateArgs,
        on_complete: typing.Literal["no_op"] = "no_op",
        transaction_parameters: algokit_utils.CreateTransactionParameters | None = None,
    ) -> algokit_utils.ABITransactionResponse[None]:
        return self.app_client.create(
            call_abi_method=args.method() if args else False,
            transaction_parameters=_as_dict(transaction_parameters) | {"on_complete": _convert_on_complete(on_complete)},
            **_as_dict(args),
        )

    def delete(
        self,
        *,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
    ) -> algokit_utils.TransactionResponse:
        return self.app_client.delete(
            call_abi_method=False,
            transaction_parameters=_as_dict(transaction_parameters),
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
        create_args: DeployCreate_CreateArgs,
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
            create_args=_convert_deploy_args(create_args),
            update_args=_convert_deploy_args(update_args),
            delete_args=_convert_deploy_args(delete_args),
        )
