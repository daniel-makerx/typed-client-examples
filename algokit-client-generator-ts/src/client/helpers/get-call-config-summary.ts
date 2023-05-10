import { AlgoAppSpec, CallConfig, CallConfigValue } from '../../schema/application'
import config from '../../../jest.config'

export type OnCompletion = 'no_op' | 'opt_in' | 'close_out' | 'clear_state' | 'update_application' | 'delete_application'
export const BARE_CALL = Symbol('bare')

export type MethodIdentifier = string | typeof BARE_CALL

export type MethodList = Array<MethodIdentifier>

export type CallConfigSummary = {
  createMethods: MethodList
  callMethods: MethodList
  deleteMethods: MethodList
  updateMethods: MethodList
  optInMethods: MethodList
}
export const getCallConfigSummary = (app: AlgoAppSpec) => {
  const result: CallConfigSummary = {
    createMethods: [],
    callMethods: [],
    deleteMethods: [],
    updateMethods: [],
    optInMethods: [],
  }
  if (app.bare_call_config) {
    addToConfig(result, BARE_CALL, app.bare_call_config)
  }
  if (app.hints) {
    for (const [method, hints] of Object.entries(app.hints)) {
      if (hints.call_config) {
        addToConfig(result, method, hints.call_config)
      }
    }
  }
  return result
}

const addToConfig = (result: CallConfigSummary, method: MethodIdentifier, config: CallConfig) => {
  if (hasCall(config.no_op)) {
    result.callMethods.push(method)
  }
  if (hasCreate(config.no_op)) {
    result.createMethods.push(method)
  }
  if (hasCall(config.delete_application)) {
    result.deleteMethods.push(method)
  }
  if (hasCall(config.update_application)) {
    result.updateMethods.push(method)
  }
  if (hasCall(config.opt_in)) {
    result.optInMethods.push(method)
  }
}

const hasCall = (config: CallConfigValue | undefined) => {
  return config === 'CALL' || config === 'ALL'
}
const hasCreate = (config: CallConfigValue | undefined) => {
  return config === 'CREATE' || config === 'ALL'
}
