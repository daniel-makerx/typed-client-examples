import { algorandFixture } from '@algorandfoundation/algokit-utils/testing'
import { beforeEach, describe, expect, test } from '@jest/globals'
import * as ed from '@noble/ed25519'
import algosdk from 'algosdk'
import invariant from 'tiny-invariant'
import { expectType } from 'tsd'
import { VotingRoundAppClient } from './client-ts'

describe('hello world typed client', () => {
  const localnet = algorandFixture()
  beforeEach(localnet.beforeEach, 10_000)

  let client: VotingRoundAppClient

  beforeEach(() => {
    const { algod, indexer, testAccount } = localnet.context
    client = new VotingRoundAppClient(
      {
        resolveBy: 'creatorAndName',
        sender: testAccount,
        creatorAddress: testAccount.addr,
        findExistingUsing: indexer,
      },
      algod,
    )
  })

  test('global_state', async () => {
    const { algod } = localnet.context
    const status = await algod.status().do()
    const lastRound = Number(status['last-round'])
    const round = await algod.block(lastRound).do()
    const currentTime = Number(round.block.ts)

    const quorum = Math.ceil(Math.random() * 1000)

    const questionCount = Math.ceil(Math.random() * 10)
    const questionCounts = new Array(questionCount).fill(0).map((_) => Math.ceil(Math.random() * 10))
    const totalQuestionOptions = questionCounts.reduce((a, b) => a + b, 0)

    const privateKey = Buffer.from(ed.utils.randomPrivateKey())
    const publicKey = await ed.getPublicKey(privateKey)

    const createResult = await client.create(
      {
        method: 'create',
        vote_id: `V${new Date().getTime().toString(32).toUpperCase()}`,
        metadata_ipfs_cid: 'cid',
        start_time: BigInt(currentTime), // todo: allow number and convert
        end_time: BigInt(currentTime + 1000),
        quorum: BigInt(quorum),
        snapshot_public_key: publicKey,
        nft_image_url: 'ipfs://cid',
        option_counts: questionCounts,
      },
      { deletable: true, sendParams: { fee: (1_000 + 1_000 * 4).microAlgos() } },
    )
    expectType<void>(createResult.return)

    const state = await client.getGlobalState()

    invariant(state.snapshot_public_key !== undefined)
    expect(state.snapshot_public_key.raw).toEqual(publicKey)
    state.snapshot_public_key.raw = new Uint8Array([1])
    state.snapshot_public_key.string = '[PK]'

    expect(state.metadata_ipfs_cid!.string).toBe('cid')
    expect(state.start_time!.number).toBe(currentTime)
    expect(state.end_time!.number).toBe(currentTime + 1000)
    expect(state.close_time!.number).toBe(0)
    expect(state.quorum!.number).toBe(quorum)
    expect(state.is_bootstrapped!.number).toBe(0)
    expect(state.voter_count!.number).toBe(0)
    expect(state.nft_image_url!.string).toBe('ipfs://cid')
    expect(state.nft_asset_id!.number).toBe(0)
    expect(state.total_options!.number).toBe(totalQuestionOptions)
    const optionCountsType = new algosdk.ABIArrayDynamicType(new algosdk.ABIUintType(8))
    expect(optionCountsType.decode(state.option_counts!.raw).map(Number)).toEqual(questionCounts)
  })
})
