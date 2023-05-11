import {
  ABIAddressType,
  ABIArrayDynamicType,
  ABIArrayStaticType,
  ABIBoolType,
  ABIByteType,
  ABIStringType,
  ABITupleType,
  ABIType,
  ABIUfixedType,
  ABIUintType,
} from 'algosdk'

export function getEquivalentType(abiTypeStr: string): string {
  switch (abiTypeStr) {
    case 'void':
      return 'void'
    case 'txn':
    case 'pay':
    case 'keyreg':
    case 'acfg':
    case 'axfer':
    case 'afrz':
    case 'appl':
      return 'TransactionToSign | Transaction | Promise<SendTransactionResult>'
  }

  const abiType = ABIType.from(abiTypeStr)

  return abiTypeToTs(abiType)

  function abiTypeToTs(abiType: ABIType): string {
    if (abiType instanceof ABIUintType) {
      if (abiType.bitSize <= 51) return 'number'
      return 'bigint'
    }
    if (abiType instanceof ABIArrayDynamicType) {
      if (abiType.childType instanceof ABIByteType) return 'Uint8Array'
      return `${abiTypeToTs(abiType.childType)}[]`
    }
    if (abiType instanceof ABIArrayStaticType) {
      if (abiType.childType instanceof ABIByteType) return 'Uint8Array'
      return `[${new Array(abiType.staticLength).fill(abiTypeToTs(abiType.childType)).join(', ')}]`
    }
    if (abiType instanceof ABIAddressType) {
      return 'string'
    }
    if (abiType instanceof ABIBoolType) {
      return 'boolean'
    }
    if (abiType instanceof ABIUfixedType) {
      return 'number'
    }
    if (abiType instanceof ABITupleType) {
      return `[${abiType.childTypes.map(abiTypeToTs).join(', ')}]`
    }
    if (abiType instanceof ABIByteType) {
      return 'number'
    }
    if (abiType instanceof ABIStringType) {
      return 'string'
    }
    return 'unknown'
  }
}
