import * as fs from 'fs'
import { Schema, Validator } from 'jsonschema'
import appJsonSchema from './application.json'
import contractSchema from './contract.json'
import { boom } from '../boom'
import { AlgoAppSpec } from './application'

export function load(appJsonPath: string) {
  if (!fs.existsSync(appJsonPath)) boom(`Could not find application.json file at ${appJsonPath}`)
  const validator = new Validator()
  validator.addSchema(contractSchema, '/contract.json')

  const file = JSON.parse(fs.readFileSync(appJsonPath, 'utf-8'))
  const result = validator.validate(file, appJsonSchema as unknown as Schema)

  if (!result.valid) boom(result.toString())

  return file as AlgoAppSpec
}
