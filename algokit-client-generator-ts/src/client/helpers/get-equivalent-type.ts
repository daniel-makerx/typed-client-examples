import {
  ABIType,
  ABIUintType,
  ABIArrayDynamicType,
  ABIArrayStaticType,
  ABIAddressType,
  ABIBoolType,
  ABIUfixedType,
  ABITupleType,
  ABIByteType,
  ABIStringType,
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
      return 'TransactionWithSigner'
  }

  const abiType = ABIType.from(abiTypeStr)

  return abiTypeToTs(abiType)

  function abiTypeToTs(abiType: ABIType): string {
    if (abiType instanceof ABIUintType) {
      if (abiType.bitSize <= 51) return 'number'
      return 'bigint'
    }
    if (abiType instanceof ABIArrayDynamicType) {
      return `${abiTypeToTs(abiType.childType)}[]`
    }
    if (abiType instanceof ABIArrayStaticType) {
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
      return 'Uint8Array'
    }
    if (abiType instanceof ABIStringType) {
      return 'string'
    }
    return 'unknown'
  }
}
