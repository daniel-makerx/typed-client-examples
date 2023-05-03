import { algorandFixture } from '@algorandfoundation/algokit-utils/testing'
import { beforeEach, describe, expect, test } from '@jest/globals'
import { getHelloWorldAppClient } from './client'

describe('hello world typed client', () => {
  const localnet = algorandFixture()
  beforeEach(localnet.beforeEach, 10_000)

  test('Calls hello', async () => {
    const { algod, indexer, testAccount } = localnet.context
    const client = await getHelloWorldAppClient(
      {
        sender: testAccount,
        creatorAddress: testAccount.addr,
        indexer,
      },
      algod,
    )
    await client.appClient.deploy()

    const response = await client.hello('World')
    expect(response).toBe('Hello, World')
  })
})
