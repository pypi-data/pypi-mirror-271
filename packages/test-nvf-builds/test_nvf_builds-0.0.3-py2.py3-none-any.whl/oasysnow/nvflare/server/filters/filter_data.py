from nvflare.apis.dxo import DXO, DataKind, from_shareable
from nvflare.apis.filter import Filter
from nvflare.apis.fl_constant import FLContextKey
from nvflare.apis.fl_context import FLContext
from nvflare.apis.shareable import Shareable
from nvflare.app_common.app_constant import AppConstants

from cryptography.hazmat.primitives.asymmetric import ec
import cryptography.hazmat.primitives.serialization as ser

class FilterData(Filter):

    def __init__(self):
        super().__init__()

    def process(self, shareable: Shareable, fl_ctx: FLContext) -> Shareable:
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


        contributor_name = fl_ctx.get_peer_context().get_identity_name()
        nonce = fl_ctx.get_peer_context().get_prop("nonce")
        current_round = shareable.get_cookie(AppConstants.CONTRIBUTION_ROUND)
        job_id = fl_ctx.get_job_id()

        private_key_server = ec.generate_private_key(ec.SECP384R1())
        public_key_server_bytes = private_key_server.public_key().public_bytes(ser.Encoding.PEM, ser.PublicFormat.SubjectPublicKeyInfo)

        # TODO: Add attestation report

        fl_ctx.set_prop(f"server_sk_{contributor_name}", private_key_server, private=True)

        # TODO: replace dxo.get_meta_prop with direct fl_ctx.get_peer_context
        fl_ctx.set_prop(f"test", f"{current_round}:{nonce}", False, False)

        dxo.set_meta_prop(f"server_pk_{contributor_name}", public_key_server_bytes)
        dxo.set_meta_prop(f"nonce_{contributor_name}", nonce)
        dxo.set_meta_prop(f"attestation_report_{contributor_name}", "eyJhbGciOiJSUzI1NiIsImtpZCI6IjZiNDExYzJlZTAyNTdjNjE4YTI2NWRlZjcyNGY4NjNlM2I3OTg5YTMiLCJ0eXAiOiJKV1QifQ.eyJhdWQiOiJob3NwaXRhbDEiLCJleHAiOjE3MTQ3NDc4MDksImlhdCI6MTcxNDc0NDIwOSwiaXNzIjoiaHR0cHM6Ly9jb25maWRlbnRpYWxjb21wdXRpbmcuZ29vZ2xlYXBpcy5jb20iLCJuYmYiOjE3MTQ3NDQyMDksInN1YiI6Imh0dHBzOi8vd3d3Lmdvb2dsZWFwaXMuY29tL2NvbXB1dGUvdjEvcHJvamVjdHMvb2FzeXMtY29sYWItdGVzdDIvem9uZXMvZXVyb3BlLXdlc3Q0LWEvaW5zdGFuY2VzL3NlY3VuZHVzLXNlY29uZC12bSIsImVhdF9ub25jZSI6InNvbWUgZnJlc2gganVjeSBub25jZSIsInNlY2Jvb3QiOnRydWUsIm9lbWlkIjoxMTEyOSwiaHdtb2RlbCI6IkdDUF9BTURfU0VWIiwic3duYW1lIjoiQ09ORklERU5USUFMX1NQQUNFIiwic3d2ZXJzaW9uIjpbIjI0MDIwMCJdLCJkYmdzdGF0IjoiZGlzYWJsZWQtc2luY2UtYm9vdCIsInN1Ym1vZHMiOnsiY29uZmlkZW50aWFsX3NwYWNlIjp7InN1cHBvcnRfYXR0cmlidXRlcyI6WyJMQVRFU1QiLCJTVEFCTEUiLCJVU0FCTEUiXSwibW9uaXRvcmluZ19lbmFibGVkIjp7Im1lbW9yeSI6ZmFsc2V9fSwiY29udGFpbmVyIjp7ImltYWdlX3JlZmVyZW5jZSI6InVzLWRvY2tlci5wa2cuZGV2L29hc3lzLWNvbGFiLXRlc3QxL3ByaW11cy13b3JrbG9hZHMvcmE6bGF0ZXN0IiwiaW1hZ2VfZGlnZXN0Ijoic2hhMjU2OjUwYTJmNTVjY2VlMzQxMTE0ZTUwYTQzZTk0ZTY2MmIxMDA5MWYzOWQzOTU5N2RlOGYyY2EyMDZkNDhlYzE3ODUiLCJyZXN0YXJ0X3BvbGljeSI6Ik5ldmVyIiwiaW1hZ2VfaWQiOiJzaGEyNTY6ODNhNzI5ZDVkNDA2YmUxMTVhYThlZmIxZWJmZTRiNTFmMTcwNDkxMWFlZjA3M2Y1Yzg1NWJjMjQxNDJjM2Y0MSIsImVudiI6eyJIT1NUTkFNRSI6InNlY3VuZHVzLXNlY29uZC12bSIsIk5PREVfVkVSU0lPTiI6IjIwLjEwLjAiLCJQQVRIIjoiL3Vzci9sb2NhbC9zYmluOi91c3IvbG9jYWwvYmluOi91c3Ivc2JpbjovdXNyL2Jpbjovc2JpbjovYmluIiwiWUFSTl9WRVJTSU9OIjoiMS4yMi4xOSJ9LCJhcmdzIjpbImRvY2tlci1lbnRyeXBvaW50LnNoIiwieWFybiIsInN0YXJ0OnByb2QiXX0sImdjZSI6eyJ6b25lIjoiZXVyb3BlLXdlc3Q0LWEiLCJwcm9qZWN0X2lkIjoib2FzeXMtY29sYWItdGVzdDIiLCJwcm9qZWN0X251bWJlciI6Ijk3Njc3NTUyNjA4NSIsImluc3RhbmNlX25hbWUiOiJzZWN1bmR1cy1zZWNvbmQtdm0iLCJpbnN0YW5jZV9pZCI6IjMyNjMxNDgyOTg3MzA2ODcyOTQifX0sImdvb2dsZV9zZXJ2aWNlX2FjY291bnRzIjpbInJ1bi1jb25maWRlbnRpYWwtdm1Ab2FzeXMtY29sYWItdGVzdDIuaWFtLmdzZXJ2aWNlYWNjb3VudC5jb20iXX0.M0flMeLHhq2Sk9J7JIxQLPH_qVnxL0feFMOgfqovsflZ5lp4up13du7FnrmmTNJAv-0-nKJmfcsr3aOQz1NqkM_IXOHtH4746-2w1WZGpoD8_WoeDrgXRudub_qGwohN1d7sW3N0ej55EPH96mNOss9oJe-Oo0DkrJJFgCFc4EAVtUqEX0eMWHAoRuSIKxqFF3WgGUxwnEQRsxgxV3Oe2v-OE3x81sSXs89lBdM4jIl7GpEYfW2EeS9-GEDg3EChq-DRN4EIgXGBhTmbCaAx6lSeL7xjZdACPdACLIfKm1ratN27cz-B-aDG8OcPmTy3KSNdGtKF1Ib2U4niv0ctkQ")

        print(f"\n>>>>>>> FILTER_DATA_SERVER, contributor_name: {contributor_name}; current_round: {current_round}; job_id: {job_id}; nonce: {nonce}\n")

        return dxo.update_shareable(shareable)
