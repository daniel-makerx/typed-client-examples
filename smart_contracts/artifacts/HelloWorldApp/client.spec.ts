import { algorandFixture } from '@algorandfoundation/algokit-utils/testing'
import { beforeEach, describe, expect, test } from '@jest/globals'
import { HelloWorldAppClient } from './client'

describe('hello world typed client', () => {
  const localnet = algorandFixture()
  beforeEach(localnet.beforeEach, 10_000)

  test('Calls hello', async () => {
    const { algod, indexer, testAccount } = localnet.context
    const client = new HelloWorldAppClient(
      {
        sender: testAccount,
        creatorAddress: testAccount.addr,
        indexer,
      },
      algod,
    )
    await client.appClient.deploy()

    const response = await client.hello('World')
    expect(response.return).toBe('Hello, World')
  })
})
