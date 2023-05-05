import pathlib
from typing import overload

import algokit_utils
import algosdk
from algosdk.atomic_transaction_composer import TransactionSigner


class HelloWorldAppClient:
    @overload
    def __init__(
        self,
        algod_client: algosdk.v2client.algod.AlgodClient,
        *,
        app_id: int = 0,
        signer: TransactionSigner | algokit_utils.Account | None = None,
        sender: str | None = None,
        suggested_params: algosdk.transaction.SuggestedParams | None = None,
        template_values: algokit_utils.TemplateValueMapping | None = None,
    ):
        ...

    @overload
    def __init__(
        self,
        algod_client: algosdk.v2client.algod.AlgodClient,
        *,
        creator: str | algokit_utils.Account,
        indexer_client: algosdk.v2client.indexer.IndexerClient | None = None,
        existing_deployments: algokit_utils.AppLookup | None = None,
        signer: TransactionSigner | algokit_utils.Account | None = None,
        sender: str | None = None,
        suggested_params: algosdk.transaction.SuggestedParams | None = None,
        template_values: algokit_utils.TemplateValueMapping | None = None,
    ):
        ...

    def __init__(
        self,
        algod_client: algosdk.v2client.algod.AlgodClient,
        *,
        creator: str | algokit_utils.Account | None = None,
        indexer_client: "algosdk.v2client.indexer.IndexerClient | None" = None,
        existing_deployments: algokit_utils.AppLookup | None = None,
        app_id: int = 0,
        signer: TransactionSigner | algokit_utils.Account | None = None,
        sender: str | None = None,
        suggested_params: algosdk.transaction.SuggestedParams | None = None,
        template_values: algokit_utils.TemplateValueMapping | None = None,
    ):
        app_spec_path = pathlib.Path(__file__).parent / "application.json"  # TODO: embed
        self.app_spec = algokit_utils.ApplicationSpecification.from_json(app_spec_path.read_text())

        # calling full __init__ signature, so ignoring mypy warning about overloads
        self.app_client = algokit_utils.ApplicationClient(  # type: ignore[call-overload, misc]
            algod_client=algod_client,
            app_spec=self.app_spec,
            app_id=app_id,
            creator=creator,
            indexer_client=indexer_client,
            existing_deployments=existing_deployments,
            signer=signer,
            sender=sender,
            suggested_params=suggested_params,
            template_values=template_values,
        )

    def hello(  # from $.contract.methods[name="hello"]
        self,
        name: str,
        transaction_parameters: algokit_utils.CommonCallParameters
        | algokit_utils.CommonCallParametersDict
        | None = None,
    ) -> algokit_utils.ABITransactionResponse[str]:
        # convert parameters into OnCompleteCallParameters with NoOpOC
        parameters = (
            transaction_parameters.__dict__
            if isinstance(transaction_parameters, algokit_utils.CommonCallParameters)
            else (transaction_parameters or {})
        )
        transaction_parameters = algokit_utils.OnCompleteCallParameters(
            **parameters, on_complete=algosdk.transaction.OnComplete.NoOpOC
        )
        # call is used because the ABI method call config for hello is no_op
        # from $.hints["hello(string)string""].call_config
        return self.app_client.call("hello(string)string", name=name, transaction_parameters=transaction_parameters)

    def create(  # from $.bare_call_config.no_op == 'CREATE'
        self,
        args: None = None,  # not required in this scenario, so takes None and defaults to None. Included so that if the
        # smart contract changes to have ABI parameters the signature will still be similar
        transaction_parameters: algokit_utils.CreateCallParameters
        | algokit_utils.CreateCallParametersDict
        | None = None,
    ) -> algokit_utils.TransactionResponse:
        return self.app_client.create(
            call_abi_method=False,  # False is used to indicate we want to call the bare_method, not an ABI method
            transaction_parameters=transaction_parameters,
        )

    def delete(  # from $.bare_call_config.delete_application == 'CALL'
        self,
        args: None = None,  # not required in this scenario, so takes None and defaults to None. Included so that if the
        # smart contract changes to have ABI parameters the signature will still be similar
        transaction_parameters: algokit_utils.CommonCallParameters
        | algokit_utils.CommonCallParametersDict
        | None = None,
    ) -> algokit_utils.TransactionResponse:
        return self.app_client.delete(
            call_abi_method=False,  # False is used to indicate we want to call the bare_method, not an ABI method
            transaction_parameters=transaction_parameters,
        )

    def update(  # from $.bare_call_config.update_application == 'CALL'
        self,
        args: None = None,  # not required in this scenario, so takes None and defaults to None. Included so that if the
        # smart contract changes to have ABI parameters the signature will still be similar
        transaction_parameters: algokit_utils.CommonCallParameters
        | algokit_utils.CommonCallParametersDict
        | None = None,
    ) -> algokit_utils.TransactionResponse:
        return self.app_client.update(
            call_abi_method=False,  # False is used to indicate we want to call the bare_method, not an ABI method
            transaction_parameters=transaction_parameters,
        )

    def deploy(
        self,
        version: str | None = None,
        *,
        signer: TransactionSigner | None = None,
        sender: str | None = None,
        allow_update: bool | None = None,
        allow_delete: bool | None = None,
        on_update: algokit_utils.OnUpdate = algokit_utils.OnUpdate.Fail,
        on_schema_break: algokit_utils.OnSchemaBreak = algokit_utils.OnSchemaBreak.Fail,
        template_values: algokit_utils.TemplateValueMapping | None = None,
        create_args: algokit_utils.ABICallArgs | None = None,
        update_args: algokit_utils.ABICallArgs | None = None,
        delete_args: algokit_utils.ABICallArgs | None = None,
    ) -> algokit_utils.DeployResponse:
        return self.app_client.deploy(
            version,
            signer=signer,
            sender=sender,
            allow_update=allow_update,
            allow_delete=allow_delete,
            on_update=on_update,
            on_schema_break=on_schema_break,
            template_values=template_values,
            create_args=create_args,
            update_args=update_args,
            delete_args=delete_args,
        )
