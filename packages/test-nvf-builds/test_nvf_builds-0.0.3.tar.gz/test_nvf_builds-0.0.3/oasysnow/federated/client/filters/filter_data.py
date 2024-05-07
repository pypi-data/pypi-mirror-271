from nvflare.apis.dxo import DXO, DataKind, from_shareable
from nvflare.apis.filter import Filter
from nvflare.apis.fl_context import FLContext
from nvflare.apis.shareable import Shareable
from nvflare.app_common.app_constant import AppConstants
import json
from jwt import PyJWKClient
import jwt
import requests

class FilterData(Filter):

    def __init__(self):
        super().__init__()

    def process(self, shareable: Shareable, fl_ctx: FLContext) -> Shareable:
        client_name = fl_ctx.get_identity_name()
        current_round = shareable.get_cookie(AppConstants.CONTRIBUTION_ROUND)

        try:
            dxo = from_shareable(shareable)
        except:
            self.log_exception(fl_ctx, "shareable data is not a valid DXO")
            return shareable

        assert isinstance(dxo, DXO)
        if dxo.data_kind not in (DataKind.WEIGHT_DIFF, DataKind.WEIGHTS):
            self.log_debug(fl_ctx, "I cannot handle {}".format(dxo.data_kind))
            return shareable

        if dxo.data is None:
            self.log_debug(fl_ctx, "no data to filter")
            return shareable

        nonce = fl_ctx.get_prop("nonce")
        server_nonce = dxo.get_meta_prop(f"nonce_{client_name}")
        if not nonce == server_nonce:
            raise Exception(">>>>>>>>ERROR nonce != server_nonce", nonce, server_nonce)

        public_key_server_bytes = dxo.get_meta_prop(f"server_pk_{client_name}")
        attestation_report = dxo.get_meta_prop(f"attestation_report_{client_name}")

        # TODO: Add attestation verification
        # TODO: check if the hash of public key of server from attestation report is equal to public_key_server_b64
        if not public_key_server_bytes or not attestation_report:
            raise Exception("Attestation Failed: NO public key or Report")
        fl_ctx.set_prop("server_pk", public_key_server_bytes, private=True)

        verified_attestation = self.verify_attestation_report(attestation_report)
        if not verified_attestation:
            raise Exception("Attestation Failed: Invalid report")

        # TODO: replace dxo.get_meta_prop with direct fl_ctx.get_peer_context
        test_props = fl_ctx.get_peer_context().get_prop("test")
        print(f"\n>>>>>>> FILTER_DATA_CLIENT client_name: {client_name}; current_round: {current_round}; nonce: {nonce} server_nonce: {server_nonce}; test_props: {test_props}\n")

        return shareable

    def verify_attestation_report(self, report: str):
        try:
            issuer_url = "https://confidentialcomputing.googleapis.com/.well-known/openid-configuration"
            issuer = json.loads(requests.get(issuer_url).text)
            jwks_uri = issuer['jwks_uri']
            supported_algs = issuer['id_token_signing_alg_values_supported']
            optional_custom_headers = {"User-agent": "custom-user-agent"}
            jwks_client = PyJWKClient(jwks_uri, headers=optional_custom_headers)
            signing_key = jwks_client.get_signing_key_from_jwt(report)
            data = jwt.decode(
                report,
                signing_key.key,
                algorithms=supported_algs,
                audience="hospital1",
                options={"verify_exp": False},
            )
            print(json.dumps(data, indent=2))
            print('\n\n>>>>>> Attestation SUCCEEDED')
            return True
        except Exception as e:
            print('\n\n>>>>>> Attestation FAILED')
            print(">>>>", e)

