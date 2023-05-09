export function getEquivalentType(abiType: string): string {
  if (abiType.endsWith('[]')) {
    return `${getEquivalentType(abiType.slice(0, -2))}[]`
  }
  // TODO: Improve this: current version is super dodgy, doesn't account for nested tuples
  if (abiType.startsWith('(') && abiType.endsWith(')')) {
    return `[${abiType.slice(1, -1).split(',').map(getEquivalentType).join(',')}]`
  }

  const uintRegex = /^uint(\d+)$/
  const [isUint, size] = uintRegex.exec(abiType) ?? [false, 0]
  if (isUint) {
    if (Number(size) >= 51) {
      return 'bigint'
    }
    return 'number'
  }
  switch (abiType) {
    case 'byte':
      return 'number'
    case 'void':
      return 'void'
    default:
      return 'string'
  }
}
