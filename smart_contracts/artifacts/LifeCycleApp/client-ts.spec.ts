import { algorandFixture } from '@algorandfoundation/algokit-utils/testing'
import { beforeEach, describe, expect, test } from '@jest/globals'
import { LifeCycleAppClient } from './client-ts'

describe('hello world typed client', () => {
  const localnet = algorandFixture()
  beforeEach(localnet.beforeEach, 10_000)

  test('Calls hello', async () => {
    const { algod, indexer, testAccount } = localnet.context
    const client = new LifeCycleAppClient(
      {
        resolveBy: 'creatorAndName',
        sender: testAccount,
        creatorAddress: testAccount.addr,
        findExistingUsing: indexer,
      },
      algod,
    )
    const x = await client.create({ method: 'create_1', greeting: 'a' }, { updatable: true })
    x.return // This should be string, not unknown

    const response = await client.hello({ name: 'World' })
    expect(response.return).toBe('Hello, World')

    const response2 = await client.hello(['World!'])
    expect(response2.return).toBe('Hello, World!')
  })
})
