import { DocumentParts } from '../output/writer'

export function* imports(): DocumentParts {
  yield `import * as algokit from '@algorandfoundation/algokit-utils'
import {
  AppCallTransactionResultOfType,
  CoreAppCallArgs,
  RawAppCallArgs,
  TealTemplateParams,
  AppCallTransactionResult,
} from '@algorandfoundation/algokit-utils/types/app'
import {
  AppClientCallArgs,
  AppClientCallCoreParams,
  AppClientCompilationParams,
  AppClientDeployCoreParams,
  AppDetails,
  ApplicationClient,
} from '@algorandfoundation/algokit-utils/types/app-client'
import { AppSpec } from '@algorandfoundation/algokit-utils/types/app-spec'
import { Algodv2, TransactionWithSigner } from 'algosdk'`
}
