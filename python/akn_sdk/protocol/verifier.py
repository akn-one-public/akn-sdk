# akn_sdk/protocol/verifier.py

import json
from nacl.signing import VerifyKey
from nacl.encoding import Base64Encoder
from nacl.exceptions import BadSignatureError


def verify_signature(public_key, payload, signature):

    verify_key = VerifyKey(public_key.encode(), encoder=Base64Encoder)

    canonical = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":")
    ).encode()

    try:
        verify_key.verify(canonical, Base64Encoder.decode(signature.encode()))
        return True
    except BadSignatureError:
        return False