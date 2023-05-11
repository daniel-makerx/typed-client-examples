import { AlgoAppSpec } from '../schema/application'
import { CallConfigSummary, getCallConfigSummary } from './helpers/get-call-config-summary'
import { makeSafeTypeIdentifier } from '../util/sanitization'

export type GeneratorContext = {
  app: AlgoAppSpec
  name: string
  callConfig: CallConfigSummary
}

export const createGeneratorContextx = (app: AlgoAppSpec) => ({
  app,
  name: makeSafeTypeIdentifier(app.contract.name),
  callConfig: getCallConfigSummary(app),
})
