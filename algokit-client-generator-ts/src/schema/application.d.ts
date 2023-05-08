/* eslint-disable */
/**
 * This file was automatically generated by json-schema-to-typescript.
 * DO NOT MODIFY IT BY HAND. Instead, modify the source JSONSchema file,
 * and run json-schema-to-typescript to regenerate this file.
 */

export type StructElement = [] | [FieldName] | [FieldName, ABIType];
export type FieldName = string;
export type ABIType = string;
export type ArgumentSource = "global-state" | "local-state" | "abi-method" | "constant";
export type CallConfigValue = "NEVER" | "CALL" | "CREATE" | "ALL";

export interface AlgoAppSpec {
  hints?: {
    [k: string]: Hint;
  };
  source: AppSources;
  contract: AbiContract;
  schema: SchemaSpec;
  state: StateSchemaSpec;
  bare_call_config?: CallConfig;
}
export interface Hint {
  read_only?: boolean;
  structs?: {
    [k: string]: Struct;
  };
  default_arguments?: {
    [k: string]: DefaultArgument;
  };
  call_config?: CallConfig;
}
export interface Struct {
  name?: string;
  elements?: StructElement[];
}
export interface DefaultArgument {
  source?: ArgumentSource;
  data?: string | number;
  [k: string]: unknown;
}
export interface CallConfig {
  no_op?: CallConfigValue;
  opt_in?: CallConfigValue;
  close_out?: CallConfigValue;
  clear_state?: CallConfigValue;
  update_application?: CallConfigValue;
  delete_application?: CallConfigValue;
}
export interface AppSources {
  approval?: string;
  clear?: string;
}
export interface AbiContract {
  name: string;
  methods: ContractMethod[];
  networks?: {
    [k: string]: {
      appID: number;
    };
  };
}
export interface ContractMethod {
  name: string;
  description?: string;
  args: ContractMethodArg[];
  returns?: {
    desc?: string;
    type?:
      | (
          | "string[]"
          | "byte[]"
          | "uint64"
          | "uint64[]"
          | "uint8"
          | "uint8[]"
          | "bool[]"
          | "pay"
          | "address"
          | "account"
          | "asset"
          | "application"
        )
      | string;
  };
}
export interface ContractMethodArg {
  desc?: string;
  type:
    | (
        | "string[]"
        | "byte[]"
        | "uint64"
        | "uint64[]"
        | "uint8"
        | "uint8[]"
        | "bool[]"
        | "pay"
        | "address"
        | "account"
        | "asset"
        | "application"
      )
    | string;
  name: string;
}
/**
 * The schema for global and local storage
 */
export interface SchemaSpec {
  global?: Schema;
  local?: Schema;
}
export interface Schema {
  declared?: {
    [k: string]: DeclaredSchemaValueSpec;
  };
  reserved?: {
    [k: string]: DeclaredSchemaValueSpec;
  };
}
export interface DeclaredSchemaValueSpec {
  /**
   * The type of the value
   */
  type: "uint64" | "bytes";
  /**
   * The name of the key
   */
  key: string;
  /**
   * A description of the variable
   */
  desc?: string;
  /**
   * Whether the value is set statically (at create time only) or dynamically
   */
  static: boolean;
  [k: string]: unknown;
}
export interface StateSchemaSpec {
  global: StateSchema;
  local: StateSchema;
}
export interface StateSchema {
  num_uints: number;
  num_byte_slices: number;
}