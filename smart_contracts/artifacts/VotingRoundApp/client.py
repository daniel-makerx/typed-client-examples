import pathlib
from typing import overload

import algokit_utils
import algosdk
from algosdk.atomic_transaction_composer import TransactionSigner, TransactionWithSigner


class VotingRoundAppClient:
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
        app_spec_path = pathlib.Path(__file__).parent / "application.json"
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

    def deploy(self) -> None:
        raise NotImplementedError

    def create(
        self,
        *,
        vote_id: str,
        snapshot_public_key: bytes,
        metadata_ipfs_cid: str,
        start_time: int,
        end_time: int,
        option_counts: list[int],
        quorum: int,
        nft_image_url: str,
        transaction_parameters: algokit_utils.CreateCallParameters | None = None,
    ) -> None:
        result = self.app_client.create(
            "create(string,byte[],string,uint64,uint64,uint8[],uint64,string)void",
            transaction_parameters=transaction_parameters,
            vote_id=vote_id,
            snapshot_public_key=snapshot_public_key,
            metadata_ipfs_cid=metadata_ipfs_cid,
            start_time=start_time,
            end_time=end_time,
            option_counts=option_counts,
            quorum=quorum,
            nft_image_url=nft_image_url,
        )
        return result.return_value

    def bootstrap(
        self,
        *,
        fund_min_bal_req: TransactionWithSigner,
        transaction_parameters: algokit_utils.CommonCallParameters | None = None,
    ) -> None:
        result = self.app_client.call(
            "bootstrap(pay)void", transaction_parameters=transaction_parameters, fund_min_bal_req=fund_min_bal_req
        )
        assert result

    def close(self, transaction_parameters: algokit_utils.CreateCallParameters | None = None) -> None:
        result = self.app_client.call("close()void", transaction_parameters=transaction_parameters)
        return result.return_value

    def get_preconditions(
        self, *, signature: bytes, transaction_parameters: algokit_utils.CreateCallParameters | None = None
    ) -> tuple[int, int, int, int]:
        result = self.app_client.call(
            "get_preconditions(byte[])(uint64,uint64,uint64,uint64)",
            signature=signature,
            transaction_parameters=transaction_parameters,
        )
        return result.return_value

    def vote(
        self,
        *,
        fund_min_bal_req: algosdk.transaction.PaymentTxn,
        signature: bytes,
        answer_ids: list[int],
        transaction_parameters: algokit_utils.CreateCallParameters | None = None,
    ) -> None:
        result = self.app_client.call(
            "vote(pay,byte[],uint8[])void",
            fund_min_bal_req=fund_min_bal_req,
            signature=signature,
            answer_ids=answer_ids,
            transaction_parameters=transaction_parameters,
        )
        return result.return_value
