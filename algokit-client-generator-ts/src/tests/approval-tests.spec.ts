import fs from 'fs'
import path from 'path'
import { writeDocumentPartsToString } from '../output/writer'
import { generateClient } from '../client/generate-client'
import { load } from '../schema/load'

const writeActual = process.env.TEST_ENV !== 'ci'

describe('When generating a ts client for a the contract', () => {
  test.each([{ contractName: 'HelloWorldApp' }])('$contractName, the generated client matches the approved one', ({ contractName }) => {
    const dir = path.join(__dirname, `../../../smart_contracts/artifacts/${contractName}/`)
    const spec = load(path.join(dir, `application.json`))

    const result = writeDocumentPartsToString(generateClient(spec))
    if (writeActual) fs.writeFileSync(path.join(dir, `client-ts.generated.ts`), result)

    const approvalDoc = fs.readFileSync(path.join(dir, `client-ts.ts`), 'utf-8')

    expect(result).toBe(approvalDoc)
  })
})
